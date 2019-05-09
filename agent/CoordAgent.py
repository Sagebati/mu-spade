from spade.agent import Agent

from agent.coordination import Action


class CoordAgent(Agent):
    def __init__(self, jid, password, actions: [Action], contacts: [Agent] = [], verify_security=False):
        super().__init__(jid, password, verify_security)
        self.actions = actions
        self.contacts = contacts
