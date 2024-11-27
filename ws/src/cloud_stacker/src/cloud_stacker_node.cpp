#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "sensor_msgs/msg/point_cloud2.hpp"
#include <pcl_conversions/pcl_conversions.h> 
#include <pcl/filters/passthrough.h>

using std::placeholders::_1;

class CloudStacker : public rclcpp::Node
{
public:
  CloudStacker()
      : Node("cloud_stacker")
  {
    auto qos_profile = rclcpp::QoS(rclcpp::KeepLast(10)).best_effort().durability_volatile();
    point_cloud_subscription_ = this->create_subscription<sensor_msgs::msg::PointCloud2>("/utlidar/cloud_deskewed", qos_profile, std::bind(&CloudStacker::point_cloud_callback, this, _1));
    stacked_pc_publisher_ = this->create_publisher<sensor_msgs::msg::PointCloud2>("/registered_scan", 1);
  }

private:
  void point_cloud_callback(const sensor_msgs::msg::PointCloud2::SharedPtr point_cloud_msg)
  {
    /*
		pcl::PointCloud<pcl::PointXYZI>::Ptr stacked_cloud(new pcl::PointCloud<pcl::PointXYZI>);
        
    // keep the last N clouds
    for (int layer = 0; layer < 16; ++layer)
    {
        for (size_t i = 0; i < point_cloud_msg->ranges.size(); ++i)
        {

          if(point_cloud_msg->ranges[i]<point_cloud_msg->range_min || 
              point_cloud_msg->ranges[i]>point_cloud_msg->range_max){
            continue;
          }

          pcl::_PointXYZI point;
          double angle = point_cloud_msg->angle_min + point_cloud_msg->angle_increment * i;
          // TODO: cache the cos/sin values
          point.x = point_cloud_msg->ranges[i] * cos(angle);
          point.y = point_cloud_msg->ranges[i] * sin(angle);
          point.z = -0.5 + layer * 0.05;  // Adjust the z-offset as needed
          point.intensity = 1.0;
          stacked_cloud->points.push_back(point);
       }
    }
    
    stacked_cloud->width = stacked_cloud->points.size()/16;  // Width remains the same
    stacked_cloud->height = 16;  // Height is set to the number of layers

    // Convert to ROS PointCloud2 message
    sensor_msgs::msg::PointCloud2 output_pointcloud_msg;
    pcl::toROSMsg(*stacked_cloud, output_pointcloud_msg);
		*/
		pcl::PointCloud<pcl::PointXYZI>::Ptr stacked_cloud(new pcl::PointCloud<pcl::PointXYZI>);
    


		for(int i = 0; i < curently_stacked_clouds_; i++){
			RCLCPP_INFO(this->get_logger(), "Moving point_cloud %d to %d", i+1, i);
			clouds[i] = clouds[i+1];
			*stacked_cloud += clouds[i];
		}
		if(curently_stacked_clouds_ < num_wanted_clouds_stacked_ -1){
			
			curently_stacked_clouds_ ++;
			RCLCPP_INFO(this->get_logger(), "increasing curently_stacked_clouds_ %d", curently_stacked_clouds_);
		}

		pcl::fromROSMsg( *point_cloud_msg, clouds[curently_stacked_clouds_]);
		
		// if(curently_stacked_clouds_ == num_wanted_clouds_stacked_){
		// 	cloud[curently_stacked_clouds_] = 
		// }

		*stacked_cloud += clouds[curently_stacked_clouds_];


		sensor_msgs::msg::PointCloud2 output_pointcloud_msg;
		//pcl::toROSMsg(stacked_cloud, output_pointcloud_msg);

		pcl::toROSMsg(*stacked_cloud, output_pointcloud_msg);
		output_pointcloud_msg.header = point_cloud_msg->header;
    
    // Publish the stacked point cloud
    //stacked_pc_publisher_->publish(output_pointcloud_msg);
    stacked_pc_publisher_->publish(output_pointcloud_msg);
  }

  rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr point_cloud_subscription_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr stacked_pc_publisher_;

	int num_wanted_clouds_stacked_ = 2;
	int curently_stacked_clouds_ = 0; 
	pcl::PointCloud<pcl::PointXYZI> clouds[15];

};

int main(int argc, char *argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<CloudStacker>());
  rclcpp::shutdown();
  return 0;
}