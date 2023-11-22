from django.shortcuts import render,redirect
from .forms import RegisterForm
from polls.models import Quiz, UserAnswer
from django.utils import timezone
def register(request):

    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_staff = False
            new_user.save()

            # 여기에서 퀴즈 데이터를 가져오고 UserAnswer에 추가하는 로직을 추가하세요.
            latest_quiz_list = Quiz.objects.all()  # 예시: 가장 최근의 퀴즈 목록을 가져오는 예제
            for quiz in latest_quiz_list:
                # UserAnswer에 새로운 레코드 추가
                user_answer = UserAnswer.objects.create(
                    user=new_user,
                    quiz=quiz,
                    selected_answer=None,
                    is_correct=False,
                    image=None,
                    date_answered=timezone.now(),
                    score=0
                )

            return render(request, 'registration/register_done.html', {'new_user':new_user})
    else:
        user_form = RegisterForm()

    return render(request, 'registration/register.html',{'form':user_form})