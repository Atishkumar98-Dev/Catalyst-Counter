import csv
import os
from celery import shared_task
from .models import Company

@shared_task
def process_csv(file_path):
    print(file_path)
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        decoded_file = csv_file.read().splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            # Check for blank fields (only save rows that have all required fields)
            if all(row[field] for field in ['name', 'domain', 'year founded', 'industry', 
                                             'size range', 'locality', 'country', 
                                             'linkedin url', 'current employee estimate', 
                                             'total employee estimate']):
                # Check for existing company with the same domain or LinkedIn URL
                if not Company.objects.filter(domain=row['domain']).exists() and not Company.objects.filter(linkedin_url=row['linkedin url']).exists():
                    Company.objects.create(
                        name=row['name'],
                        domain=row['domain'],
                        year_founded=row['year founded'],
                        industry=row['industry'],
                        size_range=row['size range'],
                        locality=row['locality'],
                        country=row['country'],
                        linkedin_url=row['linkedin url'],
                        current_employee_estimate=row['current employee estimate'],
                        total_employee_estimate=row['total employee estimate']
                    )

    # Optional: Clean up the temporary file after processing
    os.remove(file_path)
