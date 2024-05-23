import streamlit as st
from menu import menu
from controllers import teams as teams_controller

def main():
    menu()

    st.markdown("##### Registrar demanda")
    st.text_area("Descrição")

    teams = teams_controller.list()

    if teams:
        st.selectbox("Atribuir para", teams)
    else:
        st.info("Você precisa adicionar um time para registrar uma demanda.")

    st.button("Registrar")

if __name__ == "__main__":
    main()