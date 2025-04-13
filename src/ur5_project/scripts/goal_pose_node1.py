#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import numpy as np

def publish_joint_states():
    rospy.init_node("ur5_fk_joint_publisher", anonymous=True)
    joint_pub = rospy.Publisher("/joint_states", JointState, queue_size=10)
    rate = rospy.Rate(1)  # 1 Hz

    # ✅ Example joint configurations (you can modify these)
    joint_configs = [
        [0, -1.57, 1.57, 0, 1.57, 0],   # Bent elbow
        [0.5, -1.2, 1.2, 0.5, 1.0, 0.2],  # Another pose
        [-0.5, -0.8, 0.8, -0.5, 0.5, -0.2]  # Reverse pose
    ]

    idx = 0
    while not rospy.is_shutdown():
        joints = JointState()
        joints.header = Header()
        joints.header.stamp = rospy.Time.now()
        joints.name = [f"joint{i+1}" for i in range(6)]
        joints.position = joint_configs[idx % len(joint_configs)]

        joint_pub.publish(joints)
        rospy.loginfo(f"Published Joint Configuration: {np.round(joints.position, 2)}")

        idx += 1
        rate.sleep()

if __name__ == "__main__":
    try:
        publish_joint_states()
    except rospy.ROSInterruptException:
        pass
