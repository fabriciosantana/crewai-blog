import streamlit as st
from controllers import teams as teams_controller
import app_session_state


def show(team_id: str):
    st.markdown("#### Adicionar Agentes ao Time")
    team_id = st.text_input("ID do Time", value=team_id)
    agent_role = st.text_input("Papel do Agente", value="Planejador de Conteúdo")
    agent_goal = st.text_input("Objetivo do Agente", value="Planejar conteúdo envolvente e factual sobre <<topic>>")
    agent_context = st.text_area("Contexto do Agente", value="Você está trabalhando no planejamento de um artigo de blog "
                                                            "sobre o tópico: {topic}. "
                                                            "Você coleta informações que ajudam o "
                                                            "público a aprender algo "
                                                            "e a tomar decisões informadas. "
                                                            "Seu trabalho é a base para "
                                                            "o Escritor de Conteúdo escrever um artigo sobre este tópico.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Adicionar Agente", type="primary"):
            if team_id and agent_role and agent_goal and agent_context:
                agent_data = {
                    "role": agent_role,
                    "goal": agent_goal,
                    "context": agent_context
                }
                result = teams_controller.add_agent(team_id, agent_data)

                if result:
                    st.success("Agente adicionado com sucesso!")
                else:
                    st.error("Erro ao adicionar o agente")
            else:
                st.warning("Por favor, preencha todos os campos.")
    with col2:
        if st.button("Voltar"):
            app_session_state.set_session_state_editing_team(True, team_id)
    return None