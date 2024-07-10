set(_AMENT_PACKAGE_NAME "diffdrive_arduino")
set(diffdrive_arduino_VERSION "0.0.0")
set(diffdrive_arduino_MAINTAINER "Dr.-Ing. Denis Štogl <denis.stogl@stoglrobotics.de>, Bence Magyar <bence.magyar.robotics@gmail.com>, Christoph Froehlich <christoph.froehlich@ait.ac.at>")
set(diffdrive_arduino_BUILD_DEPENDS "hardware_interface" "pluginlib" "rclcpp" "rclcpp_lifecycle" "libserial-dev")
set(diffdrive_arduino_BUILDTOOL_DEPENDS "ament_cmake")
set(diffdrive_arduino_BUILD_EXPORT_DEPENDS "hardware_interface" "pluginlib" "rclcpp" "rclcpp_lifecycle" "libserial-dev")
set(diffdrive_arduino_BUILDTOOL_EXPORT_DEPENDS )
set(diffdrive_arduino_EXEC_DEPENDS "ros2_controllers_test_nodes" "joint_state_broadcaster" "diff_drive_controller" "ros2controlcli" "controller_manager" "rviz2" "robot_state_publisher" "hardware_interface" "pluginlib" "rclcpp" "rclcpp_lifecycle" "libserial-dev")
set(diffdrive_arduino_TEST_DEPENDS "ament_cmake_gtest")
set(diffdrive_arduino_GROUP_DEPENDS )
set(diffdrive_arduino_MEMBER_OF_GROUPS )
set(diffdrive_arduino_DEPRECATED "")
set(diffdrive_arduino_EXPORT_TAGS)
list(APPEND diffdrive_arduino_EXPORT_TAGS "<build_type>ament_cmake</build_type>")
