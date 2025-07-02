"""
Página 3: Core Loop Developer
Desenvolve core loops detalhados para conceitos de jogos.
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Adiciona o diretório raiz ao path para importar os módulos utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import GeminiClient, CoreLoopDetalhado, render_sidebar

# --- Configuração da página ---
st.set_page_config(layout="wide", page_title="Core Loop Developer - Game Concept Forge")

# --- Renderiza a sidebar ---
render_sidebar()

# --- Título e Descrição ---
st.title("🔄 Core Loop Developer")
st.markdown("""
    Desenvolva core loops detalhados e balanceados!
    Esta ferramenta cria sistemas de recompensas, feedback loops,
    mecânicas de retenção e balanceamento para seu jogo.
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

# --- Função para exibir core loop detalhado ---
def display_core_loop_detailed(core_loop: CoreLoopDetalhado):
    """Exibe o core loop detalhado de forma estruturada."""

    # Visão geral
    st.subheader("🎯 Visão Geral do Core Loop")

    # Ações principais
    with st.expander("🎮 Ações Principais do Jogador", expanded=True):
        acoes = core_loop.get('acoes_principais', [])
        if acoes:
            for i, acao in enumerate(acoes, 1):
                st.markdown(f"**{i}.** {acao}")
        else:
            st.info("Nenhuma ação principal definida.")

    st.markdown("---")

    # Sistema de Recompensas
    st.subheader("🏆 Sistema de Recompensas")

    sistema_recompensas = core_loop.get('sistema_recompensas', {})

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("⚡ Recompensas Imediatas", expanded=True):
            recompensas_imediatas = sistema_recompensas.get('recompensas_imediatas', [])
            if recompensas_imediatas:
                for recompensa in recompensas_imediatas:
                    st.markdown(f"• {recompensa}")
            else:
                st.info("Nenhuma recompensa imediata definida.")

    with col2:
        with st.expander("🎁 Recompensas de Longo Prazo"):
            recompensas_longo_prazo = sistema_recompensas.get('recompensas_longo_prazo', [])
            if recompensas_longo_prazo:
                for recompensa in recompensas_longo_prazo:
                    st.markdown(f"• {recompensa}")
            else:
                st.info("Nenhuma recompensa de longo prazo definida.")

    # Sistema de Progressão
    with st.expander("📈 Sistema de Progressão", expanded=True):
        sistema_progressao = sistema_recompensas.get('sistema_progressao', 'N/A')
        st.markdown(f"**Sistema:** {sistema_progressao}")

    st.markdown("---")

    # Feedback Loops
    st.subheader("🔄 Feedback Loops")

    with st.expander("🔄 Loops de Feedback", expanded=True):
        feedback_loops = core_loop.get('feedback_loops', [])
        if feedback_loops:
            for i, loop in enumerate(feedback_loops, 1):
                st.markdown(f"**Loop {i}:** {loop}")
        else:
            st.info("Nenhum feedback loop definido.")

    # Mecânicas de Retenção
    with st.expander("🎯 Mecânicas de Retenção"):
        mecanicas_retencao = core_loop.get('mecanicas_retencao', [])
        if mecanicas_retencao:
            for i, mecanica in enumerate(mecanicas_retencao, 1):
                st.markdown(f"**{i}.** {mecanica}")
        else:
            st.info("Nenhuma mecânica de retenção definida.")

    st.markdown("---")

    # Balanceamento
    st.subheader("⚖️ Balanceamento")

    balanceamento = core_loop.get('balanceamento', {})

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("🎯 Dificuldade Inicial", expanded=True):
            dificuldade_inicial = balanceamento.get('dificuldade_inicial', 'N/A')
            st.markdown(f"**Dificuldade:** {dificuldade_inicial}")

    with col2:
        with st.expander("📊 Curva de Dificuldade"):
            curva_dificuldade = balanceamento.get('curva_dificuldade', 'N/A')
            st.markdown(f"**Curva:** {curva_dificuldade}")

    # Pontos de Ajuste
    with st.expander("🔧 Pontos de Ajuste"):
        pontos_ajuste = balanceamento.get('pontos_ajuste', [])
        if pontos_ajuste:
            for i, ponto in enumerate(pontos_ajuste, 1):
                st.markdown(f"**{i}.** {ponto}")
        else:
            st.info("Nenhum ponto de ajuste definido.")

    st.markdown("---")
    st.success("Core loop detalhado desenvolvido! Use essas informações para implementar o sistema de jogo.")

# --- Interface principal ---
st.markdown("### 🎮 Conceito para Desenvolvimento do Core Loop")

# Verifica se há um conceito na sessão
if 'current_gdd' in st.session_state and 'current_concept' in st.session_state:
    st.info("📋 Usando conceito atual da sessão")
    current_concept = st.session_state['current_concept']
    current_gdd = st.session_state['current_gdd']

    # Exibe informações do conceito atual
    with st.expander("📋 Conceito Atual"):
        st.markdown(f"**Título:** {current_gdd.get('titulo_provisorio', 'Sem título')}")
        st.markdown(f"**Gênero:** {current_gdd.get('genero', 'N/A')}")
        st.markdown(f"**Core Loop Básico:** {current_gdd.get('core_loop', {}).get('acao', 'N/A')}")

    # Permite editar o conceito para desenvolvimento
    concept_for_development = st.text_area(
        "Edite o conceito para desenvolvimento do core loop (opcional):",
        value=current_concept,
        height=100
    )
else:
    st.warning("⚠️ Nenhum conceito encontrado na sessão. Gere um conceito primeiro ou insira um manualmente.")
    st.markdown("[Ir para Concept Generator](/concept_generator)")
    concept_for_development = st.text_area(
        "Descreva o conceito de jogo para desenvolvimento do core loop:",
        placeholder="Ex: Um jogo de cartas onde os jogadores constroem baralhos baseados em personagens históricos...",
        height=150
    )

# Opções de desenvolvimento
with st.expander("⚙️ Opções de Desenvolvimento"):
    focus_area = st.multiselect(
        "Áreas de Foco:",
        ["Sistema de Recompensas", "Feedback Loops", "Mecânicas de Retenção", "Balanceamento"],
        default=["Sistema de Recompensas", "Feedback Loops"]
    )

    complexity_level = st.selectbox(
        "Nível de Complexidade:",
        ["Simples", "Intermediário", "Complexo"],
        index=1
    )

    target_platform = st.selectbox(
        "Plataforma Alvo:",
        ["Mobile", "PC", "Console", "Multiplataforma"],
        index=0
    )

# --- Botão de desenvolvimento ---
if st.button("🔄 Desenvolver Core Loop", type="primary") and concept_for_development:
    with st.spinner("Desenvolvendo core loop detalhado..."):
        try:
            # Gera o core loop detalhado
            core_loop_detailed = client.develop_core_loop(concept_for_development)

            # Exibe o resultado
            display_core_loop_detailed(core_loop_detailed)

            # Salva na sessão
            st.session_state['core_loop_detailed'] = core_loop_detailed
            st.session_state['core_loop_concept'] = concept_for_development

            # Adiciona ao histórico
            if 'core_loop_history' not in st.session_state:
                st.session_state.core_loop_history = []

            st.session_state.core_loop_history.append({
                'concept': concept_for_development,
                'core_loop': core_loop_detailed,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'complexity': complexity_level,
                'focus_areas': focus_area
            })

        except Exception as e:
            st.error(f"Erro ao desenvolver core loop: {e}")
            st.info("Verifique se sua chave de API está configurada corretamente.")

# --- Histórico de core loops ---
if 'core_loop_history' in st.session_state and st.session_state.core_loop_history:
    with st.expander("📚 Histórico de Core Loops"):
        for i, core_loop_record in enumerate(st.session_state.core_loop_history):
            st.markdown(f"**{i+1}. Core Loop {core_loop_record['complexity']}** - {core_loop_record['date']}")
            st.markdown(f"*Foco: {', '.join(core_loop_record['focus_areas'])}*")
            if st.button(f"Carregar core loop {i+1}", key=f"load_core_loop_{i}"):
                st.session_state['core_loop_detailed'] = core_loop_record['core_loop']
                st.session_state['core_loop_concept'] = core_loop_record['concept']
                st.rerun()

# --- Seção de ajuda ---
with st.expander("❓ Como desenvolver um bom core loop"):
    st.markdown("""
    **Um core loop eficaz deve:**

    1. **Ser viciante:** O jogador deve querer repetir a ação
    2. **Ter recompensas claras:** Feedback imediato e satisfatório
    3. **Progredir naturalmente:** Evolução constante sem frustração
    4. **Ser balanceado:** Desafio adequado ao nível do jogador

    **Elementos essenciais:**
    - **Ação clara:** O que o jogador faz repetidamente
    - **Recompensa imediata:** Feedback positivo instantâneo
    - **Progressão:** Sensação de evolução e crescimento
    - **Variedade:** Diferentes formas de executar a ação
    - **Mastery:** Possibilidade de melhorar a habilidade

    **Exemplos de core loops bem-sucedidos:**
    - **Candy Crush:** Trocar doces → Explodir → Progressão
    - **Clash Royale:** Coletar cartas → Construir deck → Batalhar
    - **Minecraft:** Minerar → Craftar → Construir
    """)

# --- Exportar core loop ---
if 'core_loop_detailed' in st.session_state:
    st.markdown("---")
    st.markdown("### 📤 Exportar Core Loop")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Exportar como JSON"):
            import json
            core_loop_data = {
                'concept': st.session_state.get('core_loop_concept', ''),
                'core_loop': st.session_state['core_loop_detailed'],
                'date': datetime.now().isoformat()
            }
            st.download_button(
                label="⬇️ Download JSON",
                data=json.dumps(core_loop_data, indent=2, ensure_ascii=False),
                file_name=f"core_loop_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json"
            )

    with col2:
        if st.button("📊 Gerar Diagrama"):
            st.info("Funcionalidade de diagrama em desenvolvimento!")

# --- Visualização do fluxo ---
if 'core_loop_detailed' in st.session_state:
    st.markdown("---")
    st.markdown("### 🔄 Visualização do Fluxo")

    # Cria um fluxograma simples
    core_loop = st.session_state['core_loop_detailed']
    acoes = core_loop.get('acoes_principais', [])

    if acoes:
        st.markdown("**Fluxo de Ações:**")
        for i, acao in enumerate(acoes):
            if i < len(acoes) - 1:
                st.markdown(f"**{i+1}.** {acao} →")
            else:
                st.markdown(f"**{i+1}.** {acao} 🔄")
    else:
        st.info("Nenhuma ação definida para visualização.")