import streamlit as st
class ChatBubble:
    def __init__(self,bg_color=None):
        self.bg_color = None
        self.align = None
        self.chat_style ='''
            <div style="
                background-color: {bg_color};
                color:white;
                padding:10px;
                border-radius:15px;
                max-width:100%;
                margin-{align}:auto;
                margin-bottom:15px;
            ">
                {content}
            </div>

        ''' 
    def render_chat(self,role,content,type="Rebuttal"):
      
        bg_color = self.bg_color or ("#1D9A5DA0" if role == "user" else "#1C0A09")
        #align = "right" if role == "user" else "left"  
        if type == 'Follow Up':
            if role == "assistant":
                
                chat_box= self.chat_style.format(bg_color=bg_color,align="center",content=content)
              
                st.markdown(
                    chat_box
                    , unsafe_allow_html=True
                )
                
            else:
                chat_box= self.chat_style.format(bg_color=bg_color,align="center",content=content)
                st.markdown(
                    chat_box,
                    unsafe_allow_html=True
                )
    
            
        
        else:
            if role == "assistant":
                counter_argument = content["counter_argument"]
                chat_box= self.chat_style.format(bg_color=bg_color,align="center",content=counter_argument)
                details = content['details']
                st.markdown(
                    chat_box
                    , unsafe_allow_html=True
                )
                with st.expander(f'Additional Details'):
                    st.write(details)
            else:
                chat_box= self.chat_style.format(bg_color=bg_color,align="center",content=content)
                st.markdown(
                    chat_box,
                    unsafe_allow_html=True
                )
    

    
    
    




       


        
