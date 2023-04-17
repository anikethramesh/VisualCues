# Instructions to use the Repo

1. Clone the repo and make it your workspace: `https://github.com/anikethramesh/VisualCues.git`
2. `cd` into the `src` folder.
3. Download the `JSK Visualisation Package` into the `src` folder: `git clone https://github.com/jsk-ros-pkg/jsk_visualization.git`

##### Update the Husky Configuration file:
- Open the file `gedit /etc/ros/setup.bash`
- Paste the Following:
----
export HUSKY_LMS1XX_ENABLED=true
export HUSKY_SENSOR_ARCH=true
export HUSKY_SENSOR_ARCH_RPY="0 0 0"
export HUSKY_TOP_PLATE_ENABLED=true
export HUSKY_REALSENSE_ENABLED=true
export HUSKY_REALSENSE_MOUNT_FRAME="sensor_arch_mount_link"
export HUSKY_REALSENSE_PARENT="sensor_arch_mount_link"
export HUSKY_REALSENSE_OFFSET="0 0 0"
export HUSKY_IMU_PORT=/dev/clearpath/imu
export HUSKY_IMU_XYZ="0.19 0.0 0.149"
export HUSKY_IMU_RPY="0.0 -1.5708 3.1416"

----

- Save and Exit

### Building the system

1. Run: `catkin_make` at the root of the directory
2. Run `source /etc/ros/setup.bash`
3. Run `source ./devel/setup.bash`

The system is now built. 
