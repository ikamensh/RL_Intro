from scipy.stats import poisson


#list of tuples (specific_outcome, prob)
def generate_situations(success_chance):
    assert 0 <= success_chance <= 1
    situations =  [(True, success_chance), (False, 1-success_chance)]
    print(situations)
    print("probabilities covered by generated outcomes: " + str(sum([sit[1] for sit in situations])))
    return situations

