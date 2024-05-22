import streamlit as st
from controllers import teams as teams_controller
import app_session_state
from pages.sections import edit_team as edit_team_section

def show():

    teams = teams_controller.list()

    if teams:
        _display_teams_grid(teams)
    else:
        _display_empty_grid()

def _display_teams_grid(teams):

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Lista de times")

    with col2:
        if st.button("Adicionar novo time", type="primary"):
            app_session_state.set_session_state_adding_team(True)
            
    cols = st.columns(3)
    fields = ["Nome do Time", "Detalhes", "Excluir"]

    # header
    for col, field in zip(cols, fields):
        col.write("**" + field + "**")

    # rows
    for team in teams:
        col1, col2, col3 = st.columns(3)
        col1.write(team["name"])

        alter_placeholder = col2.empty()
        delete_placeholder = col3.empty()

        if alter_placeholder.button("Ver detalhes", key="alter_" + team["_id"]):
            #st.session_state.team_id = team["_id"]
            #st.session_state.show_create_team = False

            app_session_state.set_session_state_editing_team(True, team["_id"])
            edit_team_section.show(team["_id"])

            #show_update_team_section(team["_id"])

        if delete_placeholder.button("Excluir", key="delete_" + team["_id"]):
            result = teams_controller.delete(team["_id"])

            if result:
                st.success(f"Time {team['name']} excluído com sucesso!")                
            else:
                st.error(f"Erro ao excluir time {team['name']}")
            st.rerun()

def _display_empty_grid():
    st.markdown("##### Você ainda não tem um time cadastrado.")
    st.write("Para começar você precisa cadastrar um time.")
    st.write("Clique no botão abaixo para cadastrar um time.")
    if st.button("Cadastrar", type="primary"):
        app_session_state.set_session_state_adding_team(True)