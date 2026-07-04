from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.views import View
from django.views.generic import *
from django.views.generic.edit import *
from django.urls import reverse_lazy
from django.shortcuts import render,get_object_or_404,redirect, HttpResponse
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
        form2 = TeacherForm(request.POST, request.FILES)

        if form1.is_valid() and form2.is_valid():
            firstname = form1.cleaned_data["firstname"]
            lastname = form1.cleaned_data["lastname"]
            username = form1.cleaned_data["username"]
            email = form1.cleaned_data["email"]
            password1 = form1.cleaned_data["password1"]
            password2 = form1.cleaned_data["password2"]

            photo = form2.cleaned_data["photo"]
            gender = form2.cleaned_data["gender"]
            subject = form2.cleaned_data["subject_id"]

            acc = Account.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, is_staff=True, is_teacher=True, is_student=False, is_superuser=False, password=(password2 if password1 == password2 else password2))
            Teacher.objects.create(user_id=acc, photo=photo, gender=gender,subject_id=subject)

            return redirect("admin-teacher-acc")
        return HttpResponse("Error")

class TeacherUpdateView(View):
    def get(self,request, pk):
        acc=get_object_or_404(Account,username=pk)
        teacher = get_object_or_404(Teacher, user_id=acc)
        form1 = AccountForm(initial={
            "firstname":acc.first_name,
            "lastname": acc.last_name,
            "username":acc.username,
            "email":acc.email
        })
        form2 = TeacherForm(initial={
            "photo": teacher.photo,
            "gender": teacher.gender,
            "subject_id":teacher.subject_id
        })

        return render(request, "superuser/pages/account/teacher_update.html", context={"form1":form1, "form2":form2, "acc":acc})

    def post(self, request, pk):
        acc = get_object_or_404(Account, username=pk)
        teacher = get_object_or_404(Teacher, user_id=acc)

        form1 = AccountForm(data=request.POST)
        form2 = TeacherForm(request.POST, request.FILES)

        if form1.is_valid() and form2.is_valid():
            password1 = form1.cleaned_data["password1"]
            password2 = form1.cleaned_data["password2"]
            photo = form2.cleaned_data["photo"]
            acc.first_name = form1.cleaned_data["firstname"]
            acc.last_name = form1.cleaned_data["lastname"]
            acc.username = form1.cleaned_data["username"]
            acc.email = form1.cleaned_data["email"]

            acc.set_password(password1 if password1 == password2 else password2)

            acc.save()

            if photo:
                teacher.photo = photo
            teacher.gender = form2.cleaned_data["gender"]
            teacher.subject_id= form2.cleaned_data["subject_id"]

            teacher.save()

            return redirect("admin-teacher-update-acc", pk)

class TeacherDeleteView(View):
    def post(self,request, pk):
        acc = get_object_or_404(Account, username=pk)
        teacher = get_object_or_404(Teacher, user_id=acc)

        acc.delete()
        teacher.delete()

        return redirect("admin-teacher-acc")

class StudentView(ListView):
    model = Student
    context_object_name="students"
    template_name="superuser/pages/account/student.html" 
    paginate_by = 10

class StudentCreateView(View):
    def get(self, request):
        form1 = AccountForm()
        form2 = StudentForm()

        return render(request, "superuser/pages/account/student_add.html", context={"form1":form1, "form2":form2})

    def post(self,request):
        form1 = AccountForm(data=request.POST)
        form2 = StudentForm(request.POST, request.FILES)

        if form1.is_valid() and form2.is_valid():
            firstname = form1.cleaned_data["firstname"]
            lastname = form1.cleaned_data["lastname"]
            username = form1.cleaned_data["username"]
            email = form1.cleaned_data["email"]
            password1 = form1.cleaned_data["password1"]
            password2 = form1.cleaned_data["password2"]

            photo = form2.cleaned_data["photo"]
            gender = form2.cleaned_data["gender"]
            grade = form2.cleaned_data["grade"]

            acc = Account.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, is_staff=False, is_teacher=False, is_student=True, is_superuser=False, password=(password2 if password1 == password2 else password2))
            Student.objects.create(user_id=acc, photo=photo, gender=gender,grade=grade)

            return redirect("admin-student-acc")
        return HttpResponse("Error")

class StudentUpdateView(View):
    def get(self,request, pk):
        acc=get_object_or_404(Account,username=pk)
        student = get_object_or_404(Student, user_id=acc)
        form1 = AccountForm(initial={
            "firstname":acc.first_name,
            "lastname": acc.last_name,
            "username":acc.username,
            "email":acc.email
        })
        form2 = StudentForm(initial={
            "photo": student.photo,
            "gender": student.gender,
            "grade":student.grade
        })

        return render(request, "superuser/pages/account/student_update.html", context={"form1":form1, "form2":form2, "acc":acc})

    def post(self, request, pk):
        acc = get_object_or_404(Account, username=pk)
        student = get_object_or_404(Student, user_id=acc)

        form1 = AccountForm(data=request.POST)
        form2 = StudentForm(request.POST, request.FILES)

        if form1.is_valid() and form2.is_valid():
            password1 = form1.cleaned_data["password1"]
            password2 = form1.cleaned_data["password2"]
            photo = form2.cleaned_data["photo"]
            acc.first_name = form1.cleaned_data["firstname"]
            acc.last_name = form1.cleaned_data["lastname"]
            acc.username = form1.cleaned_data["username"]
            acc.email = form1.cleaned_data["email"]

            acc.set_password(password1 if password1 == password2 else password2)

            acc.save()

            if photo:
                student.photo = photo
            student.gender = form2.cleaned_data["gender"]
            student.grade = form2.cleaned_data["grade"]

            student.save()

            return redirect("admin-student-update-acc", pk)

class StudentDeleteView(View):
    def post(self,request, pk):
        acc = get_object_or_404(Account, username=pk)
        student = get_object_or_404(Student, user_id=acc)

        acc.delete()
        student.delete()

        return redirect("admin-student-acc")


class AdminView(ListView):
    model = Account
    context_object_name="superusers"
    template_name="superuser/pages/account/superuser.html"
    paginate_by=10

class AdminCreateView(View):
    def get(self, request):
        form = AccountForm()
        return render(request, "superuser/pages/account/superuser_add.html", context={"form":form})
    
    def post(self,request):
        form = AccountForm(data=request.POST)

        if form.is_valid():
            firstname = form.cleaned_data["firstname"]
            lastname = form.cleaned_data["lastname"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]

            Account.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, is_staff=True, is_teacher=False, is_student=False, is_superuser=True, password=(password2 if password1 == password2 else password2))

            return redirect("admin-su-acc")
        HttpResponse("Error")

class AdminUpdateView(View):
    def get(self, request, pk):
        acc = get_object_or_404(Account, username=pk)
        form = AccountForm(initial={
            "firstname": acc.first_name,
            "lastname": acc.last_name,
            "username": acc.username,
            "email": acc.email,
        })
        return render(request, "superuser/pages/account/superuser_update.html", context={"form":form, "acc":acc.username})
    
    def post(self,request, pk):
        acc = get_object_or_404(Account, username=pk)

        form = AccountForm(data=request.POST)

        if form.is_valid():
            firstname = form.cleaned_data["firstname"]
            lastname = form.cleaned_data["lastname"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]

            acc.first_name = firstname
            acc.last_name = lastname
            acc.email = email
            acc.username=username
            acc.set_password(password1 if password1 == password2 else password2)
            acc.save()
            return redirect("admin-su-update-acc", acc.username)
        HttpResponse("Error")

class ExamView(ListView):
    model = Exam
    template_name = "superuser/pages/pembelajaran/exam.html"
    context_object_name = "exams"
    paginate_by = 10

class ExamAddView(CreateView):
    form_class = ExamForm
    success_url = reverse_lazy("admin-exam-pem")
    template_name = "superuser/pages/pembelajaran/exam_add.html" 

class ExamUpdateView(UpdateView):
    model = Exam
    form_class = ExamForm
    success_url = reverse_lazy("admin-exam-pem")
    context_object_name = "u"
    template_name = "superuser/pages/pembelajaran/exam_update.html"

class MapelView(View):
    def get(self,request):
        sub = Subject.objects.all()
        sub_count = Subject.objects.count()
        form = SubjectForm
        return render(request, "superuser/pages/pembelajaran/mapel.html", context={"subjects":sub, "count":sub_count, "form":form})

    def post(self,request):
        form = SubjectForm(data=request.POST)

        if form.is_valid():
            form.save()
            return redirect("admin-mapel-pem")

class MapelDeleteView(DeleteView):
    model = Subject
    success_url = reverse_lazy("admin-mapel-pem")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class BankSoalView(View):
    def get(self, request):
        form = QuestionForm()
        q = Question.objects.all()
        return render(request,"superuser/pages/pembelajaran/bank.html", context={"questions":q, "form":form})

    def post(self,request):
        form = QuestionForm(data=request.POST)

        if form.is_valid():
            form.save()
            return redirect("admin-bank-pem") 

class QuestionView(View):
    def get(self,request, pk):
        q = None
        model = Question.objects.get(id=pk)
        form = QuestionAddForm()

        if model.question_type == "essay":
            q = Essay.objects.filter(question_id=pk)
        elif model.question_type == "multiple":
            q = MultipleChoice.objects.filter(question_id=pk)
        return render(request, "superuser/pages/pembelajaran/question.html", context={"form":form, "model":model, "question":q})

    def post(self, request, pk):
        pass
    
