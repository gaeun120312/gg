from django import forms
from .models import Quiz, Answer

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['question', 'image']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct', 'image']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['text'].widget.attrs.update({'style': 'width: 150px; height: 150px;'})
        #self.fields['image'].widget.attrs.update({'style': 'width: 30px; height: 30px;'})
        if self.instance and self.instance.quiz_id and Quiz.objects.filter(id=self.instance.quiz_id, is_text_answer=True).exists():
            self.fields['text'] = forms.CharField(max_length=100, label='Your Answer')
            del self.fields['image']
        else:
            self.fields['image'] = forms.ImageField(label='Your Answer Image')
            del self.fields['text']


class AnswerFormText(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct', 'image']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }