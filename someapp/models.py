from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=255)
    max_days = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class HabitSchedule(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='schedules')
    time = models.TimeField()
    times_per_day = models.IntegerField(default=1)

class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='completions')
    completed = models.BooleanField(default=False)
    count = models.IntegerField(default=0)
    