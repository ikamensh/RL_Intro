from scipy.stats import poisson


considered_amounts = [i for i in range(0, 10)]


def get_probable_values_and_p(considered, expected):
    result = []
    for val in considered:
        prob = poisson.pmf(val, expected)
        if prob > 1e-3:
            result.append((val, prob))

    return result


demand_a_expect = 3
return_a_expect = 3

demand_b_expect = 4
return_b_expect = 2


considered_demand_a = get_probable_values_and_p(considered_amounts, demand_a_expect)
considered_demand_b = get_probable_values_and_p(considered_amounts, demand_b_expect)
considered_return_a = get_probable_values_and_p(considered_amounts, return_a_expect)
considered_return_b = get_probable_values_and_p(considered_amounts, return_b_expect)

#list of tuples (specific_outcome, prob)
def create_possible_situations():
    possible = []
    for dem_a in considered_demand_a:
        for ret_a in considered_return_a:
            for dem_b in considered_demand_b:
                for ret_b in considered_return_b:
                    prob = dem_a[1] * ret_a[1] * dem_b[1] * ret_b[1]
                    if prob > 1e-4:
                        possible.append([[dem_a[0], ret_a[0], dem_b[0], ret_b[0]], prob])
    print("generated {} possible situations for env".format(len(possible)))
    print(possible)
    return possible


situations = create_possible_situations()
print("probabilities covered by generated outcomes: "+ str(sum([sit[1] for sit in situations ])))