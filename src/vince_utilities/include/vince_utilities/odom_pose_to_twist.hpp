#ifndef ODOM_POSE_TO_TWIST_HPP
#define ODOM_POSE_TO_TWIST_HPP

#include "rclcpp/rclcpp.hpp"
#include <nav_msgs/msg/odometry.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <geometry_msgs/msg/pose.hpp>
#include <geometry_msgs/msg/pose_with_covariance.hpp>
#include "rclcpp/time.hpp"


class OdomPoseToTwist: public rclcpp::Node
{

    public:
        OdomPoseToTwist();

    private:
        rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr odom_sub;
        rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr twist_pub;

        void odom_callback(const nav_msgs::msg::Odometry::SharedPtr msg);
        
        // last pose received from odom topic and timestamp
        geometry_msgs::msg::Pose last_odom_pose;
        rclcpp::Time last_odom_time;

        
};




#endif // ODOM_POSE_TO_TWIST_HPP