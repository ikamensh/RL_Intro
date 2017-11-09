import numpy as np

from CarRentals.Environment import action_space
from CarRentals.generate_transitions import get_transitions
from CarRentals.util import weighted_choice, draw_2darray, timestamp

discount_rate = 0.9

state_delta_threshold = 1e-3


class Agent:
    def __init__(self):
        self.V = np.zeros((21, 21))
        self.Q = np.zeros((21, 21, len(action_space)))
        self.policy = np.ones((21, 21, len(action_space)))
        self.policyMax = np.zeros((21, 21))

    def choose_action(self, state):
        cars_at_a = state[0]
        cars_at_b = state[1]
        choices = [(action_space[i], self.policy[cars_at_a, cars_at_b, i]) for i in range(len(action_space))]
        return weighted_choice(choices)

    def prob_of_action(self, s1, s2, a_index):
        return self.policy[s1, s2, a_index] / np.sum(self.policy[s1, s2, :])

    def evaluate_policy(self):
        delta = np.zeros_like(self.V)
        for s1 in range(0, 21):
            for s2 in range(0, 21):
                v_old = self.V[s1, s2]
                V_under_current_policy = self.compute_state_value(s1, s2)
                delta[s1, s2] = abs(v_old - V_under_current_policy)
                self.V[s1, s2] = V_under_current_policy
        return np.amax(delta)

    def compute_state_value(self, s1, s2):
        V_under_current_policy = 0
        for index, action in enumerate(action_space):
            prob_action = self.prob_of_action(s1, s2, index)
            expected_return = self.get_disc_return(action, s1, s2)
            self.Q[s1, s2, index] = expected_return
            V_under_current_policy += expected_return * prob_action
        return V_under_current_policy

    def get_disc_return(self, action, s1, s2):
        sum_expectations = 0
        trans_dict = get_transitions(s1, s2, action)
        for state_reward_tuple in trans_dict:
            next_state = [ state_reward_tuple[0], state_reward_tuple[1] ]
            reward = state_reward_tuple[2]
            prob_transition = trans_dict[state_reward_tuple]
            V_transition = reward + discount_rate * self.V[next_state[0], next_state[1]]
            sum_expectations += V_transition * prob_transition
        return sum_expectations

    def update_policy(self):
        any_policy_changed = False

        for s1 in range(0, 21):
            for s2 in range(0, 21):
                expected_value = self.compute_state_value(s1, s2)
                for index, action in enumerate(action_space):
                    if self.Q[s1, s2, index] > expected_value:
                        self.policy[s1, s2, :] = 0
                        self.policy[s1, s2, index] = 1
                        self.policyMax[s1, s2] = action
                        any_policy_changed = True
                        break

        return any_policy_changed


    def value_iteration(self):
        delta = np.zeros_like(self.V)
        for s1 in range(0, 21):
            for s2 in range(0, 21):
                v_old = self.V[s1, s2]
                max_return = 0
                action_chosen = -999
                for action in action_space:
                    expected_return = self.get_disc_return(action, s1, s2)
                    if max_return < expected_return:
                        max_return = expected_return
                        action_chosen = action

                self.policyMax[s1, s2] = action_chosen
                V_under_current_policy = max_return

                delta[s1, s2] = abs(v_old - V_under_current_policy)
                self.V[s1, s2] = V_under_current_policy
        return np.amax(delta)


agent = Agent()

#implement termination


change = 1
i = 0
while change > state_delta_threshold:

    change = agent.value_iteration()

    i+=1
    timestamp(i, delta=change)
    draw_2darray(agent.V, "V/{}.png".format(i))
    draw_2darray(agent.policyMax, "Policy/{}.png".format(i))

