import os
import requests
from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from main import MakeVideos

token = "1833415580:AAFeqCeMjhSdlGbNV7BgtSGBYsAV5mYBaQA"
bot = Bot(token)
images = ['png', 'jpg', 'jpeg']


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


def from_url(update, context):
    command = update.message.text
    if len(command.split(' ')) == 2 and command.split(' ')[1].split('?')[0].split('.')[-1] in images:
        url = command.split(' ')[1]
        data = requests.get(url)
        if data.status_code == 200:
            filename = f'{update.message.from_user.id}.{command.split(" ")[1].split("?")[0].split(".")[-1]}'
            with open(filename, 'wb') as f:
                f.write(data.content)
            vid = MakeVideos(filename)
            files = vid.create()
            z = 3
            for i in files:
                bot.send_video(update.message.chat_id, open(i, 'rb'), caption=f'Выкладывать {z}')
                z -= 1
                os.remove(i)
            os.remove(filename)
            return 0
    update.message.reply_text('По ссылке не находится изображение! Либо невозможно определить его тип!')


if __name__ == '__main__':
    updater = Updater(token)
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, make_videos, run_async=True))
    updater.dispatcher.add_handler(CommandHandler('start', start, run_async=True))
    updater.dispatcher.add_handler(CommandHandler('from_url', from_url, run_async=True))
    updater.start_polling()
