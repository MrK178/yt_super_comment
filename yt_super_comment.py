import csv
import re
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_RECENT

# ✅ 取得即時匯率
def get_exchange_rates():
    api_url = "https://api.exchangerate-api.com/v4/latest/TWD"
    try:
        response = requests.get(api_url)
        data = response.json()
        return data.get("rates", {})
    except Exception as e:
        print(f"⚠️ 無法獲取即時匯率: {e}")
        return {}

exchange_rates = get_exchange_rates()

# ✅ 貨幣對應表
currency_map = {
    "HK": "HKD", "SG": "SGD", "NT": "TWD", "US": "USD",
    "MY": "MYR", "JP": "JPY", "KR": "KRW", "CN": "CNY",
    "EU": "EUR", "ID": "IDR", "TH": "THB", "PH": "PHP",
    "AU": "AUD", "CAD": "CAD", "CHF": "CHF", "NZ": "NZD",
    "IN": "INR", "MX": "MXN", "BR": "BRL", "SEK": "SEK",
    "NOK": "NOK", "ZAR": "ZAR", "RUB": "RUB", "TRY": "TRY",
    "SAR": "SAR", "AED": "AED"
}

symbol_to_currency = {
    "£": "GBP", "€": "EUR", "¥": "JPY", "₩": "KRW",
    "₹": "INR", "₽": "RUB", "₺": "TRY", "₴": "UAH",
    "₱": "PHP", "₦": "NGN", "₡": "CRC", "₪": "ILS",
    "₫": "VND", "฿": "THB", "₭": "LAK", "₲": "PYG",
    "₵": "GHS"
}

# ✅ 初始化下載器
downloader = YoutubeCommentDownloader()
video_url = "https://youtu.be/hjcTwe5BHYI?si=voXtRrfglUWKl2mu"

# ✅ 處理留言
def process_comment(comment):
    """ 處理單條留言的函數 """
    if "paid" in comment and comment["paid"]:
        user = comment["author"]
        amount_text = comment["paid"]
        twd_local = 0
        twd_count_local = 0
        currency_totals_local = {}

        if amount_text.startswith("$"):  # 台幣
            match = re.search(r"[\d,.]+", amount_text)
            if match:
                amount_value = float(match.group().replace(",", ""))
                twd_local += amount_value
                twd_count_local += 1
        else:  # 其他貨幣
            match = re.match(r"([A-Za-z]+|[£€¥₩₹₽₺₴₱₦₡₪₫฿₭₲₵])\$?\s?([\d,]+\.?\d*)", amount_text)
            if match:
                currency_type = match.group(1)
                amount_value = float(match.group(2).replace(",", ""))
                mapped_currency = currency_map.get(currency_type, symbol_to_currency.get(currency_type, currency_type))
                if mapped_currency in exchange_rates:
                    currency_totals_local[mapped_currency] = currency_totals_local.get(mapped_currency, 0) + amount_value

        return (user, amount_text, twd_local, twd_count_local, currency_totals_local)
    return None

# ✅ **爬取留言 (多執行緒)**
print("\n🔄 正在爬取超級留言...")
start_time = time.perf_counter()

super_chats = []
twd_total = 0
twd_count = 0
currency_totals = {}

comment_generator = downloader.get_comments_from_url(video_url, sort_by=SORT_BY_RECENT)
comments = []  # 先存留言，然後用多線程處理

for index, comment in enumerate(comment_generator, 1):
    elapsed_time = int(time.perf_counter() - start_time)
    print(f"\r⏳ 已執行 {elapsed_time} 秒，已抓取 {index} 筆留言", end="", flush=True)
    
    comments.append(comment)

print("\n✅ 留言抓取完成，開始處理...")

# ✅ **使用多執行緒並行處理留言**
with ThreadPoolExecutor(max_workers=8) as executor:  # 設定 8 線程
    futures = [executor.submit(process_comment, comment) for comment in comments]

    for future in as_completed(futures):
        result = future.result()
        if result:
            user, amount_text, twd_local, twd_count_local, currency_totals_local = result
            super_chats.append((user, amount_text))
            twd_total += twd_local
            twd_count += twd_count_local
            for key, value in currency_totals_local.items():
                currency_totals[key] = currency_totals.get(key, 0) + value

elapsed_time = int(time.perf_counter() - start_time)
print(f"\n✅ 處理完成！總共用時 {elapsed_time} 秒，已處理 {len(super_chats)} 筆留言")

# ✅ **寫入 CSV**
csv_filename = "super_chat_data.csv"
with open(csv_filename, "w", newline="", encoding="utf-8-sig") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["用戶名", "超級留言金額"])
    csv_writer.writerows(super_chats)

print(f"\n📁 已將超級留言數據儲存至 {csv_filename}")

# ✅ **計算統計數據**
print("\n🔄 計算中... 台幣部分")
print(f"\n💰 台幣計算部分: {twd_total:,.2f} TWD (總共 {twd_count} 筆，平均 {twd_total / twd_count if twd_count > 0 else 0:,.2f} TWD/筆)")

# ✅ **計算非台幣部分**
converted_twd_total = 0
print("\n🔄 計算中... 非台幣部分\n")
for currency, amount in currency_totals.items():
    if currency in exchange_rates:
        converted_twd = amount / exchange_rates[currency]
        converted_twd_total += converted_twd
        print(f"💰 {currency}: {amount:,.2f} → 換算為台幣: {converted_twd:,.2f} TWD")
    else:
        print(f"\n💰 {currency}: {amount:,.2f} (❌ 無法轉換台幣，匯率未知)")

# ✅ **顯示總金額**
print(f"\n📊 🔥 最終超級留言總金額 (TWD): {twd_total + converted_twd_total:,.2f} TWD")
print("\n✅ 計算完成！")

