import streamlit as st
class Sidebar:

    def __init__(self):
       
        self.types = ["Academic", "Casual", "Social Media", "Witty"]
        self.agent_types = ["Research","Web Agent",'Fast']
        self.length_types = ['Long','Medium','Short']
        self.response_option = ['Rebuttal','Follow Up']
    def render_sidebar(self):
        st.sidebar.title('Rebuttal Preference')
        self.response_type = st.sidebar.selectbox('Select a Response Type', self.response_option)
        self.length = st.sidebar.selectbox("Response Length", self.length_types)
        self.debate_style = st.sidebar.radio("Style", self.types)
        self.AI_type = st.sidebar.radio('Select Ai Type', self.agent_types)
