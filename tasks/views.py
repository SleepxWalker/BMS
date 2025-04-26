from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, TaskTimer
from .forms import TaskForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from users.decorators import  role_in_required
from django.contrib import messages

@login_required()
def task_list(request):
    user = request.user
    if user.role in ['admin', 'manager']:
        tasks = Task.objects.select_related('project', 'assigned_to').all()
    elif user.role == 'team':
        tasks = Task.objects.select_related('project', 'assigned_to').filter(assigned_to=user)
    else:
        tasks = Task.objects.none()

    query = request.GET.get('q', '')
    if query:
        tasks = tasks.filter(task_name__icontains=query)

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'query': query,
    })


@login_required()
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    user = request.user

    if user.role in ['admin', 'manager']:
        pass  # הכל בסדר
    elif user.role == 'team':
        if task.assigned_to != user:
            return render(request, '403.html', status=403)
    else:
        return render(request, '403.html', status=403)

    active_timer = task.timers.filter(user=user, end_time__isnull=True).first()
    user_times = task.get_user_times()

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'active_timer': active_timer,
        'user_times': user_times,
    })


@role_in_required(['admin', 'manager'])
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required()
def start_timer(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    user = request.user

    if user.role == 'team' and task.assigned_to != user:
        return render(request, '403.html', status=403)

    # עצור טיימרים פתוחים אחרים
    TaskTimer.objects.filter(user=user, end_time__isnull=True).update(end_time=timezone.now())

    TaskTimer.objects.create(
        task=task,
        user=user,
        start_time=timezone.now()
    )
    return redirect('task_detail', pk=task_id)


@login_required()
def stop_timer(request, task_id):
    user = request.user
    timer = TaskTimer.objects.filter(task__pk=task_id, user=user, end_time__isnull=True).first()

    if timer:
        timer.end_time = timezone.now()
        timer.save()

    return redirect('task_detail', pk=task_id)


@login_required()
@role_in_required(['admin', 'manager'])
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully.")
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'edit_mode': True})

@login_required()
@role_in_required(['admin', 'manager'])
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()  # כאן מבצעים מחיקה רגילה כי אין בעיה למחוק משימה שהתבצעה
    messages.success(request, "Task deleted successfully.")
    return redirect('task_list')