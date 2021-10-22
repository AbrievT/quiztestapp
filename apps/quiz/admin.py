from django.contrib import admin
from .models import *

admin.site.register(Session)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(AnswerWithChoice)
admin.site.register(UserAnswersWithText)
admin.site.register(UserAnswersWithChoices)