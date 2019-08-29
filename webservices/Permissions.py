from rest_framework import permissions


class FotopartnerPermission(permissions.BasePermission):
    """
    Permisos de fotopartner
    """

    def has_permission(self, request, view):
        if request.user is not None:
            return request.user.rol.pk in [3,4]
        return False

class WebHookPermission(permissions.BasePermission):
    """
    Permission for Conekta IPs.
    """

    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        conekta_ips = ['52.200.151.182']
        if ip_addr in conekta_ips:
            return True
        return False