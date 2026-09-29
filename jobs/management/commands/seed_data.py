from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User
from applications.models import Application, ApplicationStatusEvent, Interview
from companies.models import Company
from jobs.models import Category, Job
from notifications.models import Notification

PASSWORD = 'Password123!'


class Command(BaseCommand):
    help = 'Wipe and re-seed the database with fictional demo data.'

    def handle(self, *args, **options):
        for model in [Notification, Interview, ApplicationStatusEvent, Application, Job, Category, Company]:
            model.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        cats = {name: Category.objects.create(name=name, slug=name.lower()) for name in ['Engineering', 'Design', 'Marketing', 'Data', 'Operations']}

        admin, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@demo.test', 'role': 'admin', 'is_staff': True, 'is_superuser': True})
        admin.set_password(PASSWORD)
        admin.save()

        seeker1 = User.objects.create_user(username='sam', email='seeker@demo.test', password=PASSWORD, first_name='Sam', last_name='Rivera', role='seeker', title='Frontend Developer', location='Lisbon', skills='React, CSS, TypeScript', bio='Frontend developer who cares about accessibility.')
        seeker2 = User.objects.create_user(username='priya', email='priya@demo.test', password=PASSWORD, first_name='Priya', last_name='Nair', role='seeker', title='Data Analyst', location='Remote', skills='SQL, Python')
        employer1 = User.objects.create_user(username='olu', email='employer@demo.test', password=PASSWORD, first_name='Olu', last_name='Bright', role='employer')
        employer2 = User.objects.create_user(username='mei', email='mei@demo.test', password=PASSWORD, first_name='Mei', last_name='Tanaka', role='employer')

        c1 = Company.objects.create(owner=employer1, name='Brightwave Labs', industry='Software', location='Lisbon', size='51-200', founded_year=2016, description='Fictional studio building scheduling tools for clinics.', website='https://example.com')
        c2 = Company.objects.create(owner=employer2, name='Northfield Foods', industry='Food & Beverage', location='Toronto', size='201-500', founded_year=2009, description='Fictional regional grocery and logistics group.', website='https://example.com')

        deadline = timezone.now().date() + timedelta(days=30)
        job_specs = [
            ('Senior React Engineer', c1, cats['Engineering'], 'senior', 'remote', 'Remote', 90000, 120000, 'React, TypeScript'),
            ('Product Designer', c1, cats['Design'], 'mid', 'hybrid', 'Lisbon', 60000, 80000, 'Figma, Research'),
            ('Backend Developer (Node)', c1, cats['Engineering'], 'mid', 'hybrid', 'Lisbon', 70000, 95000, 'Node.js, MongoDB'),
            ('Data Analyst', c2, cats['Data'], 'entry', 'on-site', 'Toronto', 55000, 70000, 'SQL, Python'),
            ('Logistics Coordinator', c2, cats['Operations'], 'mid', 'on-site', 'Toronto', 50000, 62000, 'Planning'),
            ('Marketing Intern', c2, cats['Marketing'], 'entry', 'remote', 'Remote', 15000, 20000, 'Copywriting'),
        ]
        jobs = []
        for title, company, cat, level, mode, location, lo, hi, skills in job_specs:
            jobs.append(Job.objects.create(
                title=title, company=company, category=cat, experience_level=level, work_mode=mode, location=location,
                salary_min=lo, salary_max=hi, skills=skills, employment_type='internship' if 'Intern' in title else 'full-time',
                description=f'{title} at {company.name}. Work with a small, collaborative team on real problems.',
                responsibilities='Own features end to end\nCollaborate with product and design',
                requirements='Relevant experience\nClear communication', benefits='Health cover\nLearning budget', deadline=deadline,
            ))

        app1 = Application.objects.create(candidate=seeker1, job=jobs[0], cover_letter='I have four years of React experience and would love to contribute.', status='interview')
        for s in ['applied', 'under-review', 'interview']:
            ApplicationStatusEvent.objects.create(application=app1, status=s)
        Application.objects.create(candidate=seeker2, job=jobs[3], cover_letter='I enjoy turning messy data into decisions.')
        Interview.objects.create(application=app1, scheduled_at=timezone.now() + timedelta(days=5), type='video', location_or_link='https://meet.example.com/demo', notes='Technical conversation, 45 minutes')
        Notification.objects.create(user=seeker1, message='Interview scheduled for Senior React Engineer.')

        self.stdout.write(self.style.SUCCESS(f'Seeded. Demo password for all accounts: {PASSWORD}'))
        self.stdout.write('admin (superuser) | seeker@demo.test | priya@demo.test | employer@demo.test | mei@demo.test')
