from rest_framework import permissions


class EditPermission(permissions.BasePermission):
    '''
    Checks access rights for request available to
    author of objects.
    '''

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.author
                or request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj)
