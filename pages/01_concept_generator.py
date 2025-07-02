"""
Página 1: Concept Generator
Gera conceitos de jogos a partir de ideias iniciais.
"""

import streamlit as st
from PIL import Image
from typing import Optional, cast
import sys
import os

# Adiciona o diretório raiz ao path para importar os módulos utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import GeminiClient, OnePageGDD, render_sidebar, add_to_concept_history

# --- Configuração da página ---
st.set_page_config(layout="wide", page_title="Concept Generator - Game Concept Forge")

# --- Renderiza a sidebar ---
render_sidebar()

# --- Título e Descrição ---
st.title("🎮 Concept Generator")
st.markdown("""
    Transforme sua ideia inicial em um conceito de jogo estruturado!
    Esta ferramenta gera automaticamente um One-Page GDD com core loop,
    mecânicas, monetização e diferenciais, além de sugerir uma arte conceitual.
""")

# --- Inicialização do cliente Gemini ---
@st.cache_resource
def get_gemini_client():
    """Inicializa e cacheia o cliente Gemini."""
    try:
        return GeminiClient()
    except ValueError as e:
        st.error(f"Erro de configuração: {e}")
        st.stop()

client = get_gemini_client()

# --- Função para exibir o GDD de forma estruturada ---
def display_gdd_concept(gdd_data: OnePageGDD, generated_image: Optional[Image.Image] = None):
    """Exibe o GDD de forma estruturada e moderna."""
    st.subheader(f"✨ Conceito de Jogo: {gdd_data.get('titulo_provisorio', 'Sem Título')}")

    # Apresenta a imagem gerada ou o placeholder
    if generated_image:
        st.image(generated_image, caption="Arte Conceitual Gerada", use_container_width=True)
    else:
        # URL de placeholder
        image_url = "https://placehold.co/600x300/007bff/ffffff?text=Arte+Conceitual+Gerada"
        st.image(image_url, caption="Arte Conceitual (Placeholder)", use_column_width=True)

    st.markdown("---")

    # Informações básicas em colunas
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Gênero:** {gdd_data.get('genero', 'N/A')}")
        st.markdown(f"**Plataformas Alvo:** {', '.join(gdd_data.get('plataformas_alvo', ['N/A']))}")
    with col2:
        st.markdown(f"**Público-Alvo:** {', '.join(gdd_data.get('publico_alvo', ['N/A']))}")

    st.markdown("---")
    st.markdown(f"**Premissa/Conceito Central:** {gdd_data.get('premissa_conceito_central', 'N/A')}")
    st.markdown("---")

    # Core Loop
    with st.expander("🔄 Core Loop", expanded=True):
        core_loop = gdd_data.get('core_loop', {})
        st.markdown(f"**Ação:** {core_loop.get('acao', 'N/A')}")
        st.markdown(f"**Recompensa:** {core_loop.get('recompensa', 'N/A')}")
        st.markdown(f"**Progressão:** {core_loop.get('progressao', 'N/A')}")

    # Mecânicas Principais
    with st.expander("⚙️ Mecânicas Principais"):
        mecanicas = gdd_data.get('mecanicas_principais', [])
        if mecanicas:
            for mec in mecanicas:
                st.markdown(f"**{mec.get('nome', 'N/A')}**: {mec.get('descricao', 'N/A')}")
        else:
            st.markdown("Nenhuma mecânica principal detalhada.")

    # Monetização Opcional
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

# --- Instruções do Modelo Gemini ---
system_instruction = """
Você é um "Arquiteto de Conceitos de Jogo", uma inteligência artificial especializada em transformar ideias iniciais de usuários em conceitos de jogo estruturados. Sua função principal é:

1. **Analisar a Ideia Central:** Compreender a essência da ideia do usuário para o jogo.
2. **Desenvolver o Core Loop:** Descrever o ciclo fundamental de atividades que o jogador repetirá no jogo, incluindo Ação, Recompensa e Progressão.
3. **Propor Mecânicas de Jogo:** Detalhar as regras e sistemas que governam a interação do jogador com o mundo do jogo e seus elementos.
4. **Elaborar uma Minuta de One-Page GDD:** Gerar um documento conciso que resuma os elementos chave do conceito.

**Restrições e Diretrizes:**
* Mantenha a concisão e a clareza. O objetivo é uma "minuta" de GDD de uma página.
* Concentre-se em conceitos jogáveis e viáveis.
* Evite jargões excessivos sem explicação.
* Se a ideia do usuário for vaga, faça suposições razoáveis e criativas para preencher as lacunas.
* Sempre retorne o conceito de jogo estruturado e a minuta do GDD.
"""

# --- Interface principal ---
st.markdown("### 💡 Conte sua ideia de jogo")
ideia = st.text_area(
    "Descreva sua ideia de jogo aqui:",
    placeholder="Ex: Um jogo de cartas onde os jogadores constroem baralhos baseados em personagens históricos do Rio de Janeiro...",
    height=150
)

# Opções avançadas
with st.expander("⚙️ Opções Avançadas"):
    generate_image = st.checkbox("Gerar arte conceitual", value=True)
    model_choice = st.selectbox(
        "Modelo Gemini:",
        ["gemini-2.5-flash", "gemini-1.5-flash"],
        index=0
    )

# --- Botão de processamento ---
if st.button("🚀 Gerar Conceito", type="primary") and ideia:
    with st.spinner("Estou gerando um conceito incrível para o seu jogo..."):
        try:
            # Gera o conceito
            gdd_data = client.generate_content(
                prompt=ideia,
                system_instruction=system_instruction,
                response_schema={
                    "type": "object",
                    "properties": {
                        "titulo_provisorio": {"type": "string"},
                        "genero": {"type": "string"},
                        "plataformas_alvo": {"type": "array", "items": {"type": "string"}},
                        "premissa_conceito_central": {"type": "string"},
                        "publico_alvo": {"type": "array", "items": {"type": "string"}},
                        "core_loop": {
                            "type": "object",
                            "properties": {
                                "acao": {"type": "string"},
                                "recompensa": {"type": "string"},
                                "progressao": {"type": "string"}
                            }
                        },
                        "mecanicas_principais": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "nome": {"type": "string"},
                                    "descricao": {"type": "string"}
                                }
                            }
                        },
                        "monetizacao_opcional": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "tipo": {"type": "string"},
                                    "descricao": {"type": "string"}
                                }
                            }
                        },
                        "pontos_de_venda_unicos_usps": {"type": "array", "items": {"type": "string"}}
                    }
                },
                model=model_choice
            )

            gdd_data: OnePageGDD = cast(OnePageGDD, gdd_data)

            # Gera imagem se solicitado
            image_generated = None
            if generate_image:
                with st.spinner("Gerando arte conceitual..."):
                    image_generated = client.generate_image(
                        f"arte conceitual do jogo: {gdd_data['premissa_conceito_central']}"
                    )

            # Exibe o resultado
            display_gdd_concept(gdd_data, image_generated)

            # Salva na sessão
            st.session_state['current_gdd'] = gdd_data
            st.session_state['current_concept'] = ideia

            # Adiciona ao histórico
            add_to_concept_history(
                gdd_data.get('titulo_provisorio', 'Sem título'),
                gdd_data,
                ideia
            )

        except Exception as e:
            st.error(f"Erro ao gerar conceito: {e}")
            st.info("Verifique se sua chave de API está configurada corretamente.")

# --- Seção de ajuda ---
with st.expander("❓ Como usar"):
    st.markdown("""
    **Para obter melhores resultados:**

    1. **Seja específico:** Descreva o gênero, mecânicas principais e público-alvo
    2. **Mencione inspirações:** Cite jogos similares que você admira
    3. **Defina o contexto:** Explique onde e como o jogo seria jogado
    4. **Pense na experiência:** Descreva como o jogador deve se sentir

    **Exemplo de boa descrição:**
    > "Um jogo de estratégia por turnos onde jogadores gerenciam uma cidade medieval.
    > Inspirado em Civilization e Age of Empires, mas focado em construção e diplomacia.
    > Público-alvo: jogadores casuais de 25-40 anos que gostam de estratégia sem complexidade excessiva."
    """)

# --- Histórico de conceitos ---
if 'concept_history' in st.session_state and st.session_state.concept_history:
    with st.expander("📚 Histórico de Conceitos"):
        for i, concept in enumerate(st.session_state.concept_history):
            st.markdown(f"**{i+1}. {concept['title']}** - {concept['date']}")
            if st.button(f"Carregar conceito {i+1}", key=f"load_{i}"):
                st.session_state['current_gdd'] = concept['gdd']
                st.session_state['current_concept'] = concept['concept']
                st.rerun()