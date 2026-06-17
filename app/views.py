from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.views import View
from django.views.generic import FormView, ListView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from datetime import datetime
from .forms import *
from .models import *
from .mixin import *


# Create your views here.


class SigninView(LoginView):
    template_name = "auth/login.html"
    authentication_form = LoginForm

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser:
            return reverse_lazy("home")
        if user.is_teacher and user.is_staff:
            return reverse_lazy("home")
        if user.is_student:
            return reverse_lazy("home")


class HomeView(ListView):
    model = Exam
    template_name = "client/pages/home.html"
    paginate_by = 6

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        context["exam_count"] = Exam.objects.count(),
        context["exam_active"] = Exam.objects.filter(
            start_time__lte=timezone.localtime().time(),
            end_time__gte=timezone.localtime().time()
        )
        context["exam_ended"] = Exam.objects.filter(
            end_time__lte=timezone.localtime().time()
        )
        context["exam_inactive"] = Exam.objects.filter(
            start_time__gte=timezone.localtime().time()
        )
        return context


class StartExamView(View):
    def get(self, request, pk):
        question = Question.objects.get(id=pk)
        efinish = False
        types = None 
        c = None
        time_e = Exam.objects.get(id=pk).end_time
        time_s = datetime.now()

        if ExamFinish.objects.filter(student=request.user, exam=pk):
            efinish = ExamFinish.objects.get(student=request.user, exam=pk).finished

        if question.question_type == "multiple":
            types = MultipleChoice.objects.filter(question_id=question.id)
            c = MultipleChoice.objects.count()
        elif question.question_type == "essay":
            types = Essay.objects.filter(question_id=question.id)
            c = Essay.objects.count()

        return render(
            request,
            "client/pages/start_exam.html",
            {
                "question": question,
                "choices": types,
                "count": c,
                "time_start": ((time_s.hour * 3600) + (time_s.minute * 60) + time_s.second),
                "time_end":((time_e.hour * 3600) + (time_e.minute * 60) +time_e.second),
                "is_ended": efinish
            },
        )

    def post(self, request, pk):

        data = request.POST.items()
        test = []

        for var, val in data:
            if var.startswith("jawaban_"):

                test.append(val)

                Result(
                    student_id=request.user,
                    question_id=Question.objects.get(id=pk),
                    answer=val,
                ).save()

        ExamFinish(student=request.user, exam=get_object_or_404(Exam, id=pk), finished=True).save()

        return redirect("home")


class DashboardView(TemplateView):
    template_name = "superuser/pages/dashboard.html"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student_c"] = Student.objects.count()
        context["teacher_c"] = Teacher.objects.count()
        context["exam_c"] = Exam.objects.count()
        context["question_c"] = Question.objects.count()
        return context

class TeacherView(ListView):
    model = Teacher
    template_name = "superuser/pages/account/teacher.html"
    context_object_name = "teachers"
    paginate_by = 10

class TeacherCreateView(View):
    def get(self, request):
        form1 = AccountForm()
        form2 = TeacherForm()
        return render(request,"superuser/pages/account/teacher_add.html", context={"form1":form1, "form2":form2})

    def post(self, request):
        form1 = AccountForm(data=request.POST)
        form2 = TeacherForm(data=request.POST)

        if form1.is_valid() and form2.is_valid():
            firstname = form1.cleaned_data["firstname"]
            lastname = form1.cleaned_data["lastname"]
            username = form1.cleaned_data["username"]
            email = form1.cleaned_data["email"]
            password1 = form1.cleaned_data["password1"]
            password2 = form1.cleaned_data["password2"]

            Account(first_name=firstname, last_name=lastname, email=email, username=username, is_staff=True, is_teacher=True, is_student=False, is_superuser=False, password=(password2 if password1 == password2 else password2)).save()
            form2.save()

            return redirect("admin-teacher-acc")
    
class StudentView(ListView):
    model = Student
    context_object_name="students"
    template_name="superuser/pages/account/student.html" 
    paginate_by = 10

class AdminView(ListView):
    model = Account
    context_object_name="superusers"
    template_name="superuser/pages/account/superuser.html"
    paginate_by=10
