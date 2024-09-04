# copyright option3 ensma
import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.actions import DeclareLaunchArgument
import launch_ros.actions
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource

from launch_ros.actions import Node



def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='crawler' #<--- CHANGE ME
    
    controller_params_file = os.path.join(
        get_package_share_directory(package_name),
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

    fast_lio = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('fast_lio'),'launch', 'mapping.launch.py')]),
            launch_arguments={'use_sim_time': 'false',
                               'rviz' : 'false',
                               'rviz_cfg' : os.path.join(get_package_share_directory('crawler'), 'config', 'rviz_nav2_fastlio.rviz'),
                               }.items()
    )


    body_to_base_link = Node(
        package='tf2_ros', executable='static_transform_publisher',
        name='static_tf_pub_body_to_odom',
        arguments=['0.0', '0', '0.0', '0.0', '0.0', '0.0', 'body', 'base_link'],
        output='screen'

    )

    terrain_analysis = IncludeLaunchDescription(
        XMLLaunchDescriptionSource([os.path.join(
            get_package_share_directory('terrain_analysis'),'launch', 'terrain_analysis.launch')]),
            launch_arguments={'use_sim_time': 'true'}.items()
    )

    terrain_analysis_ext = IncludeLaunchDescription(
        XMLLaunchDescriptionSource([os.path.join(
            get_package_share_directory('terrain_analysis_ext'),'launch', 'terrain_analysis_ext.launch')]),
    )   


    delayed_terrain_analysis = TimerAction(
        period=5.0,
        actions=[terrain_analysis],
    )

    delayed_terrain_analysis_ext = TimerAction(
        period=7.0,
        actions=[terrain_analysis_ext],
    )

    # Launch them all!
    return LaunchDescription([
        rsp,
        delayed_controller_manager,
        delayed_joint_broad_spawner,
        delayed_skid_drive_spawner,
        fast_lio,
        body_to_base_link,
        
    ])