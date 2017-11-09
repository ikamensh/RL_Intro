from CarRentals.Environment import Environment
from scipy.stats import poisson

env = Environment()

for i in range(50):
    print(env.step(0))

print(poisson.pmf(3,3.5))
considered_amounts = [i for i in range(0, 10)]
print(considered_amounts)