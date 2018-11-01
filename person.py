import random

class Person(object):
    '''
    Person objects will populate the simulation.
    '''
    def __init__(self, _id, is_vaccinated, infection=None):
        # FIXME: Add comment explanation for what this method does
        self._id = _id
        self.is_vaccinated = is_vaccinated
        self.is_alive = True
        self.infection = infection

    def did_survive_infection(self, survival_rate):
        survivaL_rate = random.uniform(0,1)
        #PERSON IS DEAD IF MORTALITY RATE IS GREATER THAN SURVIVAL RATE
        if self.infection.mortality_rate > survival_rate:
            self.is_alive = False
            return False
        #PERSON IS VACCINATED IF SURVIVES THE INFECTION
        else:
            self.is_vaccinated = True
            self.infection = None
            return True
