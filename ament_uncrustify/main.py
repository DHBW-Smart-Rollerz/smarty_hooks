# Copyright (c) 2024 Smart Rollerz e.V.
# All rights reserved.

import subprocess
import argparse
import os


def reformat_ros_folder(ros_version):
    # Get all file names of changed files in the staging area
    try:
        result = subprocess.run(
            ["git", "diff", "--staged", "--name-only"],
            stdout=subprocess.PIPE,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while getting changed files: {e}")
        exit(1)
    changed_files = result.stdout.decode("utf-8").splitlines()

    if not changed_files:
        print("No files to reformat.")
        return

    # Prepare the command to source the ROS environment and run ament_uncrustify
    command = f"source /opt/ros/{ros_version}/setup.bash && ament_uncrustify --reformat {' '.join(changed_files)}"

    try:
        # Run the command in a shell
        subprocess.run(command, check=True, shell=True, executable="/bin/bash")
        print("ROS folder reformatted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while reformatting ROS folder: {e}")
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "ros_version",
        type=str,
        default="jazzy",
        help="ROS version of the package to be reformatted",
    )
    args = parser.parse_args()

    allowed = ["foxy", "galactic", "rolling", "jazzy", "humble", "iron"]

    if args.ros_version not in allowed:
        print(f"Invalid ROS version. Allowed values are: {', '.join(allowed)}")
        exit(1)

    reformat_ros_folder(args.ros_version)
