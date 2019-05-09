from spade.agent import Agent


class DummyAgent(Agent):
    async def setup(self):
        print("Hello world! I'm agent {}".format(str(self.jid)))
