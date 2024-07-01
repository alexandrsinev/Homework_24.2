from rest_framework import permissions


class IsModer(permissions.BasePermission):
    message = 'Вы не являетесь модератором.'

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.course_owner or obj.lesson_owner == request.user:
            return True
        return False
