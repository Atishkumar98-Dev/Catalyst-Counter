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

import os
import tempfile
import csv
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Company
from .tasks import process_csv  # Ensure you have this import for the background task

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('file')
        
        if not csv_file:
            return JsonResponse({'status': 'error', 'message': 'No file uploaded.'})

        # Use system's temp directory instead
        upload_dir = tempfile.gettempdir()
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, csv_file.name)

        # Save the file to the specified location
        with open(file_path, 'wb+') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)

        # Trigger the background processing task
        process_csv.delay(file_path)

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
