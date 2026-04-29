import argparse
import os
import time

import requests
import telegram
from dotenv import load_dotenv


def verified_work_message(attempt):
    lesson_title = attempt["lesson_title"]
    lesson_url = attempt["lesson_url"]
    if attempt["is_negative"]:
        verdict_text = "Работа не принята, в решении есть ошибки."
    else:
        verdict_text = "Работа принята. Можно переходить к следующему уроку."
    return (
        "Преподаватель проверил вашу работу.\n"
        f'Урок: "{lesson_title}"\n'
        f"Результат: {verdict_text}\n"
        f"Ссылка на урок: {lesson_url}"
    )


def parse_args(default_chat_id):
    parser = argparse.ArgumentParser(
        description="Отправляет уведомления о проверках уроков на Devman в Telegram.",
    )
    parser.add_argument(
        "--chat-id",
        dest="chat_id",
        default=default_chat_id,
        help="Telegram chat_id получателя уведомлений.",
    )
    return parser.parse_args()


def main():
    load_dotenv()
    args = parse_args(os.getenv("TG_CHAT_ID"))
    devman_token = os.getenv("DEVMAN_TOKEN")
    tg_token = os.getenv("TG_TOKEN")
    tg_chat_id = args.chat_id

    if not devman_token:
        raise RuntimeError("Переменная DEVMAN_TOKEN не найдена в .env")
    if not tg_token:
        raise RuntimeError("Переменная TG_TOKEN не найдена в .env")
    if not tg_chat_id:
        raise RuntimeError(
            "Укажите chat_id через --chat-id или переменную TG_CHAT_ID в .env",
        )

    headers = {
        "Authorization": f"Token {devman_token}",
    }
    bot = telegram.Bot(token=tg_token)

    timestamp = None
    while True:
        params = {}
        if timestamp is not None:
            params["timestamp"] = timestamp

        try:
            response = requests.get(
                "https://dvmn.org/api/long_polling/",
                headers=headers,
                params=params,
                timeout=100,
            )
            response.raise_for_status()
            api_response = response.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            time.sleep(5)
            continue

        status = api_response.get("status")
        if status == "timeout":
            timestamp = api_response["timestamp_to_request"]
        elif status == "found":
            timestamp = api_response["last_attempt_timestamp"]
            for attempt in api_response["new_attempts"]:
                bot.send_message(
                    text=verified_work_message(attempt),
                    chat_id=tg_chat_id,
                )


if __name__ == "__main__":
    main()
