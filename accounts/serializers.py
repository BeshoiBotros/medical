from rest_framework import serializers
from .models import CustomUser

# for registration
class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name',  'role']

class DoctorSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only = True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'is_available', 'bio', 'image', 'medical_spesification', 'phone_number', 'address', 'first_name', 'last_name']

class PatientSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only = True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'image', 'phone_number', 'first_name', 'last_name']