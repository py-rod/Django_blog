from django.urls import path
from . import views

urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("logout", views.closesession, name="logout"),
    path("profile/<int:id>", views.profile, name="profile"),


    # PARA ACTIVAR CORREO
    path("activate/<uidb64>/<token>", views.activate, name="activate"),

    # PARA CAMBIAR CONTRASEÑA
    path("password_change", views.password_change, name="password_change"),
    path("password_reset", views.password_reset, name="password_reset"),
    path("reset/<uidb64>/<token>", views.password_reset_confirm,
         name="password_reset_confirm")
]
