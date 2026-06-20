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
    path("test/account/student/", StudentView.as_view(), name="admin-student-acc"),
    path("test/account/student/add/", StudentCreateView.as_view(), name="admin-student-add-acc"),
    path("test/account/superuser/", AdminView.as_view(), name="admin-su-acc"),
    path("", HomeView.as_view(), name="home"),
]
