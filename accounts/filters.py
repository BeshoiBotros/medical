import django_filters
from .models import CustomUser

class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class DoctorFilter(django_filters.FilterSet):
    medical_spesification = CharInFilter(field_name='medical_spesification', lookup_expr='in')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    is_available = django_filters.BooleanFilter(field_name='is_available', lookup_expr='exact')
    phone_number = django_filters.CharFilter(field_name='phone_number', lookup_expr='icontains')
    address = django_filters.CharFilter(field_name='address', lookup_expr='icontains')

    class Meta:
        model = CustomUser
        fields = ['medical_spesification', 'first_name',
                  'email', 'is_available', 'phone_number',
                  'address'
                 ]

class PatientFilter(django_filters.FilterSet):
    first_name = CharInFilter(field_name='first_name', lookup_expr='in')
    email = CharInFilter(field_name='email', lookup_expr='in')
    phone_number = CharInFilter(field_name='phone_number', lookup_expr='in')

    class Meta:
        model = CustomUser
        fields = ['first_name',
                  'email', 'phone_number',
                 ]