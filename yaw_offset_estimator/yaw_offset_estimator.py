# 파일명: yaw_offset_estimator.py

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, NavSatFix
import numpy as np
from math import atan2, sin, cos, radians, degrees

class YawOffsetEstimator(Node):
    def __init__(self):
        super().__init__('yaw_offset_estimator')
        self.declare_parameter('magnetic_declination_deg', 0.0)

        self.mag_decl = self.get_parameter('magnetic_declination_deg').get_parameter_value().double_value

        self.imu_yaw = None
        self.gps_pos_1 = None
        self.gps_pos_2 = None

        self.subscription_imu = self.create_subscription(
            Imu, '/imu/data', self.imu_callback, 10)
        self.subscription_gps = self.create_subscription(
            NavSatFix, '/gps/fix', self.gps_callback, 10)

        self.get_logger().info('Yaw Offset Estimator Node Started.')

    def imu_callback(self, msg):
        # orientation → yaw (라디안)
        q = msg.orientation
        yaw = self.quaternion_to_yaw(q.x, q.y, q.z, q.w)
        self.imu_yaw = yaw
        self.try_compute()

    def gps_callback(self, msg):
        lat = msg.latitude
        lon = msg.longitude
        if self.gps_pos_1 is None:
            self.gps_pos_1 = (lat, lon)
            self.get_logger().info("GPS 위치 1 저장됨.")
        elif self.gps_pos_2 is None:
            self.gps_pos_2 = (lat, lon)
            self.get_logger().info("GPS 위치 2 저장됨.")
            self.try_compute()

    def quaternion_to_yaw(self, x, y, z, w):
        # Quaternion to Euler (yaw)
        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        return atan2(siny_cosp, cosy_cosp)

    def compute_gps_heading(self, lat1, lon1, lat2, lon2):
        # 위도/경도로부터 bearing 계산
        d_lon = radians(lon2 - lon1)
        lat1 = radians(lat1)
        lat2 = radians(lat2)

        x = sin(d_lon) * cos(lat2)
        y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(d_lon)
        bearing = atan2(x, y)  # 라디안
        return bearing  # 0 = 동쪽, π/2 = 북쪽

    def try_compute(self):
        if self.imu_yaw is not None and self.gps_pos_1 and self.gps_pos_2:
            gps_heading = self.compute_gps_heading(*self.gps_pos_1, *self.gps_pos_2)
            yaw_offset = gps_heading - (self.imu_yaw + radians(self.mag_decl))
            yaw_offset = atan2(sin(yaw_offset), cos(yaw_offset))  # 정규화

            self.get_logger().info(f"IMU Yaw (rad): {self.imu_yaw:.4f}")
            self.get_logger().info(f"GPS Heading (rad): {gps_heading:.4f}")
            self.get_logger().info(f"Yaw Offset (rad): {yaw_offset:.4f}")
            self.get_logger().info(f"Yaw Offset (deg): {degrees(yaw_offset):.2f}")

            # 다시 초기화 (원한다면 유지)
            self.gps_pos_1 = None
            self.gps_pos_2 = None


def main(args=None):
    rclpy.init(args=args)
    node = YawOffsetEstimator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
