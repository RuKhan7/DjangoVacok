from django import forms
from django.contrib.auth.models import User
from .models import Habit, HabitSchedule, HabitCompletion

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'max_days']

class HabitScheduleForm(forms.ModelForm):
    class Meta:
        model = HabitSchedule
        fields = ['time', 'times_per_day']


class HabitCompletionForm(forms.ModelForm):
    class Meta:
        model = HabitCompletion
        fields = ['completed', 'count']