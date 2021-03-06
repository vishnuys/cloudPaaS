import os
import json
import pika
import threading
import mimetypes
from IPython import embed
from .helper import job_accept_cb
from .models import Job, Node, Result
from interface.settings import ARCHIVE_DIR
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, FileResponse


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
        users = User.objects.filter(is_staff=False, is_superuser=False)
        userlist = []
        for user in users:
            results = Result.objects.filter(user_id=user)
            jobs = Job.objects.filter(user_id=user)
            counts = [x.count for x in results if x.count is not None]
            total = sum(counts)
            services = [len(json.loads(x.services_order)) for x in jobs]
            services_count = sum(services)
            price = total * services_count / 100
            userlist.append({
                'id': user.id,
                'user': user.username,
                'records': total,
                'services': services_count,
                'price': price
            })
        print(userlist)
        total_jobs = sum([u['records'] for u in userlist])
        total_services = sum([u['services'] for u in userlist])
        return render(request, 'admin.html', {'userlist': userlist, 'total_jobs': total_jobs, 'total_services': total_services})


@method_decorator(csrf_exempt, name='dispatch')
class UserPage(TemplateView):

    def get(self, request):
        joblist = []
        resultlist = []
        jobs = Job.objects.filter(user=request.user)
        for job in jobs:
            joblist.append({
                'name': job.name,
                'services_order': "->".join(json.loads(job.services_order)),
                'date_created': job.date_created.strftime('%D-%m-%Y %H:%M'),
            })
        results = Result.objects.filter(user_id=request.user)
        for res in results:
            if res.filepath is not None:
                filename = os.path.basename(res.filepath)
                filepath = os.path.join('/file', filename)
            else:
                filename = None
                filepath = None

            resultlist.append({
                'job_name': res.job_id.name,
                'count': res.count,
                'min_val': res.min_val,
                'max_val': res.max_val,
                'avg_val': res.avg_val,
                'filename': filename,
                'filepath': filepath,
            })
        counts = [x['count'] for x in resultlist if x['count']is not None]
        total = sum(counts)
        services = [len(json.loads(x.services_order)) for x in jobs]
        services_count = sum(services)
        price = total * services_count / 100
        usage = {
            'records': total,
            'services': services_count,
            'price': price
        }
        return render(request, 'user.html', {'jobs': joblist, 'results': resultlist, 'usage': usage})

    def post(self, request):
        jobname = request.POST.get('jobname')
        datatype = request.POST.get('datatype')
        colname = request.POST.get('colname')
        serviceslist = request.POST.get('serviceslist')
        servicesjson = json.loads(serviceslist)
        file = request.FILES['file']
        filepath = os.path.join(ARCHIVE_DIR, file.name)
        with open(filepath, 'wb') as fp:
            for chunk in file.chunks():
                fp.write(chunk)

        job_model = Job(name=jobname, data_type=datatype, user=request.user, services_order=serviceslist, filepath=filepath, colname=colname)
        node = Node.objects.first()
        job_model.node_id = node
        job_model.save()
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
        channel.basic_consume(queue='job_accept_queue',
                              auto_ack=True,
                              on_message_callback=job_accept_cb)
        x = threading.Thread(target=channel.start_consuming)
        x.start()
        return HttpResponse('Success')


class FileDownload(TemplateView):

    def get(self, request, name):
        filepath = os.path.join(ARCHIVE_DIR, name)
        if not os.path.exists(filepath):
            print('NOT FOUND')
            return HttpResponseNotFound('File not found')
        response = FileResponse(open(filepath, 'rb'), as_attachment=True)
        return response
