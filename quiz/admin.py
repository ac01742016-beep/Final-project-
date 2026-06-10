from django.contrib import admin
from .models import Question, Choice, QuizRecord  # 🌟 新增引入 QuizRecord

# 讓選項可以直接在題目的頁面裡新增 (你之前應該有寫過類似的)
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

# 註冊到後台
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizRecord)  # 🌟 新增這行：把作答紀錄註冊到後台