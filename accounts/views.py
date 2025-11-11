from rest_framework.views import APIView
from medical.utils import IsDoctor, IsPatient
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .serializers import CustomUserSerializer, DoctorSerializer, PatientSerializer, SubProfileSerializer, CustomTokenObtainPairSerializer
from . import models as accounts_models
from rest_framework.permissions import IsAuthenticated
from medical.utils import get_object_or_404
from .filters import DoctorFilter, PatientFilter
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(APIView):

    def post(self, request: Request):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DoctorView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        elif self.request.method == 'PATCH':
            return [IsDoctor()]
        return super().get_permissions()

    def get(self, request: Request, id=None):
        
        if id:
            queryset = get_object_or_404(accounts_models.CustomUser, role='doctor', pk=id)
            doctor_serializer = DoctorSerializer(queryset)
            return Response(doctor_serializer.data, status=status.HTTP_200_OK)
        
        queryset = accounts_models.CustomUser.objects.filter(role='doctor')
        filterset = DoctorFilter(request.query_params, queryset=queryset)
        
        # if filterset.is_valid():
        queryset = filterset.qs
        
        doctor_serializer = DoctorSerializer(queryset, many=True)
        return Response(doctor_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request):
        
        doctor_serializer = DoctorSerializer(instance=request.user, data=request.data, partial=True)
        if doctor_serializer.is_valid():
            doctor_serializer.save()
            return Response(doctor_serializer.data, status=status.HTTP_200_OK)
        
        return Response(doctor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'PATCH':
            return [IsPatient()]
        return super().get_permissions()

    def get(self, request: Request, id=None):
        
        if id:
            queryset = get_object_or_404(accounts_models.CustomUser, role='patient', pk=id)
            serializer = PatientSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        queryset = accounts_models.CustomUser.objects.filter(role='Patient')
        filterset = PatientFilter(request.query_params, queryset=queryset)

        # if filterset.is_valid():
        queryset = filterset.qs
        
        serializer = PatientSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request: Request):

        serializer = PatientSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        user = request.user
        serializer = SubProfileSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)