import streamlit as st
from controllers import teams as teams_controller
from controllers import agent_templates as agent_templates_controller
import app_session_state


def show(team, agent):
    st.markdown("##### Time > Agente > Tarefa > Adionar tarefa")

    st.text_input("ID do Time:", value=team["_id"], disabled=True)
    st.text_input("Nome do Time:", value=team["name"], disabled=True)

    st.text_input("Papel do Agente:", value=agent["role"], disabled=True)
    st.text_input("Objetivo do Agente:", value=agent["goal"], disabled=True)
    st.text_area("Contexto do Agente:", value=agent["backstory"], disabled=True)

    task_title = st.text_input("Título da Tarefa:")
    task_description = st.text_area("Descrição da Tarefa:")
    task_expected_output = st.text_area("Saída Esperada da Tarefa:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Salvar", type="primary"):

            if task_title and task_description and task_expected_output:
                task_data = {
                    "title": task_title,
                    "description": task_description,
                    "expected_output": task_expected_output
                }
                result = teams_controller.add_task(team["_id"], agent["_id"], task_data)
                st.session_state.agent_template = {}

                if result:
                    st.success("Agente adicionado com sucesso!")
                else:
                    st.error("Erro ao adicionar o agente")
            else:
                st.warning("Por favor, preencha todos os campos.")
    with col2:
        if st.button("Voltar"):
            app_session_state.set_session_state_editing_agent(True, team, agent)
    return None
    
