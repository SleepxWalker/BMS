from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import render

def role_in_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Access denied: user not authenticated.")
            if request.user.role not in allowed_roles:
                return render(request, '403.html', status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def role_required(role):
    def decorator(view_func):
        decorated_view_func = user_passes_test(
            lambda u: u.is_authenticated and u.role == role,
            login_url='login'
        )(view_func)
        return decorated_view_func
    return decorator

