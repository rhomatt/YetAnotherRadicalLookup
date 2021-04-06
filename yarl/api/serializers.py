from rest_framework import serializers
from .models import Kanji, Word, Result

class KanjiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kanji
        fields = ('kanji', 'strokes', 'frequency')

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ('lemma',)

class ResultSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    readings = serializers.CharField()
    definitions = serializers.CharField()

    def create(self, data):
        return Result.objects.create(**data)

    def update(self, instance, data):
        instance.id = data.get('id', instance.id)
        instance.readings = data.get('readings', instance.readings)
        instance.definitions = data.get('definitions', instance.definitions)
        instance.save()
        return instance
