import os
import telebot
from openai import OpenAI
from threading import Thread

# Environment Variables
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Bot setup
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=OPENROUTER_API_KEY)

# Render ka Port error hatane ke liye chota sa server
from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello(): return "Bot is Running"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Main zinda hoon! Kuch bhi poocho.")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-exp:free",
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

if __name__ == "__main__":
    # Flask ko background mein chalana
    Thread(target=run_flask).start()
    print("Bot is starting...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
