from django.urls import path
from . import views

urlpatterns = [
    path('schedule/', views.ScheduleView.as_view()),
    path('schedule/<int:schedule_pk>/', views.ScheduleView.as_view()),
    path('schedule/doctor/<int:doctor_pk>/', views.ScheduleView.as_view()),

    path('available/', views.AvailableSlotsView.as_view()),
    
    path('', views.AppointmentView.as_view()),
    path('<int:appointment_pk>/', views.AppointmentView.as_view()),
]
