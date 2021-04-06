from django.db import models

# Create your models here.
class Kanji(models.Model):
    kanji = models.CharField(max_length=1, primary_key=True)
    strokes = models.IntegerField()
    frequency = models.IntegerField(null=True)
    radicals = models.ManyToManyField(
            'Radical',
            through='Krad',
            through_fields=('kanji', 'radical')
            )

class Radical(models.Model):
    radical = models.CharField(max_length=1, primary_key=True)
    strokes = models.IntegerField()

class Krad(models.Model):
    kanji = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    radical = models.ForeignKey(Radical, on_delete=models.CASCADE)

class Synset_def(models.Model):
    synset = models.TextField()
    lang = models.TextField()
    definition = models.TextField()
    sid = models.TextField()

class Word(models.Model):
    wordid = models.IntegerField(primary_key=True)
    lang = models.TextField()
    lemma = models.TextField()
    pron = models.TextField(null=True)
    pos = models.TextField()

class Result(models.Model):
    id = models.IntegerField(primary_key=True)
    readings = models.TextField()
    definitions = models.TextField()
