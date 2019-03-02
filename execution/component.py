import os
import importlib
from copy import deepcopy
from configparser import ConfigParser

from circuits import Component, handler

from events import *
from execution.exception import SelfLocationNotFoundException

class TasKExecutorComponent(Component):

	

	def __init__(self):
		super(TasKExecutorComponent, self).__init__()
		config = ConfigParser()
		config.read("./plugins/plugins.ini")
		self.pluginPreference = config["plugins"]
		self.plugins = self.getPlugins()
		print(self.plugins)

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


