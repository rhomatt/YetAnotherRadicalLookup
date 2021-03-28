from django.urls import path
from . import views

urlpatterns = [
    path('kanji', views.KanjiView.as_view()),
    path('search', views.WordView.as_view()),
        ]
