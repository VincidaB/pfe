cmake_minimum_required(VERSION 3.5)
project(crawler)

find_package(ament_cmake REQUIRED)


install(
    DIRECTORY description launch meshes config cpr_office_gazebo
    DESTINATION share/${PROJECT_NAME}
)


ament_package()