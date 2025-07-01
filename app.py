import streamlit as st
from google import genai
from google.genai import types
import typing_extensions as typing
import os
import json
from PIL import Image
from io import BytesIO
import base64

from typing import List, Dict, TypedDict, Optional, cast

# --- Definição das estruturas aninhadas ---
class CoreLoop(typing.TypedDict):
    """Define a estrutura do Core Loop do jogo."""
    acao: str
    recompensa: str
    progressao: str

class Mecanica(typing.TypedDict):
    """Define a estrutura de uma Mecânica de Jogo individual."""
    nome: str
    descricao: str

class Monetizacao(typing.TypedDict):
    """Define a estrutura de uma opção de Monetização."""
    tipo: str
    descricao: str

# --- Definição da estrutura principal do GDD de uma página ---
class OnePageGDD(typing.TypedDict):
    """
    Define a estrutura completa para o One-Page GDD gerado pela IA.
    Corresponde ao JSON de saída esperado do modelo Gemini.
    """
    titulo_provisorio: str
    genero: str
    plataformas_alvo: List[str]
    premissa_conceito_central: str
    publico_alvo: List[str]
    core_loop: CoreLoop
    mecanicas_principais: List[Mecanica]
    monetizacao_opcional: List[Monetizacao]
    pontos_de_venda_unicos_usps: List[str]

# Configuração da chave de API do Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# --- Verificação da Chave de API do Gemini ---
if not GEMINI_API_KEY:
    st.warning('Por favor, defina a variável de ambiente GEMINI_API_KEY com sua chave de API do Gemini.')
    st.stop()

# --- Função para exibir o GDD de forma estruturada e moderna ---
def display_gdd_concept(gdd_data: OnePageGDD, generated_image: Optional[Image.Image] = None):
    st.subheader(f"✨ Conceito de Jogo: {gdd_data.get('titulo_provisorio', 'Sem Título')}")

    # Apresenta a imagem gerada ou o placeholder
    if generated_image:
        st.image(generated_image, caption="Arte Conceitual Gerada", use_container_width=True)
    else:
        # URL de placeholder com tema de Rio de Janeiro/Cartas
        image_url = "https://placehold.co/600x300/007bff/ffffff?text=Rio+de+Cartas+-+Arte+Conceitual"
        st.image(image_url, caption="Arte Conceitual (Placeholder)", use_column_width=True)

    st.markdown("---") # Separador visual

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Gênero:** {gdd_data.get('genero', 'N/A')}")
        st.markdown(f"**Plataformas Alvo:** {', '.join(gdd_data.get('plataformas_alvo', ['N/A']))}")
    with col2:
        st.markdown(f"**Público-Alvo:** {', '.join(gdd_data.get('publico_alvo', ['N/A']))}")

    st.markdown("---") # Separador visual

    st.markdown(f"**Premissa/Conceito Central:** {gdd_data.get('premissa_conceito_central', 'N/A')}")

    st.markdown("---") # Separador visual

    # Core Loop em um expander
    with st.expander("🔄 Core Loop"):
        core_loop = gdd_data.get('core_loop', {})
        st.markdown(f"**Ação:** {core_loop.get('acao', 'N/A')}")
        st.markdown(f"**Recompensa:** {core_loop.get('recompensa', 'N/A')}")
        st.markdown(f"**Progressão:** {core_loop.get('progressao', 'N/A')}")

    # Mecânicas Principais em um expander
    with st.expander("⚙️ Mecânicas Principais"):
        mecanicas = gdd_data.get('mecanicas_principais', [])
        if mecanicas:
            for mec in mecanicas:
                st.markdown(f"**{mec.get('nome', 'N/A')}**: {mec.get('descricao', 'N/A')}")
        else:
            st.markdown("Nenhuma mecânica principal detalhada.")

    # Monetização Opcional em um expander
    if gdd_data.get('monetizacao_opcional'):
        with st.expander("💰 Monetização Opcional"):
            monetizacoes = gdd_data.get('monetizacao_opcional', [])
            if monetizacoes:
                for mon in monetizacoes:
                    st.markdown(f"**{mon.get('tipo', 'N/A')}**: {mon.get('descricao', 'N/A')}")
            else:
                st.markdown("Nenhuma opção de monetização sugerida.")

    # Pontos de Venda Únicos (USPs)
    with st.expander("🌟 Pontos de Venda Únicos (USPs)"):
        usps = gdd_data.get('pontos_de_venda_unicos_usps', [])
        if usps:
            for usp in usps:
                st.markdown(f"- {usp}")
        else:
            st.markdown("Nenhum USP detalhado.")

    st.markdown("---")
    st.info("Esta é uma minuta de One-Page GDD gerada por IA. Use-a como ponto de partida para seu design!")


# --- Título e Descrição do Aplicativo Streamlit ---
st.set_page_config(layout="wide", page_title="Game Concept Forge")
st.title("🎮 Game Concept Forge")
st.markdown("""
    Bem-vindo ao **Game Concept Forge**! Eu sou sua inteligência artificial dedicada à validação rápida de ideias de jogos.
    Minha especialidade é transformar sua visão inicial em um conceito de jogo estruturado, completo com **Core Loop**,
    **Mecânicas de Jogo** e uma **Minuta de One-Page GDD**.
    Vamos construir o seu próximo jogo juntos!
""")

# --- Instruções do Modelo Gemini ---
system_instruction = """
Você é um "Arquiteto de Conceitos de Jogo", uma inteligência artificial especializada em transformar ideias iniciais de usuários em conceitos de jogo estruturados. Sua função principal é:

1.  **Analisar a Ideia Central:** Compreender a essência da ideia do usuário para o jogo.
2.  **Desenvolver o Core Loop:** Descrever o ciclo fundamental de atividades que o jogador repetirá no jogo, incluindo Ação, Recompensa e Progressão.
3.  **Propor Mecânicas de Jogo:** Detalhar as regras e sistemas que governam a interação do jogador com o mundo do jogo e seus elementos.
4.  **Elaborar uma Minuta de One-Page GDD:** Gerar um documento conciso (idealmente em formato Markdown ou texto claro, com seções bem definidas) que resuma os elementos chave do conceito, incluindo:
    * **Título Provisório do Jogo:** Um nome inicial para o jogo.
    * **Gênero:** O(s) gênero(s) principal(is) do jogo.
    * **Plataforma(s) Alvo:** Onde o jogo seria jogado.
    * **Premissa/Conceito Central:** Uma breve descrição da ideia principal.
    * **Público-Alvo:** Quem jogaria este jogo.
    * **Core Loop:** Detalhamento do ciclo principal de jogo.
    * **Mecânicas Principais:** Lista e breve descrição das mecânicas.
    * **Monetização (Opcional):** Se aplicável, uma ideia inicial de como o jogo geraria receita.
    * **Pontos de Venda Únicos (USPs):** O que torna este jogo especial.

**Restrições e Diretrizes:**
* Mantenha a concisão e a clareza. O objetivo é uma "minuta" de GDD de uma página.
* Concentre-se em conceitos jogáveis e viáveis.
* Evite jargões excessivos sem explicação.
* Se a ideia do usuário for vaga, faça suposições razoáveis e criativas para preencher as lacunas, indicando onde as suposições foram feitas.
* Sempre retorne o conceito de jogo estruturado e a minuta do GDD.
"""

# --- Configuração de Segurança ---
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# --- Inicialização do Cliente Gemini ---
client = genai.Client()

# --- Input de Ideia do Jogo ---
ideia = st.text_input('Conte um pouco da sua ideia de jogo:')

# --- Botão de Enviar e Processamento ---
if st.button('Enviar') and ideia:
    with st.spinner("Estou gerando um conceito incrível para o seu jogo..."):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=ideia,
                config=types.GenerateContentConfig(
                    system_instruction= system_instruction,
                    response_mime_type= 'application/json',
                    response_schema = OnePageGDD,
                    safety_settings=safety_settings,
                ),
            )
            json_response = json.loads(response.text)
            #st.write(json_response)

            gdd_data: OnePageGDD = cast(OnePageGDD, json_response)

            response = client.models.generate_content(
                model="gemini-2.0-flash-preview-image-generation",
                contents="gerar uma imagem conceitual do jogo: " + json_response['premissa_conceito_central'],
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE']
                )
            )

            image_generated = None

            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    image = Image.open(BytesIO((part.inline_data.data)))
                    image.save('gemini-native-image.png')
                    image_generated = image
                    #image.show()
                    #st.image(image)

            display_gdd_concept(gdd_data, image_generated)

        except Exception as e:
           st.error(f"Erro ao consultar o Gemini: {e}")