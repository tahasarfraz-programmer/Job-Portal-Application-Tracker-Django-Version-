from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from companies.models import Company
from jobs.models import Job
from notifications.services import notify

from .forms import InterviewForm, StatusForm
from .models import Application, ApplicationStatusEvent


def _assert_access(user, application):
    if user.is_admin_role() or application.candidate_id == user.id:
        return
    company = Company.objects.filter(owner=user).first()
    if user.role == 'employer' and company and application.job.company_id == company.id:
        return
    raise PermissionDenied('You do not have access to this application.')


@login_required
def tracker(request):
    apps = Application.objects.filter(candidate=request.user).select_related('job', 'job__company').prefetch_related('interviews')
    status = request.GET.get('status')
    if status:
        apps = apps.filter(status=status)
    view = request.GET.get('view', 'table')
    return render(request, 'applications/tracker.html', {'apps': apps, 'view': view, 'statuses': Application.Status.choices, 'selected': status})


@login_required
def application_detail(request, pk):
    app = get_object_or_404(Application.objects.select_related('job', 'job__company', 'candidate').prefetch_related('history', 'interviews'), pk=pk)
    _assert_access(request.user, app)
    statuses = [c for c in Application.Status.choices if c[0] not in ('rejected', 'withdrawn')]
    return render(request, 'applications/detail.html', {'app': app, 'statuses': statuses})


@login_required
def withdraw(request, pk):
    app = get_object_or_404(Application, pk=pk, candidate=request.user)
    if app.status in ('hired', 'rejected', 'withdrawn'):
        messages.error(request, 'This application can no longer be withdrawn.')
    else:
        app.status = Application.Status.WITHDRAWN
        app.save()
        ApplicationStatusEvent.objects.create(application=app, status=app.status)
        messages.success(request, 'Application withdrawn.')
    return redirect('applications:tracker')


@login_required
def update_status(request, pk):
    app = get_object_or_404(Application.objects.select_related('job', 'candidate'), pk=pk)
    _assert_access(request.user, app)
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            app.status = form.cleaned_data['status']
            app.save()
            ApplicationStatusEvent.objects.create(application=app, status=app.status)
            notify(app.candidate, f'{app.job.title} moved to "{app.get_status_display()}".')
            messages.success(request, 'Status updated.')
    return redirect('applications:applicants', job_id=app.job_id)


@login_required
def schedule_interview(request, pk):
    app = get_object_or_404(Application.objects.select_related('job', 'candidate'), pk=pk)
    _assert_access(request.user, app)
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = app
            interview.save()
            if app.status != Application.Status.INTERVIEW:
                app.status = Application.Status.INTERVIEW
                app.save()
                ApplicationStatusEvent.objects.create(application=app, status=app.status)
            notify(app.candidate, f'Interview scheduled for {app.job.title}.')
            messages.success(request, 'Interview scheduled.')
        else:
            messages.error(request, ' '.join(sum(form.errors.values(), [])))
    return redirect('applications:applicants', job_id=app.job_id)


@login_required
def applicants(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    company = Company.objects.filter(owner=request.user).first()
    if request.user.role != 'admin' and (not company or job.company_id != company.id):
        raise PermissionDenied('You can only view applicants for your own jobs.')
    apps = Application.objects.filter(job=job).select_related('candidate')
    return render(request, 'applications/applicants.html', {'job': job, 'apps': apps, 'status_form': StatusForm(), 'interview_form': InterviewForm()})
