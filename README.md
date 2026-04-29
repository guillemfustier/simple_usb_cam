# simple_usb_cam

Minimal ROS 2 USB camera publisher. Python only. Deps: `rclpy`, `sensor_msgs`, `opencv-python`, `numpy`. No `cv_bridge`, no `image_transport`.

## Topics
- `<camera_name>/image_raw` (`sensor_msgs/Image`, `bgr8`)
- `<camera_name>/image_raw/compressed` (`sensor_msgs/CompressedImage`, JPEG)

## Parameters
| Name | Default | Notes |
|---|---|---|
| `video_device` | `/dev/video0` | also accepts integer index |
| `width` / `height` | 640 / 480 | |
| `fps` | 30.0 | |
| `frame_id` | `camera` | |
| `publish_raw` | `true` | |
| `publish_compressed` | `true` | |
| `jpeg_quality` | 80 | 0–100 |
| `fourcc` | `MJPG` | `YUYV`, `MJPG`, `H264`... or empty |

## Build
```bash
cd ~/Documents/Projects/pruebas_ws
colcon build --packages-select simple_usb_cam
source install/setup.bash
```

## Run single
```bash
ros2 launch simple_usb_cam single_camera.launch.py video_device:=/dev/video0 camera_name:=cam0
```

## Run multi
Edit `CAMERAS` list in `launch/multi_camera.launch.py`, then:
```bash
ros2 launch simple_usb_cam multi_camera.launch.py
```

## Run direct
```bash
ros2 run simple_usb_cam camera_node --ros-args -p video_device:=/dev/video2 -p width:=1280 -p height:=720
```
