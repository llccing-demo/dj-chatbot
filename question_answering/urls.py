from django.urls import path
from . import views

urlpatterns = [
    path('', views.answer_question, name='answer_question'),
]