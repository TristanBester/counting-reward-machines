from abc import ABC, abstractmethod
from typing import Generic, TypeVar

import gymnasium as gym
import numpy as np

from crm.automaton import CountingRewardMachine
from crm.label import LabellingFunction

GroundObsType = TypeVar("GroundObsType")
ObsType = TypeVar("ObsType")
ActType = TypeVar("ActType")
RenderFrame = TypeVar("RenderFrame")


class CrossProduct(ABC, gym.Env, Generic[GroundObsType, ObsType, ActType, RenderFrame]):
    """Base class for cross product Markov decision process environments."""

    def __init__(
        self,
        ground_env: gym.Env,
        crm: CountingRewardMachine,
        lf: LabellingFunction[ObsType, ActType],
        max_steps: int,
    ) -> None:
        """Initialize the cross product Markov decision process environment."""
        self.ground_env = ground_env
        self.crm = crm
        self.lf = lf
        self.max_steps = max_steps

    @abstractmethod
    def _get_obs(
        self, ground_obs: GroundObsType, u: int, c: tuple[int, ...]
    ) -> ObsType:
        """Get the cross product observation."""

    def reset(
        self, *, seed: int | None = None, options: dict | None = None
    ) -> tuple[ObsType, dict]:
        """Reset the cross product environment."""
        super().reset(seed=seed, options=options)

        self.steps = 0
        self._u = self.crm.u_0
        self._c = self.crm.c_0
        ground_obs, _ = self.ground_env.reset()

        return (
            self._get_obs(ground_obs, self._u, self._c),
            {},
        )

    def step(self, action: ActType) -> tuple[ObsType, float, bool, bool, dict]:
        """Take a step in the cross product environment."""
        self.steps += 1
        self._ground_obs = self._ground_obs_next

        self._ground_obs_next, _, _, _, _ = self.ground_env.step(action)
        self._props = self.lf(self._ground_obs, action, self._ground_obs_next)

        self._u, self._c, reward_fn = self.crm.transition(self._u, self._c, self._props)
        reward = reward_fn(self._ground_obs, action, self._ground_obs_next)

        terminated = self._u in self.crm.F
        truncated = self.steps >= self.max_steps

        return (
            self._get_obs(self._ground_obs, self._u, self._c),
            reward,
            terminated,
            truncated,
            {},
        )

    def render(self) -> RenderFrame | list[RenderFrame] | None:
        """Render the cross product environment."""
        return self.ground_env.render()

    def generate_counterfactual_experience(self, ground_obs, action, next_ground_obs):
        """Generate counterfactual experiences."""
        (
            obs_buffer,
            action_buffer,
            obs_next_buffer,
            reward_buffer,
            done_buffer,
            info_buffer,
        ) = ([] for _ in range(6))

        for u_i in self.crm.U:
            for c_i in self.crm.sample_counter_configurations():
                # try:
                # TODO: Crash this so we can see what the exception should be
                u_j, c_j, rf_j = self.crm.transition(u_i, c_i, self._props)  # type: ignore
                # except:
                #     continue

                r_j = rf_j(ground_obs, action, next_ground_obs)

                obs_buffer.append(self._get_obs(ground_obs, u_i, c_i))
                action_buffer.append(action)
                obs_next_buffer.append(self._get_obs(next_ground_obs, u_j, c_j))
                reward_buffer.append(r_j)
                done_buffer.append(u_j in self.crm.F)
                info_buffer.append({})
        return (
            np.array(obs_buffer),
            np.array(action_buffer),
            np.array(obs_next_buffer),
            np.array(reward_buffer),
            np.array(done_buffer),
            np.array(info_buffer),
        )