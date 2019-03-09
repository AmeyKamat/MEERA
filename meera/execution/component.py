import os
import importlib
from copy import deepcopy
from configparser import ConfigParser

from circuits import Component, handler

from events import TaskExecutedEvent, SelfLocationRequiredEvent, NoPluginsAvailableEvent
from definitions import ABS_PLUGINS_DIR, PLUGINS_DIR
from execution.exception import SelfLocationNotFoundException

class TasKExecutorComponent(Component):

    def __init__(self):
        super(TasKExecutorComponent, self).__init__()
        
        config = ConfigParser()
        print(os.path.join(ABS_PLUGINS_DIR, 'plugins.ini'))
        config.read(os.path.join(ABS_PLUGINS_DIR, 'plugins.ini'))
        
        self.pluginPreference = config['plugins']
        self.plugins = self.getPlugins()

    @handler("EntitiesPreprocessedEvent")
    def execute(self, context):
        intent = context.nlpAnalysis.intent
        plugin = self.plugins.get(intent)
        print(plugin)
        if plugin is not None:
            try:
                context.result = plugin.execute(deepcopy(context))
                self.fire(TaskExecutedEvent(context))
            except SelfLocationNotFoundException:
                self.fire(SelfLocationRequiredEvent(context))
        else:
            self.fire(NoPluginsAvailableEvent(context))
        

    def getPlugins(self):
        installedPlugins = [f.name for f in os.scandir(ABS_PLUGINS_DIR) if f.is_dir() and f.name != "__pycache__"] 
        
        plugins = {}
        for plugin in installedPlugins:
            config = ConfigParser()
            configPath = os.path.join(ABS_PLUGINS_DIR, '{0}/plugin.ini'.format(plugin))
            config.read(os.path.join(configPath))

            pluginClassName = config.sections()[0]
            pluginIntent = config[pluginClassName]['intent']
            
            if self.pluginPreference[pluginIntent] == pluginClassName:
                module = importlib.import_module('{0}.{1}.executor'.format(PLUGINS_DIR, plugin))
                plugins[pluginIntent] = getattr(module, pluginClassName)(config[pluginClassName])
        return plugins


