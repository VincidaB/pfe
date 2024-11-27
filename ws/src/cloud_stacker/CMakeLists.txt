cmake_minimum_required(VERSION 3.8)
project(cloud_stacker)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(pcl_conversions REQUIRED)




add_executable(cloud_stacker_node src/cloud_stacker_node.cpp)
ament_target_dependencies(cloud_stacker_node 
  rclcpp
  std_msgs
  sensor_msgs
  pcl_conversions
)
target_link_libraries(cloud_stacker_node ${catkin_LIBRARIES})

install(TARGETS
  cloud_stacker_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
