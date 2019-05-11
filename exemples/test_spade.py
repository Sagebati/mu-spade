import rospy

from agent.coordination import Action
from turtle.GoToMapPose import GoToMapPose

pwd = "dummy"
jwd1 = "turtle_a@172.27.96.17"


def action_test(a):
    print("Test spade reussi")


actions = [
    Action("Bouger1", function=action_test),
]

if __name__ == '__main__':
    from agent.Turtle import Turtle

    turtleBot_a = Turtle(jwd1, pwd, actions)
    turtleBot_a.start()
    turtleBot_a.web.start(hostname="127.0.0.1", port="10000")
    turtleBot_a.stop()