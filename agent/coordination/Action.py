import asyncio


class Action:
    """
    Represents an action.
    """

    def __init__(self, name="", function=None):
        super().__init__()
        self.name = name
        self.todo = function

    async def _todo(self, agent):
        self.todo(agent)

    async def do(self, agent):
        await asyncio.create_task(self._todo(agent))
