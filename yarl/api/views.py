from django.shortcuts import render
from django.db import connection
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

    def get(self, request):
        searchexp = ""
        if "exp" in request.query_params:
            searchexp = request.query_params["exp"]
        query, params = Rlux(searchexp).generate_query()
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            queryset = cursor.fetchall()
        # queryset = Word.objects.raw(query, params=params)

        return Response([q[1] for q in queryset])
