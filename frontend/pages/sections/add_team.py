import streamlit as st
from controllers import teams as teams_controller
import app_session_state

def show():
    print("Carregando seção para criar time")

    st.markdown("#### Cadastrar novo time")
    team_name = st.text_input("Nome do Time", key="team_name", placeholder="Digite o nome do time")

    col1, col2, col3 = st.columns(3)

    with col1:
        error_message = ""
        success_message = ""

        if st.button("Salvar", type="primary",):
            if team_name:
                result = teams_controller.add(team_name)

                if result["team_id"]:
                    success_message = f"Time cadastrado com sucesso com _id {result['team_id']}"
                else:
                    error_message = "Ocorreu um erro ao cadastrar o time."
            else:
                error_message = "Por favor, insira o nome do time."

    if success_message:
        st.success(success_message)
    if error_message:
        st.error(error_message)

    with col2:
        if st.button("Voltar", type="secondary"):
            app_session_state.set_session_state_listing_team(True)
    with col3:
        st.button("Limpar")
  
    return None