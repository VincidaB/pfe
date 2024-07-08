cmake_minimum_required(VERSION 3.5)
project(crawler)

find_package(ament_cmake REQUIRED)


install(
    DIRECTORY description launch meshes
    DESTINATION share/${PROJECT_NAME}
)


ament_package()