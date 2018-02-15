from typing import Optional, List

from telegram import Message, Update, Bot
from telegram import ParseMode, MAX_MESSAGE_LENGTH
from telegram.ext import CommandHandler, MessageHandler, DispatcherHandlerStop, run_async, Filters
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import escape_markdown

import tg_bot.modules.sql.logger_sql as sql
from tg_bot import dispatcher
from tg_bot.modules.helper_funcs.extraction import extract_user

from time import strftime

@run_async
def logger(bot: Bot, update: Update):
    """Primary Logger. Handles incoming bot messages and saves them to DB"""
    try:
    
        user = update.message.from_user
        
        if sql.id_exists(user.id) == True:
            sql.log_message(user.id, update.message.text)
            print("message logged: ")
        
        
        else:
            
            add_user_success = sql.add_user(user.id, user.first_name, user.last_name, user.username)
            
            if add_user_success == True:
                print("User added: {}".format(user.id))
                sql.log_message(user.id, update.message.text)
                print("message logged: ")
            else:
                print("Something went wrong adding the user {}".format(user.id), file=sys.stderr)
    
        
        if update.message.text:
            print("{} {} ({}) : {}".format(
                strftime("%Y-%m-%dT%H:%M:%S"),
                user.id,
                (user.username or (user.first_name + " " + user.last_name) or "").encode('utf-8'),
                update.message.text.encode('utf-8'))
            )
    
    except Exception as e:
        print(e)

__help__ = """
  Logging all messages sent in the public group.
"""

__name__ = "Logger"

LOG_HANDLER = MessageHandler(Filters.text, logger)

dispatcher.add_handler(LOG_HANDLER)
