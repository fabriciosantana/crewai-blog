import streamlit as st
from controllers import teams as teams_controller
from controllers import task_templates as task_templates_controller
import app_session_state

def show(team, agent):
    st.markdown("##### Time > Agente > Tarefa > Adionar tarefa")

    st.text_input("ID do Time:", value=team["_id"], disabled=True)
    st.text_input("Nome do Time:", value=team["name"], disabled=True)

    st.text_input("Papel do Agente:", value=agent["role"], disabled=True)
    st.text_input("Objetivo do Agente:", value=agent["goal"], disabled=True)
    st.text_area("Contexto do Agente:", value=agent["backstory"], disabled=True)
    
    task_title = ""
    task_description = ""
    task_expected_output = ""

    task_templates = task_templates_controller.list()

    with st.expander("Ver modelos de tarefas"):

        for task_template in task_templates:
            
            st.text_input("Título:", 
                          value=task_template["title"], 
                          key=f"task_title_{task_template['_id']}",
                          disabled=True)
            
            st.text_area("Descrição:",
                          value=task_template["description"],
                          key=f"task_description_{task_template['_id']}",
                          disabled=True)
            
            st.text_area("Saída esperada:",
                         key=f"task_expected_output_{task_template['_id']}",
                         value=task_template["expected_output"],
                         disabled=True)

            if st.button("Usar modelo", key=f"use_task_template_{task_template['_id']}"):
                st.session_state.task_template = {
                    "title": task_template["title"],
                    "description": task_template["description"],
                    "expected_output": task_template["expected_output"]
                }

    if st.session_state.task_template:
        task_title = st.text_input("Título", value=st.session_state.task_template['title'])    
        task_description = st.text_input("Descrição", value=st.session_state.task_template["description"])
        task_expected_output = st.text_area("Saída esperada", value=st.session_state.task_template["expected_output"])
    else:
        task_title = st.text_input("Título", value=task_title)
        task_description = st.text_input("Descrição", value=task_description)
        task_expected_output = st.text_area("Saída esperada", value=task_expected_output)

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
                st.session_state.task_template = {}

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
    
