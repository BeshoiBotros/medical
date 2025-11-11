from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from medical.utils import IsDoctor, IsPatient, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializers import DoctorAppointmentSerializer, PatientAppointmentSerializer, ScheduleSerializer
from rest_framework.request import Request
from . import models as appointments_models
from datetime import datetime, timedelta, date

class ScheduleView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        else:
            return [IsDoctor()]
        
    def get(self, request: Request, schedule_pk=None, doctor_pk=None):

        self_param = request.query_params.get('self', False)
        queryset = appointments_models.Schedule.objects.filter(doctor=request.user.pk)

        if self_param:
            serializer = ScheduleSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
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



class AvailableSlotsView(APIView):

    def get(self, request: Request):
        schedule_pk = request.query_params.get('schedule_pk')
        doctor_pk = request.query_params.get('doctor_pk')
        day = request.query_params.get('day')

        if schedule_pk:
            schedule = get_object_or_404(appointments_models.Schedule, pk=schedule_pk)
        elif doctor_pk and day:
            schedule = get_object_or_404(appointments_models.Schedule, doctor=doctor_pk, day=day)
        else:
            return Response({'detail': 'Provide schedule_pk or doctor_pk and day'}, status=status.HTTP_400_BAD_REQUEST)

        if not schedule.is_available:
            return Response({'detail': 'Schedule not available'}, status=status.HTTP_400_BAD_REQUEST)

        start = schedule.start_time
        end = schedule.end_time
        duration_delta = timedelta(minutes=schedule.min_session_duration)
        current_time = start
        available = []

        while (datetime.combine(date.today(), current_time) + duration_delta).time() <= end:
            if not appointments_models.Appointment.objects.filter(
                doctor=schedule.doctor,
                schedule=schedule,
                start_time=current_time,
                status__in=['W', 'A'],
                cancle=False
            ).exists():
                available.append(str(current_time))

            current = datetime.combine(date.today(), current_time) + duration_delta
            current_time = current.time()

        return Response({'available_slots': available}, status=status.HTTP_200_OK)

class AppointmentView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsPatient()]
        elif self.request.method == 'PATCH':
            return [IsAuthenticated()]
        return []

    def get(self, request: Request, appointment_pk=None):

        self_param = request.query_params.get('self', False)
        
        if self_param:
            if request.user.role == 'patient':
                queryset = appointments_models.Appointment.objects.filter(patient=request.user)
                serializer = PatientAppointmentSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif request.user.role == 'doctor':
                queryset = appointments_models.Appointment.objects.filter(doctor=request.user)
                serializer = DoctorAppointmentSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
        
        if appointment_pk:
            instance = get_object_or_404(appointments_models.Appointment, pk=appointment_pk)
            if request.user != instance.patient and request.user != instance.doctor:
                return Response({'detail': 'Not authorized to view this appointment'}, status=status.HTTP_403_FORBIDDEN)
            if request.user.role == 'patient':
                serializer = PatientAppointmentSerializer(instance)
            else:
                serializer = DoctorAppointmentSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Provide self parameter or appointment_pk'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request: Request):
        
        serializer = PatientAppointmentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request, appointment_pk):
        appointment: appointments_models.Appointment = get_object_or_404(appointments_models.Appointment, pk=appointment_pk)
        
        if request.user == appointment.patient and request.user.role == 'patient':
            if 'cancle' not in request.data:
                return Response({'detail': 'Patients can only update the cancle field'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = PatientAppointmentSerializer(instance=appointment, data=request.data, partial=True)
        elif request.user == appointment.doctor and request.user.role == 'doctor':
            if 'status' not in request.data:
                return Response({'detail': 'Doctors can only update the status field'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = DoctorAppointmentSerializer(instance=appointment, data=request.data, partial=True)
        else:
            return Response({'detail': 'Not authorized to update this appointment'}, status=status.HTTP_403_FORBIDDEN)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)