from rest_framework import permissions


class IsTaskOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of a task object to edit it.
    Assumes the model instance has an `user` attribute.
    """

    def has_object_permission(self, request, view, task_obj):
        # Read permissions are allowed only to user,
        if request.method in permissions.SAFE_METHODS:
            return True

        return task_obj.user == request.user
