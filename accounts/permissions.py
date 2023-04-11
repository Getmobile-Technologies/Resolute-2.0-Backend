from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed



class IsAdmin(permissions.BasePermission):
   
    def has_permission(self, request, view):
        if request.user.is_admin:
            return True
        else:
            raise AuthenticationFailed(detail="Authentication credentials were not provided oh ")
        

class IsSuperUser(permissions.BasePermission):
   
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            raise AuthenticationFailed(detail="Authentication credentials were not provided oh ")