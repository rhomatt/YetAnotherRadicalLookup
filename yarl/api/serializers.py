from rest_framework import serializers
from .models import Kanji, Word

class KanjiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kanji
        fields = ('kanji', 'strokes', 'frequency')

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ('lemma',)
