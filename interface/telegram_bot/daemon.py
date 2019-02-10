#!/usr/bin/env python3.6

import json
import telegram
import websockets
import asyncio
from configparser import ConfigParser

config = ConfigParser()
config.read("./interface/telegram_bot/telegram.ini")

update_id = None

async def start():
	global update_id 
	bot = telegram.Bot(config["telegram"]["token"])
	try:
		update_id = bot.get_updates()[0].update_id
	except IndexError:
		update_id = None
	async with websockets.connect(config["meera"]["url"]) as websocket:
		await websocket.send(json.dumps({
			"type": "hello",
			"name": "telegram",
			"deviceType": "telegram_bot"
		}))
		client = websocket.recv()
		client = json.loads(await asyncio.wait_for(client, 5))
		while True:
			try:
				for update in bot.get_updates(offset=update_id, timeout=0):
					update_id = update.update_id + 1
					if update.message and update.message.text:
						await websocket.send(json.dumps({
							"clientId": client["id"],
							"type": "message",
							"message": update.message.text 
						}))
						try:
							message = websocket.recv()
							message = await asyncio.wait_for(message, 5)
							update.message.reply_text(message)
						except(asyncio.TimeoutError):
							print(update.message.text)
							update.message.reply_text("ERROR Occured")
			except(telegram.error.TimedOut):
				print("timeout")
				pass
			except(telegram.error.Unauthorized):
				print("Bot Blocked by {} {}: {}".format(update.effective_user.first_name, update.effective_user.last_name, update.effective_user.username))
				print(update)
				pass

asyncio.get_event_loop().run_until_complete(start())
asyncio.get_event_loop().run_forever()
