from rest_framework.permissions import BasePermission


class QuizAndQuestionPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        if request.method != 'GET' and str(request.user) != "AnonymousUser":
            return True

