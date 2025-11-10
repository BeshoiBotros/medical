from rest_framework import serializers
from .models import CustomUser

# for registration
class CustomUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name',  'role']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser.objects.create(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

class DoctorSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only = True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'is_available', 'bio', 'image', 'medical_spesification', 'phone_number', 'address', 'first_name', 'last_name', 'role']


class PatientSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only = True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'image', 'phone_number', 'first_name', 'last_name', 'role']