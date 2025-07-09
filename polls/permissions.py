from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    # Permette solo al proprietario dell'oggetto di modificarlo/eliminarlo.
    # Gli altri utenti possono solo leggerlo.

    def has_object_permission(self, request, view, obj):
        # Read: permesso a tutti
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write: solo il proprietario può modificare/cancellare
        return IsOwner().has_object_permission(request, obj)
    
class IsOwner(permissions.BasePermission):

    # Permette solo al proprietario dell'oggetto di accedervi.

    def has_object_permission(self, request, obj):
        return obj.created_by == request.user

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    
    #Permette solo agli utenti autenticati di votare.

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated