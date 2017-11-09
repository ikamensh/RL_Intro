import random
from Gambler.generate_situations import generate_situations
from numpy.random import poisson


action_space = [i for i in range(1, 100)]
goal_amount = 100


class Environment:
    def __init__(self, success_chance):
        self.player_money = 20
        self.success_chance = success_chance
        self.cache_transitions = {}

    def is_action_valid(self, gamble_amount):
        return 1 <= gamble_amount <= self.player_money

    def step_deterministic(self, gamble_amount, success):

        if not self.is_action_valid(gamble_amount):
            return -1, False
        else:
            if success:
                self.player_money += gamble_amount
            else:
                self.player_money -= gamble_amount
            if self.player_money >= goal_amount:
                self.player_money = 20
                return 1, True
            elif self.player_money == 0:
                self.player_money = 20
                return -1, True
            else:
                return 0, False



    def step(self, gamble_amount):

            if random.uniform < self.success_chance:
                return self.step_deterministic(gamble_amount, True)
            else:
                return self.step_deterministic(gamble_amount, False)



    # cache it - must be the most expensive part
    def get_transitions(self, state, gamble_amount):
        if (state, gamble_amount) in self.cache_transitions:
            return self.cache_transitions[(state, gamble_amount)]
        else:
            next_states = {}
            env = Environment(self.success_chance)

            for situation in generate_situations(self.success_chance):
                success = situation[0]
                prob = situation[1]
                env.player_money = state
                reward, _ = env.step_deterministic(gamble_amount, success)
                new_state = env.player_money
                if (new_state, reward) in next_states:
                    next_states[(new_state, reward)] += prob
                else:
                    next_states[(new_state, reward)] = prob
            self.cache_transitions[(state, gamble_amount)] = next_states
            return next_states










