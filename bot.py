import os
import sqlite3
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Render এর জন্য Flask সার্ভার (যাতে বট স্লিপ না হয়)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# আপনার কনফিগারেশন
TOKEN = os.getenv('BOT_TOKEN') # Render এর Environment Variable থেকে নিবে
CHANNEL_ID = -1003802624784 

def init_db():
    conn = sqlite3.connect('storage.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS files 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, file_id TEXT)''')
    conn.commit()
    conn.close()

# বাকি আগের কোডটুকু (start, handle_docs, handle_search) এখানে বসবে...
# (সংক্ষিপ্ত করার জন্য আগের লজিক অপরিবর্তিত রাখা হয়েছে)

def main():
    init_db()
    keep_alive() # সার্ভার চালু করা
    
    application = Application.builder().token(TOKEN).build()
    
    # হ্যান্ডলার অ্যাড করুন (আগের কোডের মতো)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ATTACHMENT, handle_docs))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_search))

    print("বটটি রেন্ডারে চলছে...")
    application.run_polling()

if __name__ == '__main__':
    main()
