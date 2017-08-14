from rest_framework import permissions
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


class CustomPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        assert False
        print("user is {user}".format(user=request.user))
        return request.user.groups.filter(name = 'reader').exists()

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user

class CustomPermissions2(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        print("in my customom2 permissions class")
        return False
        return request.user.groups.filter(name = 'reader').exists()

    def has_object_permission(self, request, view, obj):
        print("in my customom2 permissions class")
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        return False
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return False
        return obj.owner == request.user

class CustomPermissions3(TokenHasReadWriteScope):
    pass
