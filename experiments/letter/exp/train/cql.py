import os

import gymnasium as gym
import hydra
import numpy as np
from omegaconf import DictConfig

import experiments.letter.lib  # noqa: F401 - register the environment
from crm.agents.tabular.cql import CounterfactualQLearningAgent


@hydra.main(config_path="../conf", config_name="config", version_base=None)
def main(config: DictConfig) -> None:
    """Train a Counterfactual Q-learning agent."""
    results = []

    for seed in range(config.exp.n_runs):
        env = gym.make("LetterWorld-v0", seed=seed)
        agent = CounterfactualQLearningAgent(env)
        returns = agent.learn(total_episodes=config.exp.n_episodes)
        results.append(returns)

    output_dir = os.path.join(config.exp.log_dir, "results_cql.npy")
    np.save(output_dir, results)


if __name__ == "__main__":
    main()
