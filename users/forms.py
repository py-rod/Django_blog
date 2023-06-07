from django import forms
# CREATE USER
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# LOG IN
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.utils.translation import get_language
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm


class UserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "password1", "password2"]
        widgets = {
            "first_name": forms.TextInput(attrs={"autofocus": True})
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        if get_language() == "es-sv":
            self.error_messages = {
                "invalid_login": (
                    "Por favor, introduzca de manera correcta el correo o la contraseña. "
                    "Los campos pueden ser sensibles a mayúsculas."
                ),
                "inactive": ("Esta cuenta está inactiva."),
            }

        else:
            self.error_messages = {
                "invalid_login": (
                    "Please enter a correct email and password. Note that both "
                    "fields may be case-sensitive."
                ),
                "inactive": ("This account is inactive."),
            }

    username = forms.CharField(widget=forms.EmailInput(
        attrs={"autofocus": True}), label="Email")
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
        attrs={"class": "content-recaptcha", "required": True}))


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email", "description"]
        widgets = {
            "email": forms.EmailInput(attrs={"readonly": True}),
            "description": forms.Textarea(attrs={"rows": 3})
        }


# PASSWORD CHANGE
class SetPasswordForm(SetPasswordForm):
    model = get_user_model()
    fields = ["new_password1", "new_password2"]


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(attrs={"required": False}))
