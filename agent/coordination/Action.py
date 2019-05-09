class Action:
    """
    Behaviour to do the action.
    """

    def __init__(self, name="", function=None):
        """
        """
        super().__init__()
        self.name = name
        self.todo = function

    def do(self):
        self.todo(self)
