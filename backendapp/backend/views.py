from datetime import date
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import creds
# from .models import Credentials, todo
# from .serializers import todoSerializer,credsSerializer
# from rest_framework import viewsets
import os
import csv
details = {}
message = {}

def get_ip(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

###########################################################################

def login(request):
    global message
    template = loader.get_template('login.html')
    try:
        vals = {
            'message': message[get_ip(request)]
        }
    except:
        vals = {
            'message': ''
        }
    return HttpResponse(template.render(vals,request))
    # return HttpResponse(template.render({},request))

def login_check(request):
    global message
    a = request.POST['username']
    b = request.POST['password']
    login_vals = creds.objects.all().values()
    for i in login_vals:
        if i['username'] == a and i['password'] == b:
            ip = get_ip(request)    
            details[ip] = [i['username'],i['level']]
            message[get_ip(request)] = ''
            print("Success login")
            return HttpResponseRedirect('/')
    message[get_ip(request)] = 'Wrong Credentials!!'
    return HttpResponseRedirect('/login')


def register_process(request):
    global message
    a = request.POST['user']
    b = request.POST['passwd']
    c = request.POST['email']
    d = request.POST['role']
    c = creds(username=a,password=b,email=c,level=d)
    c.save()

    data = creds.objects.all().values()
    csv_file = 'build/static/csv/users.csv'
    with open(csv_file, 'w', newline='') as file:
        fieldnames = ['username', 'email','role']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for user in data:
            writer.writerow({'username': user['username'], 'email': user['email'], 'role': user['level']})

    print("Success register")
    message[get_ip(request)] = ''
    return HttpResponseRedirect('/login')
    
def serve_users(request):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/csv/users.csv')
    with open(file_path, 'r') as file:
        response = HttpResponse(file.read(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'
        return response


############################################################################

def index(request):
    ip = get_ip(request)
    if ip in details.keys():
        template = loader.get_template('index.html')
        return HttpResponse(template.render({},request))
    else:
        template = loader.get_template('login.html')
        message[get_ip(request)] = ''
        vals = {
            'message': message[get_ip(request)]
        }
        return HttpResponse(template.render(vals,request))
    


def serve_csv(request):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'build/static/csv/Data_set.csv')
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

def serve_favicon(request):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    favicon_path = os.path.join(base_dir, 'build/favicon.ico')
    with open(favicon_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='image/x-icon')
        response['Content-Disposition'] = 'inline; filename="favicon.ico"'
        return response
# Create your views here.
