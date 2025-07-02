"""
Página 2: Competitor Analysis
Analisa concorrentes e mercado para um conceito de jogo.
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Adiciona o diretório raiz ao path para importar os módulos utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import GeminiClient, AnaliseConcorrentes, render_sidebar

# --- Configuração da página ---
st.set_page_config(layout="wide", page_title="Competitor Analysis - Game Concept Forge")

# --- Renderiza a sidebar ---
render_sidebar()

# --- Título e Descrição ---
st.title("🔍 Análise de Concorrentes")
st.markdown("""
    Analise o mercado e identifique oportunidades de diferenciação!
    Esta ferramenta examina concorrentes diretos e similares,
    identificando pontos fortes, fracos e tendências de mercado.
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

# --- Função para exibir análise de concorrentes ---
def display_competitor_analysis(analysis: AnaliseConcorrentes):
    """Exibe a análise de concorrentes de forma estruturada."""

    # Métricas rápidas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Concorrentes Diretos", len(analysis.get('concorrentes_diretos', [])))
    with col2:
        st.metric("Jogos Similares", len(analysis.get('jogos_similares', [])))
    with col3:
        st.metric("Oportunidades", len(analysis.get('oportunidades_diferencacao', [])))
    with col4:
        st.metric("Tendências", len(analysis.get('tendencias_mercado', [])))

    st.markdown("---")

    # Concorrentes Diretos
    with st.expander("🎯 Concorrentes Diretos", expanded=True):
        concorrentes = analysis.get('concorrentes_diretos', [])
        if concorrentes:
            for i, concorrente in enumerate(concorrentes, 1):
                st.markdown(f"**{i}.** {concorrente}")
        else:
            st.info("Nenhum concorrente direto identificado.")

    # Jogos Similares
    with st.expander("🎮 Jogos Similares"):
        similares = analysis.get('jogos_similares', [])
        if similares:
            for i, jogo in enumerate(similares, 1):
                st.markdown(f"**{i}.** {jogo}")
        else:
            st.info("Nenhum jogo similar identificado.")

    # Análise SWOT dos Concorrentes
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("✅ Pontos Fortes dos Concorrentes"):
            pontos_fortes = analysis.get('pontos_fortes_concorrentes', [])
            if pontos_fortes:
                for ponto in pontos_fortes:
                    st.markdown(f"• {ponto}")
            else:
                st.info("Nenhum ponto forte identificado.")

    with col2:
        with st.expander("❌ Pontos Fracos dos Concorrentes"):
            pontos_fracos = analysis.get('pontos_fracos_concorrentes', [])
            if pontos_fracos:
                for ponto in pontos_fracos:
                    st.markdown(f"• {ponto}")
            else:
                st.info("Nenhum ponto fraco identificado.")

    # Oportunidades de Diferenciação
    with st.expander("💡 Oportunidades de Diferenciação", expanded=True):
        oportunidades = analysis.get('oportunidades_diferencacao', [])
        if oportunidades:
            for i, oportunidade in enumerate(oportunidades, 1):
                st.markdown(f"**{i}.** {oportunidade}")
        else:
            st.info("Nenhuma oportunidade de diferenciação identificada.")

    # Tendências de Mercado
    with st.expander("📈 Tendências de Mercado"):
        tendencias = analysis.get('tendencias_mercado', [])
        if tendencias:
            for i, tendencia in enumerate(tendencias, 1):
                st.markdown(f"**{i}.** {tendencia}")
        else:
            st.info("Nenhuma tendência de mercado identificada.")

    # Recomendações
    with st.expander("🎯 Recomendações Estratégicas", expanded=True):
        recomendacoes = analysis.get('recomendacoes', [])
        if recomendacoes:
            for i, recomendacao in enumerate(recomendacoes, 1):
                st.markdown(f"**{i}.** {recomendacao}")
        else:
            st.info("Nenhuma recomendação disponível.")

    st.markdown("---")
    st.success("Análise de concorrentes concluída! Use essas informações para posicionar seu jogo estrategicamente.")

# --- Interface principal ---
st.markdown("### 🎮 Conceito para Análise")

# Verifica se há um conceito na sessão
if 'current_gdd' in st.session_state and 'current_concept' in st.session_state:
    st.info("📋 Usando conceito atual da sessão")
    current_concept = st.session_state['current_concept']
    current_gdd = st.session_state['current_gdd']

    # Exibe informações do conceito atual
    with st.expander("📋 Conceito Atual"):
        st.markdown(f"**Título:** {current_gdd.get('titulo_provisorio', 'Sem título')}")
        st.markdown(f"**Gênero:** {current_gdd.get('genero', 'N/A')}")
        st.markdown(f"**Premissa:** {current_gdd.get('premissa_conceito_central', 'N/A')}")

    # Permite editar o conceito para análise
    concept_for_analysis = st.text_area(
        "Edite o conceito para análise (opcional):",
        value=current_concept,
        height=100
    )
else:
    st.warning("⚠️ Nenhum conceito encontrado na sessão. Gere um conceito primeiro ou insira um manualmente.")
    st.markdown("[Ir para Concept Generator](/concept_generator)")
    concept_for_analysis = st.text_area(
        "Descreva o conceito de jogo para análise:",
        placeholder="Ex: Um jogo de cartas onde os jogadores constroem baralhos baseados em personagens históricos...",
        height=150
    )

# Opções de análise
with st.expander("⚙️ Opções de Análise"):
    analysis_depth = st.selectbox(
        "Profundidade da Análise:",
        ["Básica", "Intermediária", "Detalhada"],
        index=1
    )

    include_market_trends = st.checkbox("Incluir tendências de mercado", value=True)
    include_recommendations = st.checkbox("Incluir recomendações estratégicas", value=True)

# --- Botão de análise ---
if st.button("🔍 Analisar Concorrentes", type="primary") and concept_for_analysis:
    with st.spinner("Analisando concorrentes e mercado..."):
        try:
            # Gera a análise
            analysis = client.analyze_competitors(concept_for_analysis)

            # Exibe o resultado
            display_competitor_analysis(analysis)

            # Salva na sessão
            st.session_state['competitor_analysis'] = analysis
            st.session_state['analysis_concept'] = concept_for_analysis

            # Adiciona ao histórico
            if 'analysis_history' not in st.session_state:
                st.session_state.analysis_history = []

            st.session_state.analysis_history.append({
                'concept': concept_for_analysis,
                'analysis': analysis,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'depth': analysis_depth
            })

        except Exception as e:
            st.error(f"Erro ao analisar concorrentes: {e}")
            st.info("Verifique se sua chave de API está configurada corretamente.")

# --- Histórico de análises ---
if 'analysis_history' in st.session_state and st.session_state.analysis_history:
    with st.expander("📚 Histórico de Análises"):
        for i, analysis_record in enumerate(st.session_state.analysis_history):
            st.markdown(f"**{i+1}. Análise {analysis_record['depth']}** - {analysis_record['date']}")
            if st.button(f"Carregar análise {i+1}", key=f"load_analysis_{i}"):
                st.session_state['competitor_analysis'] = analysis_record['analysis']
                st.session_state['analysis_concept'] = analysis_record['concept']
                st.rerun()

# --- Seção de ajuda ---
with st.expander("❓ Como usar a análise de concorrentes"):
    st.markdown("""
    **Esta análise ajuda você a:**

    1. **Identificar oportunidades:** Encontre lacunas no mercado que seu jogo pode preencher
    2. **Evitar erros:** Aprenda com os pontos fracos dos concorrentes
    3. **Posicionar estrategicamente:** Diferencie seu jogo dos demais
    4. **Entender tendências:** Mantenha-se atualizado com o que está funcionando

    **Para análises mais precisas:**
    - Seja específico sobre o gênero e mecânicas
    - Mencione jogos similares que você conhece
    - Defina claramente seu público-alvo
    - Considere diferentes plataformas e mercados
    """)

# --- Exportar análise ---
if 'competitor_analysis' in st.session_state:
    st.markdown("---")
    st.markdown("### 📤 Exportar Análise")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Exportar como JSON"):
            import json
            analysis_data = {
                'concept': st.session_state.get('analysis_concept', ''),
                'analysis': st.session_state['competitor_analysis'],
                'date': datetime.now().isoformat()
            }
            st.download_button(
                label="⬇️ Download JSON",
                data=json.dumps(analysis_data, indent=2, ensure_ascii=False),
                file_name=f"competitor_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json"
            )

    with col2:
        if st.button("📊 Gerar Relatório"):
            st.info("Funcionalidade de relatório em desenvolvimento!")