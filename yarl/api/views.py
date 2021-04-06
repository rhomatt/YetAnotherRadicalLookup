from django.shortcuts import render
from django.db import connection
from .models import Kanji, Result
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import KanjiSerializer, ResultSerializer
from .rlux import Rlux

# Create your views here.
class KanjiView(APIView):
    serializer_class = KanjiSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

class ResultView(APIView):

    def get(self, request):
        searchexp = ""
        if "exp" in request.query_params:
            searchexp = request.query_params["exp"]
        query, params = Rlux(searchexp).generate_query()
        queryset = Result.objects.raw(query, params)
        serializer = ResultSerializer(queryset, many=True)
        # queryset = Word.objects.raw(query, params=params)

        return Response(serializer.data)
