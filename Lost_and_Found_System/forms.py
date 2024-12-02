from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text="essential")
    password1 = forms.CharField (
        label = "password",
        strip = False,
        widget = forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text = "1"
    )

    password2 = forms.CharField (
        label = "password again",
        strip = False,
        widget = forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text = "1"
    )

    username = forms.CharField (
        label = "username",
        help_text = "essential"
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')