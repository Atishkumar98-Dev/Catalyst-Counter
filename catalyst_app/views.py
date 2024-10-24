from django.shortcuts import render
from django.http import HttpResponse
from .models import Company
import csv
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import csv
import os
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import csv
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.shortcuts import render
from .models import Company
from django.core.paginator import Paginator
from .tasks import process_csv  # This is the background task
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from .forms import QueryForm
from .models import Company
import os
import tempfile
import csv
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Company
from .tasks import process_csv  # Ensure you have this import for the background task

@login_required
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

        # Include the file path in the response
        return JsonResponse({'status': 'success', 'message': 'File uploaded successfully.', 'file_path': file_path})

    return render(request, 'upload_data.html')





# @api_view(['GET'])
# def filter_companies(request):
#     filters = {}
#     if 'name' in request.GET:
#         filters['name__icontains'] = request.GET['name']
#     if 'industry' in request.GET:
#         filters['industry__icontains'] = request.GET['industry']
#     if 'country' in request.GET:
#         filters['country__icontains'] = request.GET['country']
#     if 'current_employee_estimate__gte' in request.GET:
#         filters['current_employee_estimate__gte'] = request.GET['current_employee_estimate__gte']
#     if 'current_employee_estimate__lte' in request.GET:
#         filters['current_employee_estimate__lte'] = request.GET['current_employee_estimate__lte']

#     count = Company.objects.filter(**filters).count()
#     return Response({'count': count})




@login_required
def query_builder(request):
    form = QueryForm(request.GET or None)
    if form.is_valid():
        name = form.cleaned_data.get('name')
        industry = form.cleaned_data.get('industry')
        size_range = form.cleaned_data.get('size_range')
        locality = form.cleaned_data.get('locality')
        country = form.cleaned_data.get('country')
        current_employee_estimate = form.cleaned_data.get('current_employee_estimate')
        total_employee_estimate = form.cleaned_data.get('total_employee_estimate')
        filters = {}
        if name:
            filters['name__icontains'] = name
        if industry:
            filters['industry__icontains'] = industry
        if size_range:
            filters['size_range__icontains'] = size_range
        if locality:
            filters['locality__icontains'] = locality
        if country:
            filters['country__icontains'] = country
        if current_employee_estimate is not None:
            filters['current_employee_estimate'] = current_employee_estimate
        if total_employee_estimate is not None:
            filters['total_employee_estimate'] = total_employee_estimate
        
        filtered_companies = Company.objects.filter(**filters)
        count = filtered_companies.count()

        # Pagination logic
        paginator = Paginator(filtered_companies, 10)  
        page_number = request.GET.get('page')
        companies = paginator.get_page(page_number)  

        context = {
            'form': form,
            'companies': companies,  # Use the paginated companies
            'count': count,
            'paginator': paginator  # Pass the paginator for context if needed
        }
    else:
        context = {
            'form': form,
            'companies': [],
            'count': 0
        }

    return render(request, 'query_builder.html', context)



class UserListView(ListView):
    model = User
    template_name = 'user/user_list.html'
    context_object_name = 'users'

# User Create View
class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('user_list')

# User Update View
class UserUpdateView(UpdateView):
    model = User
    form_class = UserCreationForm  # You can create a custom form if needed
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('user_list')

# User Delete View
class UserDeleteView(DeleteView):
    model = User
    template_name = 'user/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')