import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from faker import Faker

from accounts.models import Company
from jobs.models import Job


class Command(BaseCommand):
    help = 'Seed the database with companies and jobs'

    def handle(self, *args, **options):
        fake = Faker()
        industries = [
            'Software', 'Finance', 'Healthcare', 'Education', 'Retail',
            'Manufacturing', 'Telecom', 'Energy', 'Consulting', 'Logistics'
        ]
        job_types = [choice[0] for choice in Job.JOB_TYPE_CHOICES]
        experience_levels = [choice[0] for choice in Job.EXPERIENCE_CHOICES]
        skill_sets = [
            'Python', 'Django', 'JavaScript', 'React', 'SQL', 'AWS', 'Docker',
            'HTML', 'CSS', 'TypeScript', 'Java', 'C++', 'Node.js', 'REST',
            'Git', 'Linux', 'Data Analysis', 'Machine Learning', 'Cybersecurity',
            'Project Management'
        ]

        self.stdout.write(self.style.NOTICE('Starting data seeding...'))

        company_count = 50
        companies_created = 0
        jobs_created = 0

        for i in range(company_count):
            try:
                company_name = fake.unique.company()
                username = f"company_{i+1}"
                email = fake.unique.email()
                website = f'https://www.{company_name.replace(" ", "").lower()}.com'
                address = fake.address().replace('\n', ', ')
                phone = fake.phone_number()
                industry = random.choice(industries)
                city = fake.city()
                state = fake.state()
                description = fake.paragraph(nb_sentences=4)

                # Create User first (skip if exists)
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': email,
                        'first_name': company_name
                    }
                )
                
                if created:
                    user.set_password('Company@123')
                    user.save()

                # Create or update Company linked to User
                company, c_created = Company.objects.get_or_create(
                    user=user,
                    defaults={
                        'company_name': company_name,
                        'phone': phone,
                        'website': website,
                        'address': address,
                        'city': city,
                        'state': state,
                        'industry': industry,
                        'description': description,
                    }
                )
                
                if c_created:
                    companies_created += 1

                job_count = random.randint(3, 10)
                for _ in range(job_count):
                    title = fake.job()
                    required_skills = ', '.join(random.sample(skill_sets, k=random.randint(3, 6)))
                    min_salary = random.randrange(3, 8)
                    max_salary = min_salary + random.randint(2, 5)
                    allowed_branches = 'CSE, ECE, ME, CE, EE'
                    deadline = timezone.now() + timedelta(days=random.randint(15, 90))
                    job = Job.objects.create(
                        company=company,
                        title=title,
                        description=fake.paragraph(nb_sentences=5),
                        required_skills=required_skills,
                        salary_min=min_salary,
                        salary_max=max_salary,
                        location=fake.city(),
                        job_type=random.choice(job_types),
                        experience_required=random.choice(experience_levels),
                        application_deadline=deadline,
                        allowed_branches=allowed_branches,
                    )
                    jobs_created += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Error creating company {i+1}: {str(e)}'))
                continue

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {companies_created} companies and {jobs_created} jobs.'
        ))
