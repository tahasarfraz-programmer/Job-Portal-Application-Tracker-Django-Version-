from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from applications.models import Application
from companies.models import Company
from jobs.forms import JobForm
from jobs.models import Category, Job


@login_required
def redirect_dashboard(request):
    return redirect({'seeker': 'applications:tracker', 'employer': 'dashboard:employer', 'admin': 'dashboard:admin'}[request.user.role])


def _require_employer(user):
    if user.role not in ('employer', 'admin'):
        raise PermissionDenied('Employer accounts only.')


@login_required
def employer_dashboard(request):
    _require_employer(request.user)
    company = Company.objects.filter(owner=request.user).first()
    jobs = Job.objects.filter(company=company).annotate(applicant_count=Count('applications')) if company else Job.objects.none()
    apps = Application.objects.filter(job__company=company) if company else Application.objects.none()
    stats = {
        'total_jobs': jobs.count(),
        'active_jobs': jobs.filter(status=Job.Status.ACTIVE).count(),
        'total_applications': apps.count(),
        'shortlisted': apps.filter(status='shortlisted').count(),
        'interviews': apps.filter(status='interview').count(),
        'hired': apps.filter(status='hired').count(),
    }
    by_status = list(apps.values('status').annotate(n=Count('id')))
    return render(request, 'dashboard/employer.html', {'company': company, 'jobs': jobs, 'stats': stats, 'by_status': by_status})


@login_required
def job_create(request):
    _require_employer(request.user)
    company = Company.objects.filter(owner=request.user).first()
    if not company:
        messages.error(request, 'Create your company profile before posting jobs.')
        return redirect('companies:mine')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            job.save()
            messages.success(request, 'Job posted.')
            return redirect('dashboard:employer')
    else:
        form = JobForm()
    return render(request, 'dashboard/job_form.html', {'form': form})


def _owned_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    company = Company.objects.filter(owner=request.user).first()
    if request.user.role != 'admin' and (not company or job.company_id != company.id):
        raise PermissionDenied('You can only manage your own jobs.')
    return job


@login_required
def job_edit(request, pk):
    job = _owned_job(request, pk)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated.')
            return redirect('dashboard:employer')
    else:
        form = JobForm(instance=job)
    return render(request, 'dashboard/job_form.html', {'form': form, 'job': job})


@login_required
def job_delete(request, pk):
    job = _owned_job(request, pk)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted.')
    return redirect('dashboard:employer')


@login_required
def job_toggle(request, pk):
    job = _owned_job(request, pk)
    job.status = Job.Status.INACTIVE if job.status == Job.Status.ACTIVE else Job.Status.ACTIVE
    job.save()
    return redirect('dashboard:employer')


@user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')
def admin_dashboard(request):
    stats = {
        'users': User.objects.count(), 'employers': User.objects.filter(role='employer').count(),
        'candidates': User.objects.filter(role='seeker').count(), 'jobs': Job.objects.count(),
        'applications': Application.objects.count(), 'active_jobs': Job.objects.filter(status='active').count(),
    }
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_apps = Application.objects.select_related('candidate', 'job').order_by('-created_at')[:5]
    tab = request.GET.get('tab', 'users')
    rows = {'users': User.objects.order_by('-date_joined'), 'companies': Company.objects.all(), 'jobs': Job.objects.select_related('company')[:200],
            'applications': Application.objects.select_related('candidate', 'job')[:200]}.get(tab, [])
    return render(request, 'dashboard/admin.html', {'stats': stats, 'recent_users': recent_users, 'recent_apps': recent_apps, 'tab': tab, 'rows': rows, 'categories': Category.objects.all()})


@user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')
def toggle_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.role != 'admin':
        user.is_active = not user.is_active
        user.save()
    return redirect('/dashboard/admin-panel/?tab=users')


@user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.role != 'admin':
        user.delete()
        messages.success(request, 'User removed.')
    return redirect('/dashboard/admin-panel/?tab=users')


@user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')
def manage_categories(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Category.objects.get_or_create(name=name, defaults={'slug': name.lower().replace(' ', '-')})
    return redirect('/dashboard/admin-panel/?tab=categories')
