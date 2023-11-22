from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Quiz, Answer, UserAnswer
from django.db.models import Max
from .forms import QuizForm, AnswerForm, AnswerFormText
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser

def quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    answers = Answer.objects.filter(quiz=quiz)
    form_class = AnswerFormText if quiz.is_text_answer else AnswerForm
    form = form_class()
    return render(request, 'polls/quiz.html', {'quiz': quiz, 'answers': answers})
def index(request):

    first_quiz = Quiz.objects.first()
    #return redirect('polls:quiz', quiz_id=first_quiz.id)

    #퀴즈 리스트 보여주기
    latest_quiz_list = Quiz.objects.all().order_by('-id')[:5]
    context = {'latest_quiz_list': latest_quiz_list}
    return render(request, 'polls/index.html', context)

@login_required(login_url='/polls/')
def check_answer(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    user = request.user

    if user.is_anonymous:
        user = AnonymousUser()

    if quiz.is_text_answer:
        #selected_answer_text = request.POST.get('answer_text', '')
        #is_correct = quiz.check_answer(selected_answer_text)
        is_correct = quiz.check_answer(request.POST.get('answer_text', ''))
    else:
        selected_answer_id = request.POST.get('answer', '')
        selected_answer = get_object_or_404(Answer, id=selected_answer_id)
        is_correct = selected_answer.is_correct

    question_score = quiz.points if is_correct else 0

    user_answer, created = UserAnswer.objects.get_or_create(user=user, quiz=quiz)
    #user_answer.selected_answer_text = selected_answer_text if quiz.is_text_answer else ''
    user_answer.selected_answer_text = request.POST.get('answer_text', '') if quiz.is_text_answer else ''
    user_answer.is_correct = is_correct
    user_answer.score = question_score
    user_answer.date_answered = timezone.now()
    user_answer.save()
    print(f"user: {user}")
    print(f"quiz: {quiz}")
    print(f"is_correct: {is_correct}")
    print(f"user_answer: {user_answer}")

    total_score = UserAnswer.objects.filter(user=user).aggregate(Sum('score'))['score__sum']

    next_quiz = Quiz.objects.filter(id__gt=quiz_id, useranswer__user=user).first() if user.is_authenticated else None

    if next_quiz:
        return redirect('polls:quiz', quiz_id=next_quiz.id)
    else:
        return render(request, 'polls/completed.html', {'total_score': total_score})

def next_quiz(request):
    user = request.user
    # Get the maximum quiz ID that the user has already answered
    max_answered_quiz_id = UserAnswer.objects.filter(user=user).aggregate(Max('quiz__id'))['quiz__id__max']

    # If the user hasn't answered any quizzes yet, max_answered_quiz_id will be None
    # In that case, we set it to -1 to make the filter below work
    if max_answered_quiz_id is None:
        max_answered_quiz_id = -1

    #next_quiz = Quiz.objects.filter(id__gt=max_answered_quiz_id).exclude(useranswer__isnull=True).first()
    #next_quiz = Quiz.objects.filter(id__gt=max_answered_quiz_id).order_by('id').first()
    next_quiz = Quiz.objects.filter(id__gt=max_answered_quiz_id).exclude(useranswer__user=user).first()
    print(f"max_answered_quiz_id: {max_answered_quiz_id}")
    print(f"next_quiz: {next_quiz}")
    if next_quiz:
        return redirect('polls:quiz', quiz_id=next_quiz.id)
    else:
        return redirect('polls:completed')
@login_required(login_url='/polls/')
def completed(request,total_score=None):
    user = request.user
    total_score = 0
    user_answers = []

    if user.is_authenticated:
        user_answers = UserAnswer.objects.filter(user=user)
        total_score = UserAnswer.objects.filter(user=user).aggregate(Sum('score'))['score__sum']

    return render(request, 'polls/completed.html', {'total_score': total_score, 'user_answers': user_answers})