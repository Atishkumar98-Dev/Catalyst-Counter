import os
import pandas as pd
from django.core.management.base import BaseCommand
from .models import Company
from django.conf import settings
from tqdm import tqdm  # Optional for progress bar

class Command(BaseCommand):
    help = 'Import CSV data into the CompanyData model'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='The path to the CSV file you want to import',
        )

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        if not os.path.exists(csv_file):
            self.stderr.write(self.style.ERROR(f"File {csv_file} does not exist"))
            return

        # Reading the CSV file using Pandas
        self.stdout.write(self.style.SUCCESS(f"Reading {csv_file}..."))
        try:
            df = pd.read_csv(csv_file)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to read CSV file: {str(e)}"))
            return

        # Check if the dataframe has required columns
        required_columns = ['company_name', 'industry', 'revenue']  # Adjust based on your model
        for col in required_columns:
            if col not in df.columns:
                self.stderr.write(self.style.ERROR(f"Missing required column: {col}"))
                return

        company_data_list = [
            Company(
                company_name=row['company_name'],
                industry=row['industry'],
                revenue=row['revenue'],
            )
            for _, row in tqdm(df.iterrows(), total=df.shape[0], desc="Importing data")
        ]

        # Bulk insert into the database
        try:
            Company.objects.bulk_create(company_data_list, batch_size=1000)
            self.stdout.write(self.style.SUCCESS(f"Successfully imported {len(company_data_list)} records into the database"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to insert data: {str(e)}"))

