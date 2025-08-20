from django.db import models
from django.conf import settings
from .validators import (
    validate_reward_or_related,
    validate_execution_time,
    validate_related_pleasant,
    validate_pleasant_habit,
    validate_periodicity
)

class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255, verbose_name="Место выполнения")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.TextField(verbose_name="Действие привычки")
    is_pleasant = models.BooleanField(default=False, verbose_name="Признак приятной привычки")
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='related_to', verbose_name="Связанная привычка")
    periodicity = models.PositiveSmallIntegerField(default=1, verbose_name="Периодичность (в днях)")
    reward = models.TextField(blank=True, null=True, verbose_name="Вознаграждение")
    execution_time = models.PositiveIntegerField(verbose_name="Время на выполнение (в секундах)")
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['id']

    def __str__(self):
        return f"{self.user} - {self.action}"

    def clean(self):
        validate_reward_or_related(self.reward, self.related_habit)
        validate_execution_time(self.execution_time)
        validate_related_pleasant(self.related_habit)
        validate_pleasant_habit(self.is_pleasant, self.reward, self.related_habit)
        validate_periodicity(self.periodicity)

    def save(self, *args, **kwargs):
        self.full_clean() # Вызывает clean()
        super().save(*args, **kwargs)
