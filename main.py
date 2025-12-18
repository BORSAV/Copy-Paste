import telebot
import re
import os
from flask import Flask
from threading import Thread

# 1. CREATE A TINY WEB SERVER
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

# 2. START THE BOT LOGIC
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

def process_text(text):
    # (Your existing logic for IFSC/Account numbers)
    ifsc_pattern = r'[A-Z]{4}0[A-Z0-9]{6}'
    acc_pattern = r'\b\d{9,18}\b'
    ifscs = re.findall(ifsc_pattern, text.upper())
    accounts = re.findall(acc_pattern, text)
    output = []
    if ifscs or accounts:
        for acc in accounts: output.append(f"💰 Account:\n`{acc}`")
        for ifsc in ifscs: output.append(f"🏦 IFSC:\n`{ifsc}`")
    output.append("--- Tap to copy line ---")
    for line in text.split('\n'):
        if line.strip(): output.append(f"`{line.strip()}`")
    return "\n\n".join(output)

@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    result = process_text(message.text)
    bot.reply_to(message, result, parse_mode='Markdown')

# 3. RUN BOTH AT THE SAME TIME
if __name__ == "__main__":
    # Start web server in a separate thread
    t = Thread(target=run_web_server)
    t.start()
    # Start bot polling
    bot.infinity_polling()
