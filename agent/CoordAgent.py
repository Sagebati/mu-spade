from spade.agent import Agent


class CoordAgent(Agent):
    def __init__(self, jid, password, actions: [], contacts: [Agent] = [], verify_security=False):
        super().__init__(jid, password, verify_security)
        self.actions = actions
        self.contacts = contacts
