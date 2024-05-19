import streamlit as st
import requests

def main():
    st.title("Gerador de Conteúdo para Blog")
    
    topic = st.text_input("Digite um tópico:")
    
    if st.button("Gerar Blog"):
        if topic:
            with st.spinner('Gerando...'):
                response = requests.post(
                    "http://127.0.0.1:8000/generate_blog",
                    json={"topic": topic}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.markdown("## Conteúdo do Blog Gerado")
                    st.write(data["content"])
                else:
                    st.error(f"Erro: {response.status_code} - {response.text}")
        else:
            st.warning("Por favor, digite um tópico")

if __name__ == "__main__":
    main()
