import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus

class Simulation(object):
    '''
    Main class that will run the herd immunity simulation program.  Expects initialization
    parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.

    # This attribute will be used to keep track of all the people that catch
    # the infection during a given time step. We'll store each newly infected
    # person's .ID attribute in here.  At the end of each time step, we'll call
    # self._infect_newly_infected() and then reset .newly_infected back to an empty
    # list.

    # TODO: Create a Logger object and bind it to self.logger.  You should use this
    # logger object to log all events of any importance during the simulation.  Don't forget
    # to call these logger methods in the corresponding parts of the simulation!
    '''

    def __init__(self, population_size, vacc_percentage, virus_name,
                 mortality_rate, basic_repro_num, initial_infected=1):
        self.population_size = population_size
        self.vacc_percentage = vacc_percentage
        self.total_infected = initial_infected
        self.current_infected = initial_infected
        self.next_person_id = 0
        self.virus_name = virus_name
        self.mortality_rate = mortality_rate
        self.basic_repro_num = basic_repro_num
        self.virus = Virus(virus_name, mortality_rate, basic_repro_num)
        self.population = self._create_population(initial_infected)
        self.newly_infected = []
        # LOGGER
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, population_size, vacc_percentage, initial_infected)
        self.logger = Logger(self.file_name + '_log.txt')


    def _create_population(self, initial_infected):
        population = []
        infected_count = 0
        
        while len(population) < self.population_size:
            if infected_count <  initial_infected:
                population.append(Person(self.next_person_id, False, self.virus))
                infected_count += 1
                self.next_person_id += 1
            else:
                # Create vaccinated people
                random_num = random.uniform(0,1)
                if random_num < self.vacc_percentage:
                    population.append(Person(self.next_person_id, True, self.virus))
                    self.next_person_id += 1
                else:
                    # Create non-vaccinated non-infected people
                    population.append(Person(self.next_person_id, False))
                    self.next_person_id += 1
        return population

    def _simulation_should_continue(self):
        # print(str(self.current_infected) + " people are infected")
        all_dead = True
        for person in self.population:
            if person.is_alive:
                all_dead = False

        some_infected = False
        for person in self.population:
            if person.infection and person.is_alive:
                some_infected = True

        if all_dead or not some_infected:
            return False
        else:
            print("Someone is alive or not everyone is infected")
            return True

    def run(self):
        time_step_counter = 0
        should_continue = self._simulation_should_continue()

        while should_continue:
            self.logger.log_time_step(time_step_counter, self.current_infected)
            self.time_step()
            self._infect_newly_infected()
            should_continue = self._simulation_should_continue()

            time_step_counter += 1
        # print('The simulation has ended after' + str(time_step_counter) + 'turns.')

    def time_step(self):
        infected_people = []
        for person in self.population:
            if person.infection is not None and person.is_alive:
                infected_people.append(person)

        for infected in infected_people:
            interaction_counter = 0

            while interaction_counter < 100:
                # declare random person
                random_number = random.randint(0, self.population_size-1)
                random_person = self.population[random_number]

                # This will check whether the random person is alive or the smae infected person
                while not random_person.is_alive or random_person._id == infected._id:
                    random_number = random.randint(0, self.population_size-1)
                    random_person = self.population[random_number]

                #print("random_person has id" + str(random_person._id) + "\t random person is alive: " + str(random_person.is_alive) + "\t random person is vaccinated: " + str(random_person.is_vaccinated))
                self.interaction(infected, random_person)
                interaction_counter += 1

    def interaction(self, person, random_person):
        '''This method should be called any time two living
        people are selected for an interaction.  That means that only living people
        should be passed into this method.  Assert statements are included to make sure
        that this doesn't happen.
        '''
        assert person.is_alive == True
        assert random_person.is_alive == True

        if random_person.is_vaccinated:
            # print("random person is vaccinated")
            self.logger.log_interaction(person, random_person, False, True, False)
        elif random_person.infection != None:
            # print(str(random_person._id) + ' person is already infected')
            self.logger.log_interaction(person, random_person, False, False, True)
        else:
            random_number = random.uniform(0,1)
            # print(random_number)
            if random_number < self.basic_repro_num:
                self.newly_infected.append(random_person._id)
                #print("random person has been infected")
                self.logger.log_interaction(person, random_person, True, False, True)
            else:
                #print("random person got lucky, interacted with a infected person but did not get infected")
                self.logger.log_interaction(person, random_person, False, False, False)
        # Remember to call self.logger.log_interaction() during this method!

    def _infect_newly_infected(self):
        self.current_infected=0

        for person in self.population:
            if(person.infection is not None):
                person.did_survive_infection(self.mortality_rate)

        for _id in self.newly_infected:
            for person in self.population:
                if _id == person._id:
                    person.infection = self.virus
                    self.current_infected += 1

        self.newly_infected = []

if __name__ == "__main__":
    params = sys.argv[1:]
    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    basic_repro_num = float(params[4])
    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

simulation = Simulation(pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num, initial_infected)
simulation.run()
