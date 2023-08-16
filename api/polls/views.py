from rest_framework import status, viewsets
from rest_framework.response import Response

from core.polls.models import Question

from . import serializers


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.QuestionSerializer
    queryset = Question.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateQuestionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
