# AI Factory Telegram Control Bot

Control interface for automated video generation pipelines:

Telegram Bot -> n8n Webhook -> processing pipeline -> n8n -> Telegram response.

The bot does not process videos locally. It only receives user input, downloads files, sends webhook requests, and shows status/results.

## Features

- Clean modular architecture (`handlers`, `services`, `utils`)
- `.env` driven configuration
- Telegram audio/video download support
- Local storage in `input/music` and `input/video`
- n8n webhook communication:
  - `POST /upload`
  - `POST /render`
  - `POST /status`
- Rotating file + console logs in `logs/`
- Friendly error handling for failed downloads/webhooks

## Project Structure

```text
Bot_n8n/
  bot/
    main.py
    handlers/
      start.py
      upload.py
      render.py
      status.py
      error.py
    services/
      telegram_downloader.py
      n8n_client.py
      user_state.py
    utils/
      logger.py
      file_manager.py
    config.py
  input/
    music/
    video/
  logs/
  main.py
  requirements.txt
  .env.example
```

## Environment Variables

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
N8N_WEBHOOK_URL=http://localhost:5678/webhook
DOWNLOAD_PATH=./input
```

## Run Locally

```bash
python -m venv .venv
# PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python main.py
```

## Commands

- `/start` - intro + available actions
- `/upload` - request file, save it, send webhook `/upload`
- `/render` - trigger webhook `/render` for latest user file
- `/status` - request webhook `/status` and display queue/render state
- `/help` - same as `/start`

## Webhook Payloads

`/upload` sends:
- `user_id`
- `file_path`
- `file_type` (`music` or `video`)
- `file_name`

`/render` sends:
- `user_id`
- `last_uploaded_file`
- `action=render_video`

`/status` sends:
- `user_id`
