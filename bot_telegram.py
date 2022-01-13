import logging

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    Filters,
)
from telegram import Chat, bot, InlineKeyboardButton, InlineKeyboardMarkup
from config import Config
from random import uniform
from flask_template import db
from views import wm, create_payload
import json
import requests



# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    global chat_id
    """Send a message when the command /start is issued."""
    user = update.message.from_user
    chat_id = user["id"]
    update.message.reply_text("Hi! use the command /anomaly to check the anomaly in your winerys")


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")


def anomaly(update, context):

    winerys = wm.get_all_winerys()
    keyboard = []
    for winery in winerys:
        label = "Winery" + str(winery.winery_id)
        callb = str(winery.winery_id)
        btn = InlineKeyboardButton(label, callback_data=label)
        keyboard.append([btn])

    print(keyboard)
    mkp = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please choose:", reply_markup=mkp)


def winery(update, context):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    chat_id = query.from_user.id
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    query.edit_message_text(text=f"Selected winery: {query.data}")
    winery = wm.get_winery_by_id(int((query.data).replace("Winery", "")))
    print(winery)
    ids = []
    keyboard = []
    for sensor in winery.sensors:
        # mean = sum(sensor.values) / len(sensor.values)
        print(sensor.values[-1].val)
        query.from_user.send_message("Sensor {type} last value: {value}".format(type = sensor.sensor_type, value = sensor.values[-1].val))
        # update.message.reply_text('media valori sensore ', sensor.sensor_id, ': ', mean)
        if sensor.anomaly:
            id = sensor.sensor_id
            label = "Sensor" + str(id)
            callb = str(id)
            btn = InlineKeyboardButton(label, callback_data=label)
            keyboard.append([btn])
    
    if keyboard:
        keyboard.append([InlineKeyboardButton("Remove Anomalys", callback_data="rmanomaly"+str(winery.winery_id))])
        mkp = InlineKeyboardMarkup(keyboard)
        query.from_user.send_message("Oh no! there is an anomaly:", reply_markup=mkp)
    
def anomaly_sensor(update, context):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    chat_id = query.from_user.id
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    query.edit_message_text(text=f"Selected anomaly on sensor: {query.data}")
    id = int((query.data).replace("Sensor", ""))
    query.from_user.bot.send_photo(chat_id = query.from_user.id, photo=open(f"./static/img/Future Values {query.data}.png",'rb'))
    sensor = wm.get_senor_by_id(id)
    keyboard = [
        [InlineKeyboardButton("Return to Winery", callback_data="Winery"+str(sensor.winery_id))]
    ]
    mkp = InlineKeyboardMarkup(keyboard)
    query.from_user.send_message('Choose Action:',reply_markup=mkp)
    

def remove_anomaly(update, context):
    query = update.callback_query
    
    id = int((query.data).replace("rmanomaly", ""))
    winery_id = id
    
    url = Config.BASE_URL+'/remove_anomalys'
    myobj = {
        'winery_id': winery_id
    }
    x = requests.post(url, data = myobj)
    query.edit_message_text(text=f"Removed all the anomalies on winery: {winery_id}")            
            
def startBot():
    """Start the bot."""
    updater = Updater(Config.BOTKEY, use_context=True)

    # Get the dispatcher to register handlers  (callbacks)
    dp = updater.dispatcher

    # add an handler for each command
    # start and help are usually defined
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("anomaly", anomaly))
    
    updater.dispatcher.add_handler(CallbackQueryHandler(winery, pattern = "^Winery"))
    updater.dispatcher.add_handler(CallbackQueryHandler(anomaly_sensor,pattern = "^Sensor"))
    updater.dispatcher.add_handler(CallbackQueryHandler(remove_anomaly,pattern = "^rmanomaly"))
    # Start the Bot (polling of messages)
    # this call is non-blocking
    updater.start_polling()
    updater.idle()
