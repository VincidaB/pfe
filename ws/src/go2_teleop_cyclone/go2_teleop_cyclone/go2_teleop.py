import time
import sys
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.obstacles_avoid.obstacles_avoid_client import ObstaclesAvoidClient

import rclpy.subscription

last_cmd_time = time.time()

client = None




class TeleopNode(Node):
	def __init__(self):
		super().__init__('teleop_node')
		self.subscription = self.create_subscription(
			Twist,
			'cmd_vel',
			self.cmd_vel_callback,
			10)
		self.subscription  # prevent unused variable warning
	
	def cmd_vel_callback(self, msg):
		global last_cmd_time
		# Process the command velocity message
		last_cmd_time = time.time()
		vx = msg.linear.x
		vy = msg.linear.y
		vyaw = msg.angular.z
		client.Move(vx, vy, vyaw)


def main(args=None):
	print("hello there")

	if len(sys.argv) > 1 or True:
		ChannelFactoryInitialize(0, "eth0")
		print("Initiliazing channel eth0")
	else:
		ChannelFactoryInitialize(0)
		print("Initiliazing channel 0")
	try:
		
		global client
		print("begining of try")
		client = ObstaclesAvoidClient()
		print("there")
		client.SetTimeout(3.0)
		client.Init()
		print("here")
		while not client.SwitchGet()[1]:
			client.SwitchSet(True)
			time.sleep(0.1)

		rclpy.init(args=args)

		client.UseRemoteCommandFromApi(True)
		time.sleep(0.5)
		teleop_node = TeleopNode()

		print("obstacles avoid switch on")

		rclpy.spin(teleop_node)
		
	except KeyboardInterrupt:
		client.Move(0.0, 0.0, 0.0)
		client.UseRemoteCommandFromApi(False)
		print("exit!!")
