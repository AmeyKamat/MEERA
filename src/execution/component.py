import os
import sys
import importlib
from copy import deepcopy
from configparser import ConfigParser

from circuits import Component, handler

from events import TaskExecutedEvent, SelfLocationRequiredEvent, PluginFailedEvent
from execution.status import STATUS_SUCCESS, STATUS_NEED_LOCATION
from definitions import ABS_PLUGINS_DIR, PLUGINS_DIR

class TasKExecutorComponent(Component):

    def __init__(self):
        super(TasKExecutorComponent, self).__init__()

        config = ConfigParser()
        config.read(os.path.join(ABS_PLUGINS_DIR, 'plugins.ini'))

        self.plugin_preference = config['plugins']
        self.plugins = self.get_plugins()
        self.response_handlers = {
            STATUS_SUCCESS: TaskExecutedEvent,
            STATUS_NEED_LOCATION: SelfLocationRequiredEvent
        }

    @handler("EntitiesPreprocessedEvent")
    def execute(self, context):
        intent = context.nlp_analysis.intent
        plugin = self.plugins.get(intent)
        print(context)
        if plugin is not None:
            self.handle_plugin(plugin, context)
        else:
            self.fire(PluginFailedEvent(context))

    def handle_plugin(self, plugin, context):
        try:
            response = plugin.execute(deepcopy(context))
            context.result = response.get('result')
            event = self.response_handlers.get(
                response['status'], PluginFailedEvent)(context)
            self.fire(event)
        # pylint: disable=broad-except
        except Exception as exception:
            print(str(exception), file=sys.stderr)
            self.fire(PluginFailedEvent(context))

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

                module = importlib.import_module('{0}.{1}.executor'.format(PLUGINS_DIR, plugin))
                plugins[plugin_intent] = getattr(
                    module, plugin_class_name)(config[plugin_class_name])
        return plugins
