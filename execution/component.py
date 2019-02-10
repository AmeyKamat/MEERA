import os
import importlib
from copy import deepcopy
from configparser import ConfigParser

from circuits import Component, handler

from events import *

class TasKExecutorComponent(Component):

	

	def __init__(self):
		super(TasKExecutorComponent, self).__init__()
		config = ConfigParser()
		config.read("./plugins/plugins.ini")
		self.pluginPreference = config["plugins"]
		self.plugins = self.getPlugins()

	@handler("EntitiesPreprocessedEvent")
	def execute(self, context):
		intent = context.intent
		plugin = self.plugins.get(intent)
		if plugin != None:
			context["result"] = plugin.execute(deepcopy(context.intent), deepcopy(context.entities))
			self.fire(TaskExecutedEvent(context))
		else:
			self.fire(NoPluginsAvailableEvent(context))
		

	def getPlugins(self):
		installedPlugins = [f.name for f in os.scandir("plugins") if f.is_dir() and f.name != "__pycache__"] 
		
		plugins = {}
		for plugin in installedPlugins:
			config = ConfigParser()
			config.read("./plugins/{0}/plugin.ini".format(plugin))
			pluginClassName = config.sections()[0]
			pluginIntent = config[pluginClassName]["intent"]
			if pluginIntent != "custom" and self.pluginPreference[pluginIntent] == pluginClassName:
				module = importlib.import_module("plugins.{0}.executor".format(plugin))
				plugins[pluginIntent] = getattr(module, pluginClassName)(config[pluginClassName])
		return plugins


