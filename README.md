# smarty_hooks

Pre-commit hooks for the smarty project.

## Hooks

### `ament_uncrustify`

Formats C/C++ files (`.c`, `.cpp`, `.h`, `.hpp`) with [`ament_uncrustify`](https://github.com/ament/ament_lint) in the ROS 2 code style. Files that are not formatted correctly are reformatted in place and the commit is stopped, so you can review and stage the changes.

Requires ROS 2 to be installed in `/opt/ros/<distro>` (default: `$ROS_DISTRO` or `jazzy`).

Add it to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/DHBW-Smart-Rollerz/smarty_hooks
    rev: v0.1.2
    hooks:
      - id: ament_uncrustify
        # args: [--ros-distro, humble]  # optional, default: $ROS_DISTRO or jazzy
```

Test it on the example file without committing:

```bash
pre-commit try-repo . ament_uncrustify --files test/cpp_test.cpp
```
