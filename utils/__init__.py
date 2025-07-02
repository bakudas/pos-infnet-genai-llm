"""
Pacote utilitário para o Game Concept Forge.
Contém módulos para cliente Gemini, estruturas de dados, sidebar e funções auxiliares.
"""

from .gemini_client import GeminiClient
from .data_models import *
from .sidebar import render_sidebar, clear_session_data, add_to_concept_history, get_session_summary
from .pdf_generator import generate_pitch_deck_pdf

__all__ = [
    'GeminiClient',
    'CoreLoop',
    'Mecanica',
    'Monetizacao',
    'OnePageGDD',
    'AnaliseConcorrentes',
    'CoreLoopDetalhado',
    'FluxoJogo',
    'PitchDeck',
    'Slide',
    'AnaliseMercado',
    'ModeloNegocio',
    'RoadmapDesenvolvimento',
    'GDDCompleto',
    'render_sidebar',
    'clear_session_data',
    'add_to_concept_history',
    'get_session_summary',
    'generate_pitch_deck_pdf'
]