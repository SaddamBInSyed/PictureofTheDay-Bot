# Python-telegram-bot libraries
import telegram
from telegram.ext import Updater, CommandHandler

# Logging and requests libraries
import logging
import requests

# Importing the Updater object with token for updates from Telegram API
# Declaring the Dispatcher object to send information to user
# Creating the bot variable and adding our token
updater = Updater(token = 'TOKEN')
dispatcher = updater.dispatcher
bot = telegram.Bot(token = 'TOKEN')

# Logging module for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# NASA API
nasa_api_key = 'API KEY'
nasa_url = 'https://api.nasa.gov/planetary/apod?api_key={}'.format(nasa_api_key)
nasa_data = requests.get(nasa_url).json()

# JSON variables
title = nasa_data['title']
explanation = nasa_data['explanation']

# '/start' command
def start(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text = "Hello there! Thank you for starting me! Use the /picture command to see today's NASA image of the day!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# '/picture' command
def pictureoftheday_message(bot, update):
    if 'image' in nasa_data['media_type']:
        image = nasa_data['hdurl']
        bot.send_message(chat_id = update.message.chat_id, text = title)
        bot.send_message(chat_id = update.message.chat_id, text = image)
        bot.send_message(chat_id = update.message.chat_id, text = explanation)
    elif 'video' in nasa_data['media_type']:
        video = nasa_data['url']
        bot.send_message(chat_id = update.message.chat_id, text = title)
        bot.send_message(chat_id = update.message.chat_id, text = video)
        bot.send_message(chat_id = update.message.chat_id, text = explanation)
    else:
        bot.send_message(chat_id = update.message.chat_id, text = "Sorry, I couldn't deliver the image / video! An error occured!")

pictureoftheday_message_handler = CommandHandler('picture', pictureoftheday_message)
dispatcher.add_handler(pictureoftheday_message_handler)

# Module to start getting data
updater.start_polling()
updater.idle()