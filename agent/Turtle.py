import logging

from spade.agent import Agent

from agent.CoordAgent import CoordAgent
from agent.behaviours.GeneralBehaviour import GeneralBehaviour

logger = logging.getLogger("agent.Turtle")


class Turtle(CoordAgent):

    def __init__(self, jid, password, actions: [], contacts: [Agent], verify_security=False, movement = None, arm = None):
        super().__init__(jid, password, actions, contacts, verify_security)

    async def setup(self):
        logger.info("Started turtle")
        # self.presence.set_available(availability=True, show=PresenceShow.Chat)

        logger.info("Generating behaviour")
        self.add_behaviour(GeneralBehaviour(actions=self.actions, contacts=self.contacts))
