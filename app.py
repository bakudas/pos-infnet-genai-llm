"""
Game Concept Forge - Página Principal
Aplicação multipáginas para desenvolvimento de conceitos de jogos com IA.
"""

import streamlit as st
import sys
import os

# Adiciona o diretório raiz ao path para importar os módulos utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import render_sidebar

# --- Configuração da página ---
st.set_page_config(
    layout="wide",
    page_title="Game Concept Forge",
    page_icon="🎮",
    initial_sidebar_state="expanded"
)

# --- Verificação da chave de API ---
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    st.error('⚠️ **GEMINI_API_KEY não encontrada!**')
    st.markdown("""
    Para usar o Game Concept Forge, você precisa configurar sua chave de API do Gemini:

    1. **Obtenha sua chave gratuita:** Acesse [Google AI Studio](https://aistudio.google.com/app/apikey)
    2. **Configure a variável de ambiente:**
       ```bash
       export GEMINI_API_KEY="sua-chave-aqui"
       ```
    3. **Reinicie o aplicativo**
    """)
    st.stop()

# --- Renderiza a sidebar ---
render_sidebar()

# --- Cabeçalho principal ---
st.title("🎮 Game Concept Forge")
st.markdown("""
    **Sua ferramenta completa de desenvolvimento de conceitos de jogos com IA**

    Transforme ideias em jogos viáveis usando inteligência artificial especializada em game design.
""")

# --- Seção de funcionalidades ---
st.markdown("---")
st.subheader("🚀 Funcionalidades Disponíveis")

# Grid de funcionalidades
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📝 **Concept Generator**
    - Gera conceitos de jogos a partir de ideias iniciais
    - Cria One-Page GDD estruturado
    - Sugere arte conceitual
    - Define core loop, mecânicas e monetização

    **[Acessar →](/concept_generator)**
    """)

    st.markdown("""
    ### 🔍 **Competitor Analysis**
    - Analisa concorrentes diretos e similares
    - Identifica oportunidades de diferenciação
    - Examina tendências de mercado
    - Fornece recomendações estratégicas

    **[Acessar →](/competitor_analysis)**
    """)

with col2:
    st.markdown("""
    ### 🔄 **Core Loop Developer**
    - Desenvolve core loops detalhados
    - Cria sistemas de recompensas
    - Define feedback loops
    - Balanceia mecânicas de retenção

    **[Acessar →](/core_loop_developer)**
    """)

    st.markdown("""
    ### 🎯 **Game Flow Creator**
    - Cria fluxos de jogo completos
    - Define onboarding e tutorial
    - Mapeia progressão de níveis
    - Otimiza experiência do usuário

    **[Acessar →](/game_flow_creator)**
    """)

    st.markdown("""
    ### 📊 **Pitch Deck Creator**
    - Gera apresentações de 10 slides
    - Foca em investidores e publishers
    - Inclui análise de mercado e finanças
    - Cria call-to-action profissional

    **[Acessar →](/pitch_deck_creator)**
    """)

# --- Seção de próximas funcionalidades ---
st.markdown("---")
st.subheader("🔮 Funcionalidades em Desenvolvimento")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📄 **GDD de 10 Páginas**
    - Documento completo de game design
    - Narrativa e personagens
    - Aspectos técnicos
    - Cronograma de desenvolvimento
    """)

with col2:
    st.markdown("""
    ### 🎨 **Art Concept Generator**
    - Gera conceitos visuais
    - Cria mood boards
    - Define paleta de cores
    - Sugere estilos artísticos
    """)

with col3:
    st.markdown("""
    ### 📈 **Market Validation**
    - Análise de viabilidade
    - Estimativas de receita
    - Análise de riscos
    - Métricas de sucesso
    """)

# --- Seção de uso rápido ---
st.markdown("---")
st.subheader("⚡ Uso Rápido")

st.markdown("""
**Para começar rapidamente:**

1. **Gere um conceito** na página Concept Generator
2. **Analise concorrentes** para identificar oportunidades
3. **Desenvolva o core loop** para criar engajamento
4. **Crie o fluxo de jogo** para otimizar a experiência
5. **Crie um pitch deck** para apresentar a investidores

**Dica:** As páginas compartilham dados automaticamente. Gere um conceito primeiro e use-o nas outras ferramentas!
""")

# --- Seção de exemplos ---
st.markdown("---")
st.subheader("💡 Exemplos de Conceitos")

with st.expander("🎴 Jogo de Cartas Históricas"):
    st.markdown("""
    **Conceito:** Um jogo de cartas onde os jogadores constroem baralhos baseados em personagens históricos do Rio de Janeiro.

    **Gênero:** Card Game / Strategy
    **Plataforma:** Mobile / PC
    **Público-alvo:** Jogadores casuais de 25-40 anos

    **Core Loop:** Coletar cartas → Construir deck → Batalhar → Desbloquear novos personagens
    """)

with st.expander("🏙️ City Builder Medieval"):
    st.markdown("""
    **Conceito:** Um jogo de construção de cidades medievais com foco em diplomacia e comércio.

    **Gênero:** Strategy / Simulation
    **Plataforma:** PC / Mobile
    **Público-alvo:** Jogadores de estratégia de 30-50 anos

    **Core Loop:** Construir → Gerenciar recursos → Negociar → Expandir território
    """)

# --- Seção de ajuda ---
st.markdown("---")
st.subheader("❓ Como Obter Melhores Resultados")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **💡 Dicas para conceitos:**
    - Seja específico sobre gênero e mecânicas
    - Mencione inspirações e jogos similares
    - Defina claramente o público-alvo
    - Pense na experiência do jogador
    """)

with col2:
    st.markdown("""
    **🎯 Dicas para análise:**
    - Considere diferentes plataformas
    - Analise tendências de mercado
    - Identifique lacunas de oportunidade
    - Foque na diferenciação
    """)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🎮 <strong>Game Concept Forge</strong> - Desenvolvido para fins educacionais</p>
    <p>Disciplina de IA Generativa para Linguagem (Large Language Model) [25E2_3]</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar com informações da sessão ---
with st.sidebar:
    st.title("📋 Sessão Atual")

    if 'current_gdd' in st.session_state:
        st.success("✅ Conceito carregado")
        gdd = st.session_state['current_gdd']
        st.markdown(f"**Título:** {gdd.get('titulo_provisorio', 'Sem título')}")
        st.markdown(f"**Gênero:** {gdd.get('genero', 'N/A')}")

        if st.button("🔄 Limpar Sessão"):
            for key in ['current_gdd', 'current_concept', 'competitor_analysis', 'core_loop_detailed']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    else:
        st.info("ℹ️ Nenhum conceito carregado")
        st.markdown("Gere um conceito na página Concept Generator para começar!")

    st.markdown("---")
    st.markdown("**🔧 Configuração:**")
    st.markdown(f"API Status: {'✅ Conectado' if GEMINI_API_KEY else '❌ Não configurado'}")

    st.markdown("---")
    st.markdown("**📚 Histórico:**")
    if 'concept_history' in st.session_state and st.session_state.concept_history:
        for i, concept in enumerate(st.session_state.concept_history[-3:], 1):
            st.markdown(f"{i}. {concept['title']}")
    else:
        st.markdown("Nenhum histórico disponível")