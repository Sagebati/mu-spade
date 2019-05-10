import logging

from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State

from agent.behaviours.DoingCoordinateAction import DoingCoordinateAction
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
        self.logger = logging.getLogger()
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
        self.logger.info("Initializing the fsm behaviour")

    async def on_end(self):
        self.logger.info("Behaviour finished")
        await self.agent.stop()


class Init(State):
    def __init__(self):
        super().__init__()

    async def run(self):
        logger = logging.getLogger("agent.behaviours.Init")
        logger.info("Initialising the robot")
        logger.info("First state of the behaviour")


class DoingAction(State):
    def __init__(self, action: Action):
        super().__init__()
        self.actionTodo = action
        self.logger = logging.getLogger()

    async def on_start(self):
        self.logger.info("Begin doing the actions state")

    async def run(self):
        self.actionTodo.do()
