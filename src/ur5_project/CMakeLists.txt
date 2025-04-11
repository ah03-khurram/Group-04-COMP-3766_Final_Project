cmake_minimum_required(VERSION 3.0.2)
project(ur5_project)

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  joint_state_publisher_gui
  robot_state_publisher
  rospy
  std_msgs
  sensor_msgs
  geometry_msgs
  xacro
  urdf
  tf
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

<<<<<<< HEAD
# catkin_install_python(PROGRAMS
# #   scripts/core.py
# #   scripts/goal_pose_node.py
# #   scripts/lab3_ik_solver.py
# #   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
# )

catkin_install_python(PROGRAMS
  scripts/analytical_ik_solver.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
=======
## Install Python scripts (if you add any later like goal_pose_node.py)
catkin_install_python(PROGRAMS
  scripts/goal_pose_node.py
  scripts/inverse_kinematics.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
>>>>>>> b21607ab6a24027eaa23da3c678ec158e13e1e4f
