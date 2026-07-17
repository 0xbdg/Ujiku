from rest_framework import viewsets
from rest_framework.views import APIView
from app.models import *
from .serializer import *

# Create your views here.

class AccountViewAPI(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class StudentViewAPI(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class ExamViewAPI(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class QuestionViewAPI(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class MultipleChoiceViewAPI(viewsets.ModelViewSet):
    queryset = MultipleChoice.objects.all()
    serializer_class = MultipleChoiceSerializer

class EssayViewAPI(viewsets.ModelViewSet):
    queryset = Essay.objects.all()
    serializer_class = EssaySerializer

class ResultViewAPI(APIView):
    def post(self, request):
        pass
