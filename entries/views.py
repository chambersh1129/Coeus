from django.db.models import Count, Q
from django.shortcuts import render
from django.views import View
from rest_framework import generics
from rest_framework.views import APIView

from entries import models, serializers


class HomePageView(View):
    def get(self, request):
        return render(request, "entries/home.html")


class SubjectView(generics.ListAPIView):
    serializer_class = serializers.SubjectSerializer
    queryset = models.Subject.objects.all()

    def get_queryset(self):
        entry_filter = Q(field__entry__public=True) | Q(
            field__entry__user__username=self.request.user.username, field__entry__public=False
        )
        return models.Subject.objects.all().annotate(count=Count("field__entry", filter=entry_filter))


class FieldView(generics.ListAPIView):
    serializer_class = serializers.FieldSerializer

    def get_queryset(self):
        entry_filter = Q(entry__public=True) | Q(entry__user__username=self.request.user.username, entry__public=False)

        if self.request.GET:
            if self.request.GET.get("subject"):
                field_filter = Q(subject__name__iexact=self.request.GET.get("subject"))
                return models.Field.objects.filter(field_filter).annotate(count=Count("entry", filter=entry_filter))

        return models.Field.objects.all().annotate(count=Count("entry", filter=entry_filter))


class EntryView(generics.ListAPIView):
    serializer_class = serializers.EntrySerializer

    def get_queryset(self):
        query = Q(public=True) | Q(user__username=self.request.user.username, public=False)

        if self.request.GET:
            if self.request.GET.get("subject"):
                query &= Q(field__subject__name__iexact=self.request.GET.get("subject"))

            if self.request.GET.get("field"):
                query &= Q(field__name__iexact=self.request.GET.get("field"))

            if self.request.GET.get("nouns"):
                nouns = self.request.GET.get("nouns").upper()
                query &= Q(nouns__contains=nouns.split(","))

            if self.request.GET.get("text"):
                query &= Q(text__icontains=self.request.GET.get("text"))

        return models.Entry.objects.filter(query)


class GraphsView(APIView):
    def get(self, request, format=None):
        pass
