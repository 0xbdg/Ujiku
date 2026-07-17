from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r"accounts", AccountViewAPI, basename="account-api")
router.register(r"students", StudentViewAPI, basename="student-api")
router.register(r"exams", ExamViewAPI, basename="exam-api")
router.register(r"questions", QuestionViewAPI, basename="question-api")
router.register(r"multiplechoices", MultipleChoiceViewAPI, basename="multiplechoice-api")
router.register(r"essays", EssayViewAPI, basename="essay-api")

urlpatterns = router.urls
