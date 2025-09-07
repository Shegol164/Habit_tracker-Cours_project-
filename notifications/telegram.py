import requests
from django.conf import settings
from django.urls import reverse
from urllib.parse import urljoin

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")
        return None

def send_habit_reminder(chat_id, habit):
    """Формирует и отправляет напоминание о привычке на русском языке."""
    message = f"🔔 Напоминание!\n\n"
    message += f"Пора выполнить привычку:\n"
    message += f"📍 Место: {habit.place}\n"
    message += f"🕐 Время: {habit.time.strftime('%H:%M')}\n"
    message += f"✅ Действие: '{habit.action}'\n\n"

    if habit.reward:
        message += f"🎁 Ваше вознаграждение: {habit.reward}\n"
    elif habit.related_habit:
        message += f"😊 Сделайте приятную привычку: '{habit.related_habit.action}'\n"

    send_telegram_message(chat_id, message)