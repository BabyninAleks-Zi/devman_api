import os
import time

import requests
import telegram
from dotenv import load_dotenv

LONG_POLL_CONNECT_TIMEOUT = 5
LONG_POLL_READ_TIMEOUT = 120


def check_work(attempt):
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


def main():
    load_dotenv()
    devman_token = os.getenv("DEVMAN_TOKEN")
    tg_token = os.getenv("TG_TOKEN")
    tg_chat_id = os.getenv("TG_CHAT_ID")

    if not devman_token:
        raise RuntimeError("Переменная DEVMAN_TOKEN не найдена в .env")
    if not tg_token:
        raise RuntimeError("Переменная TG_TOKEN не найдена в .env")
    if not tg_chat_id:
        raise RuntimeError("Переменная TG_CHAT_ID не найдена в .env")

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
                timeout=(LONG_POLL_READ_TIMEOUT, LONG_POLL_CONNECT_TIMEOUT),
            )
            response.raise_for_status()
            api_response = response.json()

        except requests.exceptions.ReadTimeout:
            continue

        except requests.exceptions.ConnectionError:
            time.sleep(5)
            continue

        status = api_response.get("status")
        if status == "timeout":
            timestamp = api_response["timestamp_to_request"]
        elif status == "found":
            timestamp = api_response["last_attempt_timestamp"]
            for attempt in api_response["new_attempts"]:
                bot.send_message(
                    text=check_work(attempt),
                    chat_id=tg_chat_id,
                )


if __name__ == "__main__":
    main()
