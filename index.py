#!/usr/bin/env python3.6

import webbrowser

from circuits.web import Server

from app_config import BOOTSTRAP_MODULES

IP_ADDR = "0.0.0.0"
PORT = 8000


def bootstrapAppComponents(app, appComponents):
	for appComponent in appComponents:
		appComponent.register(app)

def bootstrapGateways(app, gateways):
	for gateway in gateways:
		gateway.register(app)

def bootstrapDispatchers(app, dispatchers):
	for dispatcher in dispatchers:
		dispatcher.register(app)

def bootstrapCircuitComponents(app, circuitComponents):
	for circuitComponent in circuitComponents:
		circuitComponent.register(app)



app = Server((IP_ADDR, PORT))
bootstrapAppComponents(app, BOOTSTRAP_MODULES["appComponents"])
bootstrapGateways(app, BOOTSTRAP_MODULES["gateways"])
bootstrapDispatchers(app, BOOTSTRAP_MODULES["dispatchers"])
bootstrapCircuitComponents(app, BOOTSTRAP_MODULES["circuitComponents"])

webbrowser.open('http://localhost:8000')

app.run()