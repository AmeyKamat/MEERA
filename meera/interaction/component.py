import os
import importlib
from configparser import ConfigParser
from copy import deepcopy

from circuits import Component, handler

from events import DialogueGeneratedEvent, NoPluginsAvailableEvent
from definitions import ABS_PLUGINS_DIR, PLUGINS_DIR
from interaction.chatInteractionManager import ChatInteractionManager

class InteractionComponent(Component):

    def __init__(self):
        super(InteractionComponent, self).__init__()
        config = ConfigParser()
        config.read(os.path.join(ABS_PLUGINS_DIR, 'plugins.ini'))
        self.pluginPreference = config['plugins']
        self.plugins = self.getPlugins()
        self.chatInteractionManager = ChatInteractionManager()

    @handler("TaskExecutedEvent")
    def generateDialogue(self, context):
        intent = context.nlpAnalysis.intent
        plugin = self.plugins.get(intent)
        if plugin != None:
            context.interaction = plugin.generate(deepcopy(context.result))
            self.fire(DialogueGeneratedEvent(context))
        else:
            self.fire(NoPluginsAvailableEvent(context))

    @handler("ChatRequestedEvent")
    def generateChat(self, context):
        context.interaction = self.chatInteractionManager.generate(context.nlpAnalysis)
        self.fire(DialogueGeneratedEvent(context))

    def getPlugins(self):
        installedPlugins = [f.name for f in os.scandir(ABS_PLUGINS_DIR) if f.is_dir() and f.name != "__pycache__"] 
        
        plugins = {}
        for plugin in installedPlugins:
            config = ConfigParser()
            configPath = os.path.join(ABS_PLUGINS_DIR, '{0}/plugin.ini'.format(plugin))
            config.read(os.path.join(configPath))

            pluginClassName = config.sections()[0]
            pluginIntent = config[pluginClassName]['intent']
            
            if pluginIntent != "custom" and self.pluginPreference[pluginIntent] == pluginClassName:
                module = importlib.import_module("{0}.{1}.dialogue".format(PLUGINS_DIR, plugin))
                plugins[pluginIntent] = getattr(module, pluginClassName)(config[pluginClassName])
        return plugins