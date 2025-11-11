from django.db import models
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import time
from accounts.models import CustomUser

class Schedule(models.Model):
    
    WEEK_DAY = [
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
        ('MON', 'Monday'),
        ('TUE', 'Teusday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday')
    ]
    
    day = models.CharField(choices=WEEK_DAY)
    start_time = models.TimeField()
    end_time = models.TimeField()
    doctor = models.ForeignKey('accounts.CustomUser', related_name='doctor_schedule', on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    min_session_duration = models.PositiveIntegerField(default=30)

    class Meta:
        unique_together = ('day', 'doctor')
        ordering = ['-start_time']

class Appointment(models.Model):

    STATUS_CHOICES = [
        ('W', 'Waiting'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    ]

    patient = models.ForeignKey('accounts.CustomUser', related_name='patient_appointment', on_delete=models.CASCADE)
    doctor = models.ForeignKey('accounts.CustomUser', related_name='doctor_appointment', on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, default='W')
    start_time = models.TimeField(default=datetime.time(0, 0))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancle = models.BooleanField(default=False)

    class Meta:
        unique_together = [('patient', 'doctor', 'schedule'), ('doctor', 'schedule', 'start_time')]
        ordering = ['-created_at']


@receiver(post_save, sender=CustomUser)
def create_doctor_schedules(sender, instance, created, **kwargs):
    if created and instance.role == 'doctor':
        for day_code, _ in Schedule.WEEK_DAY:
            Schedule.objects.create(
                day=day_code,
                start_time=time(9, 0),
                end_time=time(17, 0),
                doctor=instance,
                is_available=False,
                min_session_duration=30
            )