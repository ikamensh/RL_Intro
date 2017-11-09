import random
import operator
import numpy as np
from Bandits.Agent import Agent
from Bandits.Bandit import Bandit, get_optimal_bandit_index
from Bandits.ploting import plot_moving_avg

alpha = 0.1
n_bandits = 10
n_trials = 2000
n_steps = 5000

reward_history=np.zeros((n_steps,n_trials))
optimal_choice_history=np.zeros((n_steps,n_trials))

for epsilon in [0.01, 0.05, 0.2]:
    for trial in range(n_trials):
        bandits = [Bandit() for i in range(n_bandits)]
        agent = Agent(0, n_bandits, epsilon)
        for step in range(n_steps):
            choice = agent.choose_action()
            reward = bandits[choice].play()
            agent.update_Q_average(choice, reward)

            optimal_bandit = get_optimal_bandit_index(bandits)

            for bandit in bandits:
                bandit.random_walk()

            reward_history[step,trial]=reward
            optimal_choice_history[step,trial] = 1 if optimal_bandit == choice else 0
        if trial % 100 == 0:
            print("trial "+str(trial) + "")

    params = "values_eps={}".format(epsilon)
    folder = "ex23/"
    plot_moving_avg(np.average(reward_history, axis=1),"step","reward","reward per step",
                    folder_path=folder+"reward_"+params)
    plot_moving_avg(np.average(optimal_choice_history, axis=1),"step","optimal?","Chance of choice being optimal",
                    folder_path=folder+"optimal_"+params)









