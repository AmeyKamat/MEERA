import os
import json
import asyncio
from configparser import ConfigParser
import telegram
import websockets

#pylint: disable=unused-argument
def handle_reply(bot, update, response):
    reply_markup = telegram.ReplyKeyboardRemove()
    bot.send_message(
        chat_id=update.effective_message.chat_id,
        text=response["body"]["text"],
        disable_web_page_preview=True,
        reply_markup=reply_markup)

#pylint: disable=unused-argument
def handle_self_location_request(bot, update, response):
    location_keyboard = telegram.KeyboardButton(text="Send Location", request_location=True)
    custom_keyboard = [[location_keyboard]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(
        chat_id=update.effective_message.chat_id,
        text="Would you mind sharing your location with me?",
        reply_markup=reply_markup)

def get_update_id(bot):
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None
    return update_id

def get_hello_request():
    return json.dumps({
        "type": "hello",
        "body": {
            "name": "telegram",
            "client_type": "telegram_bot"
        }
    })

def get_message_request(client_id, context_id, message, is_user_authorized):
    return json.dumps({
        "type": "message",
        "context_id": context_id,
        "body": {
            "client_id": client_id,
            "message": message,
            "is_user_authorized": is_user_authorized
        }
    })

def get_location_request(client_id, context_id, location):
    return json.dumps({
        "type": "self-location",
        "context_id": context_id,
        "body": {
            "client_id": client_id,
            "latitude": location.latitude,
            "longitude": location.longitude
        }
    })

def is_authorized(username):
    return username in AUTHORIZED_USERS

async def say_hello(websocket):
    await websocket.send(get_hello_request())
    response = websocket.recv()
    response = json.loads(await asyncio.wait_for(response, CLIENT_TIMEOUT))
    return response['body']

async def send_message(websocket, client, context_id, message, is_user_authorized):
    await websocket.send(
        get_message_request(
            client["client_id"],
            context_id,
            message,
            is_user_authorized
        )
    )
    response = websocket.recv()
    response = json.loads(await asyncio.wait_for(response, CLIENT_TIMEOUT))
    return response

async def send_location(websocket, client, context_id, location):
    await websocket.send(get_location_request(client["client_id"], context_id, location))
    response = websocket.recv()
    response = json.loads(await asyncio.wait_for(response, CLIENT_TIMEOUT))
    return response



async def start():

    switcher = {
        "reply": handle_reply,
        "self-location-request": handle_self_location_request
    }

    bot = telegram.Bot(TOKEN)
    update_id = get_update_id(bot)
    current_context_id = None

    while True:
        try:
            async with websockets.connect(MEERA_URL) as websocket:
                client = await say_hello(websocket)

                while True:
                    try:
                        for update in bot.get_updates(offset=update_id, timeout=0):
                            update_id = update.update_id + 1
                            is_user_authorized = is_authorized(update.effective_user.username)
                            if update.message and update.message.text:
                                try:
                                    response = await send_message(
                                        websocket,
                                        client,
                                        current_context_id,
                                        update.message.text,
                                        is_user_authorized)

                                    current_context_id = response.get("reply_to")
                                    switcher[response["type"]](bot, update, response)
                                except asyncio.TimeoutError:
                                    print(update.message.text)
                            elif update.message and update.message.location:
                                try:
                                    response = await send_location(
                                        websocket,
                                        client,
                                        current_context_id,
                                        update.message.location)

                                    current_context_id = response.get("reply_to")
                                    switcher[response["type"]](bot, update, response)
                                except asyncio.TimeoutError:
                                    print(update.message.location)
                    except telegram.error.TimedOut:
                        print("timeout")
                    except telegram.error.Unauthorized:
                        print("Bot Blocked by {} {}: {}".format(
                            update.effective_user.first_name,
                            update.effective_user.last_name,
                            update.effective_user.username))
                        print(update)
        except telegram.error.Unauthorized:
            pass

def get_config():
    config = ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'telegram.ini'))
    return config

CONFIG = get_config()
TOKEN = os.environ[CONFIG['telegram']['token_variable']]
MEERA_URL = CONFIG["meera"]["url"]
CLIENT_TIMEOUT = 5
AUTHORIZED_USERS = os.environ[CONFIG["telegram"]["authorized-users-variable"]].split(":")

def main():
    asyncio.get_event_loop().run_until_complete(start())
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    main()
