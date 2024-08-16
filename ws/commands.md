

ros2 launch terrain_analysis terrain_analysis.launch
ros2 launch local_planner local_planner.launch
ros2 topic pub /way_point geometry_msgs/msg/PointStamped "{ header: { stamp: { sec: 0, nanosec: 0 }, frame_id: 'map' }, point: { x: 4.5, y: 0.0, z: 0.0 } }"


ros2 topic pub /speed std_msgs/msg/Float32 "{data: 1.0}"



