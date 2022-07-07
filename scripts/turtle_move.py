 #!/usr/bin/env python3

#from ast import Break
import math
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
#from std_srvs import Empty

# 
x = 0
y = 0
z = 0
yaw = 0


# subscriber to the Pose topic (turtle/Pose)
#rostopic info turtle1/pose
#rosmsg show turtlesim/Pose

def poseCallback(pose_message):
    global x, y, z, yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta

def euc_distance(x0, x, y0, y):
    distance = abs(0.5 * math.sqrt(((x - x0) ** 2) + ((y - y0) ** 2)))
    return distance

def turtle_rotate(angle, angular_speed, is_clockwise):
    angle_rads = math.radians(angle)
    yaw0 = yaw

    cmd_velocity = Twist()
    cmd_velocity.linear.x = 0

    if(is_clockwise):
        cmd_velocity.angular.z = -abs(angular_speed)
    else:
        cmd_velocity.angular.z = abs(angular_speed)

    loop_rate = rospy.Rate(10)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    angles_rotated = 0.0

    while(True):
        rospy.loginfo("Turtle is moving")
        velocity_publisher.publish(cmd_velocity)
        loop_rate.sleep()

        angles_rotated = abs(yaw - yaw0)
        rospy.loginfo(angles_rotated)
        if(angles_rotated >= angle_rads):
          rospy.loginfo("Destination reached")  
          break
        #rospy.spin()

    cmd_velocity.angular.z = 0.0
    velocity_publisher.publish(cmd_velocity)       


def turtle_move(distance, speed, is_forward):
    global x, y
    x0 = x
    y0 = y

    cmd_velocity = Twist()

    if(is_forward):
        cmd_velocity.linear.x = abs(speed)
    else:
        cmd_velocity.linear.x = -abs(speed)

    loop_rate = rospy.Rate(10)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    distance_moved = 0.0

    while(True):
        rospy.loginfo("Turtle is moving")
        velocity_publisher.publish(cmd_velocity)
        loop_rate.sleep()

        distance_moved = euc_distance(x0, x, y0, y)
        rospy.loginfo(distance_moved)
        if(distance_moved >= distance):
          rospy.loginfo("Destination reached")  
          break
        #rospy.spin()

    cmd_velocity.linear.x = 0.0
    velocity_publisher.publish(cmd_velocity)



if __name__ == '__main__':
    try:
        rospy.init_node('turtle_move', anonymous=True)
        # topic name, message type, queue_size
        velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        # topic name, message type, callback function
        pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, poseCallback)
        time.sleep(2)

        action = int(input("Select Action : 1-Move, 2-Rotate: "))

        if action == 1:
            is_forward = True
            distance = float(input("Enter the required distance: "))
            speed = float(input("Enter the required speed: "))
            direction = float(input("1- Forward, 0- Backwards: "))

            if not direction == 1 and not direction == 0:
                is_forward = True
            elif direction == 1:
                is_forward = True
            elif direction == 0:
                is_forward = False

            turtle_move(distance, speed, is_forward)
            
        elif action == 2:
            is_clockwise = True
            angle = float(input("Enter the to rotate in degrees: "))
            speed = float(input("Enter the required speed: "))
            direction = float(input("1- Clockwise, 0- Anti-Clockwise: "))

            if not direction == 1 and not direction == 0:
                is_clockwise = True
            elif direction == 1:
                is_clockwise = True
            elif direction == 0:
                is_clockwise = False

            turtle_rotate(angle, speed, is_clockwise)
        else:
            print("Wrong Action selected")

        #turtle_move(2.0, 0.2, False)
        #turtle_rotate(180, 0.2, False)

    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated abruptly")
