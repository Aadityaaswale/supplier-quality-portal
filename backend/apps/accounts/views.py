from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get('next') or request.POST.get('next') or 'dashboard'
                return redirect(next_url)
            else:
                messages.error(request, "Your account has been deactivated. Please contact an Administrator.")
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('login')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    my_reviews_count = request.user.quality_reviews.count()
    approved_count = request.user.quality_reviews.filter(status='Approved').count()

    context = {
        'profile': profile,
        'my_reviews_count': my_reviews_count,
        'approved_count': approved_count,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def user_management_view(request):
    # Only Admin can manage users
    user_role = getattr(request.user.profile, 'role', 'REVIEWER') if hasattr(request.user, 'profile') else 'REVIEWER'
    if not (request.user.is_superuser or user_role == 'ADMIN'):
        messages.error(request, "Access denied. Only Administrators can access User Management.")
        return redirect('dashboard')

    users = User.objects.select_related('profile').all().order_by('-date_joined')

    if request.method == 'POST':
        action = request.POST.get('action')
        target_user_id = request.POST.get('user_id')
        target_user = get_object_or_404(User, id=target_user_id)

        if action == 'toggle_status':
            if target_user == request.user:
                messages.warning(request, "You cannot deactivate your own administrative account.")
            else:
                target_user.is_active = not target_user.is_active
                target_user.save()
                messages.success(request, f"Status updated for {target_user.username}.")
        elif action == 'change_role':
            new_role = request.POST.get('role')
            if new_role in ['ADMIN', 'QUALITY_MANAGER', 'REVIEWER']:
                target_user.profile.role = new_role
                target_user.profile.save()
                messages.success(request, f"Role for {target_user.username} updated to {new_role}.")

        return redirect('user-management')

    return render(request, 'accounts/user_management.html', {'users': users})
