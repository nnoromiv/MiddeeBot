# The above code is importing the "os" module in Python. This module provides a way of using operating
# system dependent functionality like reading or writing to the file system.
import os
import time
# The above code is importing the `telebot` module in Python. This module is used to create a Telegram
# bot and interact with the Telegram API. However, the code snippet is incomplete and does not contain
# any further instructions or code to create a bot or perform any actions.
import telebot
# The above code is importing the regular expression module "re" in Python.
import re
# The above code is importing the `mysql.connector` module in Python. This module provides a way to
# connect to a MySQL database and perform various operations such as executing queries, inserting
# data, updating data, and deleting data.
import tweepy
import mysql.connector
# The above code is importing the `Error` class from the `mysql.connector` module in Python. This
# class is typically used to handle errors that may occur when working with a MySQL database using the
# `mysql.connector` module.

# The above code is importing the `load_dotenv` function from the `dotenv` module. This function is
# used to load environment variables from a `.env` file into the current environment.
from dotenv import load_dotenv
# Load environment variables from .env file
# The above code is loading environment variables from a .env file into the current environment using
# the `load_dotenv()` function from the `dotenv` library in Python. This is useful for keeping
# sensitive information, such as API keys or database credentials, separate from the code and stored
# securely in a file.
from execute_query import execute_query
from connection import connection
import keyboard as keyboard
import constants as const
from referral import Referral
from wallet import Wallet

load_dotenv()
# Instance of the robot
# The above code is initializing a Telegram bot using the `telebot` library in Python. It is
# retrieving the bot token from an environment variable named `BOTTOKEN` using the `os` library and
# then passing it to the `TeleBot` constructor to create a new instance of the bot.
BOTTOKEN = os.environ['BOTTOKEN']
bot = telebot.TeleBot(BOTTOKEN)
# The above code is creating and/or checking for the existence of three tables in a MySQL database:
# referral_link, referral_data, and wallet. It first establishes a connection to the database, then
# checks if the specified database exists and creates it if it doesn't. It then checks for the
# existence of each table and creates them if they don't exist. Finally, it closes the connection to
# the database.
RAILWAY_HOST = os.environ['RAILWAY_HOST']
RAILWAY_DB = os.environ['RAILWAY_DB']
RAILWAY_USER = os.environ['RAILWAY_USER']
RAILWAY_PASSWORD = os.environ['RAILWAY_PASSWORD']
RAILWAY_PORT =int(os.environ['RAILWAY_PORT'])
# TWEEPY_API_KEY=os.environ['TWEEPY_API_KEY']
# TWEEPY_API_SECRET_KEY=os.environ['TWEEPY_API_SECRET_KEY']
# TWEEPY_ACCESS_TOKEN=os.environ['TWEEPY_ACCESS_TOKEN']
# TWEEPY_ACCESS_TOKEN_SECRET=os.environ['TWEEPY_ACCESS_TOKEN_SECRET']

# auth = tweepy.OAuth1UserHandler(
#     TWEEPY_API_KEY,
#     TWEEPY_API_SECRET_KEY,
#     TWEEPY_ACCESS_TOKEN,
#     TWEEPY_ACCESS_TOKEN_SECRET
# )

# tweepy_api = tweepy.API(auth)

try:
    # Create a connection
    conn = connection()
    
    cursor = conn.cursor()

    # Attempt to select the database; create it if it does not exist
    try:
        cursor.execute(f"USE {RAILWAY_DB};")
    except mysql.connector.Error as err:
        print(f"Database {RAILWAY_DB} does not exist. Creating it.")
        cursor.execute(f"CREATE DATABASE {RAILWAY_DB};")
        cursor.execute(f"USE {RAILWAY_DB};")

    # Function to check and create table if not exists
    def check_and_create_table(table_creation_query, table_name):
        cursor.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '{RAILWAY_DB}' AND table_name = '{table_name}';")
        if cursor.fetchone()[0] == 0:
            cursor.execute(table_creation_query)

    # Define table creation queries
    referral_link_table_creation_query = """
        CREATE TABLE referral_link (
            user_id VARCHAR(100) PRIMARY KEY,
            referred_link VARCHAR(100)
        );"""
    referral_data_table_creation_query = """
        CREATE TABLE referral_data (
            user_id VARCHAR(100) PRIMARY KEY,
            referrer_id VARCHAR(100),
            referral_count INT,
            referral_balance INT
        );"""
    wallet_table_creation_query = """
        CREATE TABLE wallet (
            user_id BIGINT PRIMARY KEY,
            address VARCHAR(42) NOT NULL,
            balance INT
        );"""

    # Check and create tables if they don't exist
    check_and_create_table(referral_link_table_creation_query, 'referral_link')
    check_and_create_table(referral_data_table_creation_query, 'referral_data')
    check_and_create_table(wallet_table_creation_query, 'wallet')

except mysql.connector.Error as e:
    print(f"Error encountered: {e}")
finally:
    if conn and conn.is_connected():
        cursor.close()
        conn.close()

# The above code is defining two message handlers for a Python Telegram bot. The first handler is
# triggered when the user sends the "/start" command to the bot, and the second handler is triggered
# when the user sends the "🏠 Home" message to the bot. Both handlers will execute a specific block of
# code when triggered.
@bot.message_handler(commands = ['start'])
@bot.message_handler(func=lambda message: message.text == '🏠 Home')
def send_welcome(message):
    """
    This function sends a welcome message to a user and handles any errors that may occur.
    
    :param message: The message object that the bot received from the user. It contains information
    about the user who sent the message, the chat where the message was sent, and the text of the
    message
    """
    try:
        bot.reply_to(message, const.WELCOME_MESSAGE, reply_markup=keyboard.home_keyboard, parse_mode='html')        
    except telebot.apihelper.ApiTelegramException as e:
        # Handle the error message appropriately
        bot.reply_to(message, "Slow Connection Detected Restart Bot `/start`")

# The above code is defining a message handler for a Telegram bot using the Python programming
# language. Specifically, it is using a lambda function to check if the user's message text is equal
# to "➕ Affiliate". If the message matches, the handler will be triggered and the bot will perform
# some action.
@bot.message_handler(func=lambda message: message.text == '➕ Affiliate')
def handle_referrals(message):
    """
    This function handles referrals for a Telegram bot by checking if a user was referred by someone and
    adding referral data to a dictionary.
    
    :param message: The message object received by the bot from the user. It contains information about
    the user, the chat, and the message itself
    """    
    try:
        user = Referral(user_id=message.chat.id, input_link=None, referrer_id=None)
        # Check if the user was referred by someone
        link, status = user.has_link()
        if 'start=' not in message.text:        
            bot.reply_to(message, const.REFERRAL_LINK_MESSAGE, reply_markup=keyboard.no_custom_keyboard)
            
            if status is True:
                bot.send_message(message.chat.id, link, reply_markup=keyboard.set_wallet_keyboard)
            elif status is False:                   
                @bot.message_handler(func=lambda message: message.chat.id == message.chat.id and 'https://t.me/auroralite_bot?start=' in message.text)
                def handle_referrals(message):
                    # Extract the referrer's ID from the message
                    """
                    The handle_referrals function is called when a user clicks on the referral link.
                    It checks if the user has already been referred, and if not, it adds them to the database.
                    Then it increments both their balance and their referrer's balance by 10.
                    
                    :param message: Extract the referrer's id from the message
                    :doc-author: Trelent
                    """
                    
                    if status is False:
                        user = Referral(user_id=message.chat.id, input_link=message.text, referrer_id=None)
                        user.add_link()  
                        
                    referrer = message.text.split('start=')[1]
                    user = Referral(user_id=message.chat.id, input_link=message.text, referrer_id=referrer)
                    user.add_referrer_data()
                    
                    try:
                        id, count, balance = Referral(user_id=referrer, input_link=None, referrer_id=None).referrer_data()                     
                        
                        increment_data = Referral(user_id=referrer, input_link=None, referrer_id=None, referral_count=count + 1, referral_balance=balance + const.user_airdrop)
                        increment_data.increment()                        
                        
                    except mysql.connector.Error as e:
                        print('Error', e)           
                        
                    bot.reply_to(message, f"Welcome to our bot! You were referred by user ID {referrer}.", reply_markup=keyboard.set_wallet_keyboard,)
    except telebot.apihelper.ApiTelegramException as e:
        # Handle the error message appropriately
        print(e)
        bot.reply_to(message, "Slow Connection Detected Restart Bot `/start`")

# The above code is defining a message handler for the bot. It will handle messages that have the text
# "💢 Main Menu". When a user sends a message with this text, the function associated with this
# handler will be executed.
@bot.message_handler(func=lambda message: message.text == '💢 Main Menu')
def send_commands(message):
    """
    This function sends a main menu message with a keyboard as a response to a user's message.
    
    :param message: The message object that contains information about the incoming message, such as the
    chat ID, sender ID, and message text
    """
    response = "💢 Main Menu"
    bot.send_message(message.chat.id, response, reply_markup=keyboard.main_menu_keyboard)

# The above code is defining a message handler for a Telegram bot using the Python programming
# language. Specifically, it is using the `func` parameter to check if the incoming message text is
# equal to "🫡 Join us". If the message text matches, the handler will be triggered and the bot will
# perform some action.

@bot.message_handler(func=lambda message: message.text == '🫡 Join us')
def subscribe_handler(message):
    """
    This function checks if a user is a member of a Telegram group and if they follow a Twitter account,
    and replies with a success message and a keyboard if they meet the requirements, or an error message
    if they don't.
    
    :param message: The message object that triggered the handler function. It contains information
    about the message, such as the chat it was sent in, the sender, and the text of the message
    :return: The function does not return anything, it only sends a reply message to the user or catches
    an exception and sends an error message.
    """
    user_id = message.chat.id
    bot.reply_to(message, const.TWITTER_MESSAGE, reply_markup=keyboard.no_custom_keyboard, parse_mode='html')
    @bot.message_handler(func=lambda message: message.chat.id == user_id and '@' in message.text)
    def handle_subscriber(message):
        if message :
            try:
                # Get user ID from Telegram
                user_id = message.chat.id
                
                # Check if user follows the Telegram group
                try:
                    group_member = bot.get_chat_member('@auroraliteaalgroup', user_id)
                    if group_member.status not in ['member', 'administrator', 'creator']:
                        bot.reply_to(message, const.ERROR_MESSAGE, parse_mode='html')
                        return
                except telebot.apihelper.ApiTelegramException as e:
                    print(f"Telegram API error: {e}")
                    bot.reply_to(message, const.ERROR_MESSAGE, parse_mode='html')
                    return
                        
                # Check if the user follows the Twitter account
                # try:
                #     twitter_user = tweepy_api.get_user(screen_name='auroraliteaal')
                #     source_user = tweepy_api.get_user(screen_name=message)  # Using the obtained Twitter username/ID
                #     relationship = tweepy_api.show_friendship(source_id=source_user.id_str, target_id=twitter_user.id_str)
                #     if not relationship[0].following:
                #         bot.reply_to(message, const.SUCCESS_MESSAGE, reply_markup=keyboard.affiliate_keyboard, parse_mode='html')
                #         return
                # except Exception as e:
                #     print(f"Twitter API error: {e}")
                #     bot.reply_to(message, const.SUCCESS_MESSAGE, reply_markup=keyboard.affiliate_keyboard, parse_mode='html')
                #     return
                
                # If all checks pass
                bot.reply_to(message, const.SUCCESS_MESSAGE, reply_markup=keyboard.affiliate_keyboard)
            
            except Exception as e:
                # General exception handling
                print(f"An error occurred: {e}")
                bot.reply_to(message, const.ERROR_MESSAGE, parse_mode='html')

# The above code is defining a message handler for a Telegram bot using the Python programming
# language. The handler is triggered when the user sends a message with the text "📰 Change address".

@bot.message_handler(func=lambda message: message.text == '📰 Change address')
def change_wallet_address(message):
    """
    This function allows a user to change their wallet address by prompting them for a new address and
    verifying that it is a valid BSC address.
    
    :param message: The message object that contains information about the user's input and the chat
    they are in
    """
    try:
        user_id = message.chat.id
        wallet = Wallet(user_id=message.chat.id, address=None, balance=0)

        # Check if user already has a wallet then ask for wallet to be deleted
        if user_id in wallet.select_wallet():
            bot.reply_to(message, "🆕 What is your new address? ")
            
             # Wait for user input
            @bot.message_handler(func=lambda message: message.chat.id == user_id and '0x' in message.text)
            def handle_wallet_address(message):
                # Check if the message contains a BSC address
                match = re.search(const.BSC_ADDRESS_REGEX, message.text.strip())
                
                if match:
                    # Store the wallet address
                    bsc_address = match.group(0)
                    wallet = Wallet(user_id=message.chat.id, address=bsc_address)
                    
                    # Set wallet address to the wallet dictionary
                    wallet.update_address()
                    # Successful reply
                    bot.reply_to(message, "Your wallet address has been saved. Thank you!", reply_markup=keyboard.subscribe_keyboard)
                else:
                    bot.reply_to(message, "Unacceptable wallet address.")
        else:
            bot.reply_to(message, "You don't have a wallet to reset.", reply_markup=keyboard.subscribe_keyboard)
           
    except telebot.apihelper.ApiTelegramException as e:
        # Catch the ApiTelegramException and print the error message
        print(f"An error occurred: {e}")
        # Handle the error message appropriately
        bot.reply_to(message, "Slow Connection Detected Restart Bot `/start`")
# The above code is defining a message handler for a Telegram bot using the Python programming
# language. Specifically, it is using the `func` parameter to check if the user's message text is
# equal to "😌 Wallet". If the message matches, the handler will be triggered and the bot will perform
# some action.

@bot.message_handler(func=lambda message: message.text == '😌 Wallet')
def prompt_for_wallet(message):
    """
    This function prompts the user to input their BEP-20 wallet address, checks if it is valid, and
    stores it in the database if it is.
    
    :param message: The message object received by the bot. It contains information about the message
    sent by the user, such as the text, chat ID, and user ID
    """
    try:
        user_id = message.chat.id
        wallet = Wallet(user_id=message.chat.id, address=None, balance=0)
        
        address, balance = wallet.select_wallet_by_user_id()
        
        # Check if user already has a wallet
        if user_id in wallet.select_wallet():
            bot.reply_to(message, f"Your wallet address is {address}", reply_markup=keyboard.wallet_keyboard,)
        else:   
            # Ask the user for their BEP-20 wallet address
            bot.reply_to(message, const.WALLET_MESSAGE, parse_mode='html')
            
            # Wait for user input
            @bot.message_handler(func=lambda message: message.chat.id == user_id and '0x' in message.text)
            def handle_wallet_address(message):
                # Check if the message contains a BSC address
                match = re.search(const.BSC_ADDRESS_REGEX, message.text.strip())
                
                if match:
                    # Store the wallet address
                    bsc_address = match.group(0)
                    
                    set_wallet = Wallet(user_id=message.chat.id, address=bsc_address,balance=const.user_airdrop)
                    set_wallet.insert_wallet()
                    # Successful reply
                    bot.reply_to(message, "Your wallet address has been saved. Thank you!", reply_markup=keyboard.subscribe_keyboard)
                else:
                    bot.reply_to(message, "Unacceptable wallet address.")
    except telebot.apihelper.ApiTelegramException as e:
        # Catch the ApiTelegramException and print the error message
        print(f"An error occurred: {e}")
        # Handle the error message appropriately
        bot.reply_to(message, "An error has ocurred")      
# The above code is defining a message handler for a Telegram bot using the Python programming
# language. Specifically, it is using the `func` parameter to check if the user's message text is
# equal to "🤑 Balance". If the message matches, the handler will be triggered and the bot will
# perform some action (which is not shown in the code snippet).

@bot.message_handler(func=lambda message: message.text == '🤑 Balance')
def check_airdrop_balance(message):
    """
    The function calculates the total balance of a user's airdrop and referral earnings and sends a
    message with the details.
    
    :param message: The message object that contains information about the user who sent the message and
    the content of the message
    """
    # Get the user's unique ID
    id, count, referrer_balance = Referral(user_id=message.chat.id).referrer_data()
    address, wallet_balance = Wallet(user_id=message.chat.id, address=None, balance=0).select_wallet_by_user_id()
    
    total_balance = wallet_balance + referrer_balance
        
        
    response = f"""
    😲 You've earned {wallet_balance} AAL from our airdrop\n\n🔄️ Your referral count is {count} and your referral balance is {referrer_balance} AAL.\n\n🗿 Total balance is {total_balance} AAL
    """
    bot.send_message(message.chat.id, response)
# The above code is defining a message handler for a Telegram bot using the Python programming
# language. Specifically, it is using the `func` parameter to check if the user's message text is
# equal to "🧑‍🤝‍🧑 Referrals". If the user sends this message, the message handler will be triggered
# and the bot will perform some action (which is not shown in the code snippet).

@bot.message_handler(func=lambda message: message.text == '🧑‍🤝‍🧑 Referrals')
def show_referral_info(message):
    """
    The function displays referral information for a user, including their referrer's ID, referral
    count, referral balance, and referral link.
    
    :param message: The message object that contains information about the user who triggered the
    function
    """
    id, count, balance = Referral(user_id=message.chat.id, input_link=None, referrer_id=None, referral_count=None, referral_balance=None).referrer_data()                     
        
    bot.reply_to(message, f"You were referred by user ID {id}.\n\n Your referral count is {count} and your referral balance is {balance} AAL.\n\n🔗 Your referral link is https://t.me/{bot.get_me().username}?start={message.chat.id}") 


last_claim_times ={}

@bot.message_handler(func=lambda message: message.text == '🌞 Daily Claim')
def daily_claim(message):
    user_id = message.chat.id
    current_time = time.time()
    
    # Check if the user has made a claim before
    if user_id in last_claim_times:
        last_claim_time = last_claim_times[user_id]
        # Check if enough time has elapsed since the last claim (4 minutes = 240 seconds)
        if current_time - last_claim_time < 86399:
            # If not enough time has passed, inform the user
            bot.reply_to(message, "Please wait 24hrs before claiming again.")
            return
    
    # Update the last claim time for the user
    last_claim_times[user_id] = current_time
    
    # Perform the claim operation
    address, wallet_balance = Wallet(user_id=user_id, address=None, balance=0).select_wallet_by_user_id()
    try:
        Wallet(user_id=user_id, address=None, balance=wallet_balance+1).update_balance()
    except Exception as e:
        print('An exception occurred:', e)
    
    # Notify the user about the successful claim
    bot.reply_to(message, "1 AAl 🌞 Claimed")

# The above code is using the Python library `python-telegram-bot` to create a bot that can receive
# and respond to messages on the Telegram messaging platform. The `bot.infinity_polling()` method is
# used to continuously poll for new messages and handle them appropriately. The `try-except` block is
# used to catch any exceptions that may occur during the execution of the `infinity_polling()` method
# and print an error message with the details of the exception.
try:
    bot.infinity_polling()
except Exception as e:
    print(f"Error ocurred: {e}")