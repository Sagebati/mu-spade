from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
from spade.template import Template

from agent.coordination import Action, CoordinateAction


class GeneralBehaviour(FSMBehaviour):
    """The behaviour of the agent"""
    def __init__(self, actions: [Action], contacts: [Agent] = []):
        """
        Creates an State for each action on the FSMBehaviour.
        :param actions: The list of actions
        :param contacts: the contacts of the agent
        """
        super().__init__()
        init_state = Init()
        self.add_state(name="Init", state=init_state, initial=True)
        pre: Action = None
        pre_state: State = None
        for action in actions:
            state_to_add = DoingCoordinateAction(action, contacts) if isinstance(action,
                                                                                 CoordinateAction) else DoingAction(
                action)
            self.add_state(name=action.name, state=state_to_add)
            if pre is None:
                self.add_transition(source="Init", dest=action.name)
                init_state.set_next_state(action.name)
            else:
                self.add_transition(source=pre.name, dest=action.name)

            if pre_state is not None:
                pre_state.set_next_state(action.name)
            pre = action
            pre_state = state_to_add

    async def on_start(self):
        print("Initializing the fsm behaviour")

    async def on_end(self):
        print("Behaviour finished")
        await self.agent.stop()


class Init(State):
    def __init__(self):
        super().__init__()

    async def run(self):
        print("Initialising the robot")
        print("First state of the behaviour")


class DoingAction(State):
    def __init__(self, action: Action):
        super().__init__()
        self.actionTodo = action

    async def on_start(self):
        print("Do the action")

    async def run(self):
        self.actionTodo.do()


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

    async def __second_handshake(self):
        print("Waiting for instructions")
        instructions_message = await self.receive(50)
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
        print("Traiter message", message.body)
        template = Template()
        template.set_metadata("performative", "proposal")
        if template.match(message):
            if message.body == self.coord_action.goal:
                print("Accept proposal the action it's the same goal ")
                accept_pop = message.make_reply()
                accept_pop.set_metadata("performative", "accept-proposal")
                await self.send(accept_pop)
                await self.__second_handshake()
            else:
                print("Not the same goal")
                accept_pop = message.make_reply()
                accept_pop.set_metadata("performative", "reject-proposal")
                await self.send(accept_pop)

    async def __prepare_action(self):
        """Search an agent to collaborate for the coordinate action, then tries to connect with him,
            doesn't begin the action if there is no worker.
         """
        import random
        while len(self.actions_remaining) != 0:
            print("Search agent who has the same goal", self.coord_action.goal)
            msg = await self.receive(random.randint(1, 20))
            if msg:
                await self.__handle_handshake(msg)
                break
            else:
                for agent_jid in self.contacts:
                    print("Try with ", agent_jid)
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
        print("Send message to ", agent_jid)
        await self.send(message_to_send)
        print("Waiting for the reponse")
        message = await self.receive(100)
        if message is None:
            print("The dest didn't respond")
        else:
            t = Template()
            t.sender = agent_jid
            t.set_metadata("performative", "accept-proposal")
            if t.match(message):
                print(agent_jid, " accepted the proposal")
                await self.first_handshake(message)

    async def first_handshake(self, message: Message):
        """
        Send the first message for the handshake, with the action I choose to do.
        Then the agent send back his action.
        :param message:
        :return:
        """
        to_send = message.make_reply()
        my_action_key = self.__pick_my_actions()
        to_send.set_metadata("performative", "inform")
        to_send.body = my_action_key
        print("Sending my chose action to the other agent")
        await self.send(to_send)
        reply = await self.receive(100)
        reply_verif = Template()
        reply_verif.set_metadata("performative", "inform")
        if reply_verif.match(reply):
            print("Received the action of the other agent")
            self.my_actions = self.coord_action.actions[my_action_key]
            self.actions_remaining.remove(my_action_key)
            self.actions_remaining.remove(reply.body)

    async def on_start(self):
        """
        Search for helpers and populates helpers.
        :return:
        """
        print("Start coordinate action")

    async def run(self):
        print("Searching for helpers")
        await self.__prepare_action()
        for a in self.my_actions:
            a.do()
