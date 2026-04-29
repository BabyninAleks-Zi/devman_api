# Devman Telegram Notifier

Бот отслеживает проверки уроков на [dvmn.org](https://dvmn.org/) через Long Polling API и отправляет уведомления в Telegram.

В уведомлении приходит:
- название урока;
- результат проверки (принята работа или нет);
- ссылка на урок.

## Требования

- Python 3.10+
- Telegram-бот (токен от `@BotFather`)
- Токен Devman

## Установка

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
DEVMAN_TOKEN=ваш_devman_token
TG_TOKEN=ваш_telegram_bot_token
TG_CHAT_ID=ваш_chat_id
```

Где:
- `DEVMAN_TOKEN` — токен API Devman;
- `TG_TOKEN` — токен Telegram-бота;
- `TG_CHAT_ID` — chat id получателя сообщений (можно не указывать, если передавать через CLI).

## Запуск

Запуск с `chat_id` из `.env`:

```bash
python main.py
```

Запуск с явным `chat_id` через argparse:

```bash
python main.py --chat-id 123456789
```

Аргумент `--chat-id` имеет приоритет над `TG_CHAT_ID` в `.env`.

## Как это работает

Скрипт отправляет запросы к:

`https://dvmn.org/api/long_polling/`

и ждёт изменения статуса проверки. Когда появляется новая проверка, бот отправляет сообщение в Telegram.
