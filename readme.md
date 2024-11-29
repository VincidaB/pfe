## Organization of the repository

The repository is organized as follows:
- `ws` is a ROS2 workspace (tested on humble)
- `ws/src` contains the source code of all the ros2 packages
- `open-manipulator` is the code for the open robotis manipulator (arm)

## Building

### How to build every package 
```bash
cd ws
rosdep install -i --from-path src -y # install dependencies
colcon build --symlink-install --parallel-workers 3 --cmake-args -DCMAKE_BUILD_TYPE=Release
source install/setup.bash
```
To reduce the RAM usage during the build process, you can reduce the number of parallel workers. Compiling with 3 parallel workers works on a system with 16Gb of RAM.

The flag `--symlink-install` is used to create symbolic links to the executables and libraries instead of copying them. This is useful when you are developing the packages and you want to see the changes immediately.

The flag `--cmake-args -DCMAKE_BUILD_TYPE=Release` is used to compile the packages in release mode. This will optimize the code and remove the debug symbols. If this is not used, packages like `tare_planner` will not function correctly on the Jetson as it is single threaded and the debug symbols will slow down the execution.


### To compile a single package

Sometimes, you may want to compile only a single package. In that case, you can use the following command:
```bash
colcon build --symlink-install --packages-select tare_planner --cmake-args -DCMAKE_BUILD_TYPE=Release
```


## Simulation


## wheeled robot
To run the wheeled vehicle simulation, you can use the following command:
```bash
ros2 launch crawler simulation_office_construction.launch.py
```
Other simulation that can be run :
`simulation_far_planner.launch.py` far planner navigation
`simulation.launch.py`
`simulation_office_construction.launch.py` in construction office (fast_lio, terrain analysis, nav2)
`simulation_office_constructed.launch.py` constructed office (fast_lio, terrain analysis, nav2)
`simulation_full.launch.py`
`simulation_tare_planner.launch.py`
