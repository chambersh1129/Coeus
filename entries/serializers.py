from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from entries.models import Entry, Field, Subject


class FieldSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = Field
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = Subject
        fields = "__all__"


class EntrySerializer(TaggitSerializer, serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    subject = serializers.CharField(source="field.subject.name")
    nouns = TagListSerializerField()

    class Meta:
        model = Entry
        fields = "__all__"
