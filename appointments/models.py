from django.db import models

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
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    doctor = models.ForeignKey('accounts.CustomUser', related_name='doctor_schedule', on_delete=models.CASCADE)

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('patient', 'doctor', 'schedule')
        ordering = ['-created_at']


