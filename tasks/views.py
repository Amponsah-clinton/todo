from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from .models import Task, Profile
from django.utils import timezone
from twilio.rest import Client
from django.conf import settings

def send_sms_notification(phone_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number,
    )

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})

def task_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        due_date = request.POST['due_date']
        priority = request.POST['priority']
        task = Task.objects.create(
            user=request.user, 
            title=title,
            due_date=due_date, 
            priority=priority,
        )
        return redirect('task_list')
    return render(request, 'task_create.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task

@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        task.completed = True
        task.save()
        return redirect('task_list')
    
    return redirect('task_list') 

