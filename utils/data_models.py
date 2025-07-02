"""
Módulo com as estruturas de dados (TypedDict) para o Game Concept Forge.
Centraliza todas as definições de tipos usadas na aplicação.
"""

import typing_extensions as typing
from typing import List, Dict, Any

# --- Estruturas básicas ---
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

# --- Estrutura principal do One-Page GDD ---
class OnePageGDD(typing.TypedDict):
    """Define a estrutura completa para o One-Page GDD."""
    titulo_provisorio: str
    genero: str
    plataformas_alvo: List[str]
    premissa_conceito_central: str
    publico_alvo: List[str]
    core_loop: CoreLoop
    mecanicas_principais: List[Mecanica]
    monetizacao_opcional: List[Monetizacao]
    pontos_de_venda_unicos_usps: List[str]

# --- Estruturas para análise de concorrentes ---
class AnaliseConcorrentes(typing.TypedDict):
    """Define a estrutura da análise de concorrentes."""
    concorrentes_diretos: List[str]
    jogos_similares: List[str]
    pontos_fortes_concorrentes: List[str]
    pontos_fracos_concorrentes: List[str]
    oportunidades_diferencacao: List[str]
    tendencias_mercado: List[str]
    recomendacoes: List[str]

# --- Estruturas para core loop detalhado ---
class SistemaRecompensas(typing.TypedDict):
    """Define a estrutura do sistema de recompensas."""
    recompensas_imediatas: List[str]
    recompensas_longo_prazo: List[str]
    sistema_progressao: str

class Balanceamento(typing.TypedDict):
    """Define a estrutura do balanceamento do jogo."""
    dificuldade_inicial: str
    curva_dificuldade: str
    pontos_ajuste: List[str]

class CoreLoopDetalhado(typing.TypedDict):
    """Define a estrutura do core loop detalhado."""
    acoes_principais: List[str]
    sistema_recompensas: SistemaRecompensas
    feedback_loops: List[str]
    mecanicas_retencao: List[str]
    balanceamento: Balanceamento

# --- Estruturas para fluxo de jogo ---
class Onboarding(typing.TypedDict):
    """Define a estrutura do onboarding."""
    tutorial: str
    primeiros_passos: List[str]
    objetivos_iniciais: List[str]

class Progressao(typing.TypedDict):
    """Define a estrutura da progressão."""
    estrutura_niveis: str
    desbloqueios: List[str]
    momentos_chave: List[str]

class ExperienciaUsuario(typing.TypedDict):
    """Define a estrutura da experiência do usuário."""
    pontos_alto: List[str]
    pontos_baixo: List[str]
    otimizacoes: List[str]

class FluxoJogo(typing.TypedDict):
    """Define a estrutura do fluxo de jogo."""
    onboarding: Onboarding
    progressao: Progressao
    decisoes_jogador: List[str]
    checkpoints: List[str]
    fluxo_monetizacao: List[str]
    experiencia_usuario: ExperienciaUsuario

# --- Estruturas para Pitch Deck ---
class Slide(typing.TypedDict):
    """Define a estrutura de um slide do pitch deck."""
    titulo: str
    conteudo: str
    pontos_chave: List[str]
    visual_sugerido: str

class AnaliseMercado(typing.TypedDict):
    """Define a estrutura da análise de mercado para o pitch."""
    tamanho_mercado: str
    crescimento_mercado: str
    segmentos_alvo: List[str]
    tendencias: List[str]
    oportunidades: List[str]

class ModeloNegocio(typing.TypedDict):
    """Define a estrutura do modelo de negócio."""
    estrategia_monetizacao: List[str]
    fontes_receita: List[str]
    custos_estimados: List[str]
    projecao_receita: str
    break_even: str

class RoadmapDesenvolvimento(typing.TypedDict):
    """Define a estrutura do roadmap de desenvolvimento."""
    fases: List[str]
    cronograma: str
    marcos_principais: List[str]
    recursos_necessarios: List[str]
    riscos: List[str]

class PitchDeck(typing.TypedDict):
    """Define a estrutura completa do pitch deck de 10 slides."""
    # Slide 1: Título e Apresentação
    slide_titulo: Slide

    # Slide 2: Problema/Oportunidade
    slide_problema: Slide

    # Slide 3: Solução/Conceito do Jogo
    slide_solucao: Slide

    # Slide 4: Análise de Mercado
    slide_mercado: AnaliseMercado

    # Slide 5: Modelo de Negócio
    slide_modelo_negocio: ModeloNegocio

    # Slide 6: Diferenciação/Competição
    slide_diferencacao: Slide

    # Slide 7: Roadmap de Desenvolvimento
    slide_roadmap: RoadmapDesenvolvimento

    # Slide 8: Equipe/Recursos
    slide_equipe: Slide

    # Slide 9: Projeções Financeiras
    slide_financeiro: Slide

    # Slide 10: Call to Action
    slide_call_action: Slide

    # Informações adicionais
    publico_alvo_pitch: str
    duracao_apresentacao: str
    dicas_apresentacao: List[str]

# --- Estruturas para GDD de 10 páginas ---
class Personagem(typing.TypedDict):
    """Define a estrutura de um personagem."""
    nome: str
    descricao: str
    papel_jogo: str
    habilidades: List[str]
    desenvolvimento: str

class Ambiente(typing.TypedDict):
    """Define a estrutura de um ambiente."""
    nome: str
    descricao: str
    atmosfera: str
    elementos_interativos: List[str]
    importancia_narrativa: str

class Narrativa(typing.TypedDict):
    """Define a estrutura da narrativa."""
    sinopse: str
    personagens_principais: List[Personagem]
    ambientacao: List[Ambiente]
    arcos_narrativos: List[str]
    elementos_historia: List[str]

class Tecnica(typing.TypedDict):
    """Define a estrutura técnica."""
    engine: str
    plataformas: List[str]
    requisitos_minimos: Dict[str, str]
    requisitos_recomendados: Dict[str, str]
    tecnologias_especiais: List[str]

class GDDCompleto(typing.TypedDict):
    """Define a estrutura do GDD completo de 10 páginas."""
    # Página 1: Visão Geral
    titulo: str
    genero: str
    plataformas: List[str]
    publico_alvo: List[str]
    premissa: str
    sinopse: str

    # Página 2: Core Loop e Mecânicas
    core_loop_detalhado: CoreLoopDetalhado
    mecanicas_principais: List[Mecanica]
    mecanicas_secundarias: List[Mecanica]

    # Página 3: Narrativa
    narrativa: Narrativa

    # Página 4: Fluxo de Jogo
    fluxo_jogo: FluxoJogo

    # Página 5: Personagens e Ambientes
    personagens: List[Personagem]
    ambientes: List[Ambiente]

    # Página 6: Interface e UX
    interface_usuario: Dict[str, str]
    elementos_ui: List[str]
    feedback_visual: List[str]

    # Página 7: Áudio
    musica: Dict[str, str]
    efeitos_sonoros: List[str]
    dublagem: Dict[str, str]

    # Página 8: Monetização
    estrategia_monetizacao: List[Monetizacao]
    analise_mercado: AnaliseConcorrentes

    # Página 9: Aspectos Técnicos
    aspectos_tecnicos: Tecnica
    cronograma_desenvolvimento: Dict[str, str]

    # Página 10: Riscos e Mitigações
    riscos_identificados: List[str]
    estrategias_mitigacao: List[str]
    metricas_sucesso: List[str]