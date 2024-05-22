import streamlit as st
import requests
from utils import get_backend_url
from menu import menu
from controllers import teams as teams_controller
from pages.sections import list_teams as list_teams_section
from pages.sections import add_team as add_team_section
from pages.sections import edit_team as edit_team_section
from pages.sections import add_agent as add_agent_section
from pages.sections import edit_agent as edit_agent_section

def main():

    menu()

    if 'adding_team' not in st.session_state:
        st.session_state.adding_team = False
    if 'editing_team' not in st.session_state:
        st.session_state.editing_team = False
    if 'listing_team' not in st.session_state:
        st.session_state.listing_team = False
    if 'adding_agent' not in st.session_state:
        st.session_state.adding_agent = False
    if 'editing_agent' not in st.session_state:
        st.session_state.editing_agent = False

    if st.session_state.adding_team:
        add_team_section.show()
    elif st.session_state.editing_team:
        edit_team_section.show(st.session_state.team_id)
    elif st.session_state.listing_team:
        list_teams_section.show()
    elif st.session_state.adding_agent:
        add_agent_section.show(st.session_state.team_id)
    elif st.session_state.editing_agent:
        edit_agent_section.show(st.session_state.team_id, st.session_state.agent_id)
    else:
        list_teams_section.show()
        
def section_add_task():
    st.header("Adicionar Atividades ao Agente")
    team_id = st.session_state.get('team_id', '')
    agent_id = st.text_input("ID do agente", value=st.session_state.get('agent_id', ''))
    activity_description = st.text_area("Descrição da Atividade")
    expected_output = st.text_area("Saída Esperada")

    if st.button("Adicionar Atividade"):
        if agent_id and activity_description and expected_output:
            activity_data = {
                "description": activity_description,
                "expected_output": expected_output
            }
            response = requests.post(f"{get_backend_url()}/teams/{team_id}/{agent_id}/add_activity", json=activity_data)
            if response.status_code == 200:
                st.success("Atividade adicionada com sucesso!")
            else:
                st.error(f"Erro ao adicionar a atividade: {response.status_code} - {response.text}")
        else:
            st.warning("Por favor, preencha todos os campos.")

if __name__ == "__main__":
    main()