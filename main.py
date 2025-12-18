import telebot
import re
import os

# We use an Environment Variable for the token (for security)
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

def process_text(text):
    ifsc_pattern = r'[A-Z]{4}0[A-Z0-9]{6}'
    acc_pattern = r'\b\d{9,18}\b'
    
    ifscs = re.findall(ifsc_pattern, text.upper())
    accounts = re.findall(acc_pattern, text)
    
    output = []
    if ifscs or accounts:
        for acc in accounts:
            output.append(f"💰 Account:\n`{acc}`")
        for ifsc in ifscs:
            output.append(f"🏦 IFSC:\n`{ifsc}`")
    
    output.append("--- Tap to copy line ---")
    for line in text.split('\n'):
        if line.strip():
            output.append(f"`{line.strip()}`")
                
    return "\n\n".join(output)

@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    result = process_text(message.text)
    bot.reply_to(message, result, parse_mode='Markdown')

bot.infinity_polling()