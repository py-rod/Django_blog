from django.shortcuts import render, redirect
from .decorators import user_is_superuser
from django.contrib import messages

# MOSTRANDO LOS CURSOS
from .models import Courses
# MOSTRANDO LOS ARTICULOS Y POST DEL ARTICULO
from .models import ArticleCourse
# CREAR NUEVO CURSO, ACTUALIZAR Y ELIMINAR
from .forms import CourseCreateForm, CourseUpdateForm
# CREAR NUEVO ARTICULO, ACTUALIZAR Y ELIMINAR
from .forms import ArticleCreateForm, ArticleUpdateForm
# Create your views here.


# VISTA DE LOS CURSOS EN EL INDEX
def index(request):
    cursos = Courses.objects.all()
    return render(request, "index.html", {
        "objects": cursos,
    })

# VISTA DE LOS ARTICULOS DE CADA CURSO


def article_courses(request, series: str, id: int):
    # IMPORTANTE FILTRARLOS
    article = ArticleCourse.objects.filter(series__slug=series).all()
    return render(request, "articles.html", {
        "objects": article
    })


def post_article(request, series: str, id: int, article: str):
    content = ArticleCourse.objects.filter(
        series__slug=series, article_slug=article).first()
    return render(request, "post_article.html", {
        "object": content
    })


# NUEVO CURSO, ACTUALIZAR Y ELIMINAR
@user_is_superuser
def create_course(request):
    if request.method == "POST":
        form = CourseCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "New course added")
            return redirect("home")
    else:
        form = CourseCreateForm()
    return render(request, "new_course.html", {
        "form": form,
        "create": "create"
    })


def update_course(request, series, id: int):
    filter_course = Courses.objects.filter(slug=series).first()
    if request.method == "POST":
        form = CourseUpdateForm(
            request.POST, request.FILES, instance=filter_course)
        if form.is_valid():
            form.save()
            messages.info(request, "Course updated")
            return redirect("home")
    else:
        form = CourseUpdateForm(instance=filter_course)
    return render(request, "new_course.html", {
        "form": form,
        "create": "update",
        "object": filter_course
    })


def delete_course(request, series, id: int):
    course = Courses.objects.filter(slug=series).first()
    if request.method == "POST":
        course.delete()
        messages.warning(request, "Course eliminated")
        return redirect("home")
    else:
        return render(request, "delete.html", {
            "object": course,
            "type": "course"
        })


# NUEVO ARTICULO, ACTUALIZAR Y ELIMINAR

@user_is_superuser
def create_article(request):
    if request.method == "POST":
        form = ArticleCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "New article added")
            return redirect("home")
    else:
        form = ArticleCreateForm()
    return render(request, "new_article.html", {
        "form": form,
        "create": "create"
    })


def update_article(request, series, article, id: int):
    filter_article = ArticleCourse.objects.filter(
        series__slug=series, article_slug=article).first()
    if request.method == "POST":
        form = ArticleUpdateForm(
            request.POST, request.FILES, instance=filter_article)
        if form.is_valid():
            form.save()
            messages.info(request, "Article has been updated")
            return redirect("home")
    else:
        form = ArticleUpdateForm(instance=filter_article)
    return render(request, "new_article.html", {
        "form": form,
        "create": "update",
        "object": filter_article
    })


def delete_article(request, series, article, id: int):
    article = ArticleCourse.objects.filter(
        series__slug=series, article_slug=article).first()
    if request.method == "POST":
        article.delete()
        messages.warning(request, "Article eliminated")
        return redirect("home")
    else:
        return render(request, "delete.html", {
            "object": article,
            "type": "article"
        })
