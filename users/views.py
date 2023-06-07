from django.shortcuts import render, redirect

# PARA CREAR UN NUEVO USUARIO
from .forms import UserCreationForm

# PARA HACER LOG IN
from .forms import UserLoginForm
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import user_not_authenticated

# PARA ACTUALIZAR EL PERFIL
from .forms import UserUpdateForm
from django.contrib.auth import get_user_model

# PARA CONFIMACION Y ACTIVACION DE CUENTA DE GMAIL
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .token import account_activation_token
from django.contrib.auth import get_user_model


# PARA CAMBIAR EL PASSWORD
from .forms import SetPasswordForm


# PARA RESETEAR EL PASSWORD
from .forms import PasswordResetForm
from django.db.models.query_utils import Q
# Create your views here.


def activate_email(request, user, to_email):
    mail_sub = "ACtivate your user account "
    message = render_to_string("template_activate_account.html", {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_sub, message, to=[to_email])
    if email.send():
        messages.success(request, f'Check your email to verifications')
    else:
        messages.error(
            request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activate")
        return redirect("signin")
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect("home")


@user_not_authenticated
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_activate = False
            user.save()
            activate_email(request, user, form.cleaned_data.get("email"))
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {
        "form": form
    })


@user_not_authenticated
def signin(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = UserLoginForm()
    return render(request, "signin.html", {
        "form": form
    })


@login_required(login_url="signin")
def closesession(request):
    logout(request)
    messages.info(request, "Close session")
    return redirect("home")


@login_required(login_url="signin")
def profile(request, id: int):
    if request.method == "POST":
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request, "Perfil actualizado")
        else:
            for error in list(form.errors.values()).pop():
                messages.error(request, error)
    user = get_user_model().objects.filter(id=id).first()
    if user:
        form = UserUpdateForm(instance=user)
        return render(request, "profile.html", {
            "form": form,
        })
    return redirect("home")


# PASSWORD CHANGE AND RESET
@login_required(login_url="signin")
def password_change(request):
    user = request.user
    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect("signin")
    else:
        form = SetPasswordForm(user)
    return render(request, "password_change.html", {
        "form": form
    })


def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            associated_user = get_user_model().objects.filter(Q(email=email)).first()
            if associated_user:
                subjet = "Password Reset request"
                message = render_to_string("template_password_reset.html", {
                    'user':  associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    'protocol': "https" if request.is_secure() else "http"
                })
                email = EmailMessage(subjet, message, to=[
                                     associated_user.email])
                if email.send():
                    messages.success(
                        request, "Check your email for reset password")
                    return redirect("home")
    form = PasswordResetForm()
    return render(request, "password_reset.html", {
        "form": form,
        "type": "reset"
    })


def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Your password has been set, Yo may go to signin")
                return redirect("home")
        form = SetPasswordForm(user)
        return render(request, "password_reset.html", {
            "form": form,
            "type": "confirm"
        })
    else:
        messages.error(request, "Link is expired")
    messages.error(
        request, 'Something went wrong, redirecting back to Homepage')
    return redirect("home")
