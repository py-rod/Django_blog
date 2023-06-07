from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("<series>=<int:id>/", views.article_courses, name="article"),
    path("<series>/<article>=<int:id>",
         views.post_article, name="content_article"),


    # CREAR CURSO
    path("new_course", views.create_course, name="create_course"),
    path("<series>=<int:id>/update", views.update_course, name="update_course"),
    path("<series>=<int:id>/delete", views.delete_course, name="delete_course"),

    # CREAR ARTICULO
    path("new_article", views.create_article, name="create_article"),
    path("<series>/<article>=<int:id>/update",
         views.update_article, name="update_article"),
    path("<series>/<article>=<int:id>/delete",
         views.delete_article, name="delete_article")
]
