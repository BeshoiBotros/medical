from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from medical.utils import IsDoctor, IsPatient, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializers import DoctorAppointmentSerializer, PatientAppointmentSerializer, ScheduleSerializer
from rest_framework.request import Request
from . import models as appointments_models

class ScheduleView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        else:
            return [IsDoctor()]
        
    def get(self, request: Request, schedule_pk=None, doctor_pk=None):
        
        if schedule_pk:
            instance = get_object_or_404(appointments_models.Schedule, pk=schedule_pk)
            serializer = ScheduleSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif doctor_pk:
            queryset = appointments_models.Schedule.objects.filter(doctor=doctor_pk, doctor__role='doctor')
            serializer = ScheduleSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            queryset = appointments_models.Schedule.objects.all()
            serializer =  ScheduleSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        


    def post(self, request: Request):
        
        serializer = ScheduleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request, schedule_pk):
        schedule: appointments_models.Schedule = get_object_or_404(appointments_models.Schedule, pk=schedule_pk)
        if schedule.doctor != request.user:
            return Response({'detail' : 'Not Found 404 Or You Try To Update Another Doctor Schedule!'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ScheduleSerializer(instance=schedule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


