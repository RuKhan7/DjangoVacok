from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from json import loads, JSONDecodeError
from django.contrib.auth.models import User
from .models import Habit, HabitSchedule, HabitCompletion
from .forms import UserForm, HabitForm, HabitScheduleForm, HabitCompletionForm


# ================= USERS =================
@method_decorator(csrf_exempt, 'dispatch')
class UsersView(View):
    def get(self, request):
        users = list(User.objects.values('id', 'username', 'email'))
        return JsonResponse({'data': users})

    def post(self, request):
        try:
            new_data = loads(request.body)
        except JSONDecodeError:
            return JsonResponse({'status': 'error', 'code': 400}, status=400)

        form = UserForm(new_data)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(new_data['password'])
            user.save()
            return JsonResponse(
                {'status': 'success', 'message': 'Added!', 'id': user.pk}, status=201
            )
        return JsonResponse({'status': 'error', 'code': 400}, status=400)


@method_decorator(csrf_exempt, 'dispatch')
class UserView(View):
    def get(self, request, id):
        user = User.objects.values('id', 'username', 'email').get(id=id)
        return JsonResponse({'data': user})

    def put(self, request, id):
        instance = get_object_or_404(User, id=id)
        try:
            dict_from_request = loads(request.body)
        except JSONDecodeError:
            return JsonResponse({'status': 'error', 'code': 400}, status=400)

        form = UserForm(dict_from_request, instance=instance)
        if form.is_valid():
            user = form.save(commit=False)
            if dict_from_request.get('password'):
                user.set_password(dict_from_request['password'])
            user.save()
            return JsonResponse(
                {'status': 'success', 'message': 'Changed!', 'id': user.id}, status=200
            )
        return JsonResponse({'status': 'error', 'code': 400}, status=400)

    def patch(self, request, id):
        obj = get_object_or_404(User, id=id)
        dict_from_request = loads(request.body)
        current_data = model_to_dict(obj)
        current_data.update(dict_from_request)
        form = UserForm(current_data, instance=obj)
        if form.is_valid():
            if form.has_changed():
                user = form.save(commit=False)
                if dict_from_request.get('password'):
                    user.set_password(dict_from_request['password'])
                user.save()
                return JsonResponse(
                    {'status': 'success', 'message': 'Part changed!', 'id': user.id}, status=200
                )
            return JsonResponse({'status': 'success', 'message': 'No changes!'}, status=200)
        return JsonResponse({'status': 'error', 'code': 400}, status=400)

    def delete(self, request, id):
        obj = get_object_or_404(User, id=id)
        obj.delete()
        return JsonResponse({'status': 'success', 'message': 'deleted'}, status=200)


# ================= HABITS =================
@method_decorator(csrf_exempt, 'dispatch')
class UserHabitsView(View):
    def get(self, request, user_id):
        habits = list(Habit.objects.filter(user_id=user_id).values(
            'id', 'name', 'max_days', 'created_at'
        ))
        return JsonResponse({'data': habits})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        try:
            new_data = loads(request.body)
        except JSONDecodeError:
            return JsonResponse({'status': 'error', 'code': 400}, status=400)

        form = HabitForm(new_data)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = user
            habit.save()
            return JsonResponse(
                {'status': 'success', 'message': 'Added!', 'id': habit.pk}, status=201
            )
        return JsonResponse({'status': 'error', 'code': 400}, status=400)


@method_decorator(csrf_exempt, 'dispatch')
class HabitView(View):
    def get(self, request, id):
        habit = Habit.objects.values('id', 'name', 'max_days', 'user').get(id=id)
        return JsonResponse({'data': habit})

    def put(self, request, id):
        instance = get_object_or_404(Habit, id=id)
        try:
            dict_from_request = loads(request.body)
        except JSONDecodeError:
            return JsonResponse({'status': 'error', 'code': 400}, status=400)

        form = HabitForm(dict_from_request, instance=instance)
        if form.is_valid():
            habit = form.save()
            return JsonResponse(
                {'status': 'success', 'message': 'Changed!', 'id': habit.id}, status=200
            )
        return JsonResponse({'status': 'error', 'code': 400}, status=400)

    def patch(self, request, id):
        obj = get_object_or_404(Habit, id=id)
        dict_from_request = loads(request.body)
        current_data = model_to_dict(obj)
        current_data.update(dict_from_request)
        form = HabitForm(current_data, instance=obj)
        if form.is_valid():
            if form.has_changed():
                habit = form.save()
                return JsonResponse(
                    {'status': 'success', 'message': 'Part changed!', 'id': habit.id}, status=200
                )
            return JsonResponse({'status': 'success', 'message': 'No changes!'}, status=200)
        return JsonResponse({'status': 'error', 'code': 400}, status=400)

    def delete(self, request, id):
        obj = get_object_or_404(Habit, id=id)
        obj.delete()
        return JsonResponse({'status': 'success', 'message': 'deleted'}, status=200)


# ================= SCHEDULES =================
@method_decorator(csrf_exempt, 'dispatch')
class HabitSchedulesView(View):
    def get(self, request, habit_id):
        schedules = list(HabitSchedule.objects.filter(habit_id=habit_id).values(
            'id', 'time', 'times_per_day'
        ))
        return JsonResponse({'data': schedules})

    def post(self, request, habit_id):
        habit = get_object_or_404(Habit, id=habit_id)
        try:
            new_data = loads(request.body)
        except JSONDecodeError:
            return JsonResponse({'status': 'error', 'code': 400}, status=400)

        form = HabitScheduleForm(new_data)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.habit = habit
            schedule.save()
            return JsonResponse(
                {'status': 'success', 'message': 'Added!', 'id': schedule.pk}, status=201
            )
        return JsonResponse({'status': 'error', 'code': 400}, status=400)


@method_decorator(csrf_exempt, 'dispatch')
class HabitScheduleView(View):
    def get(self, request, id):
        schedule = HabitSchedule.objects.values('id', 'time', 'times_per_day', 'habit').get(id=id)
        return JsonResponse({'data': schedule})

    def put(self, request, id):
        instance = get_object_or_404(HabitSchedule, id=id)
        try:
            dict_from_request = loads(request.body)
        except JSONDecodeError:
            return JsonResponse({'status': 'error', 'code': 400}, status=400)

        form = HabitScheduleForm(dict_from_request, instance=instance)
        if form.is_valid():
            schedule = form.save()
            return JsonResponse(
                {'status': 'success', 'message': 'Changed!', 'id': schedule.id}, status=200
            )
        return JsonResponse({'status': 'error', 'code': 400}, status=400)

    def patch(self, request, id):
        obj = get_object_or_404(HabitSchedule, id=id)
        dict_from_request = loads(request.body)
        current_data = model_to_dict(obj)
        current_data.update(dict_from_request)
        form = HabitScheduleForm(current_data, instance=obj)
        if form.is_valid():
            if form.has_changed():
                schedule = form.save()
                return JsonResponse(
                    {'status': 'success', 'message': 'Part changed!', 'id': schedule.id}, status=200
                )
            return JsonResponse({'status': 'success', 'message': 'No changes!'}, status=200)
        return JsonResponse({'status': 'error', 'code': 400}, status=400)

    def delete(self, request, id):
        obj = get_object_or_404(HabitSchedule, id=id)
        obj.delete()
        return JsonResponse({'status': 'success', 'message': 'deleted'}, status=200)


# ================= COMPLETIONS =================
@method_decorator(csrf_exempt, 'dispatch')
class HabitCompletionsView(View):
    def get(self, request, habit_id):
        completions = list(HabitCompletion.objects.filter(habit_id=habit_id).values(
            'id', 'completed', 'count'
        ))
        return JsonResponse({'data': completions})

    def post(self, request, habit_id):
        habit = get_object_or_404(Habit, id=habit_id)
        try:
            new_data = loads(request.body)
        except JSONDecodeError:
            return JsonResponse({'status': 'error', 'code': 400}, status=400)

        form = HabitCompletionForm(new_data)
        if form.is_valid():
            completion = form.save(commit=False)
            completion.habit = habit
            completion.save()
            return JsonResponse(
                {'status': 'success', 'message': 'Added!', 'id': completion.pk}, status=201
            )
        return JsonResponse({'status': 'error', 'code': 400}, status=400)


@method_decorator(csrf_exempt, 'dispatch')
class HabitCompletionView(View):
    def get(self, request, id):
        completion = HabitCompletion.objects.values('id', 'completed', 'count', 'habit').get(id=id)
        return JsonResponse({'data': completion})

    def put(self, request, id):
        instance = get_object_or_404(HabitCompletion, id=id)
        try:
            dict_from_request = loads(request.body)
        except JSONDecodeError:
            return JsonResponse({'status': 'error', 'code': 400}, status=400)

        form = HabitCompletionForm(dict_from_request, instance=instance)
        if form.is_valid():
            completion = form.save()
            return JsonResponse(
                {'status': 'success', 'message': 'Changed!', 'id': completion.id}, status=200
            )
        return JsonResponse({'status': 'error', 'code': 400}, status=400)

    def patch(self, request, id):
        obj = get_object_or_404(HabitCompletion, id=id)
        dict_from_request = loads(request.body)
        current_data = model_to_dict(obj)
        current_data.update(dict_from_request)
        form = HabitCompletionForm(current_data, instance=obj)
        if form.is_valid():
            if form.has_changed():
                completion = form.save()
                return JsonResponse(
                    {'status': 'success', 'message': 'Part changed!', 'id': completion.id}, status=200
                )
            return JsonResponse({'status': 'success', 'message': 'No changes!'}, status=200)
        return JsonResponse({'status': 'error', 'code': 400}, status=400)

    def delete(self, request, id):
        obj = get_object_or_404(HabitCompletion, id=id)
        obj.delete()
        return JsonResponse({'status': 'success', 'message': 'deleted'}, status=200)