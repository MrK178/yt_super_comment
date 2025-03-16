# 🎯 YouTube SuperChat 分析工具

這是一個 Python 爬蟲工具，可以爬取 YouTube 影片的**超級留言（Super Chat）**，並計算各種貨幣的金額。

---

## 📥 安裝與執行方式

### **1️⃣ 安裝 Python**

請確認你的系統已安裝 Python（建議 3.8+），在終端機輸入：

```bash
python --version
```

### **2️⃣ 安裝必要套件**

執行以下指令安裝 `requests` 和 `youtube_comment_downloader`：

```bash
pip install requests youtube_comment_downloader
```

### **3️⃣ 執行程式**

```bash
python yt_super_comment.py
```

🔗 **GitHub 倉庫**：[點我查看](https://github.com/MrK178/yt_super_comment)

---

## 📌 主要功能

- 🔍 **自動下載** YouTube 影片的超級留言（Super Chat）。
- 💰 **支援貨幣轉換**，可自動將金額換算為台幣（TWD）。
- ⚡ **多執行緒處理**，提高留言處理速度。
- 📊 **輸出 CSV 檔案**，方便後續數據分析。

---

## 📊 資料輸出

- **`super_chat_data.csv`**：包含所有超級留言的數據。
- **終端機輸出**：
  - 顯示不同貨幣的超級留言金額，並換算為台幣 (TWD)。

🔗 **匯率 API**：[ExchangeRate-API](https://www.exchangerate-api.com/)

---

## 🛠 可能遇到的問題

### ❌ 1. `requests.exceptions.ConnectionError`

🔹 可能是網路問題，請檢查你的網路連線或稍後再試。

### ❌ 2. `youtube_comment_downloader` 無法安裝

🔹 請確保你的 Python 版本為 3.8 以上，並嘗試執行：

```bash
pip install --upgrade pip
pip install youtube_comment_downloader
```

### ❌ 3. 匯率 API 失效

🔹 預設使用 `ExchangeRate-API`，如果無法獲取匯率，可嘗試手動更新 `exchange_rates` 變數。

🔗 **使用的爬蟲工具**：[youtube-comment-downloader](https://github.com/egbertbouman/youtube-comment-downloader)

---

## 🎉 作者

開發者：[@MrK178](https://github.com/MrK178)  
聯絡方式：[Threads @k.aicash](https://www.threads.net/@k.aicash)

🚀 如果你覺得這個工具有幫助，請記得點個 ⭐ **Star** 支持這個專案！
