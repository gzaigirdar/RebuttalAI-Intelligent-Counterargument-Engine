import streamlit as st 
from ChatUI import ChatBubble
from SidebarUI import Sidebar
from LLM_Agents import Agent
from streamlit_extras.stylable_container import stylable_container   
agent = Agent()
def agent_router(agent_type,prompt,history=None):
    match agent_type:
        case 'Research':
            return agent.research_agent_response(claim=prompt)
        case "Web Agent":
            return agent.websearch_agent_response(claim=prompt)
        case "Fast":
            return agent.fast_agent_response(claim=prompt)
        case "Follow Up":
            return agent.follow_up(history,question=prompt)
        

page_bg_image = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.pexels.com/photos/2908984/pexels-photo-2908984.jpeg?_gl=1*1vk7xs0*_ga*MTY5OTYxMTQ2OC4xNzcwOTU4NDU2*_ga_8JE65Q40S6*czE3NzA5NjUyNTUkbzMkZzEkdDE3NzA5NjUzMDQkajExJGwwJGgw") !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
}
[data-testid="stHeader"]{
    background-color: rgba(0,0,0,0)

}
[data-testid="stMainBlockContainer"]{
    padding: 0px;
}
[data-testid="stBottom"]{
    background-color: rgba(0,0,0,0) !important;
    padding: 10px;
    bottom: 10px;
    witdh: 100%
}

[data-testid="stBottomBlockContainer"]{
    padding: 0px !important;
}
.st-emotion-cache-hzygls {
  
    background-color: rgba(0,0,0,0) !important;
}

</style>
"""
st.markdown(page_bg_image, unsafe_allow_html=True)

st.set_page_config(page_title="Rebuttal Ai", page_icon="🤖", layout="centered", initial_sidebar_state='expanded')
st.markdown(page_bg_image,unsafe_allow_html=True)
chat = ChatBubble()
sidebar = Sidebar()
sidebar.render_sidebar()


if "messages" not in st.session_state:
    st.session_state.messages = []

if 'follow_up' not in st.session_state:
    st.session_state.follow_up = []

st.title("Rebuttal AI Chat")
st.subheader("Enter your argument to generate a counter argument")

for msg in st.session_state.messages:
    chat.render_chat(role=msg["role"],content=msg["content"],type=msg['type'])


if prompt := st.chat_input("Enter your argument..."):
   with st.spinner(text="In progress...", show_time=False, width="content"):
        if sidebar.response_type == 'Rebuttal':
                st.session_state.messages.append({"role": "user", "content": prompt,'type':sidebar.response_type}) 
                prompt = f'claim:{prompt} \n style:{sidebar.debate_style}\n length:{sidebar.length}'
                res = agent_router(sidebar.AI_type,prompt=prompt)
                st.session_state.messages.append({"role": "assistant", "content": res,'type':sidebar.response_type})
        else:
               
                st.session_state.messages.append({"role": "user", "content": prompt,'type':sidebar.response_type}) 
                res = agent_router(agent_type='Follow Up',prompt=prompt,history=st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": res,'type':sidebar.response_type})

 




 