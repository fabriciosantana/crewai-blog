import os
from crewai import Agent, Task, Crew
from utils import get_openai_api_key

def generate_blog_content(topic):
    
    openai_api_key = get_openai_api_key()
    os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

    planner = Agent(
        role="Planejador de Conteúdo",
        goal="Planejar conteúdo envolvente e factual sobre {topic}",
        backstory="Você está trabalhando no planejamento de um artigo de blog "
                  "sobre o tópico: {topic}. "
                  "Você coleta informações que ajudam o "
                  "público a aprender algo "
                  "e a tomar decisões informadas. "
                  "Seu trabalho é a base para "
                  "o Escritor de Conteúdo escrever um artigo sobre este tópico.",
        allow_delegation=False,
        verbose=True
    )

    writer = Agent(
        role="Escritor de Conteúdo",
        goal="Escrever uma peça de opinião perspicaz e factual "
              "sobre o tópico: {topic}",
        backstory="Você está trabalhando na escrita "
                  "de uma nova peça de opinião sobre o tópico: {topic}. "
                  "Você baseia sua escrita no trabalho do "
                  "Planejador de Conteúdo, que fornece um esboço "
                  "e o contexto relevante sobre o tópico. "
                  "Você segue os principais objetivos e "
                  "a direção do esboço, "
                  "conforme fornecido pelo Planejador de Conteúdo. "
                  "Você também fornece insights objetivos e imparciais "
                  "e os fundamenta com informações "
                  "fornecidas pelo Planejador de Conteúdo. "
                  "Você reconhece em sua peça de opinião "
                  "quando suas declarações são opiniões "
                  "em vez de afirmações objetivas.",
        allow_delegation=False,
        verbose=True
    )

    editor = Agent(
        role="Editor",
        goal="Editar um post de blog dado para alinhar com "
             "o estilo de escrita da organização.",
        backstory="Você é um editor que recebe um post de blog "
                  "do Escritor de Conteúdo. "
                  "Seu objetivo é revisar o post do blog "
                  "para garantir que ele siga as melhores práticas jornalísticas, "
                  "forneça pontos de vista equilibrados "
                  "ao fornecer opiniões ou afirmações, "
                  "e também evite tópicos ou opiniões "
                  "altamente controversos sempre que possível.",
        allow_delegation=False,
        verbose=True
    )

    plan = Task(
        description=(
            "1. Priorize as últimas tendências, principais players "
                "e notícias relevantes sobre {topic}.\n"
            "2. Identifique o público-alvo, considerando "
                "seus interesses e pontos de dor.\n"
            "3. Desenvolva um esboço de conteúdo detalhado, incluindo "
                "uma introdução, pontos principais e um chamado à ação.\n"
            "4. Inclua palavras-chave de SEO e dados ou fontes relevantes."
        ),
        expected_output="Um documento de plano de conteúdo abrangente "
            "com um esboço, análise do público, "
            "palavras-chave de SEO e recursos.",
        agent=planner,
    )

    write = Task(
        description=(
            "1. Use o plano de conteúdo para criar um "
                "post de blog envolvente sobre {topic}.\n"
            "2. Incorpore palavras-chave de SEO de forma natural.\n"
            "3. As seções/subtítulos são nomeados corretamente "
                "de maneira envolvente.\n"
            "4. Certifique-se de que o post esteja estruturado com uma "
                "introdução envolvente, corpo perspicaz "
                "e uma conclusão resumida.\n"
            "5. Revise para erros gramaticais e "
                "alinhamento com a voz da marca.\n"
        ),
        expected_output="Um post de blog bem escrito "
            "em formato markdown, pronto para publicação, "
            "cada seção deve ter 2 ou 3 parágrafos.",
        agent=writer,
    )

    edit = Task(
        description=("Revise o post de blog dado para "
                    "erros gramaticais e "
                    "alinhamento com a voz da marca."),
        expected_output="Um post de blog bem escrito em formato markdown, "
                        "pronto para publicação, "
                        "cada seção deve ter 2 ou 3 parágrafos.",
        agent=editor
    )

    crew = Crew(
        agents=[planner, writer, editor],
        tasks=[plan, write, edit],
        verbose=2
    )

    result = crew.kickoff(inputs={"topic": topic})

    return result
