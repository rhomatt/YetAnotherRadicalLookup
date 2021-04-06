from django.urls import path
from . import views

urlpatterns = [
    path('kanji', views.KanjiView.as_view()),
    path('search', views.ResultView.as_view()),
        ]
