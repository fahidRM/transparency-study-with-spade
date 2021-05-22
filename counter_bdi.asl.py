import argparse
import asyncio
import time


import agentspeak
from spade import quit_spade

from spade_bdi.bdi import BDIAgent

from stag_logger.Logger import WebLogger

parser = argparse.ArgumentParser(description='spade bdi basic example')
parser.add_argument('--server', type=str, default="localhost", help='XMPP server address.')
parser.add_argument('--name', type=str, default="agent1", help='XMPP name for the agent.')
parser.add_argument('--password', type=str, default="agent1", help='XMPP password for the agent.')
arguments = parser.parse_args()

parserb = argparse.ArgumentParser(description='spade bdi basic example')
parserb.add_argument('--server', type=str, default="localhost", help='XMPP server address.')
parserb.add_argument('--name', type=str, default="agent2", help='XMPP name for the agent.')
parserb.add_argument('--password', type=str, default="agent2", help='XMPP password for the agent.')
argumentsb = parserb.parse_args()


class CounterBDIAgent(BDIAgent):
    def add_custom_actions(self, actions):
        @actions.add(".count_down", 1)
        def _count_down(agent, term, intention):
            x = agentspeak.grounded(term.args[0], intention.scope)
            for i in range(0, int(x)):
                print(self.name + " Count at: ", int(x) - (i + 1))
            yield

        @actions.add(".count_up", 1)
        def _count_up(agent, term, intention):
            counter_term = agentspeak.grounded(term.args[0], intention.scope)
            for i in range(0, int(counter_term)):
                print(self.name + " Count at: ", i + 1)
            yield


WebLogger(mas_name="Counter BDI MAS", server="localhost", port=3700)
a = CounterBDIAgent("agent1@localhost", "agent1", "./_asl_files/agent1.asl")
b = CounterBDIAgent("agent2@localhost", "agent2", "./_asl_files/agent2.asl")

a.start()
b.start()


time.sleep(2)




a.stop().result()
b.stop().result()



quit_spade()
