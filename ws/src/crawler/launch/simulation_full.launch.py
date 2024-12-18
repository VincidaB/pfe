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
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )


    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'verbose': 'true'}.items()
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'crawler',
                                   '-x','0.0',
                                   '-y','0.0',
                                   '-z', '0.1'
                                     ],
                        output='screen')

    load_joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )


    load_skid_drive_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'skid_base_controller'],
        output='screen'
    )


    delayed_skid_drive_spawner = TimerAction(
        period=1.0,
        actions=[load_skid_drive_controller],
    )

    fast_lio = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('fast_lio'),'launch', 'mapping.launch.py')]),
            launch_arguments={'use_sim_time': 'true',
                               'rviz' : 'true',
                               'rviz_cfg' : os.path.join(get_package_share_directory('crawler'), 'config', 'rviz_nav2_fastlio.rviz'),
                               'config_file' : 'mid360_simulation.yaml'
                               }.items()
    )

    point_cloud_to_laser_scan = Node(
        package='pointcloud_to_laserscan', executable='pointcloud_to_laserscan_node',
        remappings=[('cloud_in', '/cloud_registered'),
                    ('scan', '/scan')],
        parameters=[{
            'target_frame': 'laser_frame',
            'transform_tolerance': 0.01,
            'min_height': 0.0,
            'max_height': 1.0,
            'angle_min': -3.14159265,  # -M_PI
            'angle_max': 3.14159265,  # M_PI
            'angle_increment': 0.0087,  # M_PI/360.0
            'scan_time': 0.3333,
            'range_min': 0.45,
            'range_max': 10.0,
            'use_inf': True,
            'inf_epsilon': 1.0,
        }],
        name='pointcloud_to_laserscan',
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
            launch_arguments={'use_sim_time': 'true', 
                              'slam_params_file': os.path.join(
                                get_package_share_directory('crawler'),'config','mapper_params_online_async.yaml'
                              )}.items(),
    )
   
    nav2_params = os.path.join(get_package_share_directory('crawler'), 'config', 'nav2_params.yaml'),
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('crawler'),'launch', 'navigation_launch.py')]),
            launch_arguments={'use_sim_time': 'true',
                            'params_file': nav2_params,
                            'container_name': 'nav2_container',}.items(),
    )

    delayed_nav2 = TimerAction(
        period = 1.0,
        actions=[nav2]
    )


    twistStamper = Node(
        package='twist_stamper', executable='twist_stamper',
        name='twist_stamper',
        output='screen',
        remappings=[
            ('cmd_vel_in', 'skid_base_controller/cmd_vel_unstamped'),
            ('cmd_vel_out', 'skid_base_controller/cmd_vel'),
        ]
    )



    # Launch them all!
    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            #default_value=[os.path.join('worlds', 'empty.world'), ''],
            #default_value=['/home/vincent/pfe/TwoHouses.xml', ''],
            default_value=['/home/vincent/pfe/TwoHouses_ramp.xml', ''],
                description='SDF world file'),
        rsp,
        spawn_entity,
        gazebo,
        load_joint_state_broadcaster,
        delayed_skid_drive_spawner,
        fast_lio,
        point_cloud_to_laser_scan,
        body_to_base_link,
        slam2D,
        delayed_nav2,
        twistStamper
    ])