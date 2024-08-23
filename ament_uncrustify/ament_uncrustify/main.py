# Copyright (c) 2024 Smart Rollerz e.V.
# All rights reserved.

import subprocess
import argparse


def reformat_ros_folder(ros_version):

    # Get all file names of changed files in the staging area
    changed_files = subprocess.run(
        ["git", "diff", "--cached", "--name-only"], stdout=subprocess.PIPE
    ).stdout.decode("utf-8")
    changed_files = changed_files.split("\n")
    changed_files = list(filter(None, changed_files))

    try:
        subprocess.run(
            [
                "bash",
                "-c",
                f"source /opt/ros/{ros_version}/setup.bash && ament_uncrustify --reformat {' '.join(changed_files)}",
            ],
            check=True,
            shell=True,
        )
        print("ROS folder reformatted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while reformatting ROS folder: {e}")
        exit(1)

    exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "ros_version", type=str, help="ROS version of the package to be reformatted"
    )
    args = parser.parse_args()

    allowed = ["foxy", "galactic", "rolling", "jazzy", "humble", "iron"]

    if args.ros_version not in allowed:
        print(f"Invalid ROS version. Allowed values are: {', '.join(allowed)}")
        exit(1)

    reformat_ros_folder(args.ros_version)
