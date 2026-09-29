from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from jobs.models import Job

from .forms import CompanyForm
from .models import Company


def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    jobs = Job.objects.filter(company=company, status=Job.Status.ACTIVE)
    return render(request, 'companies/detail.html', {'company': company, 'jobs': jobs})


@login_required
def my_company(request):
    if request.user.role != 'employer':
        messages.error(request, 'Only employer accounts have a company profile.')
        return redirect('dashboard:redirect')
    company, _ = Company.objects.get_or_create(owner=request.user, defaults={'name': request.user.get_full_name() or request.user.username})
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company profile saved.')
            return redirect('companies:mine')
    else:
        form = CompanyForm(instance=company)
    return render(request, 'companies/form.html', {'form': form, 'company': company})
