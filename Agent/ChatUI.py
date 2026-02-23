import streamlit as st
from langchain_core.output_parsers import StrOutputParser
import markdown
class ChatBubble:
    def __init__(self,bg_color=None):
        self.bg_color = None
        self.align = None
        self.parser = StrOutputParser()
        self.chat_style = '''
            <div class={id} style="
                background: {bg_color}; 
                padding: 10px;
                border-radius: 11px;
                max-width: 90%;
                margin-{align}: auto;
                margin-bottom: 2px;
                font-family: 'Courier New', Courier, monospace;
                font-weight: 300;
                font-color: black; 
                line-height: 1.5;
                box-shadow: inset 11px 11px 22px #0d212d, 
                            inset -11px -11px 22px #173b53;
                border: 1px solid rgba(255, 255, 255, 0.1);
            ">
                {content}
            </div>
        '''
        
    def render_chat(self,role,content,id,type="Rebuttal"):
      
        bg_color = self.bg_color or ("#a0888a" if role == "user" else "#122e40")
        align = "right" if role == "user" else "left"  
        if role == "assistant":
            if type == 'Rebuttal':
               
                counter_argument = markdown.markdown(content["response"])
                chat_box= self.chat_style.format(align=align,content=counter_argument,bg_color=bg_color,id=f"chat_{id}")
                details = content['details']
                st.markdown(
                    chat_box
                    , unsafe_allow_html=True
                )
             
                with st.expander(f'Additional Details'):
                    st.write(details)



            else:
                 chat_box= self.chat_style.format(align=align,content=content,bg_color=bg_color,id=f"chat_{id}")
                
                 st.markdown(
                        chat_box
                        , unsafe_allow_html=True
                    )
           
                

            
        else:
            content = markdown.markdown(content)
            chat_box= self.chat_style.format(align=align,content=content,bg_color=bg_color,id=f"chat_{id}")
            st.markdown(
                chat_box,
                unsafe_allow_html=True
            )
                

    
  

    
    
    




       


        
