import streamlit as st
import requests
from utils import get_backend_url
from menu import menu
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode

def main():
    st.title("Gerenciamento de Times de IA")
    menu()

    # Gerenciar estado das seções
    if 'team_id' not in st.session_state:
        st.session_state.team_id = ''
    if 'agent_id' not in st.session_state:
        st.session_state.agent_id = ''

    manage_teams_page()
   
def manage_teams_page():
    
    create_team_section()

    if st.session_state.team_id:
        add_agent_section()
    if st.session_state.agent_id:
        add_activity_section()

    #teams = fetch_teams()

   #if teams:
        #display_teams_grid(teams)

    #st.button("Adicionar Novo Time", on_click=create_team_section)

def fetch_teams():
    response = requests.get(f"{get_backend_url()}/teams/list")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erro ao buscar times: {response.status_code} - {response.text}")
        return []
    
def display_teams_grid(teams):
    df = pd.DataFrame(teams)
    df['_id'] = df['_id'].astype(str)  # Ensure '_id' is a string
    df_display = df[['name']]  # Exibir apenas o nome no grid
    #st.dataframe(df_display, width=700, height=300)
    st.data_editor(df_display,
                    width=700,
                    height=300, 
                    use_container_width=True, 
                    num_rows="dynamic",
                    disabled=True, 
                    key=df["_id"])

    

def create_team_section():
    st.header("Criar Novo Time")
    team_name = st.text_input("Nome do Time")

    if st.button("Adicionar Time"):
        if team_name:
            response = requests.post(f"{get_backend_url()}/teams/create_team", json={"name": team_name})
            if response.status_code == 200:
                st.success(response.json()["message"])
                st.session_state.team_id = response.json()["team_id"]
                return response.json()["team_id"]
            else:
                st.error(f"Erro ao criar o time: {response.status_code} - {response.text}")
    return None

def add_agent_section():
    st.header("Adicionar Agentes ao Time")
    team_id = st.text_input("ID do Time", value=st.session_state.get('team_id', ''))
    agent_role = st.text_input("Papel do Agente", value="Planejador de Conteúdo")
    agent_goal = st.text_input("Objetivo do Agente", value="Planejar conteúdo envolvente e factual sobre <<topic>>")
    agent_context = st.text_area("Contexto do Agente", value="Você está trabalhando no planejamento de um artigo de blog "
                                                            "sobre o tópico: {topic}. "
                                                            "Você coleta informações que ajudam o "
                                                            "público a aprender algo "
                                                            "e a tomar decisões informadas. "
                                                            "Seu trabalho é a base para "
                                                            "o Escritor de Conteúdo escrever um artigo sobre este tópico.")

    if st.button("Adicionar Agente"):
        if team_id and agent_role and agent_goal and agent_context:
            agent_data = {
                "role": agent_role,
                "goal": agent_goal,
                "context": agent_context
            }
            response = requests.post(f"{get_backend_url()}/teams/{team_id}/add_agent", json=agent_data)
            if response.status_code == 200:
                st.success("Agente adicionado com sucesso!")
                st.session_state.agent_id = response.json()["agent_id"]
                return response.json()["agent_id"]
            else:
                st.error(f"Erro ao adicionar o agente: {response.status_code} - {response.text}")
        else:
            st.warning("Por favor, preencha todos os campos.")
    return None

def add_activity_section():
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