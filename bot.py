import asyncio
import feedparser
from telegram import Bot

# =========================
# TELEGRAM SETTINGS
# =========================

BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"
CHAT_ID = "PASTE_YOUR_CHAT_ID_HERE"

# Forex/economic news RSS feed
RSS_URL = "https://www.forexfactory.com/ffcal_week_this.xml"

# How often to check for news (seconds)
CHECK_INTERVAL = 60

# Remember news already sent
sent_news = set()


# =========================
# GET NEWS
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
# SEND NEWS
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
# MAIN BOT
# =========================

async def main():

    bot = Bot(token=BOT_TOKEN)

    print("================================")
    print("   FOREX NEWS BOT STARTED")
    print("================================")

    while True:

        try:
            await send_news(bot)

        except Exception as e:
            print("Error:", e)

        await asyncio.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())