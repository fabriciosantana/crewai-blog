import streamlit as st
from controllers import teams as teams_controller
import app_session_state


def show(team, agent, task):
    st.write("edit task")
    print(team)
    print(agent)
    print(task)

    if st.button("Voltar"):
        app_session_state.set_session_state_editing_agent(True, team, agent)