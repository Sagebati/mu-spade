import logging

from aioxmpp import PresenceShow

from agent.CoordAgent import CoordAgent
from agent.behaviours.GeneralBehaviour import GeneralBehaviour


class Turtle(CoordAgent):
    async def setup(self):
        print("Started turtle")
        # self.presence.set_available(availability=True, show=PresenceShow.Chat)

        print("Generating behaviour")
        self.add_behaviour(GeneralBehaviour(actions=self.actions, contacts=self.contacts))
