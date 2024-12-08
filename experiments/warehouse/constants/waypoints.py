import numpy as np

import experiments.warehouse.constants.simulation as cs

# Relative constants
ABOVE_DELTA = np.array([0, 0, 0.1])
GRASP_DELTA = np.array([0, 0, 0])
RELEASE_DELTA = np.array([0, 0.25, 0.15])

# Above cube waypoints
ABOVE_GREEN = cs.GREEN_CUBE_POSITION + ABOVE_DELTA
ABOVE_RED = cs.RED_CUBE_POSITION + ABOVE_DELTA
ABOVE_BLUE = cs.BLUE_CUBE_POSITION + ABOVE_DELTA

# Grasp waypoints
GRASP_GREEN = cs.GREEN_CUBE_POSITION + GRASP_DELTA
GRASP_RED = cs.RED_CUBE_POSITION + GRASP_DELTA
GRASP_BLUE = cs.BLUE_CUBE_POSITION + GRASP_DELTA

# Drop waypoints
RELEASE_GREEN = cs.GREEN_CUBE_POSITION + RELEASE_DELTA
RELEASE_RED = cs.RED_CUBE_POSITION + RELEASE_DELTA
RELEASE_BLUE = cs.BLUE_CUBE_POSITION + RELEASE_DELTA

# Debug waypoints
DEBUG_WAYPOINT_ONE = np.array([0.5, 0.0, 0.3])
DEBUG_WAYPOINT_TWO = np.array([0.4, 0.0, 0.3])
