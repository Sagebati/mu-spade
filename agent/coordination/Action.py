import asyncio


class Action:
    """
    Represents an action.
    """

    def __init__(self, name="", function=None):
        super().__init__()
        self.name = name
        self.todo = function

    async def do(self):
        await asyncio.create_task(self.todo(self))
