import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

SYSTEM_PROMPT = """
You are an Arabic language tutor.
Teach Arabic step by step.
Always provide:
- Arabic word with harakat
- pronunciation
- Russian meaning
- example sentence
Keep answers simple and short.
"""

def ask_ai(text):
    url = "https://api.deepseek.com/chat/completions"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "temperature": 0.7
    }

    res = requests.post(url, json=data, headers=headers)
    return res.json()["choices"][0]["message"]["content"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🇸🇦 Arabic AI Tutor is ready!\nНапиши: урок / слово / переведи"
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    answer = ask_ai(user_text)
    await update.message.reply_text(answer)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    app.run_polling()

if __name__ == "__main__":
    main()