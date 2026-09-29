from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render

from applications.models import Application
from companies.models import Company

from .forms import ProfileForm, RegisterForm, ResumeForm
from .models import User


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to Hirewell! Your account has been created.')
            return redirect('dashboard:redirect')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


class LoginView(auth_views.LoginView):
    template_name = 'registration/login.html'


login_view = LoginView.as_view()


def logout_view(request):
    logout(request)
    messages.info(request, "You've been logged out.")
    return redirect('jobs:home')


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def resume_upload(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            from django.utils import timezone
            user = form.save(commit=False)
            user.resume_uploaded_at = timezone.now()
            user.save()
            messages.success(request, 'Resume uploaded.')
        else:
            messages.error(request, ' '.join(sum(form.errors.values(), [])))
    return redirect('accounts:profile')


@login_required
def resume_delete(request):
    if request.method == 'POST' and request.user.resume:
        request.user.resume.delete(save=False)
        request.user.resume = None
        request.user.save()
        messages.info(request, 'Resume removed.')
    return redirect('accounts:profile')


@login_required
def resume_download(request):
    if not request.user.resume:
        raise Http404('No resume on file')
    return FileResponse(request.user.resume.open('rb'), as_attachment=True, filename=request.user.resume.name.split('/')[-1])


@login_required
def candidate_resume_download(request, user_id):
    candidate = User.objects.filter(pk=user_id, role=User.Role.SEEKER).first()
    if not candidate or not candidate.resume:
        raise Http404('No resume on file')
    allowed = request.user.is_admin_role() or request.user == candidate
    if not allowed and request.user.role == User.Role.EMPLOYER:
        company = Company.objects.filter(owner=request.user).first()
        allowed = bool(company and Application.objects.filter(candidate=candidate, job__company=company).exists())
    if not allowed:
        raise PermissionDenied('You do not have access to this resume.')
    return FileResponse(candidate.resume.open('rb'), as_attachment=True, filename=candidate.resume.name.split('/')[-1])
