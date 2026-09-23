<div align="center">

# AI Factory · Telegram × n8n

Telegram-интерфейс для видеопайплайнов n8n: загрузка аудио и видео, запуск обработки и проверка статуса.

[Правила разработки](CONTRIBUTING.md) · [Ветки](https://github.com/wuttashi1/n8nstart/branches)

</div>

---

## Возможности

- Приём аудио и видео в Telegram.
- Отправка запросов в n8n через webhooks.
- Команды `/upload`, `/render` и `/status`.
- Хранение входных файлов и журналирование.

Обработка видео выполняется внешним пайплайном n8n. Этот репозиторий содержит интерфейс управления ботом.

## Запуск

```bash
cd Bot_n8n
python -m venv .venv
# Активируйте .venv для вашей оболочки
python -m pip install -r requirements.txt
python main.py
```

Перед запуском создайте `Bot_n8n/.env` с `TELEGRAM_BOT_TOKEN` и `N8N_WEBHOOK_URL`. Необязательный `DOWNLOAD_PATH` задаёт каталог входных файлов. Подготовьте в n8n обработчики `/upload`, `/render` и `/status`.

Подробное описание запросов: [документация бота](Bot_n8n/README.md).

## Разработка

Соглашения по веткам и изменениям: [CONTRIBUTING.md](CONTRIBUTING.md).
