#!/usr/bin/env python3

import rospy
import numpy as np
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Pose
from std_msgs.msg import Header
from tf.transformations import quaternion_from_matrix

# UR5 DH Parameters
d1 = 0.089159
a2 = 0.425
a3 = 0.39225
d4 = 0.10915
d5 = 0.09465
d6 = 0.0823

def dh_transform(a, alpha, d, theta):
    return np.array([
        [np.cos(theta), -np.sin(theta)*np.cos(alpha),  np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
        [np.sin(theta),  np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
        [0,              np.sin(alpha),                np.cos(alpha),               d],
        [0,              0,                            0,                           1]
    ])

def compute_fk(thetalist):
    θ1, θ2, θ3, θ4, θ5, θ6 = thetalist
    T1 = dh_transform(0,        np.pi/2, d1, θ1)
    T2 = dh_transform(-a2,      0,       0,  θ2)
    T3 = dh_transform(-a3,      0,       0,  θ3)
    T4 = dh_transform(0,        np.pi/2, d4, θ4)
    T5 = dh_transform(0,       -np.pi/2, d5, θ5)
    T6 = dh_transform(0,        0,       d6, θ6)
    return T1 @ T2 @ T3 @ T4 @ T5 @ T6

def joint_callback(msg):
    if len(msg.position) < 6:
        rospy.logwarn("Expected 6 joint values, got fewer.")
        return

    thetalist = np.array(msg.position[:6])
    T = compute_fk(thetalist)

    position = T[:3, 3]
    quaternion = quaternion_from_matrix(T)

    # Optional: publish FK pose
    pose_msg = Pose()
    pose_msg.position.x = position[0]
    pose_msg.position.y = position[1]
    pose_msg.position.z = position[2]
    pose_msg.orientation.x = quaternion[0]
    pose_msg.orientation.y = quaternion[1]
    pose_msg.orientation.z = quaternion[2]
    pose_msg.orientation.w = quaternion[3]
    pose_pub.publish(pose_msg)

    # ❌ Do NOT broadcast to ee_link manually!
    # robot_state_publisher does this using joint_states + URDF

def main():
    global pose_pub
    rospy.init_node("ur5_forward_kinematics_node", anonymous=True)
    pose_pub = rospy.Publisher("/fk_pose", Pose, queue_size=10)
    rospy.Subscriber("/joint_states", JointState, joint_callback)
    rospy.loginfo("UR5 Forward Kinematics Node started.")
    rospy.spin()

if __name__ == "__main__":
    main()
