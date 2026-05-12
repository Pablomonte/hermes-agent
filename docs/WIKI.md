# WIKI — Proyectos P.- × Quique

> Wiki viva de proyectos, infraestructura y conocimiento compartido.
> Objetivo: reemplazar backups crudos de conversaciones con documentación estructurada y escalable.

---

## Índice

1. [Proyectos Activos](#proyectos-activos)
2. [Infraestructura](#infraestructura)
3. [Hermes Agent (saicam1)](#hermes-agent-saicam1)
4. [Proyecto VFD — Cooperativas de Agua](#proyecto-vfd--cooperativas-de-agua)
5. [Multimedia & Smart Home](#multimedia--smart-home)
6. [Voz (STT/TTS)](#voz-stttts)
7. [Música & Cultura](#música--cultura)
8. [Changelog Reciente](#changelog-reciente)
9. [Notas Técnicas](#notas-técnicas)

---

## Proyectos Activos

### Hermes Agent — Auto-mejora
- **Repo local:** `/home/siqui/hermes-agent` (siqui) + `/var/lib/hermes/dev-workspace/hermes-agent` (Quique)
- **Upstream:** `github.com/nicoechaniz/hermes-agent`
- **Fork:** `github.com/Pablomonte/hermes-agent`
- **Estado:** En desarrollo activo. Hoy (2026-05-11) se habilitó workspace de auto-mejora para Quique con acceso readonly al repo de siqui y push al fork de Pablomonte.
- **Stack reciente:** hermes-memory-kit (HRM-*, embeddings NVIDIA, dialogue-handoff)
- **Commits locales WIP:** 20+ en rama local de siqui (no publicados), incluyen auxiliary_client, run.py, workarounds post-upgrade.

### Proyecto VFD — Cooperativas de Agua Rurales Argentinas
- **Organización:** ONG 501(c) equivalente
- **Equipo:** Ingeniería + devs
- **Objetivo:** VFD (Variable Frequency Drive) para cooperativas de agua rurales
- **Topología:** Híbrida — VFD comercial + ESP32/STM32
- **Motores:** Monofásicos Y trifásicos (corregido: mayo 2026)
- **Tecnologías:** Electrónica de potencia, IGBTs/SiC, control vectorial
- **Metodología:** Actualizaciones incrementales ("de a poco")
- **Estado:** En desarrollo. Última discusión: mayo 2026 (sesión 20260504).

### Dashboard Orgapic (saicam8)
- **Host:** saicam8 (10.130.40.202, Pi ARM64)
- **Stack:** Flask + monitoreo de sistema + control PTZ Ezviz H8c
- **Funciones:** Lista de reproducción Mopidy, cámara RTSP, estado del sistema, auto-inicio persistente
- **Estado:** Activo. Puerto 5016→15021 (reverse proxy).
- **Skill:** `orgapic-dashboard`

---

## Infraestructura

### saicam1 — Máquina Principal
- **Hardware:** 4× ARM Cortex-A72, 7.6 GB RAM, 57 GB SSD (42 GB libres)
- **OS:** Linux 6.6.51+rpt-rpi-v8
- **Usuarios:**
  - `siqui` — dueño del repo original, corre gateway de Hermes
  - `hermes` — usuario del servicio, nologin shell, no systemd user access
  - `admin` — acceso root vía sudo
- **Servicios:**
  - `hermes-gateway.service` — Telegram gateway (active, PID cambiante)
  - `hermes-bridge` — uvicorn en 127.0.0.1:8088
  - gotty (episódico) — compartir terminal vía web
- **Paths clave:**
  - `/home/siqui/hermes-agent` — repo original
  - `/opt/hermes-src/` — instalación del servicio
  - `/opt/hermes-bridge-venv/` — bridge
  - `/opt/hermes-agent/config/config.yaml` — config base
  - `/var/lib/hermes/` — home de hermes, workspace, skills, memoria
  - `/var/backups/hermes-emergency/` — backup crítico (excluye .env)
- **Networking:** Múltiples interfaces (192.168.1.100, 10.10.20.158, 172.x, etc.)

### saicam8 — Backup / Secundaria
- **Hardware:** Raspberry Pi ARM64
- **IP:** 10.130.40.202
- **Servicios:**
  - Dashboard orgapic (puertos 5016→15021)
  - Bluetooth UI
  - Cámara RTSP
  - Mopidy en 6680-6682

---

## Hermes Agent (saicam1)

### Config Actual (2026-05-11)
- **Model:** `k2.6-code-preview` (provider: `kimi-coding`)
- **Model default config:** `moonshotai/kimi-k2.5` (en config.yaml)
- **STT:** whisper-1 (OpenAI API)
- **TTS:** edge-tts, voz `es-AR-TomasNeural` (opus para Telegram)
- **Plataforma:** Telegram (Bot API con token)
- **Memory:** Activada, memory_char_limit 2200, user_char_limit 1375

### Skills Activos / Creados
| Skill | Descripción | Estado |
|-------|-------------|--------|
| `orgapic-dashboard` | Setup Flask + monitoreo + PTZ | Activo |
| `tts-edge-tts-cli-workaround` | TTS local vía edge-tts cuando el tool nativo falla | Activo |
| `mopidy-bluetooth-playback` | Buscar música en YouTube vía Mopidy | Activo |
| `hermes-emergency-backup` | Backup de archivos críticos | Activo |
| `hermes-baremetal-upgrade-audit` | Audit local vs upstream | Activo |

### Identidad
- **Nombre:** Quique (diminutivo de siqui/hermes)
- **Voz TTS preferida:** Valentina (es-UY-ValentinaNeural)
- **Fallbacks:** Elena (formal), Tomas (casual)

### Workspace de Desarrollo
- **Path:** `/var/lib/hermes/dev-workspace/hermes-agent`
- **Remotes:**
  - `origin` → `github.com/Pablomonte/hermes-agent`
  - `upstream` → `github.com/nicoechaniz/hermes-agent`
- **Venv:** `.venv` instalado en editable mode
- **gh CLI:** `/var/lib/hermes/.local/bin/gh`
- **Credenciales:** HTTPS con PAT en `/var/lib/hermes/.git-credentials`

---

## Multimedia & Smart Home

### Mopidy + Iris
- **Host:** saicam8
- **Puertos:** 6680-6682
- **Bug conocido:** Al dar play no arranca de inmediato. Workaround: Iris → 3 puntitos → Play.
- **Integración:** Dashboard orgapic muestra lista de reproducción.

### Cámara RTSP — Ezviz H8c
- **Control:** PTZ vía dashboard orgapic
- **Protocolo:** RTSP

---

## Voz (STT/TTS)

### STT — Whisper.cpp (100% local)
- **Capa 1:** Dashboard `/api/voice/transcribe` (saicam8)
- **Capa 2:** `transcription_tools.py` parcheado para fallback local cuando no hay `VOICE_TOOLS_OPENAI_KEY`
- **Backup:** `/opt/hermes-agent/tools/transcription_tools.py.backup`
- **Test OK:** 14/03/2026

### TTS — edge-tts workaround
- **Provider:** edge-tts CLI
- **Voz principal:** Valentina (es-UY-ValentinaNeural)
- **Fallbacks:** Elena (formal), Tomas (casual)
- **Nota:** "Diana" no existe como voz.

---

## Música & Cultura

### Playlist Transversal (Favorita)
Incluye sin prejuicios de época/cultura:
- Górecki, Pärt, Eno
- Nick Drake, Radiohead
- Mingus, Snarky Puppy
- King Crimson, Burial
- Ali Farka Touré, Khruangbin
- Silvio Rodríguez, Nusrat Fate Ali Khan

### Cine
- Disfruta películas de diversas culturas y épocas.
- Referencia reciente: *Interstellar* (Hans Zimmer soundtrack)

---

## Changelog Reciente

### 2026-05-11 — Setup de Auto-mejora para Quique
- Agregado `BindReadOnlyPaths=/home/siqui/hermes-agent:/var/lib/hermes/siqui_repo` a `hermes-gateway.service.d/dev-volumes.conf`
- Reiniciado `hermes-gateway.service`
- Clonado upstream en `/var/lib/hermes/dev-workspace/hermes-agent`
- Configurado git con fork de Pablomonte como origin
- Instalado gh CLI y venv con proyecto en editable mode
- Quique ahora puede hacer commits locales y proponer PRs.

### 2026-05-11 — Instalación de hermes-memory-kit
- Stack HRM-* con embeddings NVIDIA
- Provider: `hmk-memory` + `dialogue-handoff` activos

### 2026-04-24 — Fix Dashboard Orgapic
- Restaurado dashboard Flask con monitoreo, Mopidy y cámara

### 2026-03-14 — Voz 100% Local
- whisper.cpp compilado y funcionando en 2 capas
- Fallback local activado

---

## Notas Técnicas

### Permisos y Sandboxing
- `hermes` user: nologin shell, no systemd user access, sudo bloqueado
- `NoNewPrivileges=true` en service file
- npm global install requiere workaround: `~/.local/lib/npm`
- Syncthing preferido para vault sync (alternativa open-source)

### Git
- Forks con historias no relacionadas → cherry-pick only, no merge
- Abortar commits grandes (15+ conflictos) para features de baja prioridad
- Pre-flight import test obligatorio antes de restart

### Backups
- **Emergencia:** `/var/backups/hermes-emergency/` — contiene `CAPACIDADES_HERMES.md`, `MEMORY.md`, `USER.md`, `config.yaml`
- **Excluye:** `.env` (seguridad)

### Troubleshooting
- **Mopidy no arranca al dar play:** Iris → 3 puntitos → Play
- **TTS no funciona:** Verificar `edge-tts` instalado, usar workaround CLI
- **Permiso denied en /home/siqui:** Verificar `ProtectHome` en systemd, usar `/var/lib/hermes/siqui_repo`
- **git dubious ownership:** `git config --global --add safe.directory /path`

---

## TODO / Ideas Futuras

- [ ] Completar instalación de `pre-commit` (hash mismatch en piwheels)
- [ ] Comparar diffs entre `/var/lib/hermes/siqui_repo` y upstream para documentar WIPs
- [ ] Agregar skill de auto-documentación de proyectos VFD
- [ ] Evaluar migración completa a `ProtectHome=read-only` vs bind mounts actuales
- [ ] Consolidar múltiples instalaciones de Hermes en saicam1

---

*Última actualización: 2026-05-11 por Quique*
*Formato: Markdown puro. Editá directamente este archivo. Commiteá cambios con buenas prácticas GH.*
