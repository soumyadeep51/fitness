# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserInputForm(forms.Form):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    weight = forms.FloatField(
        label="Weight (kg)",
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'e.g. 65'})
    )
    height = forms.FloatField(
        label="Height (cm)",
        min_value=30,
        widget=forms.NumberInput(attrs={'placeholder': 'e.g. 170'})
    )
    age = forms.IntegerField(
        label="Age",
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'e.g. 25'})
    )
    gender = forms.ChoiceField(
        label="Gender",
        choices=GENDER_CHOICES,
        widget=forms.Select()
    )
#from django import forms

class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name", widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}))
    email = forms.EmailField(label="Your Email", widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    feedback = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Share your feedback', 'rows': 4}), label="Feedback")

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name", widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}))
    email = forms.EmailField(label="Your Email", widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Type your message here', 'rows': 4}), label="Message")



class CustomUserRegisterForm(UserCreationForm):
    age = forms.IntegerField(required=True, label='Age')
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES, required=True, label='Gender')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'gender', 'password1', 'password2']

