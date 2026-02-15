from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages
from prompts import research_system_prompt
from langchain_core.messages import HumanMessage    

class State(TypedDict):
    messages: Annotated[list,add_messages]
    remaining_steps: int


'''def dynamic_modifier(state: State):
    return [
        HumanMessage(
            content=test_prompt.format(
                claim=state["claim"],
                debate_style=state["debate_style"],
                length=state["length"],
            )
        )
    ]


'''









'''
def dynamic_modifier(state: State):
    prompt = test_prompt.format(
        claim=state.get('claim', 'no claim provided'),
        debate_style=state.get('debate_style', 'Casual'),
        length=state.get('length', 'medium')
    )

    return {
        "messages": [HumanMessage(content=prompt)]
    }

'''

