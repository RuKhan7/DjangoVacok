import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Habit, HabitSchedule, HabitCompletion
from .forms import UserForm, HabitForm, HabitScheduleForm, HabitCompletionForm
@csrf_exempt
def user_list_create(request):
    if request.method == 'GET':
        users = User.objects.all()
        data = [{'id': u.id, 'username': u.username, 'email': u.email} for u in users]
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        if request.content_type == 'application/json':
            body = json.loads(request.body)
            form = UserForm(body)
        else:
            form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return JsonResponse({'id': user.id, 'username': user.username}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)

    elif request.method == 'PUT':
        body = json.loads(request.body)
        pk = body.get('id')                        # id берём из тела
        user = get_object_or_404(User, pk=pk)
        form = UserForm(body, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if body.get('password'):
                user.set_password(body['password'])
            user.save()
            return JsonResponse(
                {'status': 'success', 'message': 'Changed!', 'id': user.pk},
                status=200
            )
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@csrf_exempt
def user_habits(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if request.method == 'GET':
        habits = Habit.objects.filter(user=user)
        data = [{'id': h.id, 'name': h.name, 'max_days': h.max_days} for h in habits]
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        if request.content_type == 'application/json':
            body = json.loads(request.body)
            form = HabitForm(body)
        else:
            form = HabitForm(request.POST)

        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = user
            habit.save()
            return JsonResponse({'id': habit.id, 'name': habit.name}, status=201)

        return JsonResponse({'errors': form.errors}, status=400)


@csrf_exempt
def habit_schedule(request, habit_id):
    try:
        habit = Habit.objects.get(id=habit_id)
    except Habit.DoesNotExist:
        return JsonResponse({'error': 'Habit not found'}, status=404)

    if request.method == 'GET':
        schedules = HabitSchedule.objects.filter(habit=habit)
        data = [{'id': s.id, 'time': str(s.time), 'times_per_day': s.times_per_day} for s in schedules]
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        if request.content_type == 'application/json':
            body = json.loads(request.body)
            form = HabitScheduleForm(body)
        else:
            form = HabitScheduleForm(request.POST)

        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.habit = habit
            schedule.save()
            return JsonResponse({'id': schedule.id, 'time': str(schedule.time)}, status=201)

        return JsonResponse({'errors': form.errors}, status=400)


@csrf_exempt
def habit_completions(request, habit_id):
    try:
        habit = Habit.objects.get(id=habit_id)
    except Habit.DoesNotExist:
        return JsonResponse({'error': 'Habit not found'}, status=404)

    if request.method == 'GET':
        completions = HabitCompletion.objects.filter(habit=habit)
        data = [{'id': c.id, 'completed': c.completed, 'count': c.count} for c in completions]
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        if request.content_type == 'application/json':
            body = json.loads(request.body)
            form = HabitCompletionForm(body)
        else:
            form = HabitCompletionForm(request.POST)

        if form.is_valid():
            completion = form.save(commit=False)
            completion.habit = habit
            completion.save()
            return JsonResponse({'id': completion.id, 'completed': completion.completed}, status=201)

        return JsonResponse({'errors': form.errors}, status=400)

    
@method_decorator(csrf_exempt, name='dispatch')
class HabitUpdateView(View):
    def put(self, request, pk):
        habit = get_object_or_404(Habit, pk=pk)
        body = json.loads(request.body)
        form = HabitForm(body, instance=habit)
        if form.is_valid():
            habit = form.save()
            return JsonResponse(
                {'status': 'success', 'message': 'Changed!', 'id': habit.pk},
                status=200
            )
        return JsonResponse(
            {'status': 'error', 'errors': form.errors}, status=400
        )

    