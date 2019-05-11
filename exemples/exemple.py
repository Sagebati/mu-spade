import logging

from agent.coordination import CoordinateAction, Action

pwd = "dummy"
jwd1 = "turtle_a@172.27.96.17"
jwd2 = "turtle_b@172.27.96.17"

action_coord = CoordinateAction(goal="PushTheBox", actions={
    "action1": [
        Action(name="Preparer", function=lambda a: print("Preparer l'action")),
        Action(name="Push", function=lambda a: print("Pousser la boite"))
    ],
    "action2": [
        Action(name="Preparer2", function=lambda a: print("Preparer l'action")),
        Action(name="Push2", function=lambda a: print("Pousser la boite"))]
})

exemple1 = [
    Action("Bouger1", function=lambda a: print("Je bouger ver x,y")),
    Action("Bouger2", function=lambda a: print("Je bouger ver x,y")),
    Action("Bouger3", function=lambda a: print("Je bouger ver x,y")),
    action_coord
]

if __name__ == '__main__':
    from agent.Turtle import Turtle

    turtleBot_a = Turtle(jwd1, pwd, exemple1, [jwd2])
    turtleBot_b = Turtle(jwd2, pwd, exemple1, [jwd1])
    turtleBot_a.start()
    turtleBot_a.web.start(hostname="127.0.0.1", port="10000")
    turtleBot_b.start()
    turtleBot_b.web.start(hostname="127.0.0.1", port="10001")
    turtleBot_b.stop()
    turtleBot_a.stop()
