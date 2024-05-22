import streamlit as st
from controllers import teams as teams_controller
import app_session_state


def show(team, agent):
    print(">>>>>>>>>>>>>>>>>>")
    print(team["_id"])
    print(team["name"])
    print(agent["_id"])
    print(agent["role"])
    print(agent["goal"])
    print(agent["backstory"])

    tasks = teams_controller.get_tasks(team['_id'], agent['_id'])

    _show_edit(team, agent)

    if tasks:
        _display_tasks_grid(team, agent, tasks)
    else:
        _display_empty_task_grid(team, agent)

def _show_edit(team, agent):
    st.markdown("#### Editar Agente")
    st.text_input("ID do Time:", value=team["_id"], disabled=True)
    st.text_input("Nome do Time:", value=team["name"], disabled=True)

    st.text_input("ID do Papel do Agente:", value=agent["_id"], disabled=True)
    role = st.text_input("Papel do Agente:", value=agent["role"], disabled=True)
    goal = st.text_input("Objetivo do Agente:", value=agent["goal"], disabled=True)
    backstory = st.text_area("Contexto do Agente:", value=agent["backstory"], disabled=True)

    if st.button("Salvar", type="primary"):
        teams_controller.update_agent(team['_id'], agent['_id'], role, goal, backstory)
        st.success("Agente atualizado")
        app_session_state.set_session_state_editing_agent(True, team, agent)

def _display_tasks_grid(team, agent, tasks):
    st.write("Tasks")

def _display_empty_task_grid(team, agent):
    st.info("Este agente ainda não tem tarefa.")

    if st.button("Adicionar Tarefa", type="primary"):
            app_session_state.set_session_state_adding_task(True, team, agent)

