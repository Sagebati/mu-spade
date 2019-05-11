import logging

from agent.coordination import CoordinateAction, Action

pwd = "dummy"
jwd1 = "turtle_a@172.27.96.17"


def action_test(a):
    a.movement_service.goto()


actions = [
    Action("Bouger1", function=lambda a: print("Je bouger ver x,y")),
]

if __name__ == '__main__':
    from agent.Turtle import Turtle

    turtleBot_a = Turtle(jwd1, pwd, actions)
    turtleBot_a.start()
    turtleBot_a.web.start(hostname="127.0.0.1", port="10000")
    turtleBot_a.stop()
