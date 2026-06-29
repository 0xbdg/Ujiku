from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.fields import EmailInput
from django.forms.widgets import *

from .models import *


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        widget=TextInput(
            attrs={
                "class": "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:shadow-outline-blue focus:border-blue-300 transition duration-150 ease-in-out sm:text-sm sm:leading-5"
            }
        ),
    )
    password = forms.CharField(
        required=True,
        widget=PasswordInput(
            attrs={
                "class": "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:shadow-outline-blue focus:border-blue-300 transition duration-150 ease-in-out sm:text-sm sm:leading-5"
            }
        ),
    )

    class Meta:
        model = Account
        fields = ["username", "password"]

class AccountForm(forms.Form):
    firstname = forms.CharField(widget=TextInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400"}))
    lastname = forms.CharField(widget=TextInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400"}))
    username = forms.CharField(widget=TextInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400"}))
    email= forms.EmailField(widget=EmailInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400"}))
    password1 = forms.CharField(required=False,widget=PasswordInput(attrs={"placeholder":"Enter new password", "class":"w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400"}))
    password2 = forms.CharField(required=False,widget=PasswordInput(attrs={"placeholder":"Confirm new password","class":"w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400"})) 

class TeacherForm(forms.Form):
    photo = forms.ImageField(required=False, widget=ClearableFileInput(attrs={"class":"px-4 py-2 text-sm border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-1 focus:ring-gray-400", "accept":"image/*"}))
    gender = forms.ChoiceField(choices=GENDER,widget=Select(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400 bg-white"}))
    subject_id = forms.ModelChoiceField(queryset=Subject.objects.all(),widget=Select(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400 bg-white"}))

class StudentForm(forms.Form):
    photo = forms.ImageField(required=False, widget=ClearableFileInput(attrs={"class":"px-4 py-2 text-sm border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-1 focus:ring-gray-400", "accept":"image/*"}))
    grade = forms.ChoiceField(choices=GRADE,widget=Select(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400 bg-white"}))
    gender = forms.ChoiceField(choices=GENDER,widget=Select(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400 bg-white"}))

class ExamForm(forms.Form):
    course = forms.CharField(widget=TextInput(attrs={"class":""}))
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=Select(attrs={"class":""}))
    exam_date = forms.DateField(widget=DateInput(attrs={"class":""}))
    start_time = forms.TimeField(widget=TimeInput(attrs={"class":""}))
    end_time = forms.TimeField(widget=TimeInput(attrs={"class":""}))

class SubjectForm(forms.ModelForm):
    subject = forms.CharField(required=True, widget=TextInput(attrs={"class":"w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors", "placeholder":"Masukan mapel"}))

    class Meta:
        model = Subject
        fields = ["subject"]

class QuestionForm(forms.ModelForm):
    exam = forms.ModelChoiceField(queryset=Exam.objects.all(), widget=Select(attrs={"class":"w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors"}))
    question_type = forms.ChoiceField(choices=TYPE, widget=Select(attrs={"class":"w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors"}))

    class Meta:
        model = Question
        fields = ["exam", "question_type"]
