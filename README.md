# Quiz Project 期末專題

本專案為一個基於 Django 框架開發的線上測驗系統。

## 💻 新環境部署與執行步驟

當你在新的電腦上下載此專案後，請務必依照以下步驟執行，才能完整還原開發環境與測驗題庫。

### 第一步：環境準備
1. 請確認新電腦已安裝 Python 3.x，且安裝時有勾選 **「Add Python to PATH」**。
2. 開啟終端機 (CMD / PowerShell / VS Code Terminal)。
3. 使用 `cd` 指令進入本專案資料夾 (必須與 `manage.py` 在同一層目錄)。

### 第二步：一鍵還原系統與題庫
請在終端機依序複製並執行以下指令。

```bash
# 1. 安裝環境套件 (使用 -m 確保 Windows 系統能正確呼叫 pip)
python -m pip install -r requirements.txt

# 2. 建立資料庫結構 (建立全新的空資料表)
python manage.py migrate

# 3. 匯入預設測驗題庫 (將原本備份的題目灌入新資料庫)
python manage.py loaddata quiz_data.json

# 4. 建立後台管理員帳號 (建立新資料庫的最高權限帳號)
python manage.py createsuperuser

# 5. 啟動伺服器
python manage.py runserver