import rospy
import logging

from agent.coordination import Action, CoordinateAction
from turtle.GoToMapPose import GoToMapPose

logging.basicConfig(level=logging.INFO)

pwd = "dummy"
jwd1 = "turtle_a@172.27.96.17"


def goto_simpl(a, x, y):
    try:
        navigator = GoToMapPose()

        # Customize the following values so they are appropriate for your location
        position = {'x': x, 'y': y}
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


action_coord = CoordinateAction(goal="PushTheBox", actions={
    "action1": [
        Action(name="Push", function=lambda a: goto_simpl(a, x=4.0, y=-1.0))
    ],
    "action2": [
        Action(name="Push2", function=lambda a: goto_simpl(a, x=3.5, y=-1.0))]
})

actions = [
    Action("Move1", function=lambda a: goto_simpl(a, 3.5, -0.2)),
    action_coord
]

if __name__ == '__main__':
    from agent.Turtle import Turtle

    rospy.init_node('nav_test', anonymous=False)
    turtleBot_a = Turtle(jwd1, pwd, actions, contacts=["turtle_b@172.27.96.17"])
    turtleBot_a.start()
    turtleBot_a.web.start(hostname="127.0.0.1", port="10001")
    turtleBot_a.stop()
