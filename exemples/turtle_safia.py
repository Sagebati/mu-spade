import logging

from agent.coordination import CoordinateAction, Action

logging.basicConfig(level=logging.INFO)

pwd = "dummy"
jwd1 = "raphael@127.0.0.1"
jwd2 = "safia@127.0.0.1"

action_coord = CoordinateAction(goal="PushTheBox", actions={
    "action1": [
        Action(name="Preparer", function=lambda a: print(a.jid, ": Prepare to push the box")),
        Action(name="Push", function=lambda a: print(a.jid, ": Push the box"))
    ],
    "action2": [
        Action(name="Preparer2", function=lambda a: print(a.jid, ": Preapare to push the box")),
        Action(name="Push2", function=lambda a: print(a.jid, ": Push the box"))]
})

exemple1 = [
    Action("Move1", function=lambda a: print(a.jid, ": I move to x,y")),
    Action("Move2", function=lambda a: print(a.jid, ": I move to x,y")),
    Action("Move3", function=lambda a: print(a.jid, ": I move to x,y")),
    action_coord
]

if __name__ == '__main__':
    from agent.Turtle import Turtle

    turtleBot_b = Turtle(jwd2, pwd, exemple1, [jwd1])
    turtleBot_b.start()
    turtleBot_b.web.start(hostname="127.0.0.1", port="10001")
    turtleBot_b.stop()
