from django.core.management.base import BaseCommand
from django.utils import timezone
from myapp.models import Task, Profile
from myapp.views import send_sms_notification

class Command(BaseCommand):
    help = 'Send SMS reminders for tasks due soon'

    def handle(self, *args, **kwargs):
        tasks_due_soon = Task.objects.filter(
            due_date__lte=timezone.now() + timezone.timedelta(hours=1), 
            completed=False
        )
        
        for task in tasks_due_soon:
            profile = Profile.objects.get(user=task.user)
            message = f"Reminder: Your task '{task.title}' is due soon!"
            send_sms_notification(profile.phone_number, message)
