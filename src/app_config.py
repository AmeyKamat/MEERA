from circuits import Debugger
from circuits.web.dispatchers import WebSocketsDispatcher
from circuits.web import Logger, Static

from api.websockets import WSGateway
from api.client_controller import ClientController
from api.context_controller import ContextController
from api.conversation_controller import ConversationController
from api.status_controller import StatusController

from interface.web_app.root_controller import Root

from client.manager import ClientManager
from context.manager import ContextManager

from context.component import ContextComponent
from nlp.component import NLPAnalysisComponent
from preprocessing.component import PreprocessingComponent
from execution.component import TasKExecutorComponent
from interaction.component import InteractionComponent

# pylint: disable=invalid-name
clientManager = ClientManager()
# pylint: disable=invalid-name
contextManager = ContextManager()

BOOTSTRAP_MODULES = {
    "appComponents": [
        StatusController(contextManager, clientManager),
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
        WebSocketsDispatcher("/talk")
    ],
    "circuitComponents": [
        Logger(),
        Debugger()
    ]
}
