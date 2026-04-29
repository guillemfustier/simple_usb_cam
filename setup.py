from setuptools import setup
from glob import glob

package_name = 'simple_usb_cam'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gfustierbcr',
    maintainer_email='chapegete@gmail.com',
    license='MIT',
    entry_points={
        'console_scripts': [
            'camera_node = simple_usb_cam.camera_node:main',
        ],
    },
)
