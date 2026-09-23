<div align="center">

# AI Factory · Telegram × n8n

Telegram control interface for n8n video pipelines: upload media, trigger processing and check job status.

[Contributing](CONTRIBUTING.md) · [Branches](https://github.com/wuttashi1/n8nstart/branches)

</div>

---

## Features

- Receive audio and video through Telegram.
- Send webhook requests to n8n.
- `/upload`, `/render` and `/status` commands.
- Input file storage and application logging.

Video processing runs in an external n8n pipeline. This repository provides the Telegram control interface.

## Quick start

```bash
cd Bot_n8n
python -m venv .venv
# Activate .venv for your shell
python -m pip install -r requirements.txt
python main.py
```

Before starting, create `Bot_n8n/.env` with `TELEGRAM_BOT_TOKEN` and `N8N_WEBHOOK_URL`. Optional `DOWNLOAD_PATH` controls input storage. Configure the `/upload`, `/render` and `/status` webhook handlers in n8n.

See the [bot documentation](Bot_n8n/README.md) for request payloads.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch and contribution guidelines.
