from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

class Quiz(models.Model):
    question = models.CharField(max_length=200)
    image = models.ImageField(upload_to='quiz_images/', blank=True, null=True)
    is_text_answer = models.BooleanField(default=False)
    is_date_answer = models.BooleanField(default=False)
    points = models.PositiveIntegerField(default=1)
    date_asked = models.DateTimeField(default=timezone.now,editable=False)

    def check_answer(self, user_answer):
        if self.is_text_answer:
            correct_answer = self.answers.filter(is_correct=True).first()
            #return user_answer.lower() == datetime.now().strftime('%Y-%m-%d').lower()
            if correct_answer:
                return user_answer.lower() == correct_answer.text.lower()
            else:
                return False
        #elif self.is_date_answer:
        #    # 날짜 응답을 날짜 형식으로 변환
        #    user_date = datetime.now().date()
        #    correct_date = self.answers.filter(is_correct=True).first().date_answered.date() if self.answers.filter(is_correct=True).first() else None
        #    return user_date == correct_date if correct_date else False
        else:
            correct_answer = self.answers.filter(is_correct=True).first()
            return user_answer.lower() == correct_answer.text.lower() if correct_answer else False
            #pass
class Answer(models.Model):
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    image = models.ImageField(upload_to='answer_images/', blank=True, null=True)
    is_text_answer = models.BooleanField(default=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='answers', null=True, blank=True)

    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)  # Assuming User is your user model
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='useranswer', null=True)
    selected_answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)  # Add Answer relationship here
    #selected_answer_text = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    image = models.ImageField(upload_to='useranswer_images/', blank=True, null=True)
    date_answered = models.DateTimeField(default=timezone.now)
    score = models.PositiveIntegerField(default=0)
    #def save(self, *args, **kwargs):
     #   if not self.quiz:
      #      self.quiz = self.quiz
       # super().save(*args, **kwargs)
    def save(self, *args, **kwargs):

        if not self.quiz:
            self.quiz = self.quiz

        super().save(*args, **kwargs)