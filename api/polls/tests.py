import pytest
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from core.polls import models

client = APIClient()


@pytest.mark.django_db
@pytest.fixture
def questions_fixture():
    questions = []
    for i in range(2):
        questions.append(models.Question.objects.create(question_text=f"Question #{i}"))
    return questions


@pytest.mark.django_db
class TestQuestionAPI:
    pytestmark = pytest.mark.django_db
    QUESTION_LIST_URL = reverse("question-list")
    DETAIL_QUESTION_URL = reverse("question-detail", args=[1])

    def test_list_questions(self, questions_fixture):
        resp = client.get(self.QUESTION_LIST_URL)

        assert resp.status_code == status.HTTP_200_OK
        data = resp.data
        first_question = data[0]
        assert len(data) == models.Question.objects.count()
        assert first_question["id"] == 1
        assert first_question["question_text"] == "Question #0"

    def test_detail_question(self, questions_fixture):
        resp = client.get(self.DETAIL_QUESTION_URL)

        assert resp.status_code == status.HTTP_200_OK
        question = models.Question.objects.get(pk=resp.data["id"])
        assert resp.data["id"] == question.pk
        assert resp.data["question_text"] == question.question_text
        assert "pub_date" in resp.data
        assert resp.data["pub_date"] is not None

    def test_create_question_ok(self, questions_fixture):
        question_text = "Some title"
        resp = client.post(self.QUESTION_LIST_URL, data={"question_text": question_text})

        assert resp.status_code == status.HTTP_201_CREATED
        assert models.Question.objects.filter(question_text=question_text).exists() is True

    def test_create_question_text_duplication_fail(self, questions_fixture):
        old_count = models.Question.objects.count()
        resp = client.post(self.QUESTION_LIST_URL, data={"question_text": "Question #1"})

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "question_text" in resp.data
        assert resp.data["question_text"][0] == ErrorDetail("This field must be unique", code="invalid")
        assert models.Question.objects.count() == old_count  # new instance has not created

    def test_create_empty_data(self, questions_fixture):
        resp = client.post(self.QUESTION_LIST_URL, data={})

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "question_text" in resp.data
        assert resp.data["question_text"][0] == ErrorDetail("This field is required.", code="required")
