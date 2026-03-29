import os
import threading
import telebot
from flask import Flask
from openai import OpenAI

# ==========================================
# 1. Load Environment Variables
# ==========================================
# You will paste these into your host's environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

if not BOT_TOKEN or not HF_TOKEN:
    raise ValueError("Missing environment variables. Please set BOT_TOKEN and HF_TOKEN.")

# ==========================================
# 2. Initialize Bot and OpenAI Client
# ==========================================
bot = telebot.TeleBot(BOT_TOKEN)

# Converted from your Javascript example
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

# ==========================================
# 3. Setup Flask Application
# ==========================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram Bot and Flask Server are running successfully!"

# ==========================================
# 4. Telegram Bot Message Handlers
# ==========================================
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am connected. Send me a message and I will reply using DeepSeek-R1.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Show 'typing...' status to the user
        bot.send_chat_action(message.chat.id, 'typing')
        
        # OpenAI API Call using Hugging Face router
        chat_completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1:novita",
            messages=[
                {
                    "role": "user",
                    "content": message.text, # Takes the user's prompt from Telegram
                }
            ]
        )
        
        # Extract the response text
        bot_reply = chat_completion.choices[0].message.content
        
        # Send back to Telegram
        bot.reply_to(message, bot_reply)
        
    except Exception as e:
        # Handle API errors or token limits gracefully
        bot.reply_to(message, f"An error occurred: {str(e)}")

# ==========================================
# 5. Run Both Flask and Bot
# ==========================================
def run_bot():
    # Runs the bot polling infinitely
    bot.infinity_polling()

if __name__ == "__main__":
    # Start the Telegram bot in a separate background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Start the Flask web server on the main thread
    app.run(host="0.0.0.0", port=8080)
