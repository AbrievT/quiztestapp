from rest_framework import routers
from django.urls import path

from .views import QuizViewset, QuestionsViewset, \
                   AnswerWithChoiceView, AnswerWithTextView,\
                   UserAnswerWithChoiceView, UserTextAnsversResultView, UserChoiseAnsversResultView

router = routers.SimpleRouter()
router.register('quiz', QuizViewset)
router.register('question', QuestionsViewset)
router.register('choice/answer', AnswerWithChoiceView)

urlpatterns = router.urls + [
    path('answer_the/question_with_text', AnswerWithTextView.as_view()),
    path('answer_the/question_with_choice', UserAnswerWithChoiceView.as_view()),
    path('user_text_answer/result', UserTextAnsversResultView.as_view()),
    path('user_choise_answer/result', UserChoiseAnsversResultView.as_view())
]