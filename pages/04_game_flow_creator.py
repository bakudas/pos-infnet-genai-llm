"""
Página 4: Game Flow Creator
Cria fluxos de jogo detalhados para conceitos de jogos.
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Adiciona o diretório raiz ao path para importar os módulos utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import GeminiClient, FluxoJogo, render_sidebar

# --- Configuração da página ---
st.set_page_config(layout="wide", page_title="Game Flow Creator - Game Concept Forge")

# --- Renderiza a sidebar ---
render_sidebar()

# --- Título e Descrição ---
st.title("🎯 Game Flow Creator")
st.markdown("""
    Crie fluxos de jogo completos e otimizados!
    Esta ferramenta desenvolve onboarding, progressão de níveis,
    momentos de decisão e experiência do usuário para seu jogo.
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

# --- Função para exibir fluxo de jogo ---
def display_game_flow(game_flow: FluxoJogo):
    """Exibe o fluxo de jogo de forma estruturada."""

    # Visão geral
    st.subheader("🎯 Visão Geral do Fluxo de Jogo")

    # Onboarding
    with st.expander("🚀 Onboarding e Tutorial", expanded=True):
        onboarding = game_flow.get('onboarding', {})

        st.markdown(f"**Tutorial:** {onboarding.get('tutorial', 'N/A')}")

        st.markdown("**Primeiros Passos:**")
        primeiros_passos = onboarding.get('primeiros_passos', [])
        if primeiros_passos:
            for i, passo in enumerate(primeiros_passos, 1):
                st.markdown(f"{i}. {passo}")
        else:
            st.info("Nenhum primeiro passo definido.")

        st.markdown("**Objetivos Iniciais:**")
        objetivos = onboarding.get('objetivos_iniciais', [])
        if objetivos:
            for i, objetivo in enumerate(objetivos, 1):
                st.markdown(f"{i}. {objetivo}")
        else:
            st.info("Nenhum objetivo inicial definido.")

    st.markdown("---")

    # Progressão
    st.subheader("📈 Progressão de Níveis")

    with st.expander("🏆 Estrutura de Níveis", expanded=True):
        progressao = game_flow.get('progressao', {})

        st.markdown(f"**Estrutura:** {progressao.get('estrutura_niveis', 'N/A')}")

        st.markdown("**Desbloqueios:**")
        desbloqueios = progressao.get('desbloqueios', [])
        if desbloqueios:
            for i, desbloqueio in enumerate(desbloqueios, 1):
                st.markdown(f"{i}. {desbloqueio}")
        else:
            st.info("Nenhum desbloqueio definido.")

        st.markdown("**Momentos Chave:**")
        momentos_chave = progressao.get('momentos_chave', [])
        if momentos_chave:
            for i, momento in enumerate(momentos_chave, 1):
                st.markdown(f"{i}. {momento}")
        else:
            st.info("Nenhum momento chave definido.")

    st.markdown("---")

    # Decisões do Jogador
    st.subheader("🤔 Momentos de Decisão")

    with st.expander("🎯 Decisões do Jogador", expanded=True):
        decisoes = game_flow.get('decisoes_jogador', [])
        if decisoes:
            for i, decisao in enumerate(decisoes, 1):
                st.markdown(f"**Decisão {i}:** {decisao}")
        else:
            st.info("Nenhuma decisão do jogador definida.")

    # Checkpoints
    with st.expander("📍 Pontos de Checkpoint"):
        checkpoints = game_flow.get('checkpoints', [])
        if checkpoints:
            for i, checkpoint in enumerate(checkpoints, 1):
                st.markdown(f"**Checkpoint {i}:** {checkpoint}")
        else:
            st.info("Nenhum checkpoint definido.")

    st.markdown("---")

    # Fluxo de Monetização
    st.subheader("💰 Fluxo de Monetização")

    with st.expander("💳 Monetização", expanded=True):
        fluxo_monetizacao = game_flow.get('fluxo_monetizacao', [])
        if fluxo_monetizacao:
            for i, monetizacao in enumerate(fluxo_monetizacao, 1):
                st.markdown(f"{i}. {monetizacao}")
        else:
            st.info("Nenhum fluxo de monetização definido.")

    st.markdown("---")

    # Experiência do Usuário
    st.subheader("👤 Experiência do Usuário")

    experiencia = game_flow.get('experiencia_usuario', {})

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("⭐ Pontos Altos", expanded=True):
            pontos_alto = experiencia.get('pontos_alto', [])
            if pontos_alto:
                for ponto in pontos_alto:
                    st.markdown(f"• {ponto}")
            else:
                st.info("Nenhum ponto alto definido.")

    with col2:
        with st.expander("⚠️ Pontos de Atenção"):
            pontos_baixo = experiencia.get('pontos_baixo', [])
            if pontos_baixo:
                for ponto in pontos_baixo:
                    st.markdown(f"• {ponto}")
            else:
                st.info("Nenhum ponto de atenção definido.")

    # Otimizações
    with st.expander("🔧 Otimizações Sugeridas", expanded=True):
        otimizacoes = experiencia.get('otimizacoes', [])
        if otimizacoes:
            for i, otimizacao in enumerate(otimizacoes, 1):
                st.markdown(f"**{i}.** {otimizacao}")
        else:
            st.info("Nenhuma otimização sugerida.")

    st.markdown("---")
    st.success("Fluxo de jogo criado! Use essas informações para implementar a experiência do usuário.")

# --- Interface principal ---
st.markdown("### 🎮 Conceito para Criação do Fluxo de Jogo")

# Verifica se há um conceito na sessão
if 'current_gdd' in st.session_state and 'current_concept' in st.session_state:
    st.info("📋 Usando conceito atual da sessão")
    current_concept = st.session_state['current_concept']
    current_gdd = st.session_state['current_gdd']

    # Exibe informações do conceito atual
    with st.expander("📋 Conceito Atual"):
        st.markdown(f"**Título:** {current_gdd.get('titulo_provisorio', 'Sem título')}")
        st.markdown(f"**Gênero:** {current_gdd.get('genero', 'N/A')}")
        st.markdown(f"**Plataformas:** {', '.join(current_gdd.get('plataformas_alvo', ['N/A']))}")

    # Permite editar o conceito para criação do fluxo
    concept_for_flow = st.text_area(
        "Edite o conceito para criação do fluxo de jogo (opcional):",
        value=current_concept,
        height=100
    )
else:
    st.warning("⚠️ Nenhum conceito encontrado na sessão. Gere um conceito primeiro ou insira um manualmente.")
    concept_for_flow = st.text_area(
        "Descreva o conceito de jogo para criação do fluxo:",
        placeholder="Ex: Um jogo de cartas onde os jogadores constroem baralhos baseados em personagens históricos...",
        height=150
    )

# Opções de criação
with st.expander("⚙️ Opções de Criação"):
    flow_type = st.selectbox(
        "Tipo de Fluxo:",
        ["Linear", "Não-Linear", "Sandbox", "Híbrido"],
        index=0
    )

    target_audience = st.selectbox(
        "Público-Alvo:",
        ["Casual", "Core", "Hardcore", "Familiar"],
        index=0
    )

    monetization_type = st.selectbox(
        "Tipo de Monetização:",
        ["Freemium", "Premium", "Subscription", "Ads", "Híbrido"],
        index=0
    )

    include_onboarding = st.checkbox("Incluir onboarding detalhado", value=True)
    include_monetization = st.checkbox("Incluir fluxo de monetização", value=True)

# --- Botão de criação ---
if st.button("🎯 Criar Fluxo de Jogo", type="primary") and concept_for_flow:
    with st.spinner("Criando fluxo de jogo detalhado..."):
        try:
            # Gera o fluxo de jogo
            game_flow = client.create_game_flow(concept_for_flow)

            # Exibe o resultado
            display_game_flow(game_flow)

            # Salva na sessão
            st.session_state['game_flow'] = game_flow
            st.session_state['flow_concept'] = concept_for_flow

            # Adiciona ao histórico
            if 'flow_history' not in st.session_state:
                st.session_state.flow_history = []

            st.session_state.flow_history.append({
                'concept': concept_for_flow,
                'flow': game_flow,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'type': flow_type,
                'audience': target_audience
            })

        except Exception as e:
            st.error(f"Erro ao criar fluxo de jogo: {e}")
            st.info("Verifique se sua chave de API está configurada corretamente.")

# --- Histórico de fluxos ---
if 'flow_history' in st.session_state and st.session_state.flow_history:
    with st.expander("📚 Histórico de Fluxos"):
        for i, flow_record in enumerate(st.session_state.flow_history):
            st.markdown(f"**{i+1}. Fluxo {flow_record['type']}** - {flow_record['date']}")
            st.markdown(f"*Público: {flow_record['audience']}*")
            if st.button(f"Carregar fluxo {i+1}", key=f"load_flow_{i}"):
                st.session_state['game_flow'] = flow_record['flow']
                st.session_state['flow_concept'] = flow_record['concept']
                st.rerun()

# --- Seção de ajuda ---
with st.expander("❓ Como criar um bom fluxo de jogo"):
    st.markdown("""
    **Um fluxo de jogo eficaz deve:**

    1. **Onboarding suave:** Introduzir mecânicas gradualmente
    2. **Progressão clara:** Sensação de evolução constante
    3. **Decisões significativas:** Escolhas que impactam o jogo
    4. **Checkpoints estratégicos:** Pontos de salvamento bem posicionados
    5. **Monetização natural:** Integrada sem ser intrusiva

    **Elementos essenciais:**
    - **Tutorial interativo:** Aprender fazendo
    - **Curva de dificuldade:** Desafio crescente
    - **Feedback constante:** Informações claras sobre progresso
    - **Variedade:** Diferentes tipos de conteúdo
    - **Recompensas:** Satisfação imediata e de longo prazo

    **Exemplos de fluxos bem-sucedidos:**
    - **Candy Crush:** Tutorial → Níveis progressivos → Power-ups
    - **Clash Royale:** Tutorial → Arena → Desbloqueios → Clãs
    - **Minecraft:** Tutorial → Sobrevivência → Exploração → Construção
    """)

# --- Exportar fluxo ---
if 'game_flow' in st.session_state:
    st.markdown("---")
    st.markdown("### 📤 Exportar Fluxo de Jogo")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Exportar como JSON"):
            import json
            flow_data = {
                'concept': st.session_state.get('flow_concept', ''),
                'flow': st.session_state['game_flow'],
                'date': datetime.now().isoformat()
            }
            st.download_button(
                label="⬇️ Download JSON",
                data=json.dumps(flow_data, indent=2, ensure_ascii=False),
                file_name=f"game_flow_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json"
            )

    with col2:
        if st.button("📊 Gerar Diagrama"):
            st.info("Funcionalidade de diagrama em desenvolvimento!")

# --- Visualização do fluxo ---
if 'game_flow' in st.session_state:
    st.markdown("---")
    st.markdown("### 🎯 Visualização do Fluxo")

    # Cria um fluxograma simples
    game_flow = st.session_state['game_flow']

    # Onboarding
    onboarding = game_flow.get('onboarding', {})
    if onboarding.get('primeiros_passos'):
        st.markdown("**Fluxo de Onboarding:**")
        for i, passo in enumerate(onboarding['primeiros_passos'], 1):
            if i < len(onboarding['primeiros_passos']):
                st.markdown(f"**{i}.** {passo} →")
            else:
                st.markdown(f"**{i}.** {passo} ✅")

    # Progressão
    progressao = game_flow.get('progressao', {})
    if progressao.get('momentos_chave'):
        st.markdown("**Momentos Chave da Progressão:**")
        for i, momento in enumerate(progressao['momentos_chave'], 1):
            st.markdown(f"**{i}.** {momento}")

    # Decisões
    decisoes = game_flow.get('decisoes_jogador', [])
    if decisoes:
        st.markdown("**Pontos de Decisão:**")
        for i, decisao in enumerate(decisoes, 1):
            st.markdown(f"**{i}.** {decisao} 🤔")