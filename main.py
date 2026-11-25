import os
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from google import genai

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

ai = genai.Client(api_key=GEMINI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سڵاو! من Shblood AI ـم. چ پرسیارێکت هەیە؟"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text

    try:
        response = ai.models.generate_content(
            model="gemini-2.5-flash",
            contents=question
        )

        await update.message.reply_text(
            response.text or "هیچ وەڵامێک نەدۆزرایەوە."
        )

    except Exception:
        await update.message.reply_text(
            "هەڵەیەک ڕوویدا، دووبارە هەوڵ بدەرەوە."
        )

async def main():
    app = Application.builder().token(
        os.getenv("BOT_TOKEN")
    ).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
