## 💻 環境部署與執行指南 (教授/評分者測試專用)

本專案已完成資料庫清理，確保在全新環境下可一鍵部署並完整匯入題庫。

### 第一步：環境準備
請確保已安裝 Python 3.x，並在終端機 (CMD/Terminal) 進入本專案根目錄 (與 `manage.py` 同層)。

### 第二步：一鍵部署與自動化建置
請在終端機依序執行以下指令：

```bash
# 1. 安裝必要套件
python -m pip install -r requirements.txt

# 2. 清除舊有資料庫 (若有) 並建立全新資料庫結構
python manage.py makemigrations
python manage.py migrate

# 3. 匯入題庫 (已過濾掉成績紀錄，確保匯入無外鍵衝突)
python manage.py loaddata quiz_data.json

# 4. 建立後台管理員帳號
# 執行後請依照提示設定帳號密碼
python manage.py createsuperuser

# 5. 啟動伺服器
python manage.py runserver
