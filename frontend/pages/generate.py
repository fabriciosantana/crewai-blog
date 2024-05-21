import streamlit as st
import requests
from menu import menu
from utils import get_backend_url

def main():
    generate_blog_page()
    menu()

# Página para gerar conteúdo do blog
def generate_blog_page():
    st.title("Gerador de conteúdo")

    st.info("Informe um tópico na caixa de texto abauxo e clique em Gerar")

    topic = st.text_input("Digite um tópico:")

    col1, col2 = st.columns([1, 6])
    show_warning = False
    generate_content = False
    
    data = None

    with col1:
        if st.button("Gerar"):
            if topic:
                generate_content = True
            else:
                show_warning = True
    with col2:
            st.page_link("pages/list.py", label="Listar postagens", icon=None, help="Clique para ver as postagens que já foram geradas", disabled=False, use_container_width=None)

    if show_warning:
        st.warning("Por favor, digite um tópico")

    if generate_content:
        with st.spinner('Gerando...'):
                    response = requests.post(f"{get_backend_url()}/generate_blog",
                        json={"topic": topic}
                    )

                    if response.status_code == 200:
                        data = response.json()
                        st.markdown("#### Conteúdo Gerado")
                        st.write(data["content"])
                    else:
                        st.error(f"Erro: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()