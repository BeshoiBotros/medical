from rest_framework import serializers
from .models import Schedule, Appointment
from accounts import models as accounts_models
from accounts import serializers as accounts_serializers
from rest_framework.exceptions import ValidationError
from datetime import datetime, timedelta, date
class ScheduleSerializer(serializers.ModelSerializer):

    doctor = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Schedule
        fields = '__all__'



class PatientAppointmentSerializer(serializers.ModelSerializer):
    doctor = accounts_serializers.DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=accounts_models.CustomUser.objects.filter(role='doctor'),
        source='doctor',
        write_only=True
    )
    schedule = ScheduleSerializer(read_only=True)
    schedule_id = serializers.PrimaryKeyRelatedField(
        queryset=Schedule.objects.all(),
        source='schedule',
        write_only=True
    )
    
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'doctor_id', 'schedule', 'schedule_id', 'status', 'start_time', 'created_at', 'updated_at', 'cancle']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

    def validate(self, data):
        if self.instance:
            doctor = data.get('doctor', self.instance.doctor)
            schedule = data.get('schedule', self.instance.schedule)
            start_time = data.get('start_time', self.instance.start_time)
        else:
            doctor = data['doctor']
            schedule = data['schedule']
            start_time = data['start_time']

        if schedule.doctor != doctor:
            raise ValidationError("Schedule does not belong to the selected doctor.")

        duration_delta = timedelta(minutes=schedule.min_session_duration)
        proposed_end = (datetime.combine(date.today(), start_time) + duration_delta).time()

        if start_time < schedule.start_time or proposed_end > schedule.end_time:
            raise ValidationError("Requested start time is outside the schedule's available hours.")

        if Appointment.objects.filter(
            doctor=doctor,
            schedule=schedule,
            start_time=start_time,
            status__in=['W', 'A'],
            cancle=False
        ).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError("This time slot is already taken.")

        return data

    def create(self, validated_data):
        validated_data['patient'] = self.context['request'].user
        return super().create(validated_data)


class DoctorAppointmentSerializer(serializers.ModelSerializer):
    patient = accounts_serializers.PatientSerializer(read_only=True)
    schedule = ScheduleSerializer(read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'schedule', 'status', 'start_time', 'created_at', 'updated_at', 'cancle']
        read_only_fields = ['id', 'patient', 'schedule', 'start_time', 'created_at', 'updated_at']