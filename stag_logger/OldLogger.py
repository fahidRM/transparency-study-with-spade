
import requests


class BasicLogger (object):

    def __init__(self):
        pass

    def log_event(self, payload=None):
        if payload is None:
            payload = []
        pass


class Logger (BasicLogger):
    _listeners = []
    _persistentData = {}

    @staticmethod
    def log_event(payload=None):
        if payload is None:
            payload = []
        Logger.inform_listeners(payload)

    @staticmethod
    def add_persistent_data(agent: str = "Unknown", data: str = "Unknown"):
        if agent in Logger._persistentData:
            Logger._persistentData[agent].append(data)
        else:
            Logger._persistentData[agent] = [data]

    @staticmethod
    def remove_persistent_data(agent: str = "Unknown", data: str = "Unknown"):
        if agent in Logger._persistentData:
            if data in Logger._persistentData[agent]:
                Logger._persistentData[agent].remove(data)

    @staticmethod
    def log_plan_trace(agent: str = "Unknown", payload=None, bb_payload=None):
        agent = str(agent).split("@")[0].split(",")[0]
        if bb_payload is None:
            bb_payload = []
        if payload is None:
            payload = []
        payload_dict = {
            "AGENT": agent,
            "TYPE": "PLAN_TRACE",
            "TYPE_INFO": payload,
        }
        payloads = []
        #if len(bb_payload) > 0:
        if agent in Logger._persistentData:
            bb_payload.extend(Logger._persistentData[agent])
        payloads.append({
            "AGENT": agent,
            "TYPE": "SENSE",
            "TYPE_INFO": {
                "ACTION": "DUMP",
                "VALUES": ";".join(bb_payload)
            }
        })

        payloads.append(payload_dict)
        Logger.log_event(payloads)

    @staticmethod
    def log_plan_selection(agent: str = "Unknown", payload: dict = None, bb_payload: list = []):
        agent = str(agent).split("@")[0].split(",")[0]
        payload_dict = {
            "TYPE": "PLAN_SELECTION",
            "AGENT": agent,
            "TYPE_INFO": payload
        }
        payloads = []
        #if len(bb_payload) > 0:
        if agent in Logger._persistentData:
            bb_payload.extend(Logger._persistentData[agent])
        payloads.append({
            "AGENT": agent,
            "TYPE": "SENSE",
             "TYPE_INFO": {
                "ACTION": "DUMP",
                "VALUES": ";".join(bb_payload)
            }
        })
        payloads.append(payload_dict)
        Logger.log_event(payloads)

    @staticmethod
    def log_action(agent: str = "Unknown", payload: dict = None, bb_payload: list = []):
        agent = str(agent).split("@")[0].split(",")[0]
        payload_dict = {
            "AGENT": agent,
            "TYPE": "ACTION",
            "TYPE_INFO": payload
          }
        payloads = []
        if agent in Logger._persistentData:
            bb_payload.extend(Logger._persistentData[agent])

        payloads.append({
            "AGENT": agent,
            "TYPE": "SENSE",
            "TYPE_INFO": {
                "ACTION": "DUMP",
                "VALUES": ";".join(bb_payload)
            }
        })
        payloads.append(payload_dict)
        Logger.log_event(payloads)

    @staticmethod
    def register(listener: BasicLogger):
        if listener not in Logger._listeners:
            Logger._listeners.append(listener)

    @staticmethod
    def unregister(listener: BasicLogger):
        if listener in Logger._listeners:
            Logger._listeners.remove(listener)

    @staticmethod
    def inform_listeners(payload):
        for listener in Logger._listeners:
            if type(payload) is type(""):
                listener.log_event([payload])
            else:
                listener.log_event(payload)


class WebLogger(BasicLogger):

    def __init__(self, mas="Unknown MAS", server: str = "localhost", port: int = 3000):
        super().__init__()
        self.mas = mas
        self.sequence_number = 0
        self.url = "http://{}:{}/log".format(server, port)
        self.connect()
        self.register_with_logger()

    def connect(self):
        pass

    def register_with_logger(self):
        Logger.register(self)

    def log_event(self, payloads: list = []):
        self.sequence_number += 1

        for payload in payloads:
            print(payload)
            payload["MAS"] = self.mas
            payload["SECONDARY_TIMER"] = 0
            payload["SEQUENCE_NUMBER"] = self.sequence_number
            super(WebLogger, self).log_event(payload)
            requests.post(self.url, json={"log": payload })
            #print("logging...")
            #pass

# jack e saunders