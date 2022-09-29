from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager

import nltk
from entries.managers import EntryManager, FieldManager

nltk.data.path.append(settings.BASE_DIR / "nltk")


# Create your models here.
class Entry(models.Model):
    user = models.ForeignKey("auth.User", related_name="entry", on_delete=models.CASCADE)
    field = models.ForeignKey("Field", related_name="entry", on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    text = models.TextField()
    nouns = TaggableManager(verbose_name="Nouns")
    date = models.DateTimeField(auto_now_add=True)

    objects = EntryManager()

    class Meta:
        ordering = ("-date",)
        verbose_name_plural = "Entries"

    def list_of_nouns(self):
        return [str(noun) for noun in self.nouns.all()]

    def str_of_nouns(self):
        return ", ".join(self.list_of_nouns())


def is_noun(pos):
    return pos[:2] == "NN"


@receiver(post_save, sender=Entry)
def update_nouns(sender, instance, **kwargs):

    tokenized_text = nltk.word_tokenize(instance.text)

    nouns = [word.upper() for (word, pos) in nltk.pos_tag(tokenized_text) if is_noun(pos)]

    if instance.nouns.names() != nouns:
        instance.nouns.set(nouns, clear=True)


class Subject(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField()

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.name


class Field(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    subject = models.ForeignKey("Subject", related_name="field", on_delete=models.CASCADE)
    description = models.TextField()

    objects = FieldManager()

    class Meta:
        ordering = ("name",)
        unique_together = ("name", "subject")
        verbose_name_plural = "Fields"

    def __str__(self):
        return self.name
