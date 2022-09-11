from rest_framework import serializers

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


class EntrySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    subject = serializers.CharField(source="field.subject.name")

    class Meta:
        model = Entry
        fields = ["id", "user", "subject", "field", "text", "nouns", "date"]
