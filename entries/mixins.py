from django.db.models import Count, Q

from entries.models import Entry, Field, Subject


class EntryMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response["HX-Trigger-After-Settle"] = "renderTable"
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = self.get_queryset()
        return context

    def get_queryset(self):
        query = Q(public=True) | Q(user__username=self.request.user.username, public=False)

        if self.request.GET:
            if self.request.GET.get("subject"):
                query &= Q(field__subject__name__iexact=self.request.GET.get("subject"))

            if self.request.GET.get("field"):
                query &= Q(field__name__iexact=self.request.GET.get("field"))

            if self.request.GET.get("nouns"):
                nouns = self.request.GET.get("nouns").upper()
                query &= Q(nouns__name__in=nouns.split(","))

            if self.request.GET.get("text"):
                query &= Q(text__icontains=self.request.GET.get("text"))

        return Entry.objects.filter(query)


class FieldMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "fields" not in context:
            context["fields"] = self.get_queryset()
        return context

    def get_queryset(self):
        query = Q(entry__public=True) | Q(entry__user__username=self.request.user.username, entry__public=False)

        if self.request.GET:
            if self.request.GET.get("subject"):
                query &= Q(subject__name__iexact=self.request.GET.get("subject"))

        return Field.objects.filter(query).annotate(count=Count("entry"))


class SubjectMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "subjects" not in context:
            context["subjects"] = self.get_queryset()
        return context

    def get_queryset(self):
        query = Q(field__entry__public=True) | Q(
            field__entry__user__username=self.request.user.username, field__entry__public=False
        )

        return Subject.objects.filter(query).annotate(count=Count("field__entry"))
