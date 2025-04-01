import telebot
import requests
import json
import threading
from flask import Flask

# Telegram bot token
TOKEN = "7923532245:AAGMx14E5iLuf_vgESonhL4sgN9eJAcoT6Y"
bot = telebot.TeleBot(TOKEN)

# DeepSeek API URL
API_URL = "https://deepseek.ytansh038.workers.dev/?question="

# Flask app (for status check)
app = Flask(__name__)

@app.route('/')
def home():
    return "DeepSeek Bot is Running!"

def run_flask():
    app.run(host="0.0.0.0", port=8000)

# Start message handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "🤖 *Welcome to DeepSeek Bot!*\n\n"
        "Mujhse koi bhi sawaal puchho, main tumhari madad karne ke liye hoon. 🚀\n\n"
        "📝 Bas apna question bhejo aur main jawab dunga!"
    )

# General message handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_question = message.text

    # Typing action dikhane ke liye
    bot.send_chat_action(chat_id, "typing")

    response = requests.get(API_URL + user_question)
    if response.status_code == 200:
        try:
            data = json.loads(response.text)
            answer = data.get("message", "Koi jawab nahi mila.")
        except json.JSONDecodeError:
            answer = "JSON response parse karne mein error aayi."
    else:
        answer = "API request failed. Please try again later."

    bot.send_message(chat_id, answer)

# Run Flask in a separate thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# Start polling the bot
bot.polling(none_stop=True)
