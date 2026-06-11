import json

# 讀取原本的包裹
with open('quiz_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 只保留題目(Question)和選項(Choice)，把成績紀錄(quizrecord)踢掉
clean_data = [item for item in data if item['model'] != 'quiz.quizrecord']

# 把乾淨的資料存回包裹裡
with open('quiz_data.json', 'w', encoding='utf-8') as f:
    json.dump(clean_data, f, indent=4, ensure_ascii=False)

print("🎉 毒瘤已清除！現在包裹裡只剩純題庫了！")
