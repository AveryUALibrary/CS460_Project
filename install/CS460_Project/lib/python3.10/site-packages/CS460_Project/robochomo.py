import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from rclpy.qos import ReliabilityPolicy, QoSProfile
import math
import random
import os
from time import time, sleep

# Constants
SPEED_1 = 0.075 # m/s
SPEED_2 = 0.15 # m/s
ROTAION_SPEED_1 = math.radians(30) # degrees/s
ROTAION_SPEED_2 = math.radians(120) # degrees/s
FOLDER_NAME = 'sim_data/'
# FOLDER_NAME = 'lab_data/'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__)).split('install')[0] + FOLDER_NAME
# File name format: speed_{speed_state}_trial_{trial_type}_num_{trial_num}.txt


def grab_trial_file_name(speed_state, trial_type):
    """
    Grab all the files that match the speed state and trial type.
    Then find the highest number and return the next number.
    """
    file_name = f'speed_{speed_state}_trial_{trial_type}_num_'
    files = os.listdir(CURRENT_DIR)
    files = [file for file in files if file.startswith(file_name)]
    if not files:
        return file_name + '0.txt'
    files = sorted(files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
    return file_name + str(int(files[-1].split('_')[-1].split('.')[0]) + 1) + '.txt'

class RandomWalk(Node):
    def __init__(self):
        super().__init__('random_walk_node')
        self.start = None
        self.total_distance = 0
        self.total_rotation = 0
        self.stop = False
        self.start_time = None

        # Test Configs
        # Establish what type of test to run
        # 0 for 0.075 m/s with 30 deg/s, 1 for 0.15 m/s with 120 deg/s
        self.speed_state = 1
        # Establish what type of test to run
        # 1 for 1 meter straight
        # 2 for 5 meters straight
        # 3 for 10 degrees
        # 4 for 180 degrees
        # 5 for 360 degrees
        self.trial_type = 5
        
        self.expected_runtime = 0

        if self.speed_state == 0:
            self.speed = SPEED_1
            self.rotation_speed = ROTAION_SPEED_1
        else:
            self.speed = SPEED_2
            self.rotation_speed = ROTAION_SPEED_2

        self.file_name = str(CURRENT_DIR) + str(grab_trial_file_name(self.speed_state, self.trial_type))

        with open(f'{self.file_name}', 'w') as file:
            file.write('x y z x_rot y_rot z_rot w_rot\n')

        # Create a publisher for controlling the robot's velocity
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        
        # Subscribe to the odometry topic to receive position and orientation data
        self.subscriber2 = self.create_subscription(
            Odometry,
            '/odom',
            self.listener_callback,
            QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
        
        # Initialize additional variables for controlling the robot
        self.pose_saved = ''  # Variable to save the robot's position
        self.cmd = Twist()  # Twist message used to control the robot's velocity
        

        self.get_logger().info('Random Walk Node Initialized')
        self.get_logger().info(f'Trial Type: {self.trial_type}')
        self.get_logger().info(f'Speed: {self.speed}')
        self.get_logger().info(f'Rotation Speed: {self.rotation_speed}')
        self.get_logger().info(f'File Directory: {CURRENT_DIR}')
        self.get_logger().info(f'File Name: {self.file_name}')


    def setup_trial(self):
        """
        Establish the trial based of the configs
        We should set the self.cmd.linear.x and self.cmd.angular.z
        Also calculate the expected runtime based off the distance or rotation
        """
        if self.trial_type == 1:
            self.cmd.linear.x = self.speed
            self.cmd.angular.z = 0.0
            self.expected_runtime = 1 / self.speed
        elif self.trial_type == 2:
            self.cmd.linear.x = self.speed
            self.cmd.angular.z = 0.0
            self.expected_runtime = 5 / self.speed
        elif self.trial_type == 3:
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = self.rotation_speed
            self.expected_runtime = math.radians(10) / self.rotation_speed
        elif self.trial_type == 4:
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = self.rotation_speed
            self.expected_runtime = math.radians(180) / self.rotation_speed
        elif self.trial_type == 5:
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = self.rotation_speed
            self.expected_runtime = math.radians(360) / self.rotation_speed
        self.start_time = time()
        self.publisher_.publish(self.cmd)

    def listener_callback(self, msg2):
        """Callback function to process incoming odometry data."""
        # Extract position and orientation data from the odometry message
        position = msg2.pose.pose.position
        orientation = msg2.pose.pose.orientation
        
        # Log the position and orientation data to data file
        with open(f'{self.file_name}', 'a') as file:
            file.write(f'{position.x} {position.y} {position.z} {orientation.x} {orientation.y} {orientation.z} {orientation.w}\n')

        # Check if the robot has been running for the expected time
        if self.start_time and time() - self.start_time > self.expected_runtime:
            self.stop = True
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = 0.0
            self.publisher_.publish(self.cmd)
            self.get_logger().info('Test Complete')
            self.destroy_node()
            rclpy.shutdown()

        if not self.start_time:
            self.setup_trial()
            self.timer = self.create_timer(0.1, self.publish_velocity)
    
    def publish_velocity(self):
        """Publish the robot's velocity."""
        if self.stop:
            return
        self.publisher_.publish(self.cmd)

def main(args=None):
    rclpy.init(args=args)
    random_walk_node = RandomWalk()
    rclpy.spin(random_walk_node)
    random_walk_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
