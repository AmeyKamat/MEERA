import os
import importlib
from configparser import ConfigParser
from copy import deepcopy

from circuits import Component, handler

from events import DialogueGeneratedEvent, NoPluginsAvailableEvent
from definitions import ABS_PLUGINS_DIR, PLUGINS_DIR
from interaction.chat_interaction_manager import ChatInteractionManager

class InteractionComponent(Component):

    def __init__(self):
        super(InteractionComponent, self).__init__()
        config = ConfigParser()
        config.read(os.path.join(ABS_PLUGINS_DIR, 'plugins.ini'))
        self.plugin_preference = config['plugins']
        self.plugins = self.get_plugins()
        self.chat_interaction_manager = ChatInteractionManager()

    @handler("TaskExecutedEvent")
    def generate_dialogue(self, context):
        intent = context.nlp_analysis.intent
        plugin = self.plugins.get(intent)
        if plugin is not None:
            context.interaction = plugin.generate(deepcopy(context.result))
            self.fire(DialogueGeneratedEvent(context))
        else:
            self.fire(NoPluginsAvailableEvent(context))

    @handler("ChatRequestedEvent")
    def generate_chat(self, context):
        context.interaction = self.chat_interaction_manager.generate(context.nlp_analysis)
        self.fire(DialogueGeneratedEvent(context))

    def get_plugins(self):
        installed_plugins = [
            f.name for f in os.scandir(ABS_PLUGINS_DIR)
            if f.is_dir() and f.name != "__pycache__"
        ]

        plugins = {}
        for plugin in installed_plugins:
            config = ConfigParser()
            config_path = os.path.join(ABS_PLUGINS_DIR, '{0}/plugin.ini'.format(plugin))
            config.read(os.path.join(config_path))

            plugin_class_name = config.sections()[0]
            plugin_intent = config[plugin_class_name]['intent']

            if self.plugin_preference[plugin_intent] == plugin_class_name:

                module = importlib.import_module("{0}.{1}.dialogue".format(PLUGINS_DIR, plugin))
                plugins[plugin_intent] = getattr(
                    module, plugin_class_name)(config[plugin_class_name])
        return plugins
