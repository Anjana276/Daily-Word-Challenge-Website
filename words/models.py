from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DailyWord(models.Model):
    word = models.CharField(max_length=100)
    meaning = models.TextField(blank=True, null=True)
    phonetic = models.CharField(max_length=100, blank=True, null=True)
    audio = models.URLField(blank=True, null=True)
    example = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.word} - {self.date}"

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(DailyWord, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.word.word} - {self.completed}"


class LearnedWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    definition = models.TextField(blank=True)
    example = models.TextField(blank=True)
    date_learned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.word} - {self.user.username}"
    

class QuizScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    date_taken = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.score}/{self.total}"

class Streak(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_quiz_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Streak"


class LearnedWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    level = models.CharField(max_length=20, default='beginner')  # <-- ADD THIS
    definition = models.TextField(blank=True)
    example = models.TextField(blank=True)
    date_learned = models.DateTimeField(auto_now_add=True)

