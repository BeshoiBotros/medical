from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'role') and request.user.role == 'doctor')


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'role') and request.user.role == 'patient')
    
def _get_queryset(klass):

    # If it is a model class or anything else with ._default_manager
    if hasattr(klass, "_default_manager"):
        return klass._default_manager.all()
    return klass

def get_object_or_404(klass, error="404 Not Founded",*args, **kwargs):

    queryset = _get_queryset(klass)
    if not hasattr(queryset, "get"):
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise Http404(
            error
        )