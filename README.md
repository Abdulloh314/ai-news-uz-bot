# AI Yangiliklar Boti (O'zbek tilida, Telegram)

Bu bot AI haqidagi yangiliklarni bir nechta manbalardan o'qiydi, o'zbek tiliga
tarjima qiladi va Telegram orqali sizga avtomatik yuboradi. Har 15 daqiqada
ishlaydi va to'liq bepul (GitHub Actions + Telegram Bot API).

## 1-qadam: Telegram bot yaratish

1. Telegramda **@BotFather** ga yozing
2. `/newbot` buyrug'ini yuboring va ko'rsatmalarga amal qiling
3. Sizga bot **TOKEN** beradi (masalan: `123456789:ABCdefGhIJKlmNoPQRstuVwXyZ`) — uni saqlab qo'ying

## 2-qadam: Chat ID olish

1. Yangi yaratgan botingizga Telegramda `/start` deb yozing
2. Brauzerda quyidagi manzilni oching (TOKEN o'rniga o'zingiznikini qo'ying):
   `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Natijada `"chat":{"id": 123456789` qatorini topasiz — shu raqam sizning **CHAT_ID**ingiz

*(Agar shaxsiy chatga emas, guruhga yubormoqchi bo'lsangiz, botni guruhga qo'shing va shu usulni takrorlang)*

## 3-qadam: GitHub repo yaratish

1. github.com da yangi **public** repository yarating (public bo'lsa Actions butunlay bepul va cheksiz)
2. Ushbu papkadagi barcha fayllarni (`main.py`, `requirements.txt`, `sent.json`, `.github/workflows/ai_news.yml`) repo ichiga yuklang — papka tuzilishini saqlang

## 4-qadam: Maxfiy kalitlarni qo'shish

1. Repo ichida: **Settings → Secrets and variables → Actions → New repository secret**
2. Quyidagi ikkita secret qo'shing:
   - `TELEGRAM_BOT_TOKEN` → BotFather bergan token
   - `TELEGRAM_CHAT_ID` → 2-qadamda topgan raqam

## 5-qadam: Ishga tushirish

- Workflow avtomatik ravishda har 15 daqiqada ishlay boshlaydi
- Tezroq tekshirish uchun: repo ichida **Actions** tab → **AI News UZ Bot** → **Run workflow** tugmasini bosing

## Sozlash

- `main.py` ichidagi `FEEDS` ro'yxatiga istalgan RSS manba qo'shishingiz yoki olib tashlashingiz mumkin
- `MAX_PER_RUN` — bitta ishga tushishda nechta xabar yuborilishini belgilaydi
- Cron jadvalini (`*/15 * * * *`) `.github/workflows/ai_news.yml` faylida o'zgartirib, tezligini sozlash mumkin (lekin 5 daqiqadan tezroq qilish tavsiya etilmaydi)

## Bilib qo'ying

- To'liq "real vaqt" emas, balki ~15 daqiqalik kechikish bilan ishlaydi — chunki bu butunlay bepul yechim
- Tarjima sifati yaxshi, lekin professional tarjimondek mukammal emas
- Agar maqolalar soni juda ko'p bo'lsa, Google Translate vaqtinchalik bloklashi mumkin — shu sababli `MAX_PER_RUN` cheklovi qo'yilgan
