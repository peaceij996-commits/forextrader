import os
import asyncio
import feedparser

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# =========================
# TELEGRAM SETTINGS
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

RSS_URL = "https://www.forexfactory.com/ffcal_week_this.xml"

CHECK_INTERVAL = 60

sent_news = set()


# =========================
# GET FOREX NEWS
# =========================

def get_news():
    feed = feedparser.parse(RSS_URL)

    news_list = []

    for item in feed.entries:
        title = item.get("title", "No title")
        link = item.get("link", "")

        news_list.append({
            "title": title,
            "link": link
        })

    return news_list


# =========================
# /START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Forex News Bot!\n\n"
        "📊 I send Forex and economic news updates.\n\n"
        "Use /news to get the latest news."
    )


# =========================
# /NEWS COMMAND
# =========================

async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news = get_news()

    if not news:
        await update.message.reply_text(
            "❌ I couldn't find any Forex news right now."
        )
        return

    message = "🚨 LATEST FOREX NEWS 🚨\n\n"

    for item in news[:5]:
        message += (
            f"📰 {item['title']}\n"
            f"🔗 {item['link']}\n\n"
        )

    message += "📊 Trade carefully and manage your risk."

    await update.message.reply_text(
        message,
        disable_web_page_preview=True
    )


# =========================
# AUTOMATIC NEWS
# =========================

async def send_news(bot):
    news = get_news()

    for item in news:
        news_id = item["title"] + item["link"]

        if news_id in sent_news:
            continue

        message = (
            "🚨 FOREX NEWS UPDATE 🚨\n\n"
            f"📰 {item['title']}\n\n"
            f"🔗 {item['link']}\n\n"
            "📊 Trade carefully and manage your risk."
        )

        try:
            await bot.send_message(
                chat_id=CHAT_ID,
                text=message,
                disable_web_page_preview=True
            )

            sent_news.add(news_id)

            print("News sent:", item["title"])

        except Exception as e:
            print("Telegram error:", e)


# =========================
# BACKGROUND NEWS LOOP
# =========================

async def news_loop(application):
    while True:
        try:
            await send_news(application.bot)
        except Exception as e:
            print("News error:", e)

        await asyncio.sleep(CHECK_INTERVAL)


# =========================
# STARTUP
# =========================

async def post_init(application):
    print("================================")
    print("   FOREX NEWS BOT STARTED")
    print("================================")

    if not BOT_TOKEN:
        print("❌ BOT_TOKEN is missing!")

    if not CHAT_ID:
        print("❌ CHAT_ID is missing!")

    application.create_task(news_loop(application))


# =========================
# MAIN
# =========================

def main():

    if not BOT_TOKEN:
        print("❌ BOT_TOKEN is not set in Railway!")
        return

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("news", news_command)
    )

    print("🤖 Starting Telegram bot...")

    app.run_polling()


if __name__ == "__main__":
    main()