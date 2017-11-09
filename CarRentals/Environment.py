from numpy.random import poisson

limit_cars_per_location = 20
own_parking = 10
revenue_per_car = 10
cost_per_car_transport = 2
action_space = [i for i in range(-5, 5)]


class Environment:
    def __init__(self):
        self.rental_a = Rental_location(3, 3)
        self.rental_b = Rental_location(4, 2)
        self.day = 0

    def set_state(self, state):
        self.rental_a.cars_ready = state[0]
        self.rental_b.cars_ready = state[1]

    def get_state(self):
        return [self.rental_a.cars_ready, self.rental_b.cars_ready]

    def transition(self, demand_a, return_a, demand_b, return_b, n_transport):
        revenue = 0
        revenue -= self.transport_any_dir(n_transport)
        revenue += self.rental_a.step_specific(demand_a, return_a)
        revenue += self.rental_b.step_specific(demand_b, return_b)
        return self.get_state(), revenue

    def transport_cars(self, cars_wished_to_transp, transp_from, transp_to):
        if cars_wished_to_transp < 0:
            return 0

        cars_transported = min(transp_from.cars_ready, cars_wished_to_transp)
        transp_from.cars_ready -= cars_transported
        transp_to.add_cars_to_rdy(cars_transported)

        cost = 2 * cars_transported

        return cost



    def transport_any_dir(self, cars_wished_to_transp):
        transp_cost = 0
        if cars_wished_to_transp > 0:
            # special condition: 1 car transported for free!
            self.transport_cars(1, self.rental_a, self.rental_b)
            transp_cost = self.transport_cars(cars_wished_to_transp-1, self.rental_a, self.rental_b)
        else:
            transp_cost = self.transport_cars(-cars_wished_to_transp, self.rental_b, self.rental_a)
        return transp_cost

    def step(self, cars_wished_to_transp_a_to_b):

        revenue = 0
        revenue -= self.transport_any_dir(cars_wished_to_transp_a_to_b)
        revenue += self.rental_a.step()
        revenue += self.rental_b.step()

        return self.get_state(), revenue


class Rental_location:
    def __init__(self, expected_demand, expected_return):
        self.cars_ready = 0
        self.expected_demand = expected_demand
        self.expected_return = expected_return

    def step(self):
        demand_today = poisson(self.expected_demand)
        return_today = poisson(self.expected_return)
        return self.step_specific(demand_today, return_today)

    def step_specific(self, demand_today, return_today):

        rented_today = min(demand_today, self.cars_ready)
        self.cars_ready -= rented_today
        revenue = rented_today * 10
        self.add_cars_to_rdy(return_today)
        #special condition - for every car over 10 pieces pay $4 for parking
        if self.cars_ready > own_parking:
            revenue -= self.cars_ready * 4

        return revenue

    def add_cars_to_rdy(self, n):
        self.cars_ready += n
        if self.cars_ready > limit_cars_per_location:
            self.cars_ready = limit_cars_per_location


