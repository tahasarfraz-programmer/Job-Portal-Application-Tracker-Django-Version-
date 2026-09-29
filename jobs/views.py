from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from applications.forms import ApplicationForm
from applications.models import Application
from companies.models import Company

from .models import Category, Job, SavedJob


def home(request):
    featured = Job.objects.filter(status=Job.Status.ACTIVE).select_related('company')[:4]
    categories = Category.objects.all()[:6]
    top_companies = Company.objects.all()[:6]
    return render(request, 'jobs/home.html', {'featured': featured, 'categories': categories, 'top_companies': top_companies})


def _filtered_jobs(request):
    jobs = Job.objects.filter(status=Job.Status.ACTIVE).filter(Q(deadline__isnull=True) | Q(deadline__gte=timezone.now().date()))
    q = request.GET.get('q')
    if q:
        jobs = jobs.filter(Q(title__icontains=q) | Q(company__name__icontains=q) | Q(skills__icontains=q) | Q(description__icontains=q))
    if loc := request.GET.get('location'):
        jobs = jobs.filter(location__icontains=loc)
    if cat := request.GET.get('category'):
        jobs = jobs.filter(category__slug=cat)
    if t := request.GET.get('employment_type'):
        jobs = jobs.filter(employment_type=t)
    if lvl := request.GET.get('experience_level'):
        jobs = jobs.filter(experience_level=lvl)
    if mode := request.GET.get('work_mode'):
        jobs = jobs.filter(work_mode=mode)
    if min_salary := request.GET.get('min_salary'):
        jobs = jobs.filter(salary_max__gte=min_salary)
    if posted := request.GET.get('posted'):
        jobs = jobs.filter(posted_at__gte=timezone.now() - timezone.timedelta(days=int(posted)))
    jobs = jobs.order_by('-salary_max' if request.GET.get('sort') == 'salary' else '-posted_at')
    return jobs.select_related('company', 'category')


def job_list(request):
    jobs = _filtered_jobs(request)
    page = Paginator(jobs, 10).get_page(request.GET.get('page'))
    saved_ids = set(SavedJob.objects.filter(user=request.user).values_list('job_id', flat=True)) if request.user.is_authenticated else set()
    return render(request, 'jobs/list.html', {'page': page, 'categories': Category.objects.all(), 'saved_ids': saved_ids, 'job_types': Job.EmploymentType.choices})


def job_suggestions(request):
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return JsonResponse([], safe=False)
    titles = list(Job.objects.filter(status=Job.Status.ACTIVE, title__icontains=q).values_list('title', flat=True).distinct()[:6])
    return JsonResponse(titles, safe=False)


def job_detail(request, pk):
    job = get_object_or_404(Job.objects.select_related('company', 'category'), pk=pk)
    related = Job.objects.filter(status=Job.Status.ACTIVE, category=job.category).exclude(pk=job.pk)[:3]
    already_applied = request.user.is_authenticated and Application.objects.filter(candidate=request.user, job=job).exists()
    is_saved = request.user.is_authenticated and SavedJob.objects.filter(user=request.user, job=job).exists()
    form = ApplicationForm()
    return render(request, 'jobs/detail.html', {'job': job, 'related': related, 'already_applied': already_applied, 'is_saved': is_saved, 'form': form})


@login_required
def toggle_save(request, pk):
    job = get_object_or_404(Job, pk=pk)
    saved, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    if not created:
        saved.delete()
        messages.info(request, 'Removed from saved jobs.')
    else:
        messages.success(request, 'Job saved.')
    return redirect(request.META.get('HTTP_REFERER', job.get_absolute_url()))


@login_required
def apply(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.user.role != 'seeker':
        messages.error(request, 'Only candidate accounts can apply for jobs.')
        return redirect(job.get_absolute_url())
    if not job.is_open():
        messages.error(request, 'This job is no longer accepting applications.')
        return redirect(job.get_absolute_url())
    if not request.user.resume:
        messages.error(request, 'Upload a resume to your profile before applying.')
        return redirect('accounts:profile')
    if Application.objects.filter(candidate=request.user, job=job).exists():
        messages.error(request, 'You have already applied to this job.')
        return redirect(job.get_absolute_url())
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            from applications.models import ApplicationStatusEvent
            from notifications.services import notify

            app = form.save(commit=False)
            app.candidate = request.user
            app.job = job
            app.save()
            ApplicationStatusEvent.objects.create(application=app, status=app.status)
            notify(request.user, f'Your application for {job.title} was submitted.')
            notify(job.company.owner, f'{request.user.get_full_name() or request.user.username} applied for {job.title}.')
            messages.success(request, 'Application submitted.')
            return redirect('applications:tracker')
    return redirect(job.get_absolute_url())


@login_required
def saved_jobs(request):
    saved = SavedJob.objects.filter(user=request.user).select_related('job', 'job__company')
    return render(request, 'jobs/saved.html', {'saved': saved})


def error_404(request, exception):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '500.html', status=500)
