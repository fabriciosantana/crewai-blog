import streamlit as st
from controllers import teams as teams_controller
import app_session_state
import time

def show(team):

    agents = teams_controller.fetch_agents(team['_id'])

    _show_edit(team)

    if agents:
        _display_agents_grid(team, agents)
    else:
        _display_empty_agent_grid()

def _show_edit(team):
    st.markdown("##### Editar Time")
    st.text_input("Id do time:", value= team['_id'], disabled=True)
    
    team_name = st.text_input("Nome do time:", value=team["name"])

    team["name"] = team_name

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Salvar", type="primary"):
            result = teams_controller.update(team)
            if result:
                sucess_message = st.success("Time atualizado com sucesso!")
                time.sleep(2)
                sucess_message.empty()
            else:
                st.error("Erro ao atualizar time!")
            #app_session_state.set_session_state_editing_team(True, team)
    with col2:
        if st.button("Voltar"):
            app_session_state.set_session_state_listing_team(True)

def _display_agents_grid(team, agents):

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Lista de Agentes do Time")
    with col2:
        if st.button("Adicionar agente", type="primary"):
            app_session_state.set_session_state_adding_agent(True)

    cols = st.columns(3)
    fields = ["Papel", "Objetivo", "Ação"]

    # header
    for col, field in zip(cols, fields):
        col.write("**" + field + "**")

    # rows
    for agent in agents:
        col1, col2, col3 = st.columns(3)
        col1.write(agent["role"])
        col2.write(agent["goal"])
        #col3.write(agent["context"])

        alter_placeholder = col3.empty()
        #delete_placeholder = col4.empty()

        if alter_placeholder.button("Editar", key="alter_" + agent["_id"]):
            app_session_state.set_session_state_editing_agent(True, team, agent)

        #if delete_placeholder.button("Excluir", key="delete_" + agent["_id"]):
        #    teams_controller.delete_agent(agent["_id"])
        #    app_session_state.set_session_state_editing_team(True, team)

def _display_empty_agent_grid():
    st.info("Este time não tem um agente cadastrado.")

    if st.button("Adicionar Agente", type="primary"):
            app_session_state.set_session_state_adding_agent(True)
