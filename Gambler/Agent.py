import numpy as np

from Gambler.Environment import action_space, Environment
from Gambler.util import weighted_choice, draw_plot, timestamp

discount_rate = 0.9
N_actions = len(action_space)
state_delta_threshold = 1e-7
env = Environment(0.55)

class Agent:
    def __init__(self):
        self.V = np.zeros(100)
        self.Q = np.zeros((100, N_actions))
        self.policy = np.ones((100, N_actions))
        self.policyMax = np.zeros(100)

    def choose_action(self, state):
        choices = [(action_space[i], self.policy[state, i]) for i in range(N_actions)]
        return weighted_choice(choices)

    def prob_of_action(self, state, a_index):
        return self.policy[state, a_index] / np.sum(self.policy[state, :])

    def evaluate_policy(self):
        delta = np.zeros_like(self.V)
        for state in range(0, 100):
            v_old = self.V[state]
            V_under_current_policy = self.compute_state_value(state)
            delta[state] = abs(v_old - V_under_current_policy)
            self.V[state] = V_under_current_policy
        return np.amax(delta)

    def compute_state_value(self, state):
        V_under_current_policy = 0
        for index, action in enumerate(action_space):
            prob_action = self.prob_of_action(state, index)
            expected_return = self.get_disc_return(action, state)
            self.Q[state, index] = expected_return
            V_under_current_policy += expected_return * prob_action
        return V_under_current_policy

    def get_disc_return(self, action, state):
        sum_expectations = 0
        trans_dict = env.get_transitions(state, action)
        for state_reward_tuple in trans_dict:
            next_state = state_reward_tuple[0]
            reward = state_reward_tuple[1]
            prob_transition = trans_dict[state_reward_tuple]
            print(next_state)
            V_transition = reward + discount_rate * self.V[next_state]
            sum_expectations += V_transition * prob_transition
        return sum_expectations

    def update_policy(self):
        any_policy_changed = False
        for state in range(0, 100):
                expected_value = self.compute_state_value(state)
                for index, action in enumerate(action_space):
                    if self.Q[state, index] > expected_value:
                        self.policy[state, :] = 0
                        self.policy[state, index] = 1
                        self.policyMax[state] = action
                        any_policy_changed = True
                        break

        return any_policy_changed


    def value_iteration(self):
        delta = np.zeros_like(self.V)
        for state in range(0, 100):
                v_old = self.V[state]
                max_return = 0
                action_chosen = -999
                for action in action_space:
                    expected_return = self.get_disc_return(action, state)
                    if max_return < expected_return:
                        max_return = expected_return
                        action_chosen = action

                self.policyMax[state] = action_chosen
                V_under_current_policy = max_return
                delta[state] = abs(v_old - V_under_current_policy)
                self.V[state] = V_under_current_policy
        return np.amax(delta)


agent = Agent()

#implement termination


change = 1
i = 0
while change > state_delta_threshold:

    change = agent.evaluate_policy()
    change = agent.update_policy()

    i+=1
    timestamp(i, delta=change)
    draw_plot(agent.V, "V/{}.png".format(i))
    draw_plot(agent.policyMax, "Policy/{}.png".format(i))

