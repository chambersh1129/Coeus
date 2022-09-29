from django.db import models


class EntryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related("nouns").select_related("field", "user")


class FieldManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("subject")
