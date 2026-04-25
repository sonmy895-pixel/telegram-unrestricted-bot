import os
import telebot
from openai import OpenAI

# 1. Environment Variables nikalna
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# 2. Bot aur AI Client setup
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = OpenAI(
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
)

# 3. Start Command
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Main zinda hoon! Kuch bhi poocho.")

# 4. Messages handle karna
@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# 5. Bot chalu karna
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
    
