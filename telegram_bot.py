import os

from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from main import MakeVideos

token = "1833415580:AAFeqCeMjhSdlGbNV7BgtSGBYsAV5mYBaQA"
bot = Bot(token)


def make_videos(update, context):
    file = update.message.photo[-1].get_file()
    filename = f"{file['file_id']}.{file['file_path'].split('.')[-1]}"
    file.download(f'./{filename}')
    vid = MakeVideos(filename)
    files = vid.create()
    z = 3
    for i in files:
        bot.send_video(update.message.chat_id, open(i, 'rb'), caption=f'Выкладывать {z}')
        z -= 1
        os.remove(i)
    os.remove(f'./{filename}')


def start(update, context):
    update.message.reply_text('''
    Для работы с ботом вам надо:
    1.Отправить фото
    2.Получить 3 видео
    
    Выложить в тт (Лучше всего через кнопку ПОДЕЛИТЬСЯ)
    Для лучшего результата используйте картинки 16:9''')


if __name__ == '__main__':
    updater = Updater(token)
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, make_videos, run_async=True))
    updater.dispatcher.add_handler(CommandHandler('start', start, run_async=True))
    updater.start_polling()
