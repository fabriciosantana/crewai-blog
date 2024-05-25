import streamlit as st
from menu import menu
import app_session_state
st.set_page_config(layout="wide", page_title="Gerador de Conteúdo", page_icon="📝")

def main():

    st.title("Seja bem-vindo!")
    
    app_session_state.init()
    menu()

if __name__ == "__main__":
    main()
