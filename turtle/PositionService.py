import rospy
import tf


class PositionService:
    @staticmethod
    def get_current_position():
        listener = tf.TransformListener()
        # rate = rospy.Rate(1)
        # for i in range(1, 10):
        #    try:
        #        (trans, rot) = listener.lookupTransform("/map", "/base_link", rospy.Time(0))
        #        return trans, rot
        #    except KeyboardInterrupt:
        #        return [0,0,0], [0,0,0,1]
        #    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        #        print "exception1"
        #        print i
        #        rate.sleep()
        # return [0,0,0], [0,0,0,1]

        try:
            # wait for the transform to be found
            listener.waitForTransform("/map", "/base_link", rospy.Time(0), rospy.Duration(10.0))

            # Once the transform is found,get the initial_transform transformation.
            # (trans,rot) = listener.lookupTransform('/base_footprint', '/odom', rospy.Time(0))
            (trans, rot) = listener.lookupTransform("/map", "/base_link", rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.Duration(1.0)

        return trans, rot

    @staticmethod
    def get_behind_position(position):
        p = position
        p["position"][0] = p["position"][0] - 0.1
        return p

    @staticmethod
    def get_current_position_as_map():
        (pos, quat) = PositionService.get_current_position()
        position = {
            "position": {"x": pos[0], "y": pos[1]},
            "quaterion": {"r1": quat[0], "r2": quat[1],
                          "r3": quat[2], "r4": quat[3]}
        }
        return position


if __name__ == "__main__":
    rospy.init_node("test_positionService", anonymous=False)
    (trans, rot) = PositionService.get_current_position()
    print("getCurrentPosition(): ", str(trans))
    print("getCurrentPositionAsMap(): ", PositionService.get_current_position_as_map())
