import rospy

from agent.coordination import Action
from turtle.GoToMapPose import GoToMapPose

pwd = "dummy"
jwd1 = "turtle_a@172.27.96.17"


def action_test(a):
    try:
        rospy.init_node('nav_test', anonymous=False)
        navigator = GoToMapPose()

        # Customize the following values so they are appropriate for your location
        position = {'x': 4.50, 'y': -0.20}
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
    Action("Bouger1", function=lambda a: action_test),
]

if __name__ == '__main__':
    from agent.Turtle import Turtle

    turtleBot_a = Turtle(jwd1, pwd, actions)
    turtleBot_a.start()
    turtleBot_a.web.start(hostname="127.0.0.1", port="10000")
    turtleBot_a.stop()
