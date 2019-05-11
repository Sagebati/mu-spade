import logging

from spade.agent import Agent
from spade.behaviour import State
from spade.message import Message
from spade.template import Template

from agent.coordination import CoordinateAction

logger = logging.getLogger("agent.behaviours.DoingCoordinateAction")


async def empty_queue(state):
    msg = await state.receive()
    while msg is not None:
        msg = await state.receive()
        logger.info("Cleared the queue of {}".format(msg.body))


class DoingCoordinateAction(State):
    """
    Do an action that need more agent to resolve.
    """

    def __init__(self, coord_action: CoordinateAction, contacts: [Agent] = []):
        """
        :param coord_action: CoordinateAction
        """
        super().__init__()
        self.coord_action = coord_action
        self.contacts = contacts
        self.actions_remaining = list(self.coord_action.actions.keys())
        self.my_actions = None

    def __pick_my_actions(self):
        import random
        action_choose_key = random.choice(self.actions_remaining)
        return action_choose_key

    async def __resolution_handshake(self):
        logger.info("Waiting for instructions")
        instructions_message = await self.receive(100)
        to_reveive = Template()
        to_reveive.set_metadata("performative", "inform")
        if to_reveive.match(instructions_message):
            # Receiving what the other agent will do
            foreign_action_choose = instructions_message.body
            self.actions_remaining.remove(foreign_action_choose)
            message = instructions_message.make_reply()
            message.set_metadata("performative", "inform")
            action_choose_key = self.__pick_my_actions()
            message.body = action_choose_key
            self.my_actions = self.coord_action.actions[action_choose_key]
            self.actions_remaining.remove(action_choose_key)
            await self.send(message)

    async def __handle_handshake(self, message):
        """
        Method when the agent receives an handshake. It can accept it or reject it based on the goal of the coordinate
        action.
        :param message: the message to handle
        """
        logger.info("Traiter message {}".format(message.body))
        template = Template()
        template.set_metadata("performative", "proposal")
        if template.match(message):
            if message.body == self.coord_action.goal:
                logger.info("Accept proposal, the action it's the same goal ")
                accept_pop = message.make_reply()
                accept_pop.set_metadata("performative", "accept-proposal")
                await self.send(accept_pop)
                logger.info("Send accept-proposal to {}".format(message.sender))
                await self.__resolution_handshake()
            else:
                logger.info("Not the same goal")
                accept_pop = message.make_reply()
                accept_pop.set_metadata("performative", "reject-proposal")
                await self.send(accept_pop)

    async def __prepare_action(self):
        """
            Search an agent to collaborate for the coordinate action, then tries to connect with him,
            doesn't begin the action if there is no worker.
         """
        import random
        while len(self.actions_remaining) != 0:
            logger.info("Search agent who has the same goal: {}".format(self.coord_action.goal))
            logger.info("Waiting for some agent to contact me")
            await empty_queue(self)
            msg = await self.receive(random.randint(10, 50))
            if msg:
                await self.__handle_handshake(msg)
                break
            else:
                logger.info("Doesn't receive any messages")
                for agent_jid in self.contacts:
                    logger.info("Try with {}".format(agent_jid))
                    await self.__begin_handshake(agent_jid)

    async def __begin_handshake(self, agent_jid):
        """
        Begin the negociation with the agent, send the goal and wait for a reponse.
        if the agent accepts then launches the handshake.
        :param agent_jid: the agent to communicate
        """
        message_to_send = Message(to=agent_jid)
        message_to_send.set_metadata("performative", "proposal")
        message_to_send.body = self.coord_action.goal
        logger.info("Send message to {}".format(agent_jid))
        await self.send(message_to_send)
        logger.info("Waiting for the reponse")
        await empty_queue(self)
        message = await self.receive(25)
        if message is None:
            logger.info("The dest didn't respond")
        else:
            t = Template()
            t.set_metadata("performative", "accept-proposal")
            if t.match(message):
                logger.info("{} Accepted the proposal".format(agent_jid))
                await self.first_handshake(message)
            else:
                logger.warning("The message doesn't match the waiting")

    async def first_handshake(self, message: Message):
        """
        Send the first message for the handshake, with the action I choose to do.
        Then the agent send back his action.
        :param message:
        """
        to_send = message.make_reply()
        my_action_key = self.__pick_my_actions()
        to_send.set_metadata("performative", "inform")
        to_send.body = my_action_key
        logger.info("Sending my chose action to the other agent")
        await self.send(to_send)
        reply = await self.receive(100)
        reply_verif = Template()
        reply_verif.set_metadata("performative", "inform")
        if reply_verif.match(reply):
            logger.info("Received the action of the other agent")
            self.my_actions = self.coord_action.actions[my_action_key]
            self.actions_remaining.remove(my_action_key)
            self.actions_remaining.remove(reply.body)

    async def on_start(self):
        """
        Prepare the coordinate actions searching for workers.
        """
        logger.info("Start coordinate action")
        logger.info("Preparing")
        await self.__prepare_action()

    async def run(self):
        for a in self.my_actions:
            await a.do()
