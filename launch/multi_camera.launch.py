from launch import LaunchDescription
from launch_ros.actions import Node


CAMERAS = [
    {'name': 'cam0', 'device': '/dev/video0', 'frame_id': 'cam0',
     'width': 640, 'height': 480, 'fps': 30.0},
    {'name': 'cam1', 'device': '/dev/video2', 'frame_id': 'cam1',
     'width': 640, 'height': 480, 'fps': 30.0},
]


def generate_launch_description():
    nodes = []
    for cam in CAMERAS:
        nodes.append(Node(
            package='simple_usb_cam',
            executable='camera_node',
            name=cam['name'],
            namespace=cam['name'],
            output='screen',
            parameters=[{
                'video_device': cam['device'],
                'frame_id': cam['frame_id'],
                'width': cam['width'],
                'height': cam['height'],
                'fps': cam['fps'],
                'publish_raw': True,
                'publish_compressed': True,
                'jpeg_quality': 80,
                'fourcc': 'MJPG',
            }],
        ))
    return LaunchDescription(nodes)
