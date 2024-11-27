# Copyright (c) 2024, RoboVerse community
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import FrontendLaunchDescriptionSource, PythonLaunchDescriptionSource
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource


def generate_launch_description():

	use_sim_time = LaunchConfiguration('use_sim_time', default='false')
	with_rviz2 = LaunchConfiguration('rviz2', default='true')
	with_nav2 = LaunchConfiguration('nav2', default='false')
	with_slam = LaunchConfiguration('slam', default='false')
	with_foxglove = LaunchConfiguration('foxglove', default='false')
	with_joystick = LaunchConfiguration('joystick', default='false')
	with_teleop = LaunchConfiguration('teleop', default='true')


	return LaunchDescription([


		IncludeLaunchDescription(
			PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('go2_robot_sdk'), 'launch', 'rsp.launch.py')]),
		),
		
		IncludeLaunchDescription(
				XMLLaunchDescriptionSource([os.path.join(get_package_share_directory('terrain_analysis'), 'launch', 'terrain_analysis.launch')]),
		),
		IncludeLaunchDescription(
				XMLLaunchDescriptionSource([os.path.join(get_package_share_directory('terrain_analysis_ext'), 'launch', 'terrain_analysis_ext.launch')]),
		),

		IncludeLaunchDescription(
				XMLLaunchDescriptionSource([
						os.path.join(get_package_share_directory('local_planner'), 'launch', 'local_planner.launch')
				])
		),


	])
