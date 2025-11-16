from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
import random
import os
import json
import requests
from django.conf import settings
from .models import LearnedWord
from django.utils import timezone
from .models import QuizScore, Streak
from datetime import date, timedelta




def get_random_word_from_level(level):
    file_path = os.path.join(os.path.dirname(__file__), 'data', f'{level}.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file if line.strip()]
    return random.choice(words)


@login_required
def daily_word_view(request):
    level = request.GET.get('level', 'beginner')  # default level = beginner
    word = get_random_word_from_level(level)
    word = word.strip().encode("ascii", "ignore").decode("ascii")
    # Fetch data from Dictionary API
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    if response.status_code == 200:
        try:
            word_data = response.json()[0]
        except (ValueError, IndexError):
            word_data={}
    

    # Check if quiz should be shown
    learned_count = LearnedWord.objects.filter(user=request.user).count()
    show_quiz = learned_count >= 5 and learned_count % 5 == 0
    streak = Streak.objects.filter(user=request.user).first()
    return render(request, 'words/daily_word.html', {
        'word': word,
        'word_data': word_data,
        'level': level,
        'show_quiz': show_quiz,
        'streak': streak
    })


def level_select(request):
    if request.method == 'POST':
        level = request.POST.get('level')
        return redirect(f'/daily-word/?level={level}')  # Go to daily_word_view with level
    return render(request, 'words/level_select.html')



def load_word_data(level):
    file_path = os.path.join(settings.BASE_DIR, 'words', 'data', f'{level}.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            words = [line.strip() for line in file if line.strip()]
            return random.choice(words) if words else None
    except FileNotFoundError:
        return None

    
   

@login_required
def mark_as_learned(request):
    if request.method == 'POST':
        word = request.POST.get('word', '').strip().lower()
        definition = request.POST.get('definition', '')
        example = request.POST.get('example', '')
        level = request.POST.get('level', 'beginner')  # <-- 💥 Get the actual level!

        LearnedWord.objects.create(
            user=request.user,
            word=word,
            level=level,  # <-- 💥 Save correct level!
            definition=definition,
            example=example
        )

        learned_count = LearnedWord.objects.filter(user=request.user).count()
        if learned_count >= 5 and learned_count % 5 == 0:
            return redirect('quiz')

        return redirect('learned_words')
    
    return redirect('daily_word')


@login_required
def learned_words(request):
    words = LearnedWord.objects.filter(user=request.user).order_by('-date_learned')
    return render(request, 'words/learned_words.html', {'words': words})


@login_required
def progress_view(request):
    user = request.user
    progress_data = {}

    levels = ['beginner', 'intermediate', 'expert']
    for level in levels:
        total_words = get_total_words_from_file(level)
        learned_words = LearnedWord.objects.filter(user=user, level=level).count()

        progress = (learned_words / total_words) * 100 if total_words > 0 else 0

        progress_data[level] = {
            'learned_count': learned_words,
            'total_words': total_words,
            'progress': round(progress)
        }

    return render(request, 'words/progress.html', {'progress_data': progress_data})



@login_required
def quiz_view(request):
    user = request.user
    learned_words = list(LearnedWord.objects.filter(user=user).order_by('-date_learned'))

    if request.method == 'POST':
        score = 0
        total = int(request.POST.get('total', 0))
        for i in range(1, total + 1):
            selected = request.POST.get(f'q{i}')
            correct = request.POST.get(f'correct{i}')
            if selected == correct:
                score += 1

        QuizScore.objects.create(user=user, score=score, total=total)

        # Handle streak logic
        today = date.today()
        streak, _ = Streak.objects.get_or_create(user=user)
        if streak.last_quiz_date == today - timedelta(days=1):
            streak.current_streak += 1
        elif streak.last_quiz_date != today:
            streak.current_streak = 1  # reset if missed

        streak.last_quiz_date = today
        if streak.current_streak > streak.longest_streak:
            streak.longest_streak = streak.current_streak
        streak.save()

        return redirect('quiz_result')

    # Build quiz data with real wrong definitions
    quiz_data = []
    for i, word in enumerate(learned_words[:5]):  # limit to 5 questions
        correct = word.definition
        # Pick 3 random wrong definitions from other words
        wrong_defs = [w.definition for j, w in enumerate(learned_words) if j != i and w.definition != correct]
        random.shuffle(wrong_defs)
        wrong_options = wrong_defs[:3] if len(wrong_defs) >= 3 else ["Wrong 1", "Wrong 2", "Wrong 3"]

        options = wrong_options + [correct]
        random.shuffle(options)

        quiz_data.append({
            'word': word.word,
            'correct': correct,
            'options': options
        })

    return render(request, 'words/quiz.html', {
        'quiz_data': quiz_data,
        'total': len(quiz_data)
    })


@login_required
def quiz_result(request):
    latest_score = QuizScore.objects.filter(user=request.user).last()
    return render(request, 'words/quiz_result.html', {'score': latest_score})


def get_total_words_from_file(level):
    path = os.path.join(settings.BASE_DIR, 'words', 'data', f'{level}.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return len([line for line in f if line.strip()])
    except:
        return 0
