import os
import csv
import json
import pika
import threading
from IPython import embed
from .models import Job, Node
from helper.py import job_accept_cb
from interface.settings import ARCHIVE_DIR
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseBadRequest


# Create your views here.
class LoginPage(TemplateView):

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        if uname == '' or pwd == '':
            return HttpResponseBadRequest('Username or Password missing')
        user = authenticate(request, username=uname, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        return render(request, "login.html", {'status': 'Invalid Username or Password'})


class SignUpPage(TemplateView):

    def get(self, request):
        return render(request, "signup.html") 
    def post(self, request):
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        if uname == '' or pwd == '':
            return HttpResponseBadRequest('Username or Password missing')
        user = User.objects.create_user(username=uname, password=pwd)
        user.save()
        return redirect('/login/')


class HomePage(TemplateView):

    def get(self, request):
        return render(request, "index.html")


class DashboardPage(TemplateView):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login/')
        if request.user.is_staff:
            return redirect('/dashboard/admin/')
        return redirect('/dashboard/user/')


class LogoutPage(TemplateView):

    def get(self, request):
        logout(request)
        return redirect('/login/')


class AdminPage(TemplateView):

    def get(self, request):
        return render(request, 'admin.html')


@method_decorator(csrf_exempt, name='dispatch')
class UserPage(TemplateView):

    def get(self, request):
        return render(request, 'user.html')

    def post(self, request):
        jobname = request.POST.get('jobname')
        datatype = request.POST.get('datatype')
        serviceslist = request.POST.get('serviceslist')
        servicesjson = json.loads(serviceslist)
        file_ = request.FILES['file']
        filepath = os.path.join(ARCHIVE_DIR, file.name)
        with open(filepath, 'wb') as fp:
            for chunk in file_.chunks():
                fp.write(chunk)
        
        #with open(filepath) as csvfile:
        #    reader = csv.DictReader(csvfile)
        #    for row in reader:
                			
        job_model = Job(name=jobname, data_type=datatype, user=request.user, services_order=serviceslist, filepath=filepath)
        nodes = Node.objects.all()
        nodeid = None
        for node in nodes:
            if node.load == 'LOW':
                job_model.node_id = node
                job_model.save()
                nodeid = node.number
        message = {
            'jobid': job_model.id,
            'topology': servicesjson
        }
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='job_queue')
        channel.basic_publish(exchange='', routing_key='job_queue', body=json.dumps(message))
        connection.close()
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='job_accept_queue')
        channel.channel.basic_consume(queue='job_accept_queue',
                      auto_ack=True,
                      on_message_callback=job_accept_cb)
        x = threading.Thread(channel.start_consuming)
        x.start()
        return HttpResponse('Success')
