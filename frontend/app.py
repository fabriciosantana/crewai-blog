import streamlit as st
from menu import menu

def main():
    st.set_page_config(page_title="Gerador de Conteúdo", page_icon="📝")
    st.title("Seja bem-vindo!")
    menu()

if __name__ == "__main__":
    main()
