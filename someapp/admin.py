from django.contrib import admin
from .models import Habit, HabitSchedule, HabitCompletion


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'max_days', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('user',)


@admin.register(HabitSchedule)
class HabitScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'habit', 'time', 'times_per_day')
    list_filter = ('habit',)


@admin.register(HabitCompletion)
class HabitCompletionAdmin(admin.ModelAdmin):
    list_display = ('id', 'habit', 'completed', 'count')
    list_filter = ('completed', 'habit')