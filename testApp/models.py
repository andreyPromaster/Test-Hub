from django.contrib.auth.models import User
from django.db import models


class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    description = models.TextField(verbose_name="Описание теста", blank=True)
    name = models.CharField(max_length=60, verbose_name="Название теста")
    passing_grade = models.PositiveSmallIntegerField(verbose_name="Проходной балл")
    time_limit = models.DurationField(verbose_name="Ограничения по времени", null=True)
    start_datetime = models.DateTimeField(verbose_name="Время начала теста", null=True)
    end_datetime = models.DateTimeField(verbose_name="Время закрытия теста", null=True)


class Tag(models.Model):
    quiz = models.ManyToManyField(Quiz, related_name="tags", related_query_name="tag")
    name = models.CharField(max_length=50, verbose_name="Название тэга")


class Question(models.Model):
    ONE_ANSWER = 'OA'
    SOME_ANSWERS = "SA"
    NUMBER_INPUT = "NI"
    TEXT_INPUT = "TI"

    TYPE_OF_QUESTION = [
        (ONE_ANSWER, 'one_answer'),
        (SOME_ANSWERS, 'some_answers'),
        (NUMBER_INPUT, 'number_input'),
        (TEXT_INPUT, 'text_input'),
    ]

    type_of_question = models.CharField(max_length=2, choices=TYPE_OF_QUESTION)
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    explanation = models.TextField(verbose_name="Пояснение вопроса")
    points_for_the_right_answer = models.PositiveSmallIntegerField(verbose_name="Баллы за правильный ответ")


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255, verbose_name="Ответ")
    is_correct = models.BooleanField(verbose_name="Корректность", default=False)

    def __str__(self):
        return self.text


class Result(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


class StudentAnswer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
    taken_quiz = models.ForeignKey(Result, on_delete=models.CASCADE,
                                   related_name='taken_quiz_answers',
                                   null=True)