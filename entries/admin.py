from django.contrib import admin

from entries.models import Entry, Field, Subject


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "subject", "field", "text", "public", "str_of_nouns", "date")
    list_filter = ("user", "date", "field__subject__name", "field__name")
    readonly_fields = ("nouns",)

    def subject(self, obj):
        return obj.field.subject.name


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "description")
    list_filter = ("subject__name",)
    list_select_related = ("subject",)
