from django.db import models
from django.contrib.auth.models import User

# TEXT_CHOISE = 0
# ONE_CHOICE = 1
# MANY_CHOICES = 2


class AskingModel(models.Model):
    # Таблица опросов
    name = models.CharField(max_length=60)
    question_text = models.CharField('description', max_length=500)
    start_date = models.DateTimeField('date start')
    finish_date = models.DateTimeField('date finish')


class Question(models.Model):
    # Таблица вопросов, внешним ключом связана с опросами один-ко многим
    # Я бы сделал через noSQL JSON поле в таблице вопросов (проще расширять), но это для postgreSQL только
    # Поэтому чтобы не плодить таблицы сделал текстовое поле, сериализацию в JSON буду проводить отдельно
    ANSWER_CHOICES = (
        (1, 'Текст'),
        (2, 'Один вариант'),
        (3, 'Несколько вариантов'),
    )
    asking = models.ForeignKey(AskingModel, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    answer_type = models.IntegerField(default=1, choices=ANSWER_CHOICES)
    answer_choices = models.CharField(max_length=500, blank=True, default="")


class UserAskings(models.Model):
    # сводная таблица по опросникам
    asking = models.ForeignKey(AskingModel, on_delete=models.SET_NULL, null=True)
    is_finished = models.BooleanField(default=False)
    userid = models.ForeignKey(User, related_name="askings_assignedto", on_delete=models.CASCADE)


class UserAnswers(models.Model):
    # таблица ответов пользователя. Аналогично сделал бы через JSON, но для универсальности добавил булевое поле
    userid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    asking = models.ForeignKey(AskingModel, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    answer_text = models.CharField(max_length=200)
    answer_is_json = models.BooleanField(default=False)
