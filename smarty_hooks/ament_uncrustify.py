# Copyright (c) 2026 Smart Rollerz e.V.
# All rights reserved.

"""Pre-commit hook that runs ament_uncrustify (ROS 2 C/C++ code style) on the given files."""

import argparse
import os
import subprocess
import sys

ALLOWED_ROS_DISTROS = ["foxy", "galactic", "humble", "iron", "jazzy", "rolling"]


def main(argv=None):
    """Run ament_uncrustify on the files passed by pre-commit and return its exit code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reformat",
        action="store_true",
        help="Reformat the files in place instead of only checking them",
    )
    parser.add_argument(
        "--ros-distro",
        default=os.environ.get("ROS_DISTRO", "jazzy"),
        choices=ALLOWED_ROS_DISTROS,
        help="ROS distribution that provides ament_uncrustify (default: $ROS_DISTRO or jazzy)",
    )
    parser.add_argument(
        "files", nargs="*", help="C/C++ files to check (passed by pre-commit)"
    )
    args = parser.parse_args(argv)

    if not args.files:
        return 0

    setup_file = f"/opt/ros/{args.ros_distro}/setup.bash"
    if not os.path.isfile(setup_file):
        print(
            f"ROS 2 {args.ros_distro} is not installed ({setup_file} not found), cannot run ament_uncrustify."
        )
        return 1

    # Source ROS in a bash and pass the files as arguments (no string concatenation, so names with spaces work)
    command = [
        "ament_uncrustify",
        *(["--reformat"] if args.reformat else []),
        *args.files,
    ]
    script = f'source "{setup_file}" && exec "$@"'
    return subprocess.run(
        ["bash", "-c", script, "bash", *command], check=False
    ).returncode


if __name__ == "__main__":
    sys.exit(main())
