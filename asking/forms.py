from django import forms
from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class QuestionForm(forms.Form):
    answer = forms.CharField(label='Введите ответ на вопрос', max_length=100)
    question_id = forms.IntegerField()


class AskingForm(forms.Form):
    name = forms.CharField(max_length=60)
    question_text = forms.CharField(label='description', max_length=500)
    start_date = forms.DateTimeField(label='date start')
    finish_date = forms.DateTimeField(label='date finish')


class QuestionChangeForm(forms.Form):
    question_text = forms.CharField(label='description', max_length=500)
    answer_type = forms.IntegerField(label='answer type')
    answer_choices = forms.CharField(label='answer choices')
