from circuits import Event

class MessageReceivedEvent(Event):
    """event"""

class ContextCreatedEvent(Event):
    """event"""

class NLPConfidenceLowEvent(Event):
    """event"""

class ChatRequestedEvent(Event):
    """event"""

class SkillRequestedEvent(Event):
    """event"""

class EntitiesPreprocessedEvent(Event):
    """event"""

class TaskExecutedEvent(Event):
    """event"""

class DialogueGeneratedEvent(Event):
    """event"""

class NoPluginsAvailableEvent(Event):
    """event"""

class SelfLocationRequiredEvent(Event):
    """event"""

class ClientRegisteredEvent(Event):
    """event"""

class SelfLocationReceivedEvent(Event):
    """event"""

class PluginFailedEvent(Event):
    """event"""

class UserUnauthorizedEvent(Event):
    """event"""
