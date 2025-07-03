"""
Módulo utilitário para a sidebar do Game Concept Forge.
Centraliza a lógica da sidebar para reutilização em todas as páginas.
"""

import streamlit as st
import os
from datetime import datetime
from pathlib import Path

# Lista de páginas e ícones
PAGES = [
    {"name": "Página Inicial", "icon": "🏠", "file": "app.py"},
    {"name": "Concept Generator", "icon": "📝", "file": "pages/01_concept_generator.py"},
    {"name": "Competitor Analysis", "icon": "🔍", "file": "pages/02_competitor_analysis.py"},
    {"name": "Core Loop Developer", "icon": "🔄", "file": "pages/03_core_loop_developer.py"},
    {"name": "Game Flow Creator", "icon": "🎯", "file": "pages/04_game_flow_creator.py"},
    {"name": "Pitch Deck Creator", "icon": "📊", "file": "pages/05_pitch_deck_creator.py"},
]

def render_sidebar():
    """
    Sidebar multipage robusta: navegação customizada, status, config, histórico e sobre.
    """
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    with st.sidebar:
        # --- Navegação ---
        st.markdown("<div style='font-size:1.2em; font-weight:bold; margin-bottom:0.5em;'>📄 Navegação</div>", unsafe_allow_html=True)
        current_page = Path(st.session_state.get('__file__', '')).name.lower()
        for page in PAGES:
            is_active = Path(page['file']).name.lower() == current_page
            btn_label = f"{page['icon']} {page['name']}"
            if st.button(btn_label, use_container_width=True, disabled=is_active, key=f"nav_{page['file']}"):
                if not is_active:
                    st.switch_page(page['file'])
        st.markdown("---")

        # --- Status do conceito atual ---
        if 'current_gdd' in st.session_state:
            st.success("✅ Conceito carregado")
            gdd = st.session_state['current_gdd']
            st.markdown(f"**Título:** {gdd.get('titulo_provisorio', 'Sem título')}")
            st.markdown(f"**Gênero:** {gdd.get('genero', 'N/A')}")
            if st.button("🔄 Limpar Sessão", use_container_width=True):
                clear_session_data()
                st.rerun()
        else:
            st.info("ℹ️ Nenhum conceito carregado")
            st.markdown("Gere um conceito na página Concept Generator para começar!")
        st.markdown("---")

        # --- Status da configuração ---
        st.markdown("**🔧 Configuração:**")
        api_status = "✅ Conectado" if GEMINI_API_KEY else "❌ Não configurado"
        st.markdown(f"API Status: {api_status}")
        if not GEMINI_API_KEY:
            st.error("⚠️ GEMINI_API_KEY não encontrada!")
            st.markdown("Configure sua chave de API para usar o app.")
        st.markdown("---")

        # --- Histórico de pitch decks (dropdown elegante) ---
        st.markdown("**📊 Histórico de Pitch Decks:**")
        if 'pitch_deck_history' in st.session_state and st.session_state.pitch_deck_history:
            with st.expander("Ver últimos 5 pitch decks", expanded=False):
                for i, pitch in enumerate(st.session_state.pitch_deck_history[-5:][::-1], 1):
                    st.markdown(f"**{i}.** {pitch.get('concept_title', 'Sem título')} - {pitch.get('publico_alvo', 'N/A')}")
        else:
            st.markdown("Nenhum pitch deck disponível")
        st.markdown("---")

        # --- Sobre ---
        st.markdown("**ℹ️ Sobre:**")
        st.markdown("🎮 **Game Concept Forge @ Wilson Melo**")
        st.markdown("Versão: 1.1.0")
        st.markdown("IA Generativa para Linguagem")
        st.markdown("[25E2_3]")

def clear_session_data():
    """
    Limpa todos os dados da sessão.
    """
    keys_to_clear = [
        'current_gdd',
        'current_concept',
        'competitor_analysis',
        'analysis_concept',
        'core_loop_detailed',
        'core_loop_concept',
        'game_flow',
        'flow_concept',
        'pitch_deck_history',
        'current_pitch_deck'
    ]

    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

def add_to_concept_history(title: str, gdd_data: dict, concept: str):
    """
    Adiciona um conceito ao histórico.

    Args:
        title: Título do conceito
        gdd_data: Dados do GDD
        concept: Conceito original
    """
    if 'concept_history' not in st.session_state:
        st.session_state.concept_history = []

    st.session_state.concept_history.append({
        'title': title,
        'gdd': gdd_data,
        'concept': concept,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M")
    })

def get_session_summary():
    """
    Retorna um resumo da sessão atual.

    Returns:
        dict: Resumo da sessão
    """
    summary = {
        'has_concept': 'current_gdd' in st.session_state,
        'has_analysis': 'competitor_analysis' in st.session_state,
        'has_core_loop': 'core_loop_detailed' in st.session_state,
        'has_flow': 'game_flow' in st.session_state,
        'has_pitch_deck': 'current_pitch_deck' in st.session_state,
        'concept_count': len(st.session_state.get('concept_history', [])),
        'analysis_count': len(st.session_state.get('analysis_history', [])),
        'core_loop_count': len(st.session_state.get('core_loop_history', [])),
        'flow_count': len(st.session_state.get('flow_history', [])),
        'pitch_deck_count': len(st.session_state.get('pitch_deck_history', []))
    }

    if summary['has_concept']:
        gdd = st.session_state['current_gdd']
        summary['current_title'] = gdd.get('titulo_provisorio', 'Sem título')
        summary['current_genre'] = gdd.get('genero', 'N/A')

    return summary