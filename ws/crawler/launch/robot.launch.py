# copyright option3 ensma
import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.actions import DeclareLaunchArgument
import launch_ros.actions
from launch.substitutions import LaunchConfiguration
from launch.substitutions import Command
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch.substitutions import Command
import xacro



def generate_launch_description():

    # Declare the launch arguments
    # check if log_level is set

    logger = LaunchConfiguration('log_level')
    # if not set, set to debug
    if logger is None:
        logger = 'debug'


    package_name='crawler' #<--- CHANGE ME


    controller_params_file = os.path.join(
        get_package_share_directory("crawler"),
        'config',
        'diffbot_controllers.yaml')

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'false'}.items()
    )



    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[controller_params_file],
        remappings=[('/controller_manager/robot_description', '/robot_description')],
        output="screen",
    )

    delayed_controller_manager = TimerAction(
        period=1.0,
        actions=[controller_manager],
    )

    skid_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["skid_base_controller"],
        output="screen",
    )

    delayed_skid_drive_spawner = TimerAction(
        period=2.0,
        actions=[skid_drive_spawner],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        output="screen",
    )

    delayed_joint_broad_spawner = TimerAction(
        period=2.0,
        actions=[joint_broad_spawner],
    )

    return LaunchDescription([
        rsp,
        delayed_controller_manager,
        delayed_skid_drive_spawner,
        delayed_joint_broad_spawner,
        
    ])
