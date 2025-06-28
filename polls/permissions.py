from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    - Permette solo al proprietario dell'oggetto di modificarlo/eliminarlo.
    - Gli altri utenti possono solo leggerlo.
    """

    def has_object_permission(self, request, view, obj):
        # Read: permesso a tutti
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write: solo il proprietario può modificare/cancellare
        return obj.created_by == request.user
