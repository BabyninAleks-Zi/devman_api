# Devman Telegram Notifier

Бот отслеживает проверки уроков на [dvmn.org](https://dvmn.org/) через Long Polling API и отправляет уведомления в Telegram.

В уведомлении приходит:
- название урока;
- результат проверки (принята работа или нет);
- ссылка на урок.

Ошибки бота отправляются администратору в Telegram.

## Требования

- Python 3.10-3.12
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
- `TG_CHAT_ID` — chat id администратора, который получает уведомления и логи.

## Запуск

```bash
python main.py
```

## Как это работает

Скрипт отправляет запросы к:

`https://dvmn.org/api/long_polling/`

и ждёт изменения статуса проверки. Когда появляется новая проверка, бот отправляет сообщение в Telegram.
