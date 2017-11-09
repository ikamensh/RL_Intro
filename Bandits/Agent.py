import random
import numpy as np
from CarRentals.util import weighted_choice

class Agent:
    def __init__(self, Q_initial, N_bandits, e):
        self.Q = [ Q_initial for i in range(N_bandits)]
        self.times_tried = [0 for i in range(N_bandits)]
        self.N_bandits = N_bandits
        self.e = e

    def choose_action(self):
        if random.uniform(0, 1)< self.e:
            return random.randint(0, self.N_bandits-1)
        else:
            return self.Q.index(max(self.Q))

    def choose_action_softmax(self, t):
        greedy_a = self.Q.index(max(self.Q))
        if random.uniform(0, 1)< self.e:
            allowed_actions = [i for i in range(self.N_bandits) if i!= greedy_a]
            temp = t*np.array(self.Q)
            temp = np.concatenate((temp[:greedy_a], temp[greedy_a+1:]))
            e_x = np.exp(temp - np.max(temp))
            smax = e_x / np.sum(e_x)
            choices = [(allowed_actions[i], prob) for i, prob in enumerate(smax)]
            return weighted_choice(choices)
        else:
            return self.Q.index(max(self.Q))


    def update_Q_average(self, n_action, reward):
        self.times_tried[n_action]+=1
        self.Q[n_action] = self.Q[n_action]*(self.times_tried[n_action]-1)/self.times_tried[n_action]\
                           + reward / self.times_tried[n_action]

    def update_Q_decay(self, n_action, reward, decay_coef):
        self.times_tried[n_action]+=1
        self.Q[n_action] = self.Q[n_action] + (reward-self.Q[n_action])*decay_coef





def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()