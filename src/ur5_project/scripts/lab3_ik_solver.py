#!/usr/bin/env python3

import rospy
import numpy as np
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from core import IKinSpace

# ✅ Screw axes for UR5 in space frame
S = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, -1, 0],
    [0, -0.089159, -0.089159, -0.089159, 0, 0.089159],
    [0, 0, 0.425, 0.81725, 0.81725, 0.81725],
    [0, 0, 0, 0, 0.10915, 0]
])

# ✅ Home configuration matrix M
M = np.array([
    [-1,  0,  0,  0.81725],
    [ 0,  0,  1,  0.19145],
    [ 0,  1,  0,  0.089159],
    [ 0,  0,  0,  1]
])

def quaternion_to_rotation_matrix(q):
    x, y, z, w = q
    return np.array([
        [1 - 2*(y**2 + z**2), 2*(x*y - z*w),     2*(x*z + y*w)],
        [2*(x*y + z*w),     1 - 2*(x**2 + z**2), 2*(y*z - x*w)],
        [2*(x*z - y*w),     2*(y*z + x*w),     1 - 2*(x**2 + y**2)]
    ])

def pose_callback(msg):
    rospy.loginfo("Received pose!")
    p = msg.pose.position
    o = msg.pose.orientation

    R = quaternion_to_rotation_matrix([o.x, o.y, o.z, o.w])
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = [p.x, p.y, p.z]

    # Try different initial guesses
    guesses = [
        np.array([0.5, -0.5, 0.5, -0.5, 0.5, -0.5])]

    for guess in guesses:
        thetalist_sol, success = IKinSpace(S, M, T, guess, 0.001, 0.001)
        print("succes:",success)
        if success:
            js = JointState()
            js.header = Header()
            js.header.stamp = rospy.Time.now()
            js.name = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"]
            js.position = thetalist_sol.tolist()

            pub.publish(js)
            rospy.loginfo("Published joint state: %s", np.round(thetalist_sol, 2))
            return

    rospy.logwarn("Inverse kinematics failed to converge with all guesses.")

def main():
    global pub
    rospy.init_node("ur5_ik_solver", anonymous=True)
    rospy.Subscriber("/goal_pose", PoseStamped, pose_callback)
    pub = rospy.Publisher("/joint_states", JointState, queue_size=10)
    rospy.spin()

if __name__ == "__main__":
    main()
