from django.core.exceptions import ValidationError

def validate_reward_or_related(reward, related_habit):
    if reward and related_habit:
        raise ValidationError("Нельзя одновременно указывать вознаграждение и связанную привычку.")

def validate_execution_time(execution_time):
    if execution_time > 120:
        raise ValidationError("Время выполнения не должно превышать 120 секунд.")

def validate_related_pleasant(related_habit):
    if related_habit and not related_habit.is_pleasant:
        raise ValidationError("В связанные привычки можно добавлять только приятные привычки.")

def validate_pleasant_habit(is_pleasant, reward, related_habit):
    if is_pleasant and (reward or related_habit):
        raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")

def validate_periodicity(periodicity):
    if periodicity < 1 or periodicity > 7:
        raise ValidationError("Периодичность должна быть от 1 до 7 дней.")