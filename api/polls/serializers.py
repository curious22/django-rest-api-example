from rest_framework.serializers import ModelSerializer, ValidationError

from core.polls.models import Choice, Question


class CreateQuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = ("question_text",)

    def validate_question_text(self, value):
        if Question.objects.filter(question_text=value).exists():
            raise ValidationError("This field must be unique")

        return value


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "question_text", "pub_date")


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = ("id", "question", "choice_text", "votes")
