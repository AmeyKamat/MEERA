from circuits import Debugger
from circuits.web.dispatchers import WebSocketsDispatcher
from circuits.web import Logger, Static

from web.websockets import WSGateway
from web.root_controller import Root
from web.connection_controller import ClientController

from connection.manager import ClientManager

from context.component import ContextComponent
from nlp.component import NLPAnalysisComponent
from preprocessing.component import PreprocessingComponent
from execution.component import TasKExecutorComponent
from interaction.component import InteractionComponent

clientManager = ClientManager()

BOOTSTRAP_MODULES = {
	"appComponents": [
		ContextComponent(),
		NLPAnalysisComponent(),
		PreprocessingComponent(),
		TasKExecutorComponent(),
		InteractionComponent()
	],
	"gateways": [
		WSGateway(clientManager),
		ClientController(clientManager),
		Root(),
		Static()
	],
	"dispatchers": [
		WebSocketsDispatcher("/websocket")
	],
	"circuitComponents": [
		Logger(),
		Debugger()
	]
}