import os
import re
import json
import time
import hashlib
import requests
import feedparser
from deep_translator import GoogleTranslator

# ============ SOZLAMALAR ============
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
SENT_FILE = "sent.json"
MAX_PER_RUN = 8  # bitta ishga tushishda yuboriladigan maksimal xabar soni

# Bu yerga istalgancha AI yangiliklar manbasini qo'shishingiz mumkin
# YouTube kanal qo'shish uchun:
# ("Kanal nomi", "https://www.youtube.com/feeds/videos.xml?channel_id=KANAL_ID"),
FEEDS = [
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("The Verge AI", "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml"),
    ("VentureBeat AI", "https://venturebeat.com/category/ai/feed/"),
    ("MIT Tech Review", "https://www.technologyreview.com/feed/"),
    ("Google AI Blog", "https://blog.google/technology/ai/rss/"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/technology-lab"),
    ("Two Minute Papers (YouTube)", "https://www.youtube.com/feeds/videos.xml?channel_id=UCbfYPyITQ-7l4upoX8nvctg"),
]

# ============ YORDAMCHI FUNKSIYALAR ============

def load_sent():
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, "r", encoding="utf-8") as f:
            try:
                return set(json.load(f))
            except Exception:
                return set()
    return set()


def save_sent(sent_ids):
    with open(SENT_FILE, "w", encoding="utf-8") as f:
        json.dump(list(sent_ids)[-2000:], f)  # oxirgi 2000 tasini saqlaymiz


def entry_id(entry):
    raw = entry.get("id") or entry.get("link") or entry.get("title", "")
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def translate_uz(text):
    if not text:
        return ""
    try:
        return GoogleTranslator(source="auto", target="uz").translate(text[:1500])
    except Exception as e:
        print(f"Tarjima xatosi: {e}")
        return text


def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    r = requests.post(url, data=payload, timeout=20)
    if not r.ok:
        print(f"Telegramga yuborishda xato: {r.text}")
    return r.ok


# ============ ASOSIY LOGIKA ============

def main():
    if not BOT_TOKEN or not CHAT_ID:
        raise SystemExit("TELEGRAM_BOT_TOKEN yoki TELEGRAM_CHAT_ID topilmadi! "
                          "GitHub repo Secrets bo'limiga qo'shing.")

    sent_ids = load_sent()
    new_items = []

    for source_name, url in FEEDS:
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            print(f"{source_name} o'qishda xato: {e}")
            continue

        for entry in feed.entries[:10]:
            eid = entry_id(entry)
            if eid in sent_ids:
                continue
            new_items.append((source_name, entry, eid))

    new_items = new_items[:MAX_PER_RUN]

    if not new_items:
        print("Yangi maqola topilmadi.")
        return

    for source_name, entry, eid in new_items:
        title = entry.get("title", "")
        # YouTube RSS'da tavsif media:description ichida keladi
        summary = (
            entry.get("summary", "")
            or entry.get("description", "")
            or entry.get("media_description", "")
        )
        summary_clean = re.sub("<[^<]+?>", "", summary)

        title_uz = translate_uz(title)
        summary_uz = translate_uz(summary_clean)

        link = entry.get("link", "")

        message = (
            f"🤖 <b>{title_uz}</b>\n\n"
            f"{summary_uz[:600]}\n\n"
            f"📰 Manba: {source_name}\n"
            f"🔗 {link}"
        )

        ok = send_telegram(message)
        if ok:
            sent_ids.add(eid)
            print(f"Yuborildi: {title_uz[:60]}")
        time.sleep(2)  # Telegram limitlariga hurmat

    save_sent(sent_ids)


if __name__ == "__main__":
    main()
