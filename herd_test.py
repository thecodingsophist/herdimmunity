import pytest
import io
import sys
import logger
import person
import simulation
import virus

def test_population_creation():
    sim = simulation.Simulation(100, 0.2, "Ebola", 0.7, 0.5, 5)
    assert sim.population_size == len(sim.population)

def test_simulation_should_continue():
    sim = simulation.Simulation(100, 0.2, "Ebola", 0.7, 0.5, 5)
    any_infected = True
    if sim.current_infected == 0:
        any_infected = False
    assert sim._simulation_should_continue() == any_infected
