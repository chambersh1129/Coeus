from django.views.generic import TemplateView
from rest_framework.generics import ListAPIView

from entries.mixins import EntryMixin, FieldMixin, SubjectMixin
from entries.serializers import EntrySerializer, FieldSerializer, SubjectSerializer


class HomePageView(TemplateView):
    template_name = "entries/base.html"


class DonutGraphView(FieldMixin, TemplateView):
    template_name = "entries/donut_graph.html"


class WordCloudView(TemplateView):
    template_name = "entries/word_cloud.html"


class TableView(EntryMixin, TemplateView):
    template_name = "entries/table.html"


class SubjectView(SubjectMixin, ListAPIView):
    serializer_class = SubjectSerializer


class FieldView(FieldMixin, ListAPIView):
    serializer_class = FieldSerializer


class EntryView(EntryMixin, ListAPIView):
    serializer_class = EntrySerializer
