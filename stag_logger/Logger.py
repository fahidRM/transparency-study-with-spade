import requests


class BasicLogger (object):


    def __init__(self):
        pass

    def log_event(self, payload):
        pass


class Logger (BasicLogger):
    _listeners = []
    _persistentData = {}

    @staticmethod
    def log_event(payload={}):
        Logger.inform_listeners(payload)

    @staticmethod
    def add_persistent_data(agent: str = "Unknown", data: dict = {}):
        if agent in Logger._persistentData:
            Logger._persistentData[agent].append(data)
        else:
            Logger._persistentData[agent] = [data]

    @staticmethod
    def remove_persistent_data(agent: str = "Unknown", data: dict = {}):
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
            "source": {
                "agent": agent
            },
            "payload": {
                "category": "PLAN_TRACE",
                "contents": payload,
            }

        }
        payloads = []
        if agent in Logger._persistentData:
            bb_payload.extend(Logger._persistentData[agent])
        payloads.append({
             "source": {
                "agent": agent
            },
            "payload": {
                "category": "SENSE",
                "contents": {
                    "ACTION": "DUMP",
                    "VALUES": bb_payload
                }
            }

        })

        payloads.append(payload_dict)
        Logger.log_event(payloads)

    @staticmethod
    def log_plan_selection(agent: str = "Unknown", payload: dict = None, bb_payload: list = []):
        agent = str(agent).split("@")[0].split(",")[0]
        payload_dict = {
            "source": {
                "agent": agent
            },
            "payload": {
                "category": "PLAN_SELECTION",
                "contents": payload
            }

        }
        payloads = []
        if agent in Logger._persistentData:
            bb_payload.extend(Logger._persistentData[agent])
        payloads.append({
             "source": {
                "agent": agent
            },
            "payload": {
                "category": "SENSE",
                "contents": {
                    "ACTION": "DUMP",
                    "VALUES": bb_payload
                }
            }

        })
        payloads.append(payload_dict)
        Logger.log_event(payloads)

    @staticmethod
    def log_action(agent: str = "Unknown", payload: dict = None, bb_payload: list = []):
        agent = str(agent).split("@")[0].split(",")[0]
        payload_dict = {
             "source": {"agent": agent},
             "payload": {"category": "ACTION", "contents": payload}
          }
        payloads = []
        if agent in Logger._persistentData:
            bb_payload.extend(Logger._persistentData[agent])

        payloads.append({
             "source": {
                "agent": agent
            },
            "payload": {
                "category": "SENSE",
                "contents": {
                    "ACTION": "DUMP",
                    "VALUES": bb_payload
                }
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

    def __init__(self, mas_name="Unknown MAS", server: str = "localhost", port: int = 3000):
        super().__init__()
        self.mas = mas_name
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
            payload["source"]["mas"] = self.mas
            payload["time"] = {
                "sequence_number": self.sequence_number,
                "time_in_ms": "",
                "reasoning_cycle": 0
            }
            payload["source"]["agent"] =  payload["source"]["agent"].replace("_", "-")
            super(WebLogger, self).log_event(payload)
            requests.post(self.url, json={"log": payload })