from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    DIFFICULTY_CHOICES = [('easy', '🟢 簡單'), ('medium', '🟡 中等'), ('hard', '🔴 困難')]
    text = models.CharField(max_length=500, verbose_name="題目內容")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    def __str__(self): return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

class QuizRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    difficulty = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)