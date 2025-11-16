from django.urls import path
from .views import daily_word_view
from . import views

urlpatterns = [
    path('word/', daily_word_view, name='daily_word'),
    path('levels/', views.level_select, name='level_select'),
    path('learned/', views.learned_words, name='learned_words'),
    path('mark_as_learned/', views.mark_as_learned, name='mark_as_learned'),
    path('progress/', views.progress_view, name='progress'),
    path('quiz/', views.quiz_view, name='quiz'),

]
