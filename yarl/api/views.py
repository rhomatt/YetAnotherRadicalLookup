from django.shortcuts import render
from .models import Kanji, Word
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import KanjiSerializer, WordSerializer
from .rlux import Rlux

# Create your views here.
class KanjiView(APIView):
    serializer_class = KanjiSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

class WordView(APIView):
    serializer_class = WordSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            query, params = Rlux(serializer.data.get('lemma')).generate_query()
            queryset = Word.objects.raw(query, params=params)

            return Response([q.lemma for q in queryset])
