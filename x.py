from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from flask import Flask
from threading import Thread
import os

SCRIPT_FILE = 'script.py'

class BotState:
    def __init__(self):
        self.counter = 0
        self.first_message = None
        self.last_message = None
        self.persentase = 100

def atur(update, context):
    parameter = context.args[0]
    
    try:
        value = int(parameter)
        if value < 0 or value > 100:
            update.message.reply_text('Persentase harus berada di antara 0 hingga 100!')
            return

        context.user_data['persentase'] = value
        context.bot_data['bot_state'].persentase = value
        update.message.reply_text('Persentase telah diatur menjadi {}%'.format(value))

    except ValueError:
        update.message.reply_text('Parameter harus berupa angka!')

def lihat(update, context):
    persentase = context.bot_data['bot_state'].persentase
    update.message.reply_text('Persentase yang diatur saat ini: {}%'.format(persentase))

def buat(update, context):
    try:
        with open(SCRIPT_FILE, 'r') as file:
            script_content = file.read()
        
        update.message.reply_text(script_content)
    except FileNotFoundError:
        update.message.reply_text(f'File tidak ditemukan! \n hubungi admin untuk mendapatkan kode') # {SCRIPT_FILE}

def kirim_pesan(update, context):
    bot_state = context.bot_data.setdefault('bot_state', BotState())

    if bot_state.counter == 0:  # Jika ini pesan pertama yang diterima
        bot_state.first_message = update.message  # Simpan pesan pertama
    bot_state.counter += 1

    persentase = bot_state.persentase

    if persentase == 100:
        if bot_state.counter > 10:
            context.bot.send_message(update.effective_chat.id, bot_state.first_message.text)
            bot_state.counter = 0  # Reset counter setelah mengirim pesan

    elif persentase == 1:
        if bot_state.counter > 30:
            context.bot.send_message(update.effective_chat.id, bot_state.first_message.text)
            bot_state.counter = 0  # Reset counter setelah mengirim pesan

    elif persentase == 50:
        if bot_state.counter > 20:
            context.bot.send_message(update.effective_chat.id, bot_state.first_message.text)
            bot_state.counter = 0  # Reset counter setelah mengirim pesan

    bot_state.last_message = update.message

def stop(update, context):
    update.message.reply_text('Bot telah dihentikan.')
    os._exit(0)

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/stop')
def stop():
    os._exit(0)

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

def main():
    token = '5445531176:AAGwd6pVM-UoDrNos3R00QSlr0KuffkZLMY'
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('atur', atur))
    dispatcher.add_handler(CommandHandler('lihat', lihat))
    dispatcher.add_handler(CommandHandler('buat', buat))
    dispatcher.add_handler(CommandHandler('stop', stop))  # Menambahkan handler untuk perintah /stop
    dispatcher.add_handler(MessageHandler(Filters.text, kirim_pesan))

    updater.start_polling()

    keep_alive()

if __name__ == '__main__':
    main()
