from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from users.decorators import  role_in_required
from django.contrib import messages


@login_required()
def project_list(request):
    user = request.user
    if user.role in ['admin', 'manager']:
        projects = Project.objects.all()
    elif user.role == 'team':
        projects = Project.objects.filter(assigned_team=user)
    else:
        projects = Project.objects.none()  # למקרה שקיים תפקיד חריג
    return render(request, 'projects/project_list.html', {
        'projects': projects,
    })


@login_required()
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user.role == 'employee':
        tasks = project.task_set.filter(is_active=True, assigned_to=request.user)
    else:
        tasks = project.task_set.filter(is_active=True)

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'tasks': tasks,
    })


@login_required()
@role_in_required(['admin','manager'])
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})


@login_required()
@role_in_required(['admin', 'manager'])
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully.")
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form, 'edit_mode': True})

@login_required()
@role_in_required(['admin', 'manager'])
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()  # כאן אנחנו מבצעים מחיקה רגילה כי פרויקטים לא שומרים על היסטוריה חשובה
    messages.success(request, "Project deleted successfully.")
    return redirect('project_list')