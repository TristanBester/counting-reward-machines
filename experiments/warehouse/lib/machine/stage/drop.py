import experiments.warehouse.lib.groundenv.constants.waypoints as cw
from experiments.warehouse.lib.machine.reward import (
    create_constant_reward,
    create_penalty_waypoint_reward,
    create_waypoint_reward,
)
from experiments.warehouse.lib.machine.stage.transition import Transition


def create_drop_stage(
    block_colour: str,
    counter_state: str,
    current_state: int,
    success_state: int,
    base_counter_modifier: tuple[int, ...],
    success_counter_modifier: tuple[int, ...],
) -> list[Transition]:
    """Create a stage for moving a block to the release position."""
    if block_colour == "RED":
        waypoint = cw.RELEASE_RED
    elif block_colour == "GREEN":
        waypoint = cw.RELEASE_GREEN
    elif block_colour == "BLUE":
        waypoint = cw.RELEASE_BLUE
    else:
        raise ValueError(f"Invalid block colour: {block_colour}")

    transitions = []
    # Gripper open action executed
    transitions.append(
        Transition(
            formula=f"not GRIPPER_OPEN_ACTION_EXECUTED / {counter_state}",
            current_state=current_state,
            next_state=current_state,
            counter_modifier=base_counter_modifier,
            reward_fn=create_constant_reward(-1.0),
        )
    )
    # Not in release region
    transitions.append(
        Transition(
            formula=f"not RELEASE_REGION_{block_colour} / {counter_state}",
            current_state=current_state,
            next_state=current_state,
            counter_modifier=base_counter_modifier,
            reward_fn=create_penalty_waypoint_reward(
                waypoint=waypoint,
                penalty=-1.0,
                max_distance=1.0,
            ),
        )
    )
    # Release position with low velocity
    formula = f"RELEASE_REGION_{block_colour} and not GRIPPER_CLOSED / {counter_state}"
    transitions.append(
        Transition(
            formula=formula,
            current_state=current_state,
            next_state=success_state,
            counter_modifier=success_counter_modifier,
            reward_fn=create_constant_reward(50.0),
        )
    )
    # Other
    transitions.append(
        Transition(
            formula=(
                f"RELEASE_REGION_{block_colour} and GRIPPER_CLOSED / {counter_state}"
            ),
            current_state=current_state,
            next_state=current_state,
            counter_modifier=base_counter_modifier,
            reward_fn=create_waypoint_reward(
                waypoint=waypoint,
                max_distance=1.0,
            ),
        )
    )
    return transitions
