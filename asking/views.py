from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import HttpResponse, JsonResponse
from .forms import UserLoginForm, QuestionForm, AskingForm, QuestionChangeForm
from .models import *
import json
from django.contrib.auth.models import AnonymousUser


def index(request):
    return render(request, "index.html", context={})


def user_login(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    # messages.success(request, 'Вы успешно разавторизированы')
    return redirect('home')


def asking(request):
    # messages.success(request, 'Вы успешно разавторизированы')
    askings = AskingModel.objects.all()
    res = []
    for elem in askings:
        res.append({'name': elem.name, 'start_date': elem.start_date, 'finish_date': elem.finish_date, 'key': elem.pk})
    context = {'askings': res}
    return render(request, "asking.html", context=context)


def start_question(request, asking_id):
    # print(asking_id)
    questions_answered = UserAnswers.objects.filter(asking=asking_id)
    questions = list(Question.objects.filter(asking=asking_id).order_by('pk'))
    quest = [question.question for question in questions_answered]
    if not questions:
        return HttpResponse('Неверный запрос')

    if not request.user.is_authenticated:
        # В случае если пользователь - аноним, пробегаем по списку вопросов и выдаём следующий
        if 'question_id' in request.POST:
            for question in questions:
                if question.pk > request.POST['question_id']:
                    return redirect('/asking_go/{}_{}'.format(asking_id, questions.pk))
            else:
                # Все вопросы отвечены, сохраняем
                asking = AskingModel.objects.get(id=asking_id)
                res = UserAskings(asking=asking, is_finished=True, userid=AnonymousUser())
                res.save()
                return render(request, "done.html")
        else:
            #  Наш аноним только начал опрос
            return redirect('/asking_go/{}_{}'.format(asking_id, questions[0].pk))
    else:
        # Юзер авторизован
        for question in questions:
            # Смотрим на какие ещё не отвечал
            if question not in quest:
                return redirect('/asking_go/{}_{}'.format(asking_id, question.pk))
        else:
            # Закончил, молодец
            user = request.user
            asking = AskingModel.objects.get(id=asking_id)
            res = UserAskings(asking=asking, is_finished=True, userid=user)
            res.save()
            return render(request, "done.html")


def get_solved_askings(request, user_id):
    askings = UserAskings.objects.filter(userid=user_id)
    res = []
    for asking in askings:
        line = {
            'asking': asking.asking.pk,
            'is_finished': asking.is_finished
        }
        res.append(line)
    return JsonResponse({'data': res})


def get_solved_questions(request, user_id, asking_id):
    questions = UserAnswers.objects.filter(userid=user_id, asking=asking_id)
    res = []
    for question in questions:
        line = {
            'question': question.question.pk,
            'answer_text': question.answer_text,
            'answer_is_json': question.answer_is_json,
        }
        res.append(line)
    return JsonResponse({'data': res})


def asking_go(request, asking_id, question_id):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            answer_is_json = False
            user = ''
            if request.user.is_authenticated:
                user = request.user
            else:
                user = AnonymousUser()
            # if 'select' in request.POST:
            #     answer = json.loads(request.POST['select'])
            question = Question.objects.get(id=question_id)
            asking = AskingModel.objects.get(id=asking_id)
            p = UserAnswers(userid=user, asking=asking, question=question, answer_text=answer,
                            answer_is_json=answer_is_json)
            p.save()
        redirect('/asking_start/{}'.format(asking_id))
    question = Question.objects.get(asking=asking_id, pk=question_id)

    answers = []
    ans_num = 1
    if question.answer_type != 1:
        if 'answers' in json.loads(question.answer_choices):
            for elem in json.loads(question.answer_choices)['answers']:
                answers.append({'text': elem, 'num': ans_num})
                ans_num += 1
    res = {'text': question.question_text, 'type': question.answer_type,
               'answer_choices': question.answer_choices, 'answers': answers}
    context = {'question': res}
    return render(request, "question.html", context=context)


@login_required
def asking_change(request, asking_id=None):
    """Изменение записи в БД, только для администратора"""
    if request.user.is_superuser:
        if asking_id is None:
            # Создание новой записи
            form = AskingForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                question_text = form.cleaned_data['question_text']
                start_date = form.cleaned_data['start_date']
                finish_date = form.cleaned_data['finish_date']
                asking = AskingModel(name=name,
                                     question_text=question_text,
                                     start_date=start_date,
                                     finish_date=finish_date)
                asking.save()
                return HttpResponse('Успешно создано')
            return HttpResponse('Ошибка в форме')
        else:
            asking = AskingModel.objects.get(pk=asking_id)
            if request.method == 'POST':
                # Изменение записи
                # тут сделано через формы и через проверку их валидности, можно было в формате request.POST.get("name")
                form = AskingForm(request.POST)
                if form.is_valid():
                    asking.name = form.cleaned_data['name']
                    asking.question_text = form.cleaned_data['question_text']
                    # start_date = form.cleaned_data['start_date']
                    asking.finish_date = form.cleaned_data['finish_date']
                    asking.save()
            else:
                # Получение конкретной записи
                res = {
                    'name': asking.name,
                    'question_text': asking.question_text,
                    'start_date': asking.start_date,
                    'finish_date': asking.finish_date
                }
                return JsonResponse(res)
    else:
        return HttpResponse('Недостаточно прав для редактирования опроса')


@login_required
def question_change(request, asking_id, question_id=None):
    """Изменение записи в БД, только для администратора"""
    if request.user.is_superuser:
        if question_id is None:
            # Создание новой записи
            form = QuestionChangeForm(request.POST)
            if form.is_valid():
                question_text = form.cleaned_data['question_text']
                answer_type = form.cleaned_data['answer_type']
                answer_choices = form.cleaned_data['answer_choices']
                question = Question(question_text=question_text,
                                     answer_type=answer_type,
                                     answer_choices=answer_choices)
                question.save()
                return HttpResponse('Вопрос успешно создан')
            return HttpResponse('Ошибка в форме')
        else:
            question = Question.objects.get(pk=question_id)
            if request.method == 'POST':
                # Изменение записи
                # тут сделано через формы и через проверку их валидности, можно было в формате request.POST.get("name")
                form = AskingForm(request.POST)
                if form.is_valid():
                    asking = AskingModel.objects.get(pk=asking_id)
                    question.asking = asking
                    question.question_text = form.cleaned_data['question_text']
                    question.answer_type = form.cleaned_data['answer_type']
                    question.answer_choices = form.cleaned_data['answer_choices']
                    question.save()
            else:
                # Получение конкретной записи
                res = {
                    'question_text': question.question_text,
                    'answer_type': question.answer_type,
                    'answer_choices': question.answer_choices,
                }
                return JsonResponse(res)
    else:
        return HttpResponse('Недостаточно прав для редактирования вопросов')