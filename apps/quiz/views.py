from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.quiz import models as quiz_models
from apps.quiz import serializers as quiz_serializers
from apps.quiz.permissions import QuizAndQuestionPermission


class QuizViewset(ModelViewSet):
    queryset = quiz_models.Quiz.objects.all()
    serializer_class = quiz_serializers.QuizSerializer
    permission_classes = [QuizAndQuestionPermission]

    def get_serializer_context(self):
        return {"request": self.request}


class QuestionsViewset(ModelViewSet):
    queryset = quiz_models.Question.objects.all()
    serializer_class = quiz_serializers.QuestionSerializer
    permission_classes = [QuizAndQuestionPermission]

    def get_serializer_context(self):
        return {"request": self.request}


class AnswerWithChoiceView(ModelViewSet):
    queryset = quiz_models.AnswerWithChoice.objects.all()
    serializer_class = quiz_serializers.AnswerWithChoiceSerializer
    permission_classes = [QuizAndQuestionPermission]


class AnswerWithTextView(ListCreateAPIView):
    queryset = quiz_models.UserAnswersWithText.objects.all()
    serializer_class = quiz_serializers.UserAnswersWithTextSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        anonymous_user_id = self.request.session.session_key
        if user:
            queryset = queryset.filter(user_id=user.id)
            return queryset
        if anonymous_user_id:
            queryset = queryset.filter(anonymous_user__session_key=anonymous_user_id)
            return queryset
        return []


class UserAnswerWithChoiceView(ListCreateAPIView):
    queryset = quiz_models.UserAnswersWithChoices.objects.all()
    serializer_class = quiz_serializers.UserAnswerChoiceSerializer



    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        anonymous_user_id = self.request.session.session_key
        if str(user) != "AnonymousUser":
            queryset = queryset.filter(user_id=user.id)
            return queryset
        if anonymous_user_id:
            queryset = queryset.filter(anonymous_user__session_key=anonymous_user_id)
            return queryset
        return []


class UserTextAnsversResultView(ListAPIView):
    queryset = quiz_models.UserAnswersWithText.objects.all()
    serializer_class = quiz_serializers.UserTextAnsversResultSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        anonymous_user_id = self.request.session.session_key
        context = {"user": user, "anonymous_user_id": anonymous_user_id}
        serializer = self.serializer_class(instance=self.queryset, context=context)
        return Response(serializer.data)


class UserChoiseAnsversResultView(ListAPIView):
    queryset = quiz_models.UserAnswersWithChoices.objects.all()
    serializer_class = quiz_serializers.UserChoiseAnsversResultSerializer

    def get(self, request, *args, **kwargs):

        user = self.request.user
        anonymous_user_id = self.request.session.session_key
        context = {"user": user, "anonymous_user_id": anonymous_user_id,}
        serializer = self.serializer_class(instance=self.queryset, context=context)
        return Response(serializer.data)
