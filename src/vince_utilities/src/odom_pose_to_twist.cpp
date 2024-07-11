#include <cstdio>
#include "vince_utilities/odom_pose_to_twist.hpp"

OdomPoseToTwist::OdomPoseToTwist(): Node("odom_pose_to_twist")
{
  odom_sub = this->create_subscription<nav_msgs::msg::Odometry>("Odometry", 10, std::bind(&OdomPoseToTwist::odom_callback, this, std::placeholders::_1));
  twist_pub = this->create_publisher<geometry_msgs::msg::Twist>("twist", 10);

  last_odom_pose.position.x = 0;
  last_odom_pose.position.y = 0;
  last_odom_pose.position.z = 0;
  last_odom_pose.orientation.x = 0;
  last_odom_pose.orientation.y = 0;
  last_odom_pose.orientation.z = 0;
  last_odom_pose.orientation.w = 0;
  last_odom_time = this->now();



}

void OdomPoseToTwist::odom_callback(const nav_msgs::msg::Odometry::SharedPtr msg)
{

  // calculate time difference
  rclcpp::Time msg_time(msg->header.stamp);
  rclcpp::Duration time_diff =  msg_time - last_odom_time;

  // calculate distance difference
  double dx = msg->pose.pose.position.x - last_odom_pose.position.x;
  double dy = msg->pose.pose.position.y - last_odom_pose.position.y;

  // get distance along x axis of robot
  double dx_robot = dx * cos(last_odom_pose.orientation.z) + dy * sin(last_odom_pose.orientation.z);

  // calculate speed
  double x_speed = dx_robot / time_diff.seconds();

  // publish twist message
  geometry_msgs::msg::Twist twist_msg;

  twist_msg.linear.x = x_speed;

  twist_pub->publish(twist_msg);

  last_odom_pose = msg->pose.pose;
  last_odom_time = msg->header.stamp;

}



int main(int argc, char ** argv)
{

  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<OdomPoseToTwist>());  
}
