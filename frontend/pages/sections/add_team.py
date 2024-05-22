import streamlit as st
from controllers import teams as teams_controller
import app_session_state
import time

def show():
    print("Carregando seção para criar time")

    st.markdown("#### Adicionar time")
    team_name = st.text_input("Nome do Time", key="team_name", placeholder="Digite o nome do time")

    col1, col2 = st.columns(2)

    with col1:
        error_message = ""
        success_message = ""

        if st.button("Salvar", type="primary"):
            if team_name:
                result = teams_controller.add(team_name)
                print(f"Time adicionado: {result}")
                if result["team_id"]:
                    success_message = "Time cadastrado com sucesso"
                else:
                    error_message = "Ocorreu um erro ao cadastrar o time."
            else:
                error_message = "Por favor, insira o nome do time."

    if success_message:
        alert = st.success(success_message)
        time.sleep(1)
        alert.empty()
        app_session_state.set_session_state_listing_team(True)
    if error_message:
        st.error(error_message)

    with col2:
        if st.button("Voltar", type="secondary"):
            app_session_state.set_session_state_listing_team(True)
    
    return None