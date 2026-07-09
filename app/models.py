from django.db import models
from django.contrib.auth.models import AbstractUser
from django_ckeditor_5.fields import CKEditor5Field

GENDER = (("Male", "male"), ("Female", "female"))
GRADE = (("X", "X"), ("XI", "XI"), ("XII","XII"))
TYPE = (("multiple", "Multiple Choices"), ("essay", "Essay"))


class Account(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)


class Student(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, blank=True)
    grade = models.CharField(max_length=50, choices=GRADE)
    gender = models.CharField(max_length=20, choices=GENDER)


class Subject(models.Model):
    subject = models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.subject


class Teacher(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, blank=True)
    gender = models.CharField(max_length=50, choices=GENDER)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id.username}"


class Exam(models.Model):
    course = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_date = models.DateField(null=False)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.course


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=50, choices=TYPE)

    def __str__(self):
        return f"{self.exam.course}"


class Essay(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    question = CKEditor5Field("Text", config_name="extends")

    def __str__(self):
        return f"{self.question_id.exam} - {self.id}"


class MultipleChoice(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    question = CKEditor5Field("Text", config_name="extends")
    option1 = models.CharField(max_length=400)
    option2 = models.CharField(max_length=400)
    option3 = models.CharField(max_length=400)
    option4 = models.CharField(max_length=400)
    cat = (
        ("option1", "option1"),
        ("option2", "option2"),
        ("option3", "option3"),
        ("option4", "option4"),
    )
    answer = models.CharField(max_length=200, choices=cat)

    def __str__(self):
        return f"{self.question_id.exam} - soal nomor {self.id}"


class Result(models.Model):
    student_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=7, null=False, blank=False)

    def __str__(self):
        return f"{self.student_id.username} - {self.question_id.exam} - {self.answer}"


class ExamFinish(models.Model):
    student = models.ForeignKey(Account, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)

class Log(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    activity = models.CharField(max_length=255)
    time = models.DateTimeField()
