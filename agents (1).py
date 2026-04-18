from mesa.discrete_space import CellAgent

class SchellingAgent(CellAgent):
#birth: 
    def __init__(
        self, model, cell, agent_type: int, homophily: float = 0.4, radius: int = 1
    ): 
#lock in birth traits:         
        super().__init__(model)
        self.cell = cell
        self.type = agent_type
        self.homophily = homophily
        self.radius = radius
        self.happy = False
        self.received_intervention_this_round = False ###################
        
#define my state by defining what a neighbor is 
    def assign_state(self): 
        neighbors = list(self.cell.get_neighborhood(radius=self.radius).agents)

# Count similar neighbors
        similar_neighbors_count = len([n for n in neighbors if n.type == self.type])

# Calculate the fraction of similar neighbors
        if (valid_neighbors_count := len(neighbors)) > 0:
            similarity_fraction = similar_neighbors_count / valid_neighbors_count
        else:
# If there are no neighbors, the similarity fraction is 0
            similarity_fraction = 0.0

        if similarity_fraction < self.homophily:
            self.happy = False
        else:
            self.happy = True
            self.model.happy += 1
#Let's inject cooperation intervention  - copy from def assign_state(self)       
    def cooperate(self):    #i'm ab to try coop 
        if self.received_intervention_this_round:
            return  ###if agent had intervention this round, stop immediately, otherwise...
              #start doing the work (look for neighbors...) 
        neighbors = list(self.cell.get_neighborhood(radius=self.radius).agents)

            #only choose unlike neighbors who havent already gotten an intervention  
        unlike_neighbors = [n for n in neighbors if n.type != self.type and not n.received_intervention_this_round]

#if there are no unlike neighbors, do nothing 
        if len(unlike_neighbors) == 0:
           return
#generate a random # btw 0 and 1. If that's smaller than the intervention probability,intervention happens _ 참고 if self.random.random()<self.density  - each agent has a 20% chance of intervention_느낌: 👉 Density: “Each cell has 60% chance → many cells → ~60% filled" 👉 Intervention:“Each agent has 20% chance → many agents → ~20% intervened”
        if self.random.random() < self.model.intervention_prob:
 
#now than u received intervention, then, pick one unlike neighbor at random   
            partner = self.random.choice(unlike_neighbors)
#don't let homophily go below minimum - how? use max() tool - max(A,B) means "choose the bigger number" --> max(floor, lowered homoph as a result of intervention)   
            self.homophily = max(self.model.homophily_floor, self.homophily -self.model.intervention_effect)
#partner's homoph에도 apply
            partner.homophily = max(self.model.homophily_floor, partner.homophily - self.model.intervention_effect)
            self.received_intervention_this_round = True
            partner.received_intervention_this_round = True

#move if unhappy
    def step(self): 
   
        if not self.happy:
            self.cell = self.model.grid.select_random_empty_cell()


##LIST OF STUFF TO DO FOR MODEL 
#1.MAKE SURE MODEL RESETS SELF.HAPPY = 0 AT THE START 
#2.MAKE self.intervention_effect = scenario.intervention_effect AND!!! self.homophily_floor = scenario.homophily_floor ---> effect 0.2
#2-2. homophily drop by 0.04 
#3. self.intervention_effect = scenario.intervention_effect AND self.homophily_floor = scenario.homophily_floor ---> homophily floor 0.1
#4. self.model.intervention_effect  % 정하기 

#5. 이것도 하기: self.happy = 0 
# self.agents.shuffle_do("step")        # move first
# self.agents.shuffle_do("cooperate")   # then intervene
# self.agents.do("assign_state")        # then recompute happiness using new homophily
# self.datacollector.collect(self)
# self.running = self.happy < len(self.agents)

# this sequences the agents to move after intervention. In the AGENTS section only this: 
#def step(self):
    #if not self.happy:
        # self.cell = self.model.grid.select_random_empty_cell()

#6. add new intervention stage in step()
#7. place intervention after movement! after assign_state????... so after self.agents.do("assign_state") and before self.data.collect(self)????



