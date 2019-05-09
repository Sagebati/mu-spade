

class CoordinateAction:
    """
    Defines an action that need multiple agents to resolve
    the goal must be unique between the agents resolving this.
    """

    def __init__(self, goal, actions: {}):
        """
        :param actions: Dictionary of actions syncronised
        :type goal : str the id
        :type actions : [[Action]]
        """
        self.name = goal
        self.goal = goal
        self.actions = actions
