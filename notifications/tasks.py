from celery import shared_task
from habits.models import Habit
from notifications.telegram import send_habit_reminder
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_habit_reminders():
    """Задача для отправки напоминаний о привычках."""
    now = timezone.now()
    # Логика: напоминать за 10 минут до времени выполнения
    check_time = now + timedelta(minutes=10)
    # Находим привычки, которые должны быть выполнены в check_time
    habits_to_remind = Habit.objects.filter(
        time__hour=check_time.hour,
        time__minute=check_time.minute,
        user__telegram_chat_id__isnull=False # Только у пользователей с Telegram ID
    )

    for habit in habits_to_remind:
        send_habit_reminder(habit.user.telegram_chat_id, habit)