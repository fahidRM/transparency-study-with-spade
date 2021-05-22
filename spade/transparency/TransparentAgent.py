
import time

from spade.agent import Agent
from stag_logger.Logger import Logger


class TransparentAgent (Agent):

    def add_behaviour(self, behaviour, template=None):
        super().add_behaviour(behaviour, template)
        Logger.add_persistent_data(self.name, {"source": "self", "type": "Behaviour", "value": behaviour.get_name()} )

    def remove_behaviour(self, behaviour):
        super().remove_behaviour(behaviour)
        Logger.remove_persistent_data(self.name, {"source": "self", "type": "Behaviour", "value": behaviour.get_name()})
