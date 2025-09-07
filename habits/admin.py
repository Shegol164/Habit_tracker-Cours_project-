from django.contrib import admin
from .models import Habit

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'time', 'place', 'is_pleasant', 'is_public', 'periodicity')
    list_filter = ('is_pleasant', 'is_public', 'periodicity', 'user')
    search_fields = ('action', 'place', 'user__username')
    # raw_id_fields = ('user', 'related_habit') # Полезно для ForeignKey полей с большим кол-вом записей