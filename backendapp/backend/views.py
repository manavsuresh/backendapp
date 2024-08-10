from datetime import date
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
# from .models import Credentials, todo
# from .serializers import todoSerializer,credsSerializer
from rest_framework import viewsets
import os

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({},request))

def serve_csv(request):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'build/static/csv/data_set.csv')
    with open(file_path, 'r') as file:
        response = HttpResponse(file.read(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Data_set.csv"'
        return response
    
def serve_image(request, image_name):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    image_paths = [
        os.path.join(base_dir, 'build/static/images', image_name),
        os.path.join(base_dir, 'build/static/media', image_name)
    ]
    
    for path in image_paths:
        if os.path.exists(path):
            with open(path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='image/jpeg')
                response['Content-Disposition'] = f'inline; filename="{image_name}"'
                return response
    
    return HttpResponse(status=404)
# Create your views here.
