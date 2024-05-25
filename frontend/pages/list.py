import streamlit as st
import requests
from menu import menu
from utils import get_backend_url

def main():
    display_posts_page()
    menu()

# Página para exibir postagens armazenadas
def display_posts_page():
    st.header("Conteúdo gerado")

    with st.spinner('Carregando conteúdo...'):
        response = requests.get( f"{get_backend_url()}/blog/get_posts")

        if response.status_code == 200:
            posts = response.json()
            if not posts:
                st.info("Nenhum conteúdo encontrada.")
            else:
                #print(posts)
                for post in posts:
                    print(post)
                    st.markdown("##### Tópico: " + post["topic"])
                    created_at = post.get('created_at', 'Data não disponível')
                    st.markdown(f"###### Criado em: {created_at}")
                    with st.expander("Ver conteúdo"):
                        st.write(post["content"])
                    st.markdown("---")
        else:
            st.error(f"Erro: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()