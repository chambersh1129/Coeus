from django.urls import re_path

from entries import views

urlpatterns = [
    re_path(r"^$", views.HomePageView.as_view(), name="homepage"),
    re_path(r"api/subject/", views.SubjectView.as_view()),
    re_path(r"api/field/", views.FieldView.as_view()),
    re_path(r"api/entry/", views.EntryView.as_view()),
]
