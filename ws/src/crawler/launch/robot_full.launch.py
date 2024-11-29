# copyright option3 ensma
import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.actions import DeclareLaunchArgument
import launch_ros.actions
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

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

    livox_msg = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('livox_ros_driver2'), 'launch_ROS2', 'msg_MID360_launch.py')]),
            launch_arguments={'use_sim_time': 'false'}.items()
    )

    fast_lio = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('fast_lio'),'launch', 'mapping.launch.py')]),
            launch_arguments={'use_sim_time': 'false',
                               'rviz' : 'false',
                               'rviz_cfg' : os.path.join(get_package_share_directory('crawler'), 'config', 'rviz_nav2_fastlio.rviz'),
                               }.items()
    )

    point_cloud_to_laser_scan = Node(
        package='pointcloud_to_laserscan', executable='pointcloud_to_laserscan_node',
        remappings=[('cloud_in', '/cloud_registered'),
                    ('scan', '/scan')],
        parameters=[{
            'target_frame': 'laser_frame',
            'transform_tolerance': 0.01,
            'min_height': 0.05,
            'max_height': 1.0,
            'angle_min': -3.14159265,  # -M_PI
            'angle_max': 3.14159265,  # M_PI
            'angle_increment': 0.0087,  # M_PI/360.0
            'scan_time': 0.3333,
            'range_min': 0.2,
            'range_max': 10.0,
            'use_inf': True,
            'inf_epsilon': 1.0,
        }],
        name='pointcloud_to_laserscan',
        output='screen'
    )


    map_to_odom_link = Node(
        package='tf2_ros', executable='static_transform_publisher',
        name='static_tf_pub_body_to_odom',
        arguments=['0.0', '0', '0.0', '0.0', '0.0', '0.0', 'map', 'odom'],
        output='screen'

    )

    body_to_base_link = Node(
        package='tf2_ros', executable='static_transform_publisher',
        name='static_tf_pub_body_to_odom',
        arguments=['0.0', '0', '0.0', '0.0', '0.0', '0.0', 'body', 'base_link'],
        output='screen'

    )

    slam2D = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('slam_toolbox'),'launch', 'online_async_launch.py')]),
            launch_arguments={'use_sim_time': 'false', 
                              'slam_params_file': os.path.join(
                                get_package_share_directory('crawler'),'config','mapper_params_online_async.yaml'
                              )}.items(),
    )
   
    nav2_params = os.path.join(get_package_share_directory('crawler'), 'config', 'nav2_params.yaml'),
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('crawler'),'launch', 'navigation_launch.py')]),
            launch_arguments={'use_sim_time': 'false',
                            'params_file': nav2_params,
                            'container_name': 'nav2_container',}.items(),
    )

    delayed_nav2 = TimerAction(
        period = 5.0,
        actions=[nav2]
    )
    # Launch them all!
    return LaunchDescription([
        rsp,
        delayed_controller_manager,
        delayed_joint_broad_spawner,
        delayed_skid_drive_spawner,
        livox_msg,
        fast_lio,
        point_cloud_to_laser_scan,
        body_to_base_link,
        map_to_odom_link,
        slam2D,
        delayed_nav2
    ])