from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    args = [
        DeclareLaunchArgument('video_device', default_value='/dev/video0'),
        DeclareLaunchArgument('camera_name', default_value='camera'),
        DeclareLaunchArgument('frame_id', default_value='camera'),
        DeclareLaunchArgument('width', default_value='640'),
        DeclareLaunchArgument('height', default_value='480'),
        DeclareLaunchArgument('fps', default_value='30.0'),
        DeclareLaunchArgument('publish_raw', default_value='true'),
        DeclareLaunchArgument('publish_compressed', default_value='true'),
        DeclareLaunchArgument('jpeg_quality', default_value='80'),
        DeclareLaunchArgument('fourcc', default_value='MJPG'),
    ]

    node = Node(
        package='simple_usb_cam',
        executable='camera_node',
        name=LaunchConfiguration('camera_name'),
        namespace=LaunchConfiguration('camera_name'),
        output='screen',
        parameters=[{
            'video_device': LaunchConfiguration('video_device'),
            'frame_id': LaunchConfiguration('frame_id'),
            'width': LaunchConfiguration('width'),
            'height': LaunchConfiguration('height'),
            'fps': LaunchConfiguration('fps'),
            'publish_raw': LaunchConfiguration('publish_raw'),
            'publish_compressed': LaunchConfiguration('publish_compressed'),
            'jpeg_quality': LaunchConfiguration('jpeg_quality'),
            'fourcc': LaunchConfiguration('fourcc'),
        }],
    )

    return LaunchDescription(args + [node])
