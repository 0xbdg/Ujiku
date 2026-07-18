from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path("accounts/login/", SigninView.as_view(), name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("soal-ujian/<int:pk>/", StartExamView.as_view(), name="start-exam"),
    path("test/dashboard/", DashboardView.as_view(), name="admin-dashboard"),
    path("test/account/teacher/", TeacherView.as_view(), name="admin-teacher-acc"),
    path("test/account/teacher/add/", TeacherCreateView.as_view(), name="admin-teacher-add-acc"),
    path("test/account/teacher/update/<str:pk>/", TeacherUpdateView.as_view(), name="admin-teacher-update-acc"),
    path("test/account/teacher/delete/<str:pk>/", TeacherDeleteView.as_view(), name="admin-teacher-delete-acc"),
    path("test/account/student/", StudentView.as_view(), name="admin-student-acc"),
    path("test/account/student/add/", StudentCreateView.as_view(), name="admin-student-add-acc"),
    path("test/account/student/update/<str:pk>/", StudentUpdateView.as_view(), name="admin-student-update-acc"),
    path("test/account/student/delete/<str:pk>/", StudentDeleteView.as_view(), name="admin-student-delete-acc"),
    path("test/account/superuser/", AdminView.as_view(), name="admin-su-acc"),
    path("test/account/superuser/add/", AdminCreateView.as_view(), name="admin-su-add-acc"),
    path("test/account/superuser/update/<str:pk>/", AdminUpdateView.as_view(), name="admin-su-update-acc"),
    path("test/pembelajaran/exam/", ExamView.as_view(), name="admin-exam-pem"),
    path("test/pembelajaran/exam/add/", ExamAddView.as_view(), name="admin-exam-add-pem"),
    path("test/pembelajaran/exam/update/<int:pk>/", ExamUpdateView.as_view(), name="admin-exam-update-pem"),
    path("test/pembelajaran/mapel/", MapelView.as_view(), name="admin-mapel-pem"),
    path("test/pembelajaran/mapel/delete/<int:pk>", MapelDeleteView.as_view(), name="admin-mapel-delete-pem"),
    path("test/pembelajaran/bank/", BankSoalView.as_view(), name="admin-bank-pem"),
    path("test/pembelajaran/bank/delete/<int:pk>/", BankSoalDeleteView.as_view(), name="admin-bank-delete-pem"),
    path("test/pembelajaran/bank/question/<int:pk>/", QuestionView.as_view(), name="admin-bank-question-pem"),
    path("test/pembelajaran/bank/question/update/<int:pk>/<int:q>/", QuestionUpdateView.as_view(), name="admin-bank-question-update-pem"),
    path("test/pembelajaran/bank/question/delete/<int:pk>/<int:q>/", QuestionDeleteView.as_view(), name="admin-bank-question-delete-pem"),
    path("test/pembelajaran/hasil/", ExamResultView.as_view(), name="admin-exam-result-pem"),
    path("", HomeView.as_view(), name="home"),
]
