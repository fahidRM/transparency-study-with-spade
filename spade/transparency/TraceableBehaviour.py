
import time
from stag_logger.Logger import Logger

class TraceableBehaviour (object):

    def __init__(self, name="Unknown Behaviour", type="Unspecified"):
        self.agent = None
        self.name = name
        self.type = type

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type


    def _on_start(self):
        Logger.add_persistent_data(self.agent.name, {"source": "self", "type": "Behaviour", "value": self.name} )

    def _on_end(self):
        Logger.remove_persistent_data(self.agent.name, {"source": "self", "type": "Behaviour", "value": self.name} )

    def on_pause(self, owner):
        Logger.remove_persistent_data(owner, {"source": "self", "type": "Behaviour", "value": self.name} )

    def on_resume(self, owner):
        Logger.add_persistent_data(self.agent.name, {"source": "self", "type": "Behaviour", "value": self.name} )

    def _on_run(self):
        Logger.log_action(
            agent=self.agent.name,
            payload={
                    "META": "Running Behaviour",
                    "IDENTIFIER": self.name,
                    "CODE_LINE": "",
                    "CODE_FILE": ""
            },
            bb_payload=[]

        )
