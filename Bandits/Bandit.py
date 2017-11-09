import random

class Bandit:
    def __init__(self, avg_reward=0):
        self.avg_reward =  avg_reward

    def play(self):
        return self.avg_reward + random.uniform(-1, 1)

    def random_walk(self):
        self.avg_reward += random.uniform(-1e-2, 1e-2)


def get_optimal_bandit_index(bandits):
    avg_rewards = [bandit.avg_reward for bandit in bandits]
    return avg_rewards.index(max(avg_rewards))