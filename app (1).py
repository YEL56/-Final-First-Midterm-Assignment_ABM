import os

import solara

from model import Schelling, SchellingScenario          ##import from my own model instead of Mesa's 
from mesa.visualization import (
    Slider,
    SolaraViz,
    SpaceRenderer,
    make_plot_component,
)
from mesa.visualization.components import AgentPortrayalStyle


def get_happy_agents(model):
    """Display a text count of how many happy agents there are."""
    return solara.Markdown(f"**Happy agents: {model.happy}**")


#path = os.path.dirname(os.path.abspath(__file__))
path = os.getcwd()           ## debugging: use current directory


def agent_portrayal(agent):
    #if agent is happy
    style = AgentPortrayalStyle(
        x=agent.cell.coordinate[0],
        y=agent.cell.coordinate[1],
        marker="o",                        ## changed to marker value matplotlib accepts 
        size=75,
    )
    #COLOR CHANGE 
    if agent.type == 0:
        style.update(("color","blue"))     ## color (agent type) separately added
    else:
        style.update(("color","orange"))   ## color (agent type) separately added 
    #HAPPY STATUS CHANGE
    if not agent.happy:   
        style.update(                        
            ("marker", "x"),                ## changed to marker value matplotlib accepts 
            ("size", 50),
            ("zorder", 2), 
        )

    return style


model_params = {
    "rng": Slider("Random Seed", 42, 1, 100, 1),      ## added rng as parameter in slider form so it's treated as an integer, not text
    "density": Slider("Agent density", 0.8, 0.1, 1.0, 0.1),
    "minority_pc": Slider("Fraction minority", 0.2, 0.0, 1.0, 0.05),
    "homophily": Slider("Homophily", 0.4, 0.0, 1.0, 0.125),
    "width": 20,
    "height": 20,
    "intervention_prob": Slider("Intervention Probability", 0.2, 0.0, 1.0, 0.05),  #added intervention probability slider
    "intervention_effect": Slider("Intervention Effect", 0.04, 0.0, 0.2, 0.01) #added intervention effect slider
    }


# Note: Models with images as markers are very performance intensive.
model1 = Schelling(scenario=SchellingScenario())
renderer = SpaceRenderer(model1, backend="matplotlib").setup_agents(agent_portrayal)
# Here we use renderer.render() to render the agents and grid in one go.
# This function always renders the grid and then renders the agents or
# property layers on top of it if specified.
renderer.render()

HappyPlot = make_plot_component({"happy": "tab:green"})

def legend(model):                  ## added description of what blue/orange/o/x represent
    return solara.Markdown(
        """
**Description**  

- 🔵 Blue = Agent Type 0  
- 🟠 Orange = Agent Type 1  

- ⭕ Happy  
- ❌ Unhappy  
"""
    )

page = SolaraViz(
    model1,
    renderer,
    components=[
        HappyPlot,
        legend,                       ## ensured legend is reflected in visualization
        get_happy_agents,
    ],
    model_params=model_params,
)
page  # noqa

