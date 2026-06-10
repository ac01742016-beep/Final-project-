from django.shortcuts import render, redirect
from .models import Question, Choice, QuizRecord
import random
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

def home(request):
    return render(request, 'quiz/index.html')

def register_user(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
    return render(request, 'quiz/register.html', {'form': form})

def login_user(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('home')
    return render(request, 'quiz/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('home')

def take_quiz(request):
    if request.method == 'POST':
        score = 0
        results_data = []
        difficulty = request.POST.get('diff')
        
        # 修正：直接從資料庫計算該難度的總題數
        if difficulty:
            total_questions = Question.objects.filter(difficulty=difficulty).count()
        else:
            total_questions = Question.objects.count()

        for key, value in request.POST.items():
            if key.startswith('question_'):
                try:
                    q = Question.objects.get(id=int(key.split('_')[1]))
                    s_choice = Choice.objects.get(id=value)
                    is_correct = s_choice.is_correct
                    if is_correct:
                        score += 1
                    results_data.append({
                        'question': q.text,
                        'difficulty': q.get_difficulty_display(),
                        'selected': s_choice.text,
                        'correct_answer': q.choices.filter(is_correct=True).first().text,
                        'is_correct': is_correct
                    })
                except:
                    continue
        
        if request.user.is_authenticated and total_questions > 0:
            QuizRecord.objects.create(user=request.user, score=score, total_questions=total_questions, difficulty=difficulty or 'all')
            
        return render(request, 'quiz/result.html', {'score': score, 'total': total_questions, 'results_data': results_data})

    # (底下 GET 模式的代碼保持不變)
    diff = request.GET.get('diff')
    qs = list(Question.objects.filter(difficulty=diff).order_by('?') if diff else Question.objects.order_by('?'))
    for q in qs:
        choices = list(q.choices.all())
        random.shuffle(choices)
        for i, c in enumerate(choices):
            c.dynamic_letter = ['A', 'B', 'C', 'D', 'E', 'F'][i]
        q.shuffled_choices = choices
    return render(request, 'quiz/quiz.html', {'questions': qs, 'is_review': False})

def leaderboard(request):
    return render(request, 'quiz/leaderboard.html', {
        'top_records': QuizRecord.objects.order_by('-score')[:5],
        'user_records': QuizRecord.objects.filter(user=request.user).order_by('-created_at') if request.user.is_authenticated else []
    })