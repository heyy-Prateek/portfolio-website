"""
Batch Reactor Experiment
=======================

This module simulates an isothermal batch reactor with a first-order reaction.
"""

import math
import numpy as np
import time

# Experiment metadata
name = "Isothermal Batch Reactor"
description = "Simulation of a first-order reaction (A → B) in an isothermal batch reactor."

# Default parameters for the experiment
default_parameters = {
    "initial_concentration": 1.0,  # mol/L
    "rate_constant": 0.1,          # min^-1
    "reactor_volume": 1.0,         # L
    "simulation_time": 60.0,       # min
    "step_interval": 0.5           # min
}

# Equations used in the simulation
equations = [
    "\\frac{dC_A}{dt} = -k C_A",
    "C_A(t) = C_{A0} e^{-kt}",
    "C_B(t) = C_{A0} (1 - e^{-kt})"
]

# Variables and their descriptions
variables = {
    "C_A": "Concentration of reactant A (mol/L)",
    "C_B": "Concentration of product B (mol/L)",
    "k": "Rate constant (min^-1)",
    "t": "Time (min)",
    "C_{A0}": "Initial concentration of A (mol/L)",
    "V": "Reactor volume (L)"
}

class Simulation:
    """
    Simulation class for the batch reactor experiment.
    """
    
    def __init__(self, parameters):
        """
        Initialize the simulation with the given parameters.
        
        Args:
            parameters: Dictionary of simulation parameters
        """
        self.parameters = parameters
        self.current_time = 0.0
        self.data_points = []
        self.conversion = []
        self.conc_a = []
        self.conc_b = []
        self.times = []
        
        # Get parameters
        self.initial_conc = parameters.get("initial_concentration", default_parameters["initial_concentration"])
        self.k = parameters.get("rate_constant", default_parameters["rate_constant"])
        self.volume = parameters.get("reactor_volume", default_parameters["reactor_volume"])
        self.max_time = parameters.get("simulation_time", default_parameters["simulation_time"])
        self.step_interval = parameters.get("step_interval", default_parameters["step_interval"])
    
    def step(self):
        """
        Run a single simulation step.
        
        Returns:
            Dictionary containing simulation results for this step
        """
        # Update simulation time
        self.current_time += self.step_interval
        
        # Calculate concentrations
        ca = self.initial_conc * math.exp(-self.k * self.current_time)
        cb = self.initial_conc - ca
        conversion = (self.initial_conc - ca) / self.initial_conc * 100
        
        # Store data
        self.times.append(self.current_time)
        self.conc_a.append(ca)
        self.conc_b.append(cb)
        self.conversion.append(conversion)
        
        # Calculate reaction rate
        reaction_rate = self.k * ca
        
        # Return current data
        return {
            "time": self.current_time,
            "concentration_a": ca,
            "concentration_b": cb,
            "conversion": conversion,
            "reaction_rate": reaction_rate,
            "times": self.times,
            "conc_a": self.conc_a,
            "conc_b": self.conc_b,
            "conversion_history": self.conversion
        }
    
    def is_finished(self):
        """
        Check if the simulation is finished.
        
        Returns:
            True if simulation has reached its end time, False otherwise
        """
        return self.current_time >= self.max_time
    
    def get_step_interval(self):
        """
        Get the time interval between simulation steps.
        
        Returns:
            Step interval in seconds (for real-time simulation)
        """
        # Convert from simulation minutes to real seconds
        # Use a small value for faster simulation
        return 0.1

# Standalone step function for the generic simulator
def step(parameters, current_time):
    """
    Calculate system state at the given time.
    
    Args:
        parameters: Dictionary of simulation parameters
        current_time: Current simulation time
        
    Returns:
        Dictionary containing simulation results
    """
    # Get parameters
    initial_conc = parameters.get("initial_concentration", default_parameters["initial_concentration"])
    k = parameters.get("rate_constant", default_parameters["rate_constant"])
    
    # Calculate concentrations
    ca = initial_conc * math.exp(-k * current_time)
    cb = initial_conc - ca
    conversion = (initial_conc - ca) / initial_conc * 100
    
    # Calculate reaction rate
    reaction_rate = k * ca
    
    # Return current data
    return {
        "time": current_time,
        "concentration_a": ca,
        "concentration_b": cb,
        "conversion": conversion,
        "reaction_rate": reaction_rate
    }

# Thumbnail image path (optional)
thumbnail = None 