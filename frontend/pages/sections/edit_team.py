import streamlit as st
from controllers import teams as teams_controller
import app_session_state

def show(team_id: str):
    
    agents = teams_controller.fetch_agents(team_id)

    if agents:
        _display_agents_grid(team_id, agents)
    else:
        _display_empty_grid(team_id)

def _display_agents_grid(team_id: str, agents):

    st.markdown(f"#### Editando time *{team_id}*")

    col1, col2 = st.columns(2)
    with col1:
        
        st.markdown("#### Lista de agentes do time")
        print(agents)
    with col2:
        if st.button("Adicionar agente", type="primary"):
            app_session_state.set_session_state_adding_agent(True, team_id)

    cols = st.columns(4)
    fields = ["Papel", "Objetivo", "Contexto", "Excluir"]

    # header
    for col, field in zip(cols, fields):
        col.write("**" + field + "**")

    # rows
    for agent in agents:
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.write(agent["role"])
        col2.write(agent["goal"])
        col3.write(agent["context"])

        alter_placeholder = col3.empty()
        delete_placeholder = col4.empty()

        if alter_placeholder.button("Ver detalhes", key="alter_" + agent["_id"]):
            #st.session_state.agent_id = agent["_id"]
            #agents = fetch_agents(team["_id"])

            #if agents:
            #    display_agents_grid(agents)

            #show_update_team_section(team["_id"])

            app_session_state.set_session_state_editing_agent(True, team_id, agent["id"])

        if delete_placeholder.button("Excluir", key="delete_" + agent["_id"]):
            teams_controller.delete_agent(agent["_id"])
            app_session_state.set_session_state_editing_team(True, team_id)

def _display_empty_grid(team_id):
    st.markdown("##### Este time não tem um agente cadastrado.")
    st.write(f"O time {team_id} não tem um agente cadastrado.")
    st.write("Clique no botão abaixo para cadastrar um agente.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Cadastrar agente", type="primary"):
            app_session_state.set_session_state_adding_agent(True, team_id)
    with col2:
        if st.button("Voltar"):
            app_session_state.set_session_state_listing_team(True)
