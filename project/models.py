import random
import string
import uuid

from django.utils import timezone
from django.conf import settings
from django.db import models


class Pupil(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, editable=False)
    full_name = models.CharField(max_length=512)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs) -> None:
        if self.pk is None:
            self.id = self.generate_unique_username()
            self.password = '000000'
        super().save(*args, **kwargs)

    def generate_unique_username(self):
        while True:
            id = random.randint(10000, 99999)
            if not Pupil.objects.filter(pk=id).exists():
                return id

    def __str__(self) -> str:
        return self.full_name

class Token(models.Model):
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pupil = models.OneToOneField(Pupil, related_name='auth_token', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Exam(models.Model):
    title = models.CharField(max_length=1024)
    duration = models.IntegerField()
    code = models.CharField(max_length=6, unique=True, editable=False)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not Exam.objects.filter(code=code).exists():
                return code

    def __str__(self):
        return f"Exam {self.id} - Code: {self.code} - Duration: {self.duration} mins"

class Test(models.Model):
    exam = models.ForeignKey(Exam, related_name='tests', on_delete=models.CASCADE)
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.question

class Answer(models.Model):
    test = models.ForeignKey(Test, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class AnswerSheet(models.Model):
    pupil = models.ForeignKey(Pupil, related_name='answer_sheets', on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, related_name='answer_sheets', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.pupil.full_name} - {self.exam.title}"

    @property
    def computed_percentage(self):
        tests_count = self.exam.tests.count()
        correct_answers_count = len([x for x in self.answers.all() if x.is_correct])
        return (correct_answers_count / tests_count) * 100 if tests_count > 0 else 0

    @computed_percentage.setter
    def computed_percentage(self, value):
        self.save()
    
class PupilAnswer(models.Model):
    answer_sheet = models.ForeignKey(AnswerSheet, related_name='answers', on_delete=models.CASCADE)
    test = models.ForeignKey(Test, related_name='answer_sheets', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name='answer_sheets', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        
        self.is_correct = self.answer.is_correct and self.test == self.answer.test
        
        return super().save(*args, **kwargs)
