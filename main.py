import os
import telebot
from openai import OpenAI
from flask import Flask

# 1. API Setup (Aapka Hugging Face wala logic)
# Note: HF_TOKEN ko environment variable mein rakhna best hai
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ.get("HF_TOKEN") # Render ke Environment settings mein HF_TOKEN daal dena
)

bot = telebot.TeleBot(os.environ.get("BOT_TOKEN")) # Aapka Telegram Bot Token
app = Flask(__name__)

# 2. AUTO-REPLY KEYWORDS (Yahan naye words add kar sakte hain)
AUTO_REPLIES = {
    "hello": "Hello! Kaise hain aap? Main connected hoon. 😊",
    "kaise ho": "Main ekdum badiya! Aap bataiye?",
    "rcb": "Royal Challengers Bangalore! Ee Sala Cup Namde! ❤️🔥",
    "help": "Main keywords par turant jawab deta hoon aur baki sawalon ke liye DeepSeek-R1 use karta hoon."
}

@app.route('/')
def home():
    return "Telegram Bot and Flask Server are running successfully!"

# 3. TELEGRAM MESSAGE HANDLER
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am connected. Send me a message and I will reply using DeepSeek-R1.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Aapka promotion message
        promo_text = (
            "<b>Dost, message ke liye shukriya!</b> 🙏\n\n"
            "Aise hi aur amazing updates ke liye mere <b>YouTube Channel</b> ko subscribe zaroor karein:\n"
            "👉 <a href='https://youtube.com/shorts/dADjy9G1RKI?si=lvI7bCpVFuIQSzwc'>Yahan Click Karein</a>"
        )
        
        # Bot reply karega (HTML mode use kiya hai taaki link kaam kare)
        bot.reply_to(message, promo_text, parse_mode='HTML', disable_web_page_preview=False)
        
    except Exception as e:
        print(f"Error aaya hai: {e}")
        
        bot.reply_to(message, "Thoda wait karein, AI abhi busy hai.")

# Bot ko start karne ke liye
if __name__ == "__main__":
    # Render ke liye Flask server background mein chalega
    from threading import Thread
    def run():
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    
    Thread(target=run).start()
    print("Bot is polling...")
    bot.infinity_polling()
