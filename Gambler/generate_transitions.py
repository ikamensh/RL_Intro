from Gambler.Environment import Environment
from Gambler.generate_situations import situations

env = Environment()

cache_transitions = {}

# cache it - must be the most expensive part
def get_transitions(state):
    if (s1, s2, action) in cache_transitions:
        return cache_transitions[ (s1, s2, action) ]
    else:
        next_states = {}
        for situation in situations:
            dem_a = situation[0][0]
            ret_a = situation[0][1]
            dem_b = situation[0][2]
            ret_b = situation[0][3]
            prob = situation[1]
            env.set_state([s1, s2])
            state, reward = env.transition(dem_a, ret_a, dem_b, ret_b, action)
            if (state[0], state[1], reward) in next_states:
                next_states[(state[0], state[1], reward)] += prob
            else:
                next_states[(state[0], state[1], reward)] = prob
        cache_transitions[(s1, s2, action)] = next_states
        return next_states