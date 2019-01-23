from circuits import Debugger
from circuits.web.dispatchers import WebSocketsDispatcher
from circuits.web import Logger, Static

from web.websockets import WSGateway
from web.root_controller import Root
from context.component import ContextComponent
#from nlp.component import NLPAnalysisComponent

BOOTSTRAP_MODULES = {
	"appComponents": [
		ContextComponent(),
		#NLPAnalysisComponent()
	],
	"jobRunnerComponents": [
	],
	"gateways": [
		WSGateway(),
		Root(),
		Static()
	],
	"dispatchers": [
		WebSocketsDispatcher("/websocket")
	],
	"circuitComponents": [
		Debugger(),
		Logger(),
	]
}