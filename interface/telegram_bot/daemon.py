#!/usr/bin/env python3.6

import json
import telegram
import websockets
import asyncio
from configparser import ConfigParser

config = ConfigParser()
config.read("./interface/telegram_bot/telegram.ini")

TOKEN = config["telegram"]["token"]
MEERA_URL = config["meera"]["url"]
CLIENT_TIMEOUT = 5


def handleReply(bot, update, response):
	reply_markup = telegram.ReplyKeyboardRemove()
	bot.send_message(
		chat_id=update.effective_message.chat_id, 
		text=response["body"]["text"],
		disable_web_page_preview=True,
		reply_markup=reply_markup)

def handleSelfLocationRequest(bot, update, response):
	location_keyboard = telegram.KeyboardButton(text="Send Location", request_location=True)
	custom_keyboard = [[ location_keyboard ]]
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
	bot.send_message(
		chat_id=update.effective_message.chat_id, 
		text="Would you mind sharing your location with me?", 
		reply_markup=reply_markup)

switcher = {
	"reply": handleReply,
	"self-location-request": handleSelfLocationRequest
}

def getUpdateId(bot):
	try:
		updateId = bot.get_updates()[0].update_id
	except IndexError:
		updateId = None
	return updateId

def getHelloRequest():
	return json.dumps({
		"type": "hello",
		"body": {
			"name": "telegram",
			"deviceType": "telegram_bot"
		}
	})

def getMessageRequest(clientId, contextId, message):
	return json.dumps({
		"type": "message",
		"contextId": clientId,
		"body": {
			"clientId": clientId,
			"message": message
		}
	})

def getLocationRequest(clientId, contextId, location):
	return json.dumps({
		"type": "self-location",
		"contextId": contextId,
		"body": {
			"clientId": clientId,
			"latitude": location.latitude,
			"longitude": location.longitude
		}
	})

async def sayHello(websocket):
	await websocket.send(getHelloRequest())
	response = websocket.recv()
	return json.loads(await asyncio.wait_for(response, CLIENT_TIMEOUT))["body"]

async def sendMessage(websocket, client, contextId, message):
	await websocket.send(getMessageRequest(client["id"], contextId, message))
	response = websocket.recv()
	return json.loads( await asyncio.wait_for(response, CLIENT_TIMEOUT))

async def sendLocation(websocket, client, contextId, location):
	await websocket.send(getLocationRequest(client["id"], contextId, location))
	response = websocket.recv()
	return json.loads( await asyncio.wait_for(response, CLIENT_TIMEOUT))



async def start():

	bot = telegram.Bot(TOKEN)
	updateId = getUpdateId(bot)
	currentContextId = None

	while True:
		try:
			async with websockets.connect(MEERA_URL) as websocket:
				client = await sayHello(websocket)

				while True:
					try:
						for update in bot.get_updates(offset=updateId, timeout=0):
							updateId = update.update_id + 1
							if update.message.location is not None:
							if update.message and update.message.text:
								try:
									response = await sendMessage(websocket, client, currentContextId, update.message.text)
									currentContextId = response.get("replyTo")
									switcher[response["type"]](bot, update, response)
								except(asyncio.TimeoutError):
									print(update.message.text)
							elif update.message and update.message.location:
								try:
								 	response = await sendLocation(websocket, client, currentContextId, update.message.location)
								 	currentContextId = response.get("replyTo")
								 	switcher[response["type"]](bot, update, response)
								except(asyncio.TimeoutError):
									print(update.message.location)
							pass
					except(telegram.error.TimedOut):
						print("timeout")
						pass
					except(telegram.error.Unauthorized):
						print("Bot Blocked by {} {}: {}".format(update.effective_user.first_name, update.effective_user.last_name, update.effective_user.username))
						print(update)	
		except(telegram.error.Unauthorized):
			pass

asyncio.get_event_loop().run_until_complete(start())
asyncio.get_event_loop().run_forever()
