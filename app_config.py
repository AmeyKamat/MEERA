from circuits import Debugger
from circuits.web.dispatchers import WebSocketsDispatcher
from circuits.web import Logger, Static

from web.websockets import WSGateway
from web.root_controller import Root
from web.client_controller import ClientController
from web.context_controller import ContextController
from web.conversation_controller import ConversationController

from client.manager import ClientManager
from context.manager import ContextManager

from context.component import ContextComponent
from nlp.component import NLPAnalysisComponent
from preprocessing.component import PreprocessingComponent
from execution.component import TasKExecutorComponent
from interaction.component import InteractionComponent
from inputmessagelogging.component import InputMessageLoggingComponent

clientManager = ClientManager()
contextManager = ContextManager()

BOOTSTRAP_MODULES = {
	"appComponents": [
		InputMessageLoggingComponent(),
		ContextComponent(contextManager),
		NLPAnalysisComponent(),
		PreprocessingComponent(),
		TasKExecutorComponent(),
		InteractionComponent()
	],
	"gateways": [
		WSGateway(clientManager),
		ClientController(clientManager),
		ContextController(contextManager),
		ConversationController(contextManager),
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