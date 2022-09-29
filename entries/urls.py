from django.urls import re_path

from entries import views

urlpatterns = [
    re_path(r"^$", views.HomePageView.as_view(), name="homepage"),
    re_path(r"donut/", views.DonutGraphView.as_view(), name="donut"),
    re_path(r"table/", views.TableView.as_view(), name="table"),
    re_path(r"wordcloud/", views.WordCloudView.as_view(), name="wordcloud"),
    re_path(r"api/subject/", views.SubjectView.as_view()),
    re_path(r"api/field/", views.FieldView.as_view()),
    re_path(r"api/entry/", views.EntryView.as_view()),
]
