from django.db import models

import nltk
from coeus.settings import BASE_DIR

nltk.data.path.append(BASE_DIR / "nltk")


# Create your models here.
class Entry(models.Model):
    user = models.ForeignKey("auth.User", related_name="entry", on_delete=models.CASCADE)
    field = models.ForeignKey("Field", related_name="entry", on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    text = models.TextField()
    nouns = models.JSONField(default=list, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date",)
        verbose_name_plural = "Entries"

    def save(self, *args, **kwargs):
        def is_noun(pos):
            return pos[:2] == "NN"

        tokenized_text = nltk.word_tokenize(self.text)

        self.nouns = [word.upper() for (word, pos) in nltk.pos_tag(tokenized_text) if is_noun(pos)]

        super(Entry, self).save(*args, **kwargs)


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

    class Meta:
        ordering = ("name",)
        unique_together = ("name", "subject")
        verbose_name_plural = "Fields"

    def __str__(self):
        return self.name
