from mesa import Model
from mesa.datacollection import DataCollector
from mesa.discrete_space import OrthogonalMooreGrid
from agents import SchellingAgent              ##importing from my own agent's file instead of Mesa's              
from mesa.experimental.scenarios import Scenario


class SchellingScenario(Scenario):
    """Scenario for the Schelling model.
    
    Args:
        width: Width of the grid
        height: Height of the grid
        density: Initial chance for a cell to be populated (0-1)
        minority_pc: Chance for an agent to be in minority class (0-1)
        homophily: Minimum number of similar neighbors needed for happiness
        radius: Search radius for checking neighbor similarity
        rng: Seed for reproducibility
    """

    height: int = 20
    width: int = 20
    density: float = 0.8
    minority_pc: float = 0.5
    homophily: float = 0.4
    radius: int = 1

                                    ##added new parameters: intervention_prob, intervention_effect, homophily_floor, rng 
    intervention_prob: float = 0.2
    intervention_effect: float = 0.04
    homophily_floor: float = 0.1
    rng: int = 42


class Schelling(Model):
    """Model class for the Schelling segregation model."""

    def __init__(self, scenario: SchellingScenario = SchellingScenario()):   ##added () after = SchellingScenario so model receives concrete object instead of class
        """
        Args:
            scenario: SchellingScenario containing model parameters.
        """
        super().__init__(scenario=scenario)

        # Model parameters
        self.density = scenario.density
        self.minority_pc = scenario.minority_pc
        
        self.intervention_prob = scenario.intervention_prob     ## New model parameters 
        self.intervention_effect = scenario.intervention_effect
        self.homophily_floor = scenario.homophily_floor 
        

        # Initialize grid
        self.grid = OrthogonalMooreGrid(
            (scenario.width, scenario.height), random=self.random, capacity=1
        )

        # Track happiness
        self.happy = 0

        # Set up data collection
        self.datacollector = DataCollector(
            model_reporters={
                "happy": "happy",
                "pct_happy": lambda m: (
                    (m.happy / len(m.agents)) * 100 if len(m.agents) > 0 else 0
                ),
                "population": lambda m: len(m.agents),
                "minority_pct": lambda m: (
                    sum(1 for agent in m.agents if agent.type == 1)
                    / len(m.agents)
                    * 100
                    if len(m.agents) > 0
                    else 0
                ),
            },
            agent_reporters={"agent_type": "type"},
        )

        # Create agents and place them on the grid
        for cell in self.grid.all_cells:
            if self.random.random() < self.density:
                agent_type = 1 if self.random.random() < scenario.minority_pc else 0
                SchellingAgent(
                    self,
                    cell,
                    agent_type,
                    homophily=scenario.homophily, 
                    radius=scenario.radius,
                )

        # Collect initial state
        self.agents.do("assign_state") 
        for agent in self.agents: ## At the initial state, no one should have had an interveniton 
            agent.received_intervention_this_round = False ## At the initial state, no one should have had an interveniton 
        self.datacollector.collect(self)

    def step(self):
        """Run one step of the model."""
        self.happy = 0  # Reset counter of happy agents 
        self.agents.shuffle_do("step")                     # Activate all agents (make agents move) in random order
        self.agents.do("assign_state")                     # Check happiness
        for agent in self.agents:                          ## for the beginning of EVERY ROUND agents act as though they never had an intervention
            agent.received_intervention_this_round = False ## for the beginning of EVERY ROUND agents act as though they never had an intervention
        self.agents.shuffle_do("cooperate")                ## agents randomly cooperate (i.e., are randomly injected with a cooperative task)
        self.happy = 0                                     ## make happiness counter start from 0 (or else we add agents that became happy as a result of moving (say, 40) to the number of agents that became happy thanks to intervention (say, 48). (without this line of code, when we only want 48, we get 40+48 = 88.)
        self.agents.do("assign_state")                     ## Re-check happiness after cooperation
        self.datacollector.collect(self)                   # Collect data
        self.running = self.happy < len(self.agents)       # Continue until everyone is happy

        
