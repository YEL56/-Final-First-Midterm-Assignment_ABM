import os

import solara

from model import Schelling, SchellingScenario
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
path = os.getcwd()   #WHYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY?????


def agent_portrayal(agent):
    style = AgentPortrayalStyle(
        x=agent.cell.coordinate[0],
        y=agent.cell.coordinate[1],
        marker="o",
        size=75,
    )
    #COLOR CHANGE 
    if agent.type == 0:
        style.update(("color","blue"))  #why double parantheses? 밑에를 봐
    else:
        style.update(("color","orange"))
    #HAPPY STATUS CHANGE
    if not agent.happy:   
        style.update(                       #밑에 is here. u coulda had a lotta pairs 
            ("marker", "x"),
            ("size", 50),
            ("zorder", 2), 
        )

    return style


model_params = {
    "rng": Slider("Random Seed", 42, 1, 100, 1),
    "density": Slider("Agent density", 0.8, 0.1, 1.0, 0.1),
    "minority_pc": Slider("Fraction minority", 0.2, 0.0, 1.0, 0.05),
    "homophily": Slider("Homophily", 0.4, 0.0, 1.0, 0.125),
    "width": 20,
    "height": 20,
    "intervention_prob": Slider("Intervention Probability", 0.2, 0.0, 1.0, 0.05),  #!!!!!!!!!!!!!
    "intervention_effect": Slider("Intervention Effect", 0.04, 0.0, 0.2, 0.01) #!!!!!!!!!
    }


# Note: Models with images as markers are very performance intensive.
model1 = Schelling(scenario=SchellingScenario())
renderer = SpaceRenderer(model1, backend="matplotlib").setup_agents(agent_portrayal)
# Here we use renderer.render() to render the agents and grid in one go.
# This function always renders the grid and then renders the agents or
# property layers on top of it if specified.
renderer.render()

HappyPlot = make_plot_component({"happy": "tab:green"})

def legend(model):                  #legend - making
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
        legend,
        get_happy_agents,
    ],
    model_params=model_params,
)
page  # noqa


# 오류는 APP_3.py 파일이 Schelling과 SchellingScenario 클래스를 잘못된 위치에서 가져오려고 시도하고 있기 때문에 발생합니다. 이 클래스들은 MESA 라이브러리의 기본 모듈이 아니라, 직접 작성한 model.py 파일에 정의되어 있습니다. 따라서 APP_3.py의 import 문을 수정해야 합니다.

# What I did: Colab에서 정의한 커스텀 SchellingAgent, SchellingScenario, Schelling 클래스들을 model.py 파일로 저장하는 코드를 생성하겠습니다. 이 파일을 APP_3.py와 같은 디렉토리에 저장해야 합니다.

#그 다음, APP_3.py 파일 내의 다음 import 문을: from mesa.examples.basic.schelling.model import Schelling, SchellingScenario

#이렇게 변경해야 함: from model import Schelling, SchellingScenario