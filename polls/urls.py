from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('',views.index, name='index'),
    path('<int:quiz_id>/', views.quiz, name='quiz'),
    path('<int:quiz_id>/check_answer/', views.check_answer, name='check_answer'),
    path('completed/', views.completed, name='completed'),
    #path('incorrect/', views.incorrect, name='incorrect'),
    path('next_quiz/<int:quiz_id>/', views.next_quiz, name='next_quiz'),

]
