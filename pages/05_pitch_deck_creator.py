"""
Página para criação de Pitch Deck de 10 slides
Gera apresentações profissionais para investidores, publishers e parceiros
"""

import streamlit as st
import json
from typing import Dict, Any
from utils import GeminiClient, PitchDeck, Slide, AnaliseMercado, ModeloNegocio, RoadmapDesenvolvimento, render_sidebar, generate_pitch_deck_pdf

# Configuração da página
st.set_page_config(
    page_title="Pitch Deck Creator - Game Concept Forge",
    page_icon="📊",
    layout="wide"
)

# Renderizar sidebar
render_sidebar()

def generate_pitch_deck_system_prompt() -> str:
    """Gera o prompt do sistema para criação de pitch deck."""
    return """
    Você é um especialista em criação de pitch decks para jogos, com vasta experiência em apresentações para investidores, publishers e parceiros da indústria de games.

    Sua tarefa é criar um pitch deck profissional de 10 slides para um conceito de jogo, seguindo as melhores práticas da indústria.

    ESTRUTURA DO PITCH DECK (10 SLIDES):

    1. **SLIDE TÍTULO** - Nome do jogo, tagline, equipe
    2. **PROBLEMA/OPORTUNIDADE** - Gap no mercado, necessidade não atendida
    3. **SOLUÇÃO/CONCEITO** - Como o jogo resolve o problema
    4. **ANÁLISE DE MERCADO** - Tamanho, crescimento, segmentos
    5. **MODELO DE NEGÓCIO** - Monetização, receitas, custos
    6. **DIFERENCIAÇÃO** - Vantagens competitivas, USPs
    7. **ROADMAP** - Fases de desenvolvimento, cronograma
    8. **EQUIPE/RECURSOS** - Experiência, capacidades
    9. **PROJEÇÕES FINANCEIRAS** - Receitas, ROI, break-even
    10. **CALL TO ACTION** - Próximos passos, investimento necessário

    DIRETRIZES:
    - Cada slide deve ser conciso e impactante
    - Use dados e métricas quando possível
    - Foque em benefícios e oportunidades
    - Seja específico sobre números e prazos
    - Mantenha tom profissional mas acessível
    - Inclua elementos visuais sugeridos para cada slide

    FORMATO DE RESPOSTA:
    Retorne apenas um JSON válido seguindo a estrutura PitchDeck definida, sem texto adicional.
    """

def generate_pitch_deck(gemini_client, concept_data: Dict[str, Any]) -> PitchDeck:
    """Gera um pitch deck completo usando o Gemini."""

    system_prompt = generate_pitch_deck_system_prompt()

    user_prompt = f"""
    Crie um pitch deck profissional de 10 slides para o seguinte conceito de jogo:

    TÍTULO: {concept_data.get('titulo_provisorio', 'Jogo sem título')}
    GÊNERO: {concept_data.get('genero', 'Não especificado')}
    PLATAFORMAS: {', '.join(concept_data.get('plataformas_alvo', []))}
    PÚBLICO-ALVO: {', '.join(concept_data.get('publico_alvo', []))}
    PREMISSA: {concept_data.get('premissa_conceito_central', 'Não especificada')}
    CORE LOOP: {concept_data.get('core_loop', {})}
    MECÂNICAS: {concept_data.get('mecanicas_principais', [])}
    MONETIZAÇÃO: {concept_data.get('monetizacao_opcional', [])}
    USPs: {concept_data.get('pontos_de_venda_unicos_usps', [])}

    Crie um pitch deck que seja convincente para investidores, publishers e parceiros, destacando:
    - Oportunidade de mercado clara
    - Diferenciação competitiva
    - Modelo de negócio viável
    - Roadmap realista
    - Potencial de retorno

    Retorne apenas o JSON do pitch deck, sem texto adicional.
    """

    try:
        response = gemini_client.generate_content(
            prompt=user_prompt,
            system_instruction=system_prompt,
            response_schema={
                "type": "object",
                "properties": {
                    "slide_titulo": {
                        "type": "object",
                        "properties": {
                            "titulo": {"type": "string"},
                            "conteudo": {"type": "string"},
                            "pontos_chave": {"type": "array", "items": {"type": "string"}},
                            "visual_sugerido": {"type": "string"}
                        }
                    },
                    "slide_problema": {
                        "type": "object",
                        "properties": {
                            "titulo": {"type": "string"},
                            "conteudo": {"type": "string"},
                            "pontos_chave": {"type": "array", "items": {"type": "string"}},
                            "visual_sugerido": {"type": "string"}
                        }
                    },
                    "slide_solucao": {
                        "type": "object",
                        "properties": {
                            "titulo": {"type": "string"},
                            "conteudo": {"type": "string"},
                            "pontos_chave": {"type": "array", "items": {"type": "string"}},
                            "visual_sugerido": {"type": "string"}
                        }
                    },
                    "slide_mercado": {
                        "type": "object",
                        "properties": {
                            "tamanho_mercado": {"type": "string"},
                            "crescimento_mercado": {"type": "string"},
                            "segmentos_alvo": {"type": "array", "items": {"type": "string"}},
                            "tendencias": {"type": "array", "items": {"type": "string"}},
                            "oportunidades": {"type": "array", "items": {"type": "string"}}
                        }
                    },
                    "slide_modelo_negocio": {
                        "type": "object",
                        "properties": {
                            "estrategia_monetizacao": {"type": "array", "items": {"type": "string"}},
                            "fontes_receita": {"type": "array", "items": {"type": "string"}},
                            "custos_estimados": {"type": "array", "items": {"type": "string"}},
                            "projecao_receita": {"type": "string"},
                            "break_even": {"type": "string"}
                        }
                    },
                    "slide_diferencacao": {
                        "type": "object",
                        "properties": {
                            "titulo": {"type": "string"},
                            "conteudo": {"type": "string"},
                            "pontos_chave": {"type": "array", "items": {"type": "string"}},
                            "visual_sugerido": {"type": "string"}
                        }
                    },
                    "slide_roadmap": {
                        "type": "object",
                        "properties": {
                            "fases": {"type": "array", "items": {"type": "string"}},
                            "cronograma": {"type": "string"},
                            "marcos_principais": {"type": "array", "items": {"type": "string"}},
                            "recursos_necessarios": {"type": "array", "items": {"type": "string"}},
                            "riscos": {"type": "array", "items": {"type": "string"}}
                        }
                    },
                    "slide_equipe": {
                        "type": "object",
                        "properties": {
                            "titulo": {"type": "string"},
                            "conteudo": {"type": "string"},
                            "pontos_chave": {"type": "array", "items": {"type": "string"}},
                            "visual_sugerido": {"type": "string"}
                        }
                    },
                    "slide_financeiro": {
                        "type": "object",
                        "properties": {
                            "titulo": {"type": "string"},
                            "conteudo": {"type": "string"},
                            "pontos_chave": {"type": "array", "items": {"type": "string"}},
                            "visual_sugerido": {"type": "string"}
                        }
                    },
                    "slide_call_action": {
                        "type": "object",
                        "properties": {
                            "titulo": {"type": "string"},
                            "conteudo": {"type": "string"},
                            "pontos_chave": {"type": "array", "items": {"type": "string"}},
                            "visual_sugerido": {"type": "string"}
                        }
                    },
                    "publico_alvo_pitch": {"type": "string"},
                    "duracao_apresentacao": {"type": "string"},
                    "dicas_apresentacao": {"type": "array", "items": {"type": "string"}}
                }
            }
        )
        return response
    except Exception as e:
        st.error(f"Erro ao gerar pitch deck: {str(e)}")
        return None

def display_slide(slide: Slide, slide_number: int, slide_title: str):
    """Exibe um slide individual do pitch deck."""

    with st.expander(f"📊 Slide {slide_number}: {slide_title}", expanded=True):
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"### {slide['titulo']}")
            st.markdown(slide['conteudo'])

            if slide['pontos_chave']:
                st.markdown("**Pontos-chave:**")
                for ponto in slide['pontos_chave']:
                    st.markdown(f"• {ponto}")

        with col2:
            st.markdown("**🎨 Visual Sugerido:**")
            st.info(slide['visual_sugerido'])

def display_market_analysis(analise: AnaliseMercado):
    """Exibe a análise de mercado (Slide 4)."""

    with st.expander("📊 Slide 4: Análise de Mercado", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📈 Dados de Mercado")
            st.metric("Tamanho do Mercado", analise['tamanho_mercado'])
            st.metric("Crescimento", analise['crescimento_mercado'])

            st.markdown("**Segmentos Alvo:**")
            for segmento in analise['segmentos_alvo']:
                st.markdown(f"• {segmento}")

        with col2:
            st.markdown("**📊 Tendências:**")
            for tendencia in analise['tendencias']:
                st.markdown(f"• {tendencia}")

            st.markdown("**🎯 Oportunidades:**")
            for oportunidade in analise['oportunidades']:
                st.markdown(f"• {oportunidade}")

def display_business_model(modelo: ModeloNegocio):
    """Exibe o modelo de negócio (Slide 5)."""

    with st.expander("📊 Slide 5: Modelo de Negócio", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 💰 Estratégia de Monetização")
            for estrategia in modelo['estrategia_monetizacao']:
                st.markdown(f"• {estrategia}")

            st.markdown("**📈 Fontes de Receita:**")
            for fonte in modelo['fontes_receita']:
                st.markdown(f"• {fonte}")

        with col2:
            st.markdown("**💵 Custos Estimados:**")
            for custo in modelo['custos_estimados']:
                st.markdown(f"• {custo}")

            st.markdown("**📊 Projeções:**")
            st.info(f"Projeção de Receita: {modelo['projecao_receita']}")
            st.success(f"Break-even: {modelo['break_even']}")

def display_roadmap(roadmap: RoadmapDesenvolvimento):
    """Exibe o roadmap de desenvolvimento (Slide 7)."""

    with st.expander("📊 Slide 7: Roadmap de Desenvolvimento", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🗓️ Fases de Desenvolvimento")
            for i, fase in enumerate(roadmap['fases'], 1):
                st.markdown(f"**Fase {i}:** {fase}")

            st.markdown(f"**⏱️ Cronograma:** {roadmap['cronograma']}")

        with col2:
            st.markdown("**🎯 Marcos Principais:**")
            for marco in roadmap['marcos_principais']:
                st.markdown(f"• {marco}")

            st.markdown("**⚠️ Riscos Identificados:**")
            for risco in roadmap['riscos']:
                st.markdown(f"• {risco}")

def display_pitch_deck(pitch_deck: PitchDeck):
    """Exibe o pitch deck completo."""

    st.markdown("## 📊 Pitch Deck Gerado")
    st.markdown("---")

    # Slide 1: Título
    display_slide(pitch_deck['slide_titulo'], 1, "Título e Apresentação")

    # Slide 2: Problema
    display_slide(pitch_deck['slide_problema'], 2, "Problema/Oportunidade")

    # Slide 3: Solução
    display_slide(pitch_deck['slide_solucao'], 3, "Solução/Conceito do Jogo")

    # Slide 4: Análise de Mercado
    display_market_analysis(pitch_deck['slide_mercado'])

    # Slide 5: Modelo de Negócio
    display_business_model(pitch_deck['slide_modelo_negocio'])

    # Slide 6: Diferenciação
    display_slide(pitch_deck['slide_diferencacao'], 6, "Diferenciação/Competição")

    # Slide 7: Roadmap
    display_roadmap(pitch_deck['slide_roadmap'])

    # Slide 8: Equipe
    display_slide(pitch_deck['slide_equipe'], 8, "Equipe/Recursos")

    # Slide 9: Financeiro
    display_slide(pitch_deck['slide_financeiro'], 9, "Projeções Financeiras")

    # Slide 10: Call to Action
    display_slide(pitch_deck['slide_call_action'], 10, "Call to Action")

    # Informações adicionais
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**🎯 Público-alvo do Pitch:**")
        st.info(pitch_deck['publico_alvo_pitch'])

    with col2:
        st.markdown("**⏱️ Duração da Apresentação:**")
        st.info(pitch_deck['duracao_apresentacao'])

    with col3:
        st.markdown("**💡 Dicas de Apresentação:**")
        for dica in pitch_deck['dicas_apresentacao']:
            st.markdown(f"• {dica}")

def main():
    """Função principal da página."""

    st.title("📊 Pitch Deck Creator")
    st.markdown("Crie apresentações profissionais de 10 slides para investidores, publishers e parceiros")

    # Verificar se há conceito disponível
    if 'current_gdd' not in st.session_state or not st.session_state.current_gdd:
        st.warning("⚠️ Nenhum conceito de jogo encontrado. Gere um conceito primeiro na página 'Concept Generator'.")
        st.markdown("[Ir para Concept Generator](/concept_generator)")
        return

    concept_data = st.session_state.current_gdd

    # Verificar se concept_data é um dicionário
    if not isinstance(concept_data, dict):
        st.error("❌ Erro: Dados do conceito em formato inválido. Gere um novo conceito na página 'Concept Generator'.")
        st.markdown("[Ir para Concept Generator](/concept_generator)")
        return

    # Exibir informações do conceito atual
    with st.container():
        st.markdown("### 🎮 Conceito Atual")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Título:** {concept_data.get('titulo_provisorio', 'Sem título')}")
            st.markdown(f"**Gênero:** {concept_data.get('genero', 'Não especificado')}")
            st.markdown(f"**Plataformas:** {', '.join(concept_data.get('plataformas_alvo', []))}")

        with col2:
            st.markdown(f"**Público-alvo:** {', '.join(concept_data.get('publico_alvo', []))}")
            st.markdown(f"**Premissa:** {concept_data.get('premissa_conceito_central', 'Não especificada')}")

    st.markdown("---")

    # Configurações do pitch deck
    st.markdown("### ⚙️ Configurações do Pitch Deck")

    col1, col2 = st.columns(2)

    with col1:
        publico_alvo = st.selectbox(
            "Público-alvo do pitch:",
            ["Investidores", "Publishers", "Parceiros", "Todos os públicos"],
            help="Selecione o público principal para o qual o pitch será direcionado"
        )

        duracao = st.selectbox(
            "Duração da apresentação:",
            ["5 minutos", "10 minutos", "15 minutos", "20 minutos"],
            help="Duração estimada da apresentação"
        )

    with col2:
        foco_principal = st.selectbox(
            "Foco principal:",
            ["Oportunidade de mercado", "Inovação tecnológica", "Retorno financeiro", "Crescimento de usuários"],
            help="Aspecto principal que deve ser destacado no pitch"
        )

        nivel_detalhe = st.selectbox(
            "Nível de detalhe:",
            ["Alto nível", "Médio", "Detalhado"],
            help="Nível de detalhamento das informações"
        )

    # Botão para gerar pitch deck
    if st.button("🚀 Gerar Pitch Deck", type="primary", use_container_width=True):
        with st.spinner("Gerando pitch deck profissional..."):

            # Obter cliente Gemini
            try:
                gemini_client = GeminiClient()
            except ValueError as e:
                st.error(f"❌ Erro ao conectar com a API do Gemini: {str(e)}")
                return

            # Adicionar configurações ao conceito
            concept_data['publico_alvo_pitch'] = publico_alvo
            concept_data['duracao_apresentacao'] = duracao
            concept_data['foco_principal'] = foco_principal
            concept_data['nivel_detalhe'] = nivel_detalhe

            # Gerar pitch deck
            pitch_deck = generate_pitch_deck(gemini_client, concept_data)

            if pitch_deck:
                # Salvar no histórico
                if 'pitch_deck_history' not in st.session_state:
                    st.session_state.pitch_deck_history = []

                pitch_deck_entry = {
                    'concept_title': concept_data.get('titulo_provisorio', 'Sem título'),
                    'publico_alvo': publico_alvo,
                    'duracao': duracao,
                    'foco': foco_principal,
                    'pitch_deck': pitch_deck
                }

                st.session_state.pitch_deck_history.append(pitch_deck_entry)
                st.session_state.current_pitch_deck = pitch_deck

                st.success("✅ Pitch deck gerado com sucesso!")

                # Exibir o pitch deck
                display_pitch_deck(pitch_deck)

                # Botões de ação
                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("📋 Copiar JSON", use_container_width=True):
                        st.write("```json")
                        st.json(pitch_deck)
                        st.write("```")

                with col2:
                    # Gerar PDF
                    pdf_buffer = generate_pitch_deck_pdf(pitch_deck)
                    st.download_button(
                        label="📄 Download PDF",
                        data=pdf_buffer.getvalue(),
                        file_name=f"pitch_deck_{concept_data.get('titulo_provisorio', 'jogo').replace(' ', '_').lower()}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                with col3:
                    if st.button("🔄 Gerar Novo", use_container_width=True):
                        st.rerun()

    # Exibir pitch deck atual se existir
    elif 'current_pitch_deck' in st.session_state:
        st.markdown("### 📊 Pitch Deck Atual")
        display_pitch_deck(st.session_state.current_pitch_deck)

        # Botão de download para pitch deck existente
        col1, col2 = st.columns(2)

        with col1:
            # Gerar PDF do pitch deck atual
            pdf_buffer = generate_pitch_deck_pdf(st.session_state.current_pitch_deck)
            st.download_button(
                label="📄 Download PDF",
                data=pdf_buffer.getvalue(),
                file_name=f"pitch_deck_{concept_data.get('titulo_provisorio', 'jogo').replace(' ', '_').lower()}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        with col2:
            if st.button("📋 Copiar JSON", use_container_width=True):
                st.write("```json")
                st.json(st.session_state.current_pitch_deck)
                st.write("```")

    # Histórico de pitch decks
    if 'pitch_deck_history' in st.session_state and st.session_state.pitch_deck_history:
        st.markdown("---")
        st.markdown("### 📚 Histórico de Pitch Decks")

        for i, entry in enumerate(st.session_state.pitch_deck_history[-3:], 1):
            with st.expander(f"Pitch Deck {i}: {entry['concept_title']} - {entry['publico_alvo']}"):
                st.markdown(f"**Duração:** {entry['duracao']}")
                st.markdown(f"**Foco:** {entry['foco']}")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"Carregar Pitch Deck {i}", key=f"load_pitch_{i}"):
                        st.session_state.current_pitch_deck = entry['pitch_deck']
                        st.rerun()

                with col2:
                    # Download PDF do histórico
                    pdf_buffer = generate_pitch_deck_pdf(entry['pitch_deck'])
                    st.download_button(
                        label=f"📄 Download PDF {i}",
                        data=pdf_buffer.getvalue(),
                        file_name=f"pitch_deck_{entry['concept_title'].replace(' ', '_').lower()}_{entry['publico_alvo'].lower()}.pdf",
                        mime="application/pdf",
                        key=f"download_pdf_{i}"
                    )

if __name__ == "__main__":
    main()