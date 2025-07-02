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
    {"name": "Página Inicial", "icon": "🏠", "path": "app.py", "url": "/"},
    {"name": "Concept Generator", "icon": "📝", "path": "pages/01_concept_generator.py", "url": "/concept_generator"},
    {"name": "Competitor Analysis", "icon": "🔍", "path": "pages/02_competitor_analysis.py", "url": "/competitor_analysis"},
    {"name": "Core Loop Developer", "icon": "🔄", "path": "pages/03_core_loop_developer.py", "url": "/core_loop_developer"},
    {"name": "Game Flow Creator", "icon": "🎯", "path": "pages/04_game_flow_creator.py", "url": "/game_flow_creator"},
    {"name": "Pitch Deck Creator", "icon": "📊", "path": "pages/05_pitch_deck_creator.py", "url": "/pitch_deck_creator"},
]

def render_sidebar():
    """
    Renderiza a sidebar com menu de navegação, informações da sessão, configuração e histórico.
    """
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    with st.sidebar:
        # --- Navegação ---
        st.markdown("<div style='font-size:1.2em; font-weight:bold; margin-bottom:0.5em;'>📄 Navegação</div>", unsafe_allow_html=True)
        current_url = st.query_params.get('page', ['/'])[0]
        # Detecta página ativa pelo URL
        for page in PAGES:
            is_active = (
                (page['url'] == '/' and current_url in ['', '/']) or
                (page['url'] != '/' and page['url'].strip('/') == current_url.strip('/'))
            )
            style = (
                "background-color:#444; border-radius:8px; font-weight:bold;" if is_active else ""
            )
            st.markdown(
                f"<a href='{page['url']}' style='text-decoration:none; color:inherit; display:block; padding:0.1em 0.4em; margin-bottom:0px; {style}'>"
                f"{page['icon']} {page['name']}"
                "</a>", unsafe_allow_html=True
            )
        st.markdown("<hr style='margin:0.7em 0;' />", unsafe_allow_html=True)

        # Status do conceito atual
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

        # Status da configuração
        st.markdown("**🔧 Configuração:**")
        api_status = "✅ Conectado" if GEMINI_API_KEY else "❌ Não configurado"
        st.markdown(f"API Status: {api_status}")
        if not GEMINI_API_KEY:
            st.error("⚠️ GEMINI_API_KEY não encontrada!")
            st.markdown("Configure sua chave de API para usar o app.")

        st.markdown("---")

        # Informações da aplicação
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