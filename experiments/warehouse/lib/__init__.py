import gymnasium as gym
from gymnasium.envs.registration import register

from experiments.warehouse.lib.crossproduct import LoggingWrapper, WarehouseCrossProduct
from experiments.warehouse.lib.label.function import WarehouseLabellingFunction
from experiments.warehouse.lib.machine.machine import WarehouseCountingRewardMachine


def make_warehouse_environment(**kwargs) -> gym.Env:
    """Create the warehouse environment."""
    ground_env_kwargs = kwargs.get("ground_env_kwargs", {})
    crm_kwargs = kwargs.get("crm_kwargs", {})
    lf_kwargs = kwargs.get("lf_kwargs", {})
    crossproduct_kwargs = kwargs.get("crossproduct_kwargs", {})

    ground_env = gym.make(
        "WarehouseGround-v0",
        **ground_env_kwargs,
    )
    crm = WarehouseCountingRewardMachine(**crm_kwargs)
    lf = WarehouseLabellingFunction(**lf_kwargs)
    cp = WarehouseCrossProduct(ground_env, crm, lf, **crossproduct_kwargs)
    env = LoggingWrapper(env=cp)
    return env


register(
    id="Warehouse-v0",
    entry_point="experiments.warehouse.lib:make_warehouse_environment",
)
