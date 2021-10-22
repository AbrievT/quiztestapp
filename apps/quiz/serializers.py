from rest_framework import serializers

from apps.quiz import models as quiz_models


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = quiz_models.Quiz
        fields = "__all__"

    def update(self, instance, validated_data):
        if instance.start_date:
            raise serializers.ValidationError({"error": "this quiz cannot be changed"})
        instance.title = validated_data.get('title', None)
        instance.description = validated_data.get('description', None)
        instance.save()
        return instance

    def create(self, validated_data):
        start_date = validated_data.get('start_date', None)
        end_date = validated_data.get('end_date', None)
        if start_date is None and end_date:
            raise serializers.ValidationError({"error": "You cannot give an end time without giving a start time"})
        quiz = self.Meta.model.objects.create(**validated_data)
        return quiz


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = quiz_models.Question
        fields = "__all__"

    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_superuser:
            quiz = quiz_models.Quiz.objects.get(id=validated_data.get('quiz'))
            if quiz.quiz_status != quiz_models.Quiz.NOT_ACTIV:
                question = self.Meta.model.objects.create(**validated_data)
                return question
            raise serializers.ValidationError({"error": "You cannot create a question for an inactive quiz"})
        raise serializers.ValidationError({"error": "question can only be created by admin"})


class AnswerWithChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = quiz_models.AnswerWithChoice
        fields = "__all__"

    def create(self, validated_data):
        questionn = validated_data.get('question', None)
        if questionn.question_type == quiz_models.Question.TEXT:
            raise serializers.ValidationError({"error": "You cannot create text-type answers to a selectable question"})
        answer = self.Meta.model.objects.create(**validated_data)
        return answer


class UserAnswersWithTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = quiz_models.UserAnswersWithText
        fields = "__all__"
        read_only_fields = ('answer_status', 'user', 'anonymous_user',)

    def create(self, validated_data):
        questionn = validated_data.get('question', None)
        user = self.context['request'].user
        session_ = self.context['request']

        if questionn.question_type != quiz_models.Question.TEXT:
            raise serializers.ValidationError({"error": "This question cannot be answered with text"})
        if str(user) != "AnonymousUser":
            validated_data['user'] = user
        else:
            if not session_.session.session_key:
                anonymous_user_id = session_.session.create()
            anonymous_user_id = session_.session.session_key
            validated_data['anonymous_user_id'] = anonymous_user_id
        answer = self.Meta.model.objects.create(**validated_data)
        return answer

    def to_representation(self, instance):
        data = super(UserAnswersWithTextSerializer, self).to_representation(instance)
        data['question'] = QuestionSerializer(instance=instance.question, read_only=True).data
        return data



class UserAnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = quiz_models.UserAnswersWithChoices
        fields = "__all__"
        read_only_fields = ('answer_status', 'user', 'anonymous_user',)

    def create(self, validated_data):
        data = validated_data['answer']
        user = self.context['request'].user
        session_ = self.context['request']

        if str(user) != "AnonymousUser":
            validated_data['user'] = user
        else:
            if not session_.session.session_key:
                anonymous_user_id = session_.session.create()
            anonymous_user_id = session_.session.session_key
            validated_data['anonymous_user_id'] = anonymous_user_id

        validated_data.pop('answer', None)
        queryset = self.Meta.model.objects.create(**validated_data)

        for answer in data:
            queryset.answer.add(answer.id)


        answers = quiz_models.AnswerWithChoice.objects.filter(question_id=validated_data['question'],
                                                            answer_status=True).values_list('answer_status', flat=True)
        user_ansvers = queryset.answer.all().values_list('answer_status', flat=True)

        if list(user_ansvers) == list(answers):
            queryset.answer_status = True
            queryset.save()

        return queryset

    def to_representation(self, instance):
        data = super(UserAnswerChoiceSerializer, self).to_representation(instance)
        data['answer'] = AnswerWithChoiceSerializer(instance=instance.answer, many=True).data
        return data


class UserTextAnsversResultSerializer(serializers.Serializer):
    def to_representation(self, instance):
        data = {}
        user = self.context['user']
        anonymous_user = self.context['anonymous_user_id']
        queryset = quiz_models.UserAnswersWithText.objects

        if str(user) != "AnonymousUser":
            queryset = queryset.filter(user=user)
        if anonymous_user:
            queryset = queryset.filter(anonymous_user__session_key=anonymous_user)

        data['correct_answer'] = queryset.filter(answer_status=quiz_models.UserAnswersWithText.TRUE).count()
        data['wrong_answer'] = queryset.filter(answer_status=quiz_models.UserAnswersWithText.FALSE).count()
        data['unverified_answers'] = queryset.filter(answer_status=quiz_models.UserAnswersWithText.NOT_CHECKED).count()
        return data


class UserChoiseAnsversResultSerializer(serializers.Serializer):

    def to_representation(self, instance):
        data = {}
        user = self.context['user']
        anonymous_user = self.context['anonymous_user_id']
        queryset = quiz_models.UserAnswersWithChoices.objects

        if str(user) != "AnonymousUser":
            queryset = queryset.filter(user=user)
        if anonymous_user:
            queryset = queryset.filter(anonymous_user__session_key=anonymous_user)

        data['correct_answer'] = queryset.filter(answer_status=True).count()
        data['wrong_answer'] = queryset.filter(answer_status=False).count()
        return data