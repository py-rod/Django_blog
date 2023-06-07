from django import forms
from .models import Courses, ArticleCourse


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ["title", "author", "bg_color",
                  "image", "published", "modified"]
        widgets = {
            "published": forms.DateTimeInput(attrs={"readonly": True}),
            "modified": forms.DateTimeInput(attrs={"readonly": True}),
        }


class CourseUpdateForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ["title", "bg_color", "image"]


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = ArticleCourse
        fields = ["title", "description", "image", "author",
                  "series", "content", "published", "modified"]
        widgets = {
            "published": forms.DateTimeInput(attrs={"readonly": True}),
            "modified": forms.DateTimeInput(attrs={"readonly": True}),
        }


class ArticleUpdateForm(forms.ModelForm):
    class Meta:
        model = ArticleCourse
        fields = ["title", "description", "image",
                  "author", "series", "content"]
