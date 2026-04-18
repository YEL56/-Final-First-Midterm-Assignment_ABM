from mesa.discrete_space import CellAgent 

class SchellingAgent(CellAgent):
#birth of agents: 
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
        self.received_intervention_this_round = False ##agent has not received intervention at initialization
        
#define my state by defining what a neighbor is 
    def assign_state(self): 
        neighbors = list(self.cell.get_neighborhood(radius=self.radius).agents)

# Count similar neighbors
        similar_neighbors_count = len([n for n in neighbors if n.type == self.type])

# Calculate the fraction of similar neighbors
        if (valid_neighbors_count := len(neighbors)) > 0:    ##Changed label from valid_neighbors to valid_neigbhors_count as it is a counter
            similarity_fraction = similar_neighbors_count / valid_neighbors_count ##Changed label from similar_neighbors to similar_neigbhors_count as it is a counter
        else:
# If there are no neighbors, the similarity fraction is 0
            similarity_fraction = 0.0

        if similarity_fraction < self.homophily:
            self.happy = False
        else:
            self.happy = True
            self.model.happy += 1
#Let's inject cooperation intervention                  ## Introducing cooperative intervention task       
    def cooperate(self):    #i'm ab to try coop         ## Defined what cooperation means for agent
        if self.received_intervention_this_round:       ## If agent had intervention this round, stop immediately, otherwise...
            return                                     
        neighbors = list(self.cell.get_neighborhood(radius=self.radius).agents) ## Start doing the work of looking for neighbors
 
        unlike_neighbors = [n for n in neighbors if n.type != self.type and not n.received_intervention_this_round] ## among all neighbors, only choose unlike neighbors who havent already gotten an intervention 

        if len(unlike_neighbors) == 0:              ##if there are no unlike neighbors, do nothing 
           return
        if self.random.random() < self.model.intervention_prob: ## generate a random number btw 0 and 1. If that's smaller than the intervention probability,intervention happens 
   
            partner = self.random.choice(unlike_neighbors)      ## now than an agent received intervention, then, pick one unlike neighbor at random
            self.homophily = max(self.model.homophily_floor, self.homophily -self.model.intervention_effect) ## don't let homophily go below minimum "homophily_floor"
            partner.homophily = max(self.model.homophily_floor, partner.homophily - self.model.intervention_effect) ## don't let homophily go below minimum "homophily_floor" for counterpart agent (neighbor) as well
            self.received_intervention_this_round = True     ## both me and counterpart agent (neighbor) I interacted with received an intervention
            partner.received_intervention_this_round = True  ## both me and counterpart agent (neighbor) I interacted with received an intervention

#move if unhappy
    def step(self): 
   
        if not self.happy:
            self.cell = self.model.grid.select_random_empty_cell()






