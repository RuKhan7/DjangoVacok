from django.urls import path
from . import views

urlpatterns = [
    # Users
    path('users/', views.UsersView.as_view()),
    path('users/<int:id>/', views.UserView.as_view()),

    # Habits
    path('users/<int:user_id>/habits/', views.UserHabitsView.as_view()),
    path('habits/<int:id>/', views.HabitView.as_view()),

    # Schedules
    path('habits/<int:habit_id>/schedules/', views.HabitSchedulesView.as_view()),
    path('schedules/<int:id>/', views.HabitScheduleView.as_view()),

    # Completions
    path('habits/<int:habit_id>/completions/', views.HabitCompletionsView.as_view()),
    path('completions/<int:id>/', views.HabitCompletionView.as_view()),
]