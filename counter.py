import asyncio
import time

from spade.transparency.TransparentAgent import TransparentAgent
from stag_logger.Logger import WebLogger
from spade.behaviour import CyclicBehaviour


class DummyAgent(TransparentAgent):
    class Counter(CyclicBehaviour):

        def __init__(self):
            super().__init__("Count")


        async def on_start(self):
            self.counter = 0

        async def run(self):
            super()._on_run()
            print("Counter: {}".format(self.counter))
            self.counter += 1
            if self.counter > 3:
                self.kill(exit_code=10)
                return
            await asyncio.sleep(1)

        async def on_end(self):
            print("Behaviour finished with exit code {}.".format(self.exit_code))

    class MyBehavB(CyclicBehaviour):
        async def on_start(self):
            self.counter = 0

        async def run(self):
            print("Counter: {}".format(self.counter))
            self.counter += 1
            #if self.counter > 3:
                #self.kill(exit_code=10)
                #return
            await asyncio.sleep(1)

        async def on_end(self):
            print("Behaviour finished with exit code {}.".format(self.exit_code))

    async def setup(self):
        self.counter_behaviour = self.Counter()
        self.add_behaviour(self.counter_behaviour)


if __name__ == "__main__":

    WebLogger("COUNTER", "0.0.0.0", 3700)
    dummy = DummyAgent("agent1@localhost", "agent1")
    future = dummy.start()
    future.result()  # Wait until the start method is finished
    # wait until user interrupts with ctrl+C
    while not dummy.counter_behaviour.is_killed():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    #dummy.stop()