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
    password1 = forms.CharField(widget=PasswordInput(attrs={"placeholder":"Enter new password", "class":"w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400"}))
    password2 = forms.CharField(widget=PasswordInput(attrs={"placeholder":"Confirm new password","class":"w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400"})) 

class TeacherForm(forms.ModelForm):
    photo = forms.ImageField()
    gender = forms.ChoiceField(choices=GENDER,widget=Select(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400 bg-white"}))
    subject_id = forms.ChoiceField(widget=Select(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400 bg-white"}))

    class Meta:
        model = Teacher
        fields = ["photo", "gender", "subject_id"]
