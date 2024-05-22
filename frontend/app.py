import streamlit as st
from menu import menu
import app_session_state

def main():
    st.set_page_config(page_title="Gerador de Conteúdo", page_icon="📝")
    st.title("Seja bem-vindo!")
    
    app_session_state.init()
    menu()

if __name__ == "__main__":
    main()
