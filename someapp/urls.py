# someapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list_create, name='user_list_create'),
    path('users/<int:user_id>/habits/', views.user_habits, name='user_habits'),
    path('habits/<int:habit_id>/schedule/', views.habit_schedule, name='habit_schedule'),
    path('habits/<int:habit_id>/completions/', views.habit_completions, name='habit_completions'),
    path('habits/<int:pk>/', views.HabitUpdateView.as_view(), name='habit_update'),
]