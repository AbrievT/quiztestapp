from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models


class Quiz(models.Model):
    ACTIV = "activ"
    NOT_ACTIV = "not_activ"

    QUIZ_STATUS = (
        (ACTIV, "activ"),
        (NOT_ACTIV, "not_activ")
    )

    title = models.CharField(max_length=255)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField()
    quiz_status = models.CharField(max_length=255, choices=QUIZ_STATUS, default=ACTIV)


class Question(models.Model):
    TEXT = "text"
    CHOICE = "choice"
    MULTIPLECHOICE = "multiple_choices"

    QUIZ_TYPE = (
        (TEXT, 'text'),
        (CHOICE, 'choice'),
        (MULTIPLECHOICE, 'multiple_choices')
    )

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()
    question_type = models.CharField(max_length=30, choices=QUIZ_TYPE)


class AnswerWithChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='ansver_in_question')
    answer = models.TextField(max_length=255)
    answer_status = models.BooleanField(default=False)


class UserAnswersWithText(models.Model):
    TRUE = "true"
    FALSE = "false"
    NOT_CHECKED = "not_checked"

    ANSWER_STATUS = (
        (TRUE, "true"),
        (FALSE, "false"),
        (NOT_CHECKED, "not_checked")
    )

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    answer_status = models.CharField(max_length=30, choices=ANSWER_STATUS, default=NOT_CHECKED)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    anonymous_user = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)


class UserAnswersWithChoices(models.Model):
    TRUE = "true"
    FALSE = "false"

    ANSWER_STATUS = (
        (TRUE, "true"),
        (FALSE, "false"),
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ManyToManyField(AnswerWithChoice, related_name='answer_choice')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    anonymous_user = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    answer_status = models.BooleanField(default=False)
