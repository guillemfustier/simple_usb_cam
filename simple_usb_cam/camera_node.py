#!/usr/bin/env python3
import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import Image, CompressedImage


class UsbCamNode(Node):
    def __init__(self):
        super().__init__('simple_usb_cam')

        self.declare_parameter('video_device', '/dev/video0')
        self.declare_parameter('width', 640)
        self.declare_parameter('height', 480)
        self.declare_parameter('fps', 30.0)
        self.declare_parameter('frame_id', 'camera')
        self.declare_parameter('publish_raw', True)
        self.declare_parameter('publish_compressed', True)
        self.declare_parameter('jpeg_quality', 80)
        self.declare_parameter('fourcc', 'MJPG')

        self.device = self.get_parameter('video_device').value
        self.width = int(self.get_parameter('width').value)
        self.height = int(self.get_parameter('height').value)
        self.fps = float(self.get_parameter('fps').value)
        self.frame_id = self.get_parameter('frame_id').value
        self.pub_raw = bool(self.get_parameter('publish_raw').value)
        self.pub_comp = bool(self.get_parameter('publish_compressed').value)
        self.jpeg_quality = int(self.get_parameter('jpeg_quality').value)
        self.fourcc = self.get_parameter('fourcc').value

        dev_index = self._device_to_index(self.device)
        self.cap = cv2.VideoCapture(dev_index, cv2.CAP_V4L2)
        if not self.cap.isOpened():
            raise RuntimeError(f'Cannot open {self.device}')

        if self.fourcc and len(self.fourcc) == 4:
            fcc = cv2.VideoWriter_fourcc(*self.fourcc)
            self.cap.set(cv2.CAP_PROP_FOURCC, fcc)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)

        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )
        self.raw_pub = self.create_publisher(Image, 'image_raw', qos) if self.pub_raw else None
        self.comp_pub = self.create_publisher(CompressedImage, 'image_raw/compressed', qos) if self.pub_comp else None

        period = 1.0 / max(self.fps, 1.0)
        self.timer = self.create_timer(period, self._tick)
        self.get_logger().info(
            f'Streaming {self.device} @ {self.width}x{self.height} {self.fps}fps '
            f'(raw={self.pub_raw}, compressed={self.pub_comp})'
        )

    @staticmethod
    def _device_to_index(dev):
        try:
            return int(dev)
        except (TypeError, ValueError):
            pass
        if isinstance(dev, str) and dev.startswith('/dev/video'):
            try:
                return int(dev.replace('/dev/video', ''))
            except ValueError:
                pass
        return dev

    def _tick(self):
        ok, frame = self.cap.read()
        if not ok or frame is None:
            self.get_logger().warn('Frame grab failed', throttle_duration_sec=2.0)
            return

        stamp = self.get_clock().now().to_msg()

        if self.raw_pub is not None:
            msg = Image()
            msg.header.stamp = stamp
            msg.header.frame_id = self.frame_id
            msg.height = frame.shape[0]
            msg.width = frame.shape[1]
            msg.encoding = 'bgr8'
            msg.is_bigendian = 0
            msg.step = frame.shape[1] * 3
            msg.data = np.ascontiguousarray(frame).tobytes()
            self.raw_pub.publish(msg)

        if self.comp_pub is not None:
            ok, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, self.jpeg_quality])
            if ok:
                cmsg = CompressedImage()
                cmsg.header.stamp = stamp
                cmsg.header.frame_id = self.frame_id
                cmsg.format = 'jpeg'
                cmsg.data = buf.tobytes()
                self.comp_pub.publish(cmsg)

    def destroy_node(self):
        if self.cap is not None:
            self.cap.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = UsbCamNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
