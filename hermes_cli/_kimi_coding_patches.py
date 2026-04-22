"""Monkeypatches for kimi-coding provider bugs.

Applied when imported. Intercepts OpenAI SDK chat.completions.create for
requests to api.kimi.com and fixes:

1. api_key=None → uses KIMI_API_KEY env var
2. model name k2-6-... → restores k2.6-... (dot lost in upstream normalizer)
3. Missing X-Msh-* headers required by Kimi Coding API
"""
from __future__ import annotations

import os

from openai.resources.chat.completions import AsyncCompletions, Completions

_KIMI_HOST = "api.kimi.com"
_orig_create = Completions.create
_orig_acreate = AsyncCompletions.create


def _restore_model_dots(model: str) -> str:
    if not isinstance(model, str):
        return model
    if model.startswith("k2-6-"):
        return "k2.6-" + model[len("k2-6-"):]
    if model == "kimi-k2-6":
        return "kimi-k2.6"
    return model


def _patch_kwargs(client, kwargs):
    base_url = str(getattr(client, "base_url", "") or "")
    if _KIMI_HOST not in base_url:
        return kwargs

    current_key = getattr(client, "api_key", None)
    if not current_key or current_key in (None, "None", ""):
        env_key = os.getenv("KIMI_API_KEY")
        if env_key:
            try:
                client.api_key = env_key
            except Exception:
                pass

    if "model" in kwargs:
        kwargs["model"] = _restore_model_dots(kwargs["model"])

    try:
        from hermes_cli.auth import kimi_coding_default_headers
        msh_headers = kimi_coding_default_headers()
    except Exception:
        msh_headers = {}

    if msh_headers:
        headers = dict(kwargs.get("extra_headers") or {})
        for k, v in msh_headers.items():
            headers.setdefault(k, v)
        kwargs["extra_headers"] = headers

    return kwargs


def _wrapped_create(self, *args, **kwargs):
    kwargs = _patch_kwargs(self._client, kwargs)
    return _orig_create(self, *args, **kwargs)


async def _wrapped_acreate(self, *args, **kwargs):
    kwargs = _patch_kwargs(self._client, kwargs)
    return await _orig_acreate(self, *args, **kwargs)


Completions.create = _wrapped_create
AsyncCompletions.create = _wrapped_acreate
