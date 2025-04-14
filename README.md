# Robot Design - Universal Robots' UR5 6R Robot Arm

This Repository contain the dev container used by `COMP 3766 Group 4` to implememnt `UR5 6R Robot as the final project`.

> ### Devcontainer instructions:

Install VSCode, devcontainer extension and Docker.
Clone the repository:

    $ git clone git@github.com:ah03-khurram/Group-04-COMP-3766_Final_Project.git

On Windows:

    $ git clone -c core.autocrlf=false https://github.com/ah03-khurram/Group-04-COMP-3766_Final_Project.git

Open the folder in VSCode.
Select the option "Reopen in container" from the green square at the bottom or from the menu.  
Wait it finishing loading the folder in Docker (it can take a while).

--- 

> ## Running the Project:

To run the UR5 simulation and test the kinematic nodes in ROS, follow the steps below. Each major component should be run in a **separate terminal** to ensure all ROS nodes operate concurrently.

### **Step 1: Build the Workspace**
- Open a terminal in the root of the ROS workspace (i.e. `/workspaces /Group-04-COMP-37666_Final_Project`) and run:
```bash
catkin_make
```

### **Step 2: Source the Workspace**
Before running any launch files or nodes, **source the setup script**:
```bash
source devel/setup.bash
```

---

### **Step 3: Launch RViz with UR5 Model**
Open a **new terminal**, then run:
```bash
roslaunch ur5_project ur5_project.launch
```
This will load the URDF model into RViz and start the robot_state_publisher.
- **Verify the Robot in RViz.** Open `http://localhost:6080/` on your browser. This page shows the GUI applications from the project. Use the ***joint_state_publisher_gui*** to manipulate the joints and observe their movement.
---

### **Step 4: Run the Inverse Kinematics Node**
- Open the `src/ur5_project/launch/ur5_project.launch` and
comment out the `line number 10` (“*Joint State Publisher
GUI*”).
- Redo the steps 1 - 3
- Open **another new terminal**, then run:
```bash
source devel/setup.bash
rosrun ur5_project inverse_kinematics.py
```
This node will listen for desired poses on `/goal_pose` and publish joint angles on `/joint_states`.

---

### **Step 5: Run the Goal Pose Publisher (for IK)**
Open **another new terminal**, then run:
```bash
source devel/setup.bash
rosrun ur5_project goal_pose_node.py
```
This node publishes a fixed goal pose to `/goal_pose`, triggering the inverse kinematics solver.
- **Verify the Robot in RViz.** Open `http://localhost:6080/` on your browser. Observe the robot’s end-effector’s new position relative to the joints.

---

### **Step 6: Run the Forward Kinematics Simulation (Sequence of Joint Configurations)**
- Terminate the `Inverse Kinematics terminals` (i.e. terminals for **goal_pose_node.py** and **inverse_kinematics.py**)
- Open **another terminal**, then run:
```bash
source devel/setup.bash
rosrun ur5_project forward_kinematics_simulator.py
```
- This is a node that publishes a sequence of joint configurations to `/joint_states`, allowing the UR5 model in RViz to animate through different poses.
- **Verify the Robot in RViz.** Open `http://localhost:6080/` on your browser. Observe the robot’s joint’s movement simulation...

---
