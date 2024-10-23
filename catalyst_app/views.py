from django.shortcuts import render
from django.http import HttpResponse
from .models import Company
import csv
from rest_framework.decorators import api_view
from rest_framework.response import Response


import csv
import os
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import csv
from django.http import HttpResponse
from django.shortcuts import render
from .models import Company

from .tasks import process_csv  # This is the background task

@csrf_exempt  # You can use CSRF tokens for security
def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['file']
        # Save the file to a temporary location
        file_path = os.path.join('/tmp', csv_file.name)  # Ensure /tmp exists or use another directory
        with open(file_path, 'wb+') as destination:
            for chunk in csv_file.chunks():  # Handle large files in chunks
                destination.write(chunk)
        
        # Trigger the background processing task
        process_csv.delay(file_path)  # Call the task using Celery

        return JsonResponse({'status': 'success', 'message': 'File uploaded successfully.'})
    
    return render(request, 'upload_data.html')



@api_view(['GET'])
def filter_companies(request):
    filters = {}
    if 'industry' in request.GET:
        filters['industry'] = request.GET['industry']
    if 'country' in request.GET:
        filters['country'] = request.GET['country']

    count = Company.objects.filter(**filters).count()
    return Response({'count': count})
