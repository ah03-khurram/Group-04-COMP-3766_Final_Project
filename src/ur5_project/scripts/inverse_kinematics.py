#!/usr/bin/env python3

import rospy
import numpy as np
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Pose
from std_msgs.msg import Header

def analytical_ik_solver(T):
    """
    Solves analytical IK for UR5 using geometric approach.
    Input: T (4x4 numpy array) - desired end-effector pose.
    Output: thetalist (1D numpy array of 6 joint angles), success (bool)
    """
    # UR5 dimensions from datasheet
    d1 = 0.089159
    a2 = 0.425
    a3 = 0.39225
    d4 = 0.10915
    d5 = 0.09465
    d6 = 0.0823

    # Extract position and orientation from T
    px, py, pz = T[0, 3], T[1, 3], T[2, 3]
    ax, ay, az = T[0, 2], T[1, 2], T[2, 2]

    # Wrist center position
    wx = px - d6 * ax
    wy = py - d6 * ay
    wz = pz - d6 * az

    # θ1
    theta1 = np.arctan2(wy, wx)

    # Calculate planar distance and vertical offset
    r = np.sqrt(wx**2 + wy**2)
    s = wz - d1

    D = (r**2 + s**2 - a2**2 - a3**2) / (2 * a2 * a3)
    if abs(D) > 1:
        return None, False  # Not reachable

    theta3 = np.arctan2(-np.sqrt(1 - D**2), D)
    theta2 = np.arctan2(s, r) - np.arctan2(a3 * np.sin(theta3), a2 + a3 * np.cos(theta3))

    # Build rotation matrices
    def rot_z(theta): return np.array([[np.cos(theta), -np.sin(theta), 0],
                                       [np.sin(theta), np.cos(theta), 0],
                                       [0, 0, 1]])
    def rot_y(theta): return np.array([[np.cos(theta), 0, np.sin(theta)],
                                       [0, 1, 0],
                                       [-np.sin(theta), 0, np.cos(theta)]])

    # Compute R03
    R03 = rot_z(theta1) @ rot_y(theta2) @ rot_y(theta3)
    R36 = R03.T @ T[:3, :3]

    # θ4, θ5, θ6 from R36
    theta5 = np.arccos(R36[2, 2])
    if abs(np.sin(theta5)) < 1e-6:
        theta4 = 0
        theta6 = np.arctan2(-R36[1, 0], R36[0, 0])
    else:
        theta4 = np.arctan2(R36[1, 2], R36[0, 2])
        theta6 = np.arctan2(R36[2, 1], -R36[2, 0])

    return np.array([theta1, theta2, theta3, theta4, theta5, theta6]), True

# Helper to convert quaternion into rotation matrix
def quaternion_to_rotation_matrix(q):
    x, y, z, w = q
    return np.array([
        [1 - 2*(y**2 + z**2), 2*(x*y - z*w),     2*(x*z + y*w)],
        [2*(x*y + z*w),     1 - 2*(x**2 + z**2), 2*(y*z - x*w)],
        [2*(x*z - y*w),     2*(y*z + x*w),     1 - 2*(x**2 + y**2)]
    ])

# Callback for pose updates
def pose_callback(msg):

    # Extract position and orientation from the message
    p = msg.position
    o = msg.orientation

    R = quaternion_to_rotation_matrix([o.x, o.y, o.z, o.w])
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = [p.x, p.y, p.z]

    theta, success = analytical_ik_solver(T)

    if success:
        js = JointState()
        js.header = Header()
        js.header.stamp = rospy.Time.now()
        js.name = [f"joint{i+1}" for i in range(6)]
        js.position = theta.tolist()
        pub.publish(js)
    else:
        rospy.logwarn("IK solution not found for given pose.")

def main():
    global pub
    rospy.init_node("ur5_analytical_ik_solver", anonymous=True)
    pub = rospy.Publisher("/joint_states", JointState, queue_size=10)

    rospy.Subscriber("/goal_pose", Pose, pose_callback)
    rospy.loginfo("Analytical IK solver node ready. Listening to /goal_pose...")
    rospy.spin()

if __name__ == "__main__":
    main()