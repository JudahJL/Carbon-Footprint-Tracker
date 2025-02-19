from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CarbonFootprintForm(forms.Form):
    prompt = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your carbon footprint details. For example:\n"I drive 150km per week, use 250kwh of electricity monthly, live in an 85sqm house with 2 people. I mostly eat meat, cook 70% of meals at home, buy 2 pieces of clothing monthly, and recycle 60% of my waste. I take 2 flights per year averaging 1000km each."'
            }
        ),
        label="Describe your lifestyle and habits"
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter a password'}),
        label="Password",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        label="Confirm Password",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
