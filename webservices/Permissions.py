from rest_framework import permissions


class FotopartnerPermission(permissions.BasePermission):
    """
    Permisos de fotopartner
    """

    def has_permission(self, request, view):
        if request.user is not None:
            return request.user.rol.pk in [3,4]
        return False