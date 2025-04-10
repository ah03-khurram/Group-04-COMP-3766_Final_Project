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
)

## Declare your catkin package
catkin_package()

## Specify include directories (optional unless using C++ code)
include_directories(
  ${catkin_INCLUDE_DIRS}
)

# ## Install Python scripts (if you add any later like goal_pose_node.py)
# catkin_install_python(PROGRAMS
#   # scripts/goal_pose_node.py
#   # scripts/forward_kinematics.py
#   # scripts/inverse_kinematics.py
#   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
# )