

class CoordinateAction:
    """
    Defines an action that need multiple agents to resolve
    the goal must be unique
    """

    def __init__(self, goal, actions: {}):
        """
        :type goal : str
        :type actions : [[Action]]
        """
        self.name = goal
        self.goal = goal
        self.actions = actions
