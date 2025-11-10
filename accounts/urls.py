from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import RegisterView, DoctorView, PatientView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', RegisterView.as_view()),

    path('doctors/', DoctorView.as_view()),
    path('doctors/<int:id>/', DoctorView.as_view()),

    path('patients/', PatientView.as_view()),
    path('patients/<int:id>', PatientView.as_view()),
]

