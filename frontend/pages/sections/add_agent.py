import streamlit as st
from controllers import teams as teams_controller
from controllers import agent_templates as agent_templates_controller
import app_session_state


def show(team):
    st.markdown("##### Adicionar agentes ao time")
    team_id = st.text_input("ID do Time", value=team["_id"], disabled=True)
    
    st.text_input("Nome do Time", value=team["name"], disabled=True)

    agent_role = ""
    agent_goal = ""
    agent_backstory = ""

    agent_templates = agent_templates_controller.list()

    with st.expander("Ver modelos de agentes"):

        for agent_template in agent_templates:
            
            st.text_input("Papel do agente:", 
                          value=agent_template["role"], 
                          key=f"agent_role_{agent_template['_id']}",
                          disabled=True)
            
            st.text_input("Objetivo do agente:",
                          value=agent_template["goal"],
                          key=f"agent_goal_{agent_template['_id']}",
                          disabled=True)
            
            st.text_area("Contexto do Agente:",
                         key=f"agent_backstort_{agent_template['_id']}",
                         value=agent_template["backstory"],
                         disabled=True)

            if st.button("Usar modelo", key=f"use_agent_template_{agent_template['_id']}"):
                st.session_state.agent_template = {
                    "role": agent_template["role"],
                    "goal": agent_template["goal"],
                    "backstory": agent_template["backstory"]
                }

    if st.session_state.agent_template:
        agent_role = st.text_input("Papel do Agente", value=st.session_state.agent_template['role'])    
        agent_goal = st.text_input("Objetivo do Agente", value=st.session_state.agent_template["goal"])
        agent_backstory = st.text_area("Contexto do Agente", value=st.session_state.agent_template["backstory"])
    else:
        agent_role = st.text_input("Papel do Agente", value=agent_role)
        agent_goal = st.text_input("Objetivo do Agente", value=agent_goal)
        agent_backstory = st.text_area("Contexto do Agente", value=agent_backstory)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Salvar", type="primary"):

            if team_id and agent_role and agent_goal and agent_backstory:
                agent_data = {
                    "role": agent_role,
                    "goal": agent_goal,
                    "backstory": agent_backstory
                }
                result = teams_controller.add_agent(team_id, agent_data)
                st.session_state.agent_template = {}

                if result:
                    st.success("Agente adicionado com sucesso!")
                else:
                    st.error("Erro ao adicionar o agente")
            else:
                st.warning("Por favor, preencha todos os campos.")
    with col2:
        if st.button("Voltar"):
            app_session_state.set_session_state_editing_team(True, team)
    return None