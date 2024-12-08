from typing import Optional

import numpy as np
from panda_gym.envs.core import RobotTaskEnv
from panda_gym.pybullet import PyBullet

from experiments.warehouse.robot import PackingPanda
from experiments.warehouse.task import PackCustomerOrder


class PackCustomerOrderEnvironment(RobotTaskEnv):
    """Order packing warehouse environment."""

    # TODO: Make sure everything still works when using velocity control
    def __init__(
        self,
        render_mode: str = "rgb_array",
        control_type: str = "ee",
        renderer: str = "Tiny",
        render_width: int = 720,
        render_height: int = 480,
        render_target_position: Optional[np.ndarray] = None,
        render_distance: float = 1.4,
        render_yaw: float = 90,
        render_pitch: float = -15,
        render_roll: float = 0,
    ) -> None:
        """Initialise the order packing warehouse environment."""
        # Initialise the simulation
        sim = PyBullet(
            render_mode=render_mode,
            renderer=renderer,
            # FIXME: This should be in constants
            background_color=np.array([0, 0, 0]),
        )

        # Initialise the robot
        robot = PackingPanda(
            sim,
            block_gripper=False,
            # FIXME: This position should be in constants
            base_position=np.array([-0.1, 0.0, 0.0]),
            control_type=control_type,
        )

        # Initialise the task
        task = PackCustomerOrder(sim, show_waypoints=True, show_regions=True)

        # Initialise the environment
        super().__init__(
            robot=robot,
            task=task,
            render_width=render_width,
            render_height=render_height,
            render_target_position=render_target_position,
            render_distance=render_distance,
            render_yaw=render_yaw,
            render_pitch=render_pitch,
            render_roll=render_roll,
        )
