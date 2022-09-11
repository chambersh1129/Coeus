from django.contrib import admin

from entries.models import Entry, Field, Subject


class EntryAdmin(admin.ModelAdmin):
    list_display = ("user", "subject", "field", "text", "public", "nouns", "date")
    list_filter = ("user", "date", "field__subject__name", "field__name")
    list_select_related = ("field",)
    readonly_fields = ("nouns",)

    def subject(self, obj):
        return obj.field.subject.name


admin.site.register(Entry, EntryAdmin)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


admin.site.register(Subject, SubjectAdmin)


class FieldAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "description")
    list_filter = ("subject__name",)
    list_select_related = ("subject",)


admin.site.register(Field, FieldAdmin)
