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
        #이거...wouold my understandig b accurate in that 
        # MODEL SECTION: self.homphily_floor = scenario.homopihly floor (stores value?? 얜 뭐지: activate/ this the piece of paper below --- hace que sea viable  ---  "ok i'm ADOPTING the rule on the piece of paper" --- so this is what the world actually uses. AKA [PASSED LEGISLATION - IS IN EFFECT]
        # MODEL SECTION: homophily_floor: float = 0.1 (ただのplaceholder value, like a piece of paper sitting on a desk that says "floor should be 0.1".)     AKA [UNPASSED LEGISLATION]
        # AGENT SECTION:  actually applies hoomophily floor value - SPEAKING OF WHICH DONT I HAVE TO ADD SELF.HOMOPHILY_FLOOR TO AGENTS?!!!!!! no, again, homoph_floor is a global rule anyways. AKA [IMPLEMENTATION OF LEGISLATION]

        #scenario "this is what the homophily" model tells agent "this is ur homoph" agent implement == this is equiavelnt to just agents saying "this is what the law says" -- u have to store inside agent if u want agent to have different homophs 
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
                    homophily=scenario.homophily,  #why not add scenario.homophily_floor??????A. you could, but do not need to. homophily_floor is a global rule. 그럼 대체 왜 self, cell,agent type, homophily, radius 도 다 global rule 아님? no ----- bc they can be different per/vary with the agent!! then what about radius? in this world, im not changing the radius at all. yup. but maybe...in the future I might want to -me voy a tirar del pelo HAHA 
                    radius=scenario.radius,
                )

        # Collect initial state
        self.agents.do("assign_state") 
        for agent in self.agents: #at the initial state, no one should have had an interveniton
            agent.received_intervention_this_round = False #for round NUMBER ONE 
        self.datacollector.collect(self)

    def step(self):
        """Run one step of the model."""
        self.happy = 0  # Reset counter of happy agents (world임!) 
        self.agents.shuffle_do("step")  # Activate all agents (make agents move) in random order
        self.agents.do("assign_state") #Recalculate happiness
        for agent in self.agents:    # for EVERY ROUND u guys act like u never had intervention
            agent.received_intervention_this_round = False
        self.agents.shuffle_do("cooperate") #apply cooperation intervention here? or before assign_state? AFTER! - to make agents move > check happiness > inject cooperation>reduction in homophily for those that apply > next round 
        self.happy = 0   #makehapiness counter 0 (or else we add agents that became happy as a result of moving (say, 40) + to agetns that became happy bc intervention (48). We only want 48. Now it becomes 40+48 = 88.)
        self.agents.do("assign_state")
        self.datacollector.collect(self)  # Collect data
        self.running = self.happy < len(self.agents)  # Continue until everyone is happy

        
