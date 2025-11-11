from rest_framework import serializers
from .models import Schedule, Appointment
from accounts import models as accounts_models
from accounts import serializers as accounts_serializers

class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = '__all__'

class PatientAppointmentSerializer(serializers.ModelSerializer):

    status = serializers.CharField(read_only=True)
    doctor = serializers.PrimaryKeyRelatedField(queryset=accounts_models.CustomUser.objects.filter(role='doctor'), write_only=True)
    # patient = serializers.PrimaryKeyRelatedField(queryset=accounts_models.CustomUser.objects.filter(role='patient'))
    doctor_details = accounts_serializers.CustomUserSerializer(source='doctor', read_only=True)
    schedule = ScheduleSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'schedule', 'status', 'created_at', 'updated_at', 'doctor_details', 'patient', 'cancle']
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep.pop('doctor', None)

        return rep

class DoctorAppointmentSerializer(serializers.ModelSerializer):

    schedule = ScheduleSerializer(read_only=True)
    doctor_details = accounts_serializers.CustomUserSerializer(source='doctor', read_only=True)
    patient_details = accounts_serializers.CustomUserSerializer(source='patient', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'doctor_details', 'patient_details',  'schedule', 'status', 'created_at', 'updated_at']
