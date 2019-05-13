import rospy
import logging

from agent.coordination import Action
from turtle.GoToMapPose import GoToMapPose

logging.basicConfig(level=logging.INFO)

pwd = "dummy"
jwd1 = "turtle_a@172.27.96.17"


def point_a(a):
    goto_simpl(a, 4.5, -0.2)


def point_b(a):
    goto_simpl(a, 0, 0)


def goto_simpl(a, x, y):
    try:
        navigator = GoToMapPose()

        # Customize the following values so they are appropriate for your location
        position = {'x': x, 'y': -y}
        quaternion = {'r1': 0.000, 'r2': 0.000, 'r3': 0.000, 'r4': 1.000}

        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Hooray, reached the desired pose")
        else:
            rospy.loginfo("The base failed to reach the desired pose")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)
    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")


actions = [
    Action("Bouger1", function=point_a),
    Action("Bouger2", function=point_b),
    Action("Test1", function=lambda a: print("Bouger accompli"))
]

if __name__ == '__main__':
    from agent.Turtle import Turtle

    rospy.init_node('nav_test', anonymous=False)
    turtleBot_a = Turtle(jwd1, pwd, actions)
    turtleBot_a.start()
    turtleBot_a.web.start(hostname="127.0.0.1", port="10000")
    turtleBot_a.stop()
