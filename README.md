# turtlesim_move
This python ROS node implementation controls the movement of the turtle from the ROS Turtlesim Node. The user is prompted for the action desired, that is, linear motion or angular motion. Depending on the user's choice, the user is again prompted for parameter values to complete the action including distance to travel and direction for travel.

# Requiremets
## Turtlesim ROS Node
1. Make sre you have Ros Installed on your machine. Otherwise you can install ROS from [the link here](http://wiki.ros.org/noetic/Installation/Ubuntu)
2. Install turtlesim from [the link here](http://wiki.ros.org/turtlesim)

# Running the application
1. Clone the repository in your /src folder inside your catkin warkspace
2. Build the node using catkin_make
3. start the turtlesim node
```
rosrun turtlesim turtlesim_node
```
4. start the turtle_move node
```
rosrun turtlesim_move turtle_move.py
```

You can also run the turtle_move.py script directly, say from your catkin workspace
```
python3 src/turtlesim_move/scripts/turtle_move.py
```