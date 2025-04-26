from django.contrib.auth.decorators import login_required
from users.decorators import  role_in_required
from users.models import CustomUser
from django.shortcuts import render, get_object_or_404,redirect

from django.http import HttpResponseForbidden
from .forms import UserEditForm, CustomUserCreationForm
from django.contrib import messages

@login_required()
@role_in_required(['admin'])
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/user_form.html', {'form': form})

@login_required()
@role_in_required(['admin'])
def user_edit(request):
    user = request.user
    form = UserEditForm(request.POST or None, request.FILES or None, instance=user, current_user=user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated.')
        return redirect('user_detail', pk=user.pk)

    return render(request, 'users/user_edit.html', {'form': form})

@login_required()
@role_in_required(['admin'])
def user_edit_admin(request, pk):
    user_obj = get_object_or_404(CustomUser, pk=pk)
    form = UserEditForm(request.POST or None, request.FILES or None, instance=user_obj, current_user=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'User updated successfully.')
        return redirect('user_list')

    return render(request, 'users/user_form.html', {'form': form, 'edit_mode': True, 'user_obj': user_obj})

@login_required()
@role_in_required(['admin'])
def user_list(request):
    users = CustomUser.objects.all()
    can_manage = request.user.role == 'admin'
    return render(request, 'users/user_list.html', {
        'users': users,
        'can_manage': can_manage,
    })


@login_required()
def user_detail(request, pk):
    user_obj = get_object_or_404(CustomUser, pk=pk)

    # רק אדמין או המשתמש עצמו
    if request.user.role != 'admin' and request.user.pk != pk:
        return HttpResponseForbidden("You are not allowed to view this profile.")

    return render(request, 'users/user_detail.html', {'user_obj': user_obj})

@login_required()
@role_in_required(['admin'])
def user_delete(request, pk):
    user_obj = get_object_or_404(CustomUser, pk=pk)
    if request.user.pk == user_obj.pk:
        messages.error(request, "You can't delete yourself.")
    else:
        user_obj.delete()
        messages.success(request, "User deleted successfully.")
    return redirect('user_list')