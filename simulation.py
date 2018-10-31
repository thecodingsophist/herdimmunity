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

    _____Attributes______

    logger: Logger object.  The helper object that will be responsible for writing
    all logs to the simulation.

    population_size: Int.  The size of the population for this simulation.

    population: [Person].  A list of person objects representing all people in
        the population.

    next_person_id: Int.  The next available id value for all created person objects.
        Each person should have a unique _id value.

    virus_name: String.  The name of the virus for the simulation.  This will be passed
    to the Virus object upon instantiation.

    mortality_rate: Float between 0 and 1.  This will be passed
    to the Virus object upon instantiation.

    basic_repro_num: Float between 0 and 1.   This will be passed
    to the Virus object upon instantiation.

    vacc_percentage: Float between 0 and 1.  Represents the total percentage of population
        vaccinated for the given simulation.

    current_infected: Int.  The number of currently people in the population currently
        infected with the disease in the simulation.

    total_infected: Int.  The running total of people that have been infected since the
    simulation began, including any people currently infected.

    total_dead: Int.  The number of people that have died as a result of the infection
        during this simulation.  Starts at zero.


    _____Methods_____

    __init__(population_size, vacc_percentage, virus_name, mortality_rate,
     basic_repro_num, initial_infected=1):
        -- All arguments will be passed as command-line arguments when the file is run.
        -- After setting values for attributes, calls self._create_population() in order
            to create the population array that will be used for this simulation.

    _create_population(self, initial_infected):
        -- Expects initial_infected as an Int.
        -- Should be called only once, at the end of the __init__ method.
        -- Stores all newly created Person objects in a local variable, population.
        -- Creates all infected person objects first.  Each time a new one is created,
            increments infected_count variable by 1.
        -- Once all infected person objects are created, begins creating healthy
            person objects.  To decide if a person is vaccinated or not, generates
            a random number between 0 and 1.  If that number is smaller than
            self.vacc_percentage, new person object will be created with is_vaccinated
            set to True.  Otherwise, is_vaccinated will be set to False.
        -- Once len(population) is the same as self.population_size, returns population.
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
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, population_size, vacc_percentage, initial_infected)



        # TODO: Create a Logger object and bind it to self.logger.  You should use this
        # logger object to log all events of any importance during the simulation.  Don't forget
        # to call these logger methods in the corresponding parts of the simulation!
        self.logger = Logger(self.file_name + '_log.txt')

        # This attribute will be used to keep track of all the people that catch
        # the infection during a given time step. We'll store each newly infected
        # person's .ID attribute in here.  At the end of each time step, we'll call
        # self._infect_newly_infected() and then reset .newly_infected back to an empty
        # list.
        self.newly_infected = []
        # TODO: Call self._create_population() and pass in the correct parameters.
        # Store the array that this method will return in the self.population attribute.

    def _create_population(self, initial_infected):
        # TODO: Finish this method!  This method should be called when the simulation
        # begins, to create the population that will be used. This method should return
        # an array filled with Person objects that matches the specifications of the
        # simulation (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).
        population = []
        infected_count = 0
        # FIXME: maybe the simulation can create the virus as opposed to create population
        while len(population) < self.population_size:
            if infected_count <  initial_infected:
                # Create all the infected people first, and then worry about the rest.
                # Don't forget to increment infected_count every time you create a
                # new infected person!
                population.append(Person(self.next_person_id, False, self.virus))
                infected_count += 1
                self.next_person_id += 1
            else:
                # Now create all the rest of the people.
                # Every time a new person will be created, generate a random number between
                # 0 and 1.  If this number is smaller than vacc_percentage, this person
                # should be created as a vaccinated person. If not, the person should be
                # created as an unvaccinated person.
                random_num = random.uniform(0,1)
                if random_num < self.vacc_percentage:
                    population.append(Person(self.next_person_id, True, self.virus))
                    self.next_person_id += 1
                else:
                    population.append(Person(self.next_person_id, False))
                    self.next_person_id += 1
            # After any Person object is created, whether sick or healthy,
            # you will need to increment self.next_person_id by 1. Each Person object's
            # ID has to be unique!
        return population

    def _simulation_should_continue(self):
        # Complete this method!  This method should return True if the simulation
        # should continue, or False if it should not.  The simulation should end under
        # any of the following circumstances:
        #     - The entire population is dead.
        #     - There are no infected people left in the population.
        # In all other instances, the simulation should continue.
        print(str(self.current_infected) + " people are infected")
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
        # Finish this method.  This method should run the simulation until
        # everyone in the simulation is dead, or the disease no longer exists in the
        # population. To simplify the logic here, we will use the helper method
        # _simulation_should_continue() to tell us whether or not we should continue
        # the simulation and run at least 1 more time_step.

        # This method should keep track of the number of time steps that
        # have passed using the time_step_counter variable.  Make sure you remember to
        # the logger's log_time_step() method at the end of each time step, pass in the
        # time_step_counter variable!
        time_step_counter = 0
        # Remember to set this variable to an initial call of
        # self._simulation_should_continue()!
        should_continue = self._simulation_should_continue()
        while should_continue:
        # for every iteration of this loop, call self.time_step() to compute another
        # round of this simulation.  At the end of each iteration of this loop, remember
        # to rebind should_continue to another call of self._simulation_should_continue()!
            self.logger.log_time_step(time_step_counter, self.current_infected)
            self.time_step()
            self._infect_newly_infected()
            should_continue = self._simulation_should_continue()
            
            time_step_counter += 1
        print('The simulation has ended after' + str(time_step_counter) + 'turns.')

    def time_step(self):
        # Finish this method!  This method should contain all the basic logic
        # for computing one time step in the simulation.  This includes:
            # - For each infected person in the population:
            #        - Repeat for 100 total interactions:
            #             - Grab a random person from the population.
            #           - If the person is dead, continue and grab another new
            #                 person from the population. Since we don't interact
            #                 with dead people, this does not count as an interaction.
            #           - Else:
            #               - Call simulation.interaction(person, random_person)
            #               - Increment interaction counter by 1.
        infected_people = [] 
        for person in self.population:
            if person.infection != None and person.is_alive:
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
        # Finish this method! This method should be called any time two living
        # people are selected for an interaction.  That means that only living people
        # should be passed into this method.  Assert statements are included to make sure
        # that this doesn't happen.
        assert person.is_alive == True
        assert random_person.is_alive == True

        # The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0 and 1.  If that number is smaller
            #     than basic_repro_num, random_person's ID should be appended to
            #     Simulation object's newly_infected array, so that their .infected
            #     attribute can be changed to True at the end of the time step.

        if random_person.is_vaccinated:
            print("random person is vaccinated")
            self.logger.log_interaction(person, random_person, False, True, False)
        elif random_person.infection != None:
            print(str(random_person._id) + ' person is already infected')
            self.logger.log_interaction(person, random_person, False, False, True)
        else:
            random_number = random.uniform(0,1)
            print(random_number)
            if random_number < self.basic_repro_num:

                self.newly_infected.append(random_person._id)
                #print("random person has been infected")
                self.logger.log_interaction(person, random_person, True, False, True)
            else:
                #print("random person got lucky, interacted with a infected person but did not get infected")
                self.logger.log_interaction(person, random_person, False, False, False)
        # Remember to call self.logger.log_interaction() during this method!

        '''
        person1, person2, did_infect=None,person2_vacc=None, person2_sick=None
        '''

    def _infect_newly_infected(self):
        # Finish this method! This method should be called at the end of
        # every time step.  This method should iterate through the list stored in
        # self.newly_infected, which should be filled with the IDs of every person
        # created.  Iterate though this list.
        # For every person id in self.newly_infected:
        #   - Find the Person object in self.population that has this corresponding ID.
        #   - Set this Person's .infected attribute to True.
        print(self.newly_infected)
        self.current_infected=0

        for person in self.population:
            if(person.infection != None):
                person.did_survive_infection(self.mortality_rate)

        for _id in self.newly_infected:
            for person in self.population:
                if _id == person._id:
                    person.infection = self.virus
                    self.current_infected += 1

        # Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list!
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
