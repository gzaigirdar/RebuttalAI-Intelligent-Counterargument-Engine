import streamlit as st 
from ChatUI import ChatBubble
from SidebarUI import Sidebar
from LLM_Agents import Agent
from streamlit_extras.stylable_container import stylable_container   
from requestsLimiter import RateLimiter
import streamlit.components.v1 as components


limiter = RateLimiter()
limiter._init_db()
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
    
    #return agent.MockLLMCall(prompt)
    
  



page_bg_image = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.pexels.com/photos/2908984/pexels-photo-2908984.jpeg?_gl=1*1vk7xs0*_ga*MTY5OTYxMTQ2OC4xNzcwOTU4NDU2*_ga_8JE65Q40S6*czE3NzA5NjUyNTUkbzMkZzEkdDE3NzA5NjUzMDQkajExJGwwJGgw") !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
}
[data-testid="stHeader"]{
    
    padding: 0px !important;

}
[data-testid="stMainBlockContainer"]{
    padding: 0px;
    margin-top: 45px !important;
}
[data-testid="stBottom"]{
    background-color: rgba(0,0,0,0) !important;
    padding: 10px;
    bottom: 10px;
    witdh: 100%
}

[data-testid="stBottomBlockContainer"]{
    padding: 5px !important;
}

	

[data-testid="stBottom"] > div {
background-color: rgba(0,0,0,0) !important;

}
      


[data-testid="stHeadingWithActionElements"] > h3{
     padding: 0px !important;




}


[data-testid="stExpander"]{
    background-color: black !important;
    color: white !important;
    border-radius: 5px;
    margin-left: auto  !important;
    width: 90% !important;;
}
[data-testid="stElementContainer"]{
 padding:0px !important;

}
[data-testid="stHeading"]{
    padding:0px !important;
    


}

[data-testid="stIconMaterial"] {
 color:yellow !important;
 min-width: 2.75rem !important;
 font-size: 2.75rem !important; 
 
[data-testid="stHeadingWithActionElements"] > h2 > span {
    font-weight: 300 !important; 

}





</style>
"""
ids = 0

st.set_page_config( page_title='Rebuttal ai', page_icon="🤖", layout="centered", initial_sidebar_state='auto')
st.markdown(page_bg_image,unsafe_allow_html=True)
chat = ChatBubble()
sidebar = Sidebar()
sidebar.render_sidebar()


if "messages" not in st.session_state:
    st.session_state.messages = []


with stylable_container(
    key="header_section",
    css_styles="""
        {
            background: rgba(32, 13, 13, 0.10);
            backdrop-filter: blur(4.0px);
            -webkit-backdrop-filter: blur(4.0px);
            border: 1px solid rgba(17, 24, 23, 0.47);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            padding: 0px !important;
            border-radius: 16px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 0.30rem !important;
            margin-bottom: 0px;
            margin-top: 0px !important;
        }
        [data-testid="stIconMaterial"] {
            color: red !important;
            font-size: 2rem !important;
        }
        [data-testid="stText"] > span {
        color: green !important;
        text-align: center !important;
        
           

        
        
        }
        
        h2, h3, h4 {
            font-weight: 300 !important;
            text-align: center !important;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5) !important;
            letter-spacing: 0.5px !important;
        }

        h2 {
            color: #ffffff !important;
            font-size: 36px !important;
            font-family: "Segoe UI", "Helvetica Neue", sans-serif !important;
            margin: 10px 0 10px 0 !important;
            padding: 5px !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
        }

        h3 {
            color: #d4d4d4 !important;
            font-size: 18px !important;
            font-family: "Segoe UI", "Helvetica Neue", sans-serif !important;
            margin: 6px 0 !important;
            padding: 5px !important;
            font-weight: 300 !important;
            opacity: 0.9 !important;
        }
        h4 {
            color: red !important;
            font-size: 10px !important;
            font-family: "Segoe UI", "Helvetica Neue", sans-serif !important;
            margin: 0px 15px 15px 15px !important;
            padding: 2px 5px !important;
            font-weight: bold !important;
            font-style: italic !important;
            opacity: 0.9 !important;
        }
        [data-testid="stSelectboxVirtualDropdown"] > div > div > li:hover {
            background-color: red !important;
        }
        [data-testid="stMainBlockContainer"] {
        overflow-anchor: none !important;
    }

    """,
):
    st.header('Rebuttal Ai')
    st.subheader("Enter a Claim To Generate A Counter Argument")
    st.markdown("#### Open Sidebar To Select Preference.")

for msg in st.session_state.messages:
        chat.render_chat(role=msg["role"], content=msg["content"], type=msg["type"],id=msg['id'])



chat_holder = st.container()

if prompt := st.chat_input("Enter your argument..."):
    if limiter.is_limit_reached():
        st.error('Maximum number of requests met.')
    else:
        user_id = ids + 1 
        ids += 1

        with chat_holder:
            chat.render_chat(role="user", content=prompt, type=sidebar.response_type,id= user_id)

        st.session_state.messages.append({"role": "user", "content": prompt, 'type': sidebar.response_type,'id':user_id})

        with st.spinner("In progress..."):
            if sidebar.response_type == 'Rebuttal':
                agent_prompt = f'claim:{prompt} \n style:{sidebar.debate_style}\n length:{sidebar.length}'
                res = agent_router(sidebar.AI_type, prompt=agent_prompt)
            else:
                res = agent_router(agent_type='Follow Up', prompt=prompt, history=st.session_state.messages)

            
            bot_id = ids + 1
            ids += 1
            with chat_holder:
                chat.render_chat(role="assistant", content=res, type=sidebar.response_type,id=bot_id)
                
                
                
            
                
                
                
                
                
                
                
                components.html(
                    """
                    <script>
                    setTimeout(() => {
                        console.log("Scroll script running...");
                        var parentDoc = window.parent.document;
                        var chats = parentDoc.querySelectorAll("[class^='chat_']");
                        console.log("Number of chat bubbles found:", chats.length);

                        if(chats.length > 1) {  // Ensure there are at least two messages
                            var secondLastChat = chats[chats.length - 2];
                            console.log("Scrolling second-to-last chat bubble:", secondLastChat.className);
                            secondLastChat.scrollIntoView({behavior: "smooth", block: "start"});
                        }
                    }, 500);
                    </script>
                    """,
                    height=0,
                )
                
                
                
               

                st.session_state.messages.append({"role": "assistant", "content": res, 'type': sidebar.response_type,'id':bot_id})
            
            

           
        