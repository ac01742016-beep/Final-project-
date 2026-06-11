from django.shortcuts import render, redirect
from .models import Question, Choice, QuizRecord, UserQuizState # 確保匯入了 UserQuizState
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
        num_questions = int(request.POST.get('num_questions', 5))
        
        for key, value in request.POST.items():
            if key.startswith('question_'):
                try:
                    q = Question.objects.get(id=int(key.split('_')[1]))
                    s_choice = Choice.objects.get(id=value)
                    is_correct = s_choice.is_correct
                    
                    if is_correct:
                        score += 1
                        # 若答對且有記錄，可選標記為精通
                        if request.user.is_authenticated:
                            state = UserQuizState.objects.filter(user=request.user, question=q).first()
                            if state:
                                state.is_mastered = True
                                state.save()
                    else:
                        if request.user.is_authenticated:
                            state, created = UserQuizState.objects.get_or_create(user=request.user, question=q)
                            state.error_count += 1
                            state.is_mastered = False
                            state.save()
                    
                    results_data.append({
                        'question': q.text,
                        'difficulty': q.get_difficulty_display(),
                        'selected': s_choice.text,
                        'correct_answer': q.choices.filter(is_correct=True).first().text,
                        'is_correct': is_correct
                    })
                except: continue
        
        if request.user.is_authenticated:
            QuizRecord.objects.create(user=request.user, score=score, total_questions=num_questions, difficulty=difficulty or 'all')
            
        return render(request, 'quiz/result.html', {'score': score, 'total': num_questions, 'results_data': results_data})

    # GET 模式
    diff = request.GET.get('diff')
    num_questions = int(request.GET.get('num_questions', 5))
    
    if request.user.is_authenticated:
        # 優先抓錯題
        wrong_qs = Question.objects.filter(userquizstate__user=request.user, userquizstate__is_mastered=False)
        others = Question.objects.exclude(id__in=wrong_qs.values_list('id', flat=True))
        if diff:
            wrong_qs = wrong_qs.filter(difficulty=diff)
            others = others.filter(difficulty=diff)
        qs = list(wrong_qs) + list(others)
    else:
        qs_all = Question.objects.filter(difficulty=diff) if diff else Question.objects.all()
        qs = list(qs_all)
    
    # 隨機抽取
    random.shuffle(qs)
    qs = qs[:num_questions]
    
    for q in qs:
        choices = list(q.choices.all())
        random.shuffle(choices)
        for i, c in enumerate(choices):
            c.dynamic_letter = ['A', 'B', 'C', 'D', 'E', 'F'][i]
        q.shuffled_choices = choices
        
    return render(request, 'quiz/quiz.html', {'questions': qs, 'is_review': False, 'num_questions': num_questions})

def leaderboard(request):
    return render(request, 'quiz/leaderboard.html', {
        'top_records': QuizRecord.objects.order_by('-score')[:5],
        'user_records': QuizRecord.objects.filter(user=request.user).order_by('-created_at') if request.user.is_authenticated else []
    })
