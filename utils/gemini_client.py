"""
Módulo utilitário para operações com o cliente Gemini.
Centraliza a configuração e operações comuns da API.
"""

import os
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from typing import Optional, Dict, Any, List
import json

class GeminiClient:
    """Cliente centralizado para operações com a API Gemini."""

    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY não encontrada nas variáveis de ambiente")

        self.client = genai.Client()
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

    def generate_content(self,
                        prompt: str,
                        system_instruction: str = "",
                        response_schema: Optional[Dict] = None,
                        model: str = "gemini-2.5-flash") -> Dict[str, Any]:
        """Gera conteúdo usando o modelo Gemini."""
        config_params = {
            "model": model,
            "contents": prompt,
            "config": types.GenerateContentConfig(
                safety_settings=self.safety_settings
            )
        }

        if system_instruction:
            config_params["config"].system_instruction = system_instruction

        if response_schema:
            config_params["config"].response_mime_type = 'application/json'
            config_params["config"].response_schema = response_schema

        response = self.client.models.generate_content(**config_params)
        return json.loads(response.text) if response_schema else response.text

    def generate_image(self, prompt: str) -> Optional[Image.Image]:
        """Gera uma imagem baseada no prompt fornecido."""
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-preview-image-generation",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE']
                )
            )

            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    image = Image.open(BytesIO(part.inline_data.data))
                    return image

            return None
        except Exception as e:
            print(f"Erro ao gerar imagem: {e}")
            return None

    def analyze_competitors(self, game_concept: str) -> Dict[str, Any]:
        """Analisa concorrentes para um conceito de jogo."""
        system_instruction = """
        Você é um analista de mercado especializado em jogos. Analise o conceito fornecido e identifique:
        1. Jogos concorrentes diretos
        2. Jogos similares no mesmo gênero
        3. Pontos fortes e fracos dos concorrentes
        4. Oportunidades de diferenciação
        5. Análise de mercado e tendências

        Retorne a análise em formato JSON estruturado.
        """

        return self.generate_content(
            prompt=f"Analise os concorrentes para este conceito de jogo: {game_concept}",
            system_instruction=system_instruction,
            response_schema={
                "type": "object",
                "properties": {
                    "concorrentes_diretos": {"type": "array", "items": {"type": "string"}},
                    "jogos_similares": {"type": "array", "items": {"type": "string"}},
                    "pontos_fortes_concorrentes": {"type": "array", "items": {"type": "string"}},
                    "pontos_fracos_concorrentes": {"type": "array", "items": {"type": "string"}},
                    "oportunidades_diferencacao": {"type": "array", "items": {"type": "string"}},
                    "tendencias_mercado": {"type": "array", "items": {"type": "string"}},
                    "recomendacoes": {"type": "array", "items": {"type": "string"}}
                }
            }
        )

    def develop_core_loop(self, game_concept: str) -> Dict[str, Any]:
        """Desenvolve um core loop detalhado para o conceito de jogo."""
        system_instruction = """
        Você é um game designer especializado em core loops. Desenvolva um core loop detalhado que inclua:
        1. Ações principais do jogador
        2. Sistema de recompensas
        3. Progressão e evolução
        4. Feedback loops
        5. Mecânicas de retenção
        6. Balanceamento inicial

        Retorne o core loop em formato JSON estruturado.
        """

        return self.generate_content(
            prompt=f"Desenvolva um core loop detalhado para: {game_concept}",
            system_instruction=system_instruction,
            response_schema={
                "type": "object",
                "properties": {
                    "acoes_principais": {"type": "array", "items": {"type": "string"}},
                    "sistema_recompensas": {"type": "object", "properties": {
                        "recompensas_imediatas": {"type": "array", "items": {"type": "string"}},
                        "recompensas_longo_prazo": {"type": "array", "items": {"type": "string"}},
                        "sistema_progressao": {"type": "string"}
                    }},
                    "feedback_loops": {"type": "array", "items": {"type": "string"}},
                    "mecanicas_retencao": {"type": "array", "items": {"type": "string"}},
                    "balanceamento": {"type": "object", "properties": {
                        "dificuldade_inicial": {"type": "string"},
                        "curva_dificuldade": {"type": "string"},
                        "pontos_ajuste": {"type": "array", "items": {"type": "string"}}
                    }}
                }
            }
        )

    def create_game_flow(self, game_concept: str) -> Dict[str, Any]:
        """Cria um fluxo de jogo detalhado."""
        system_instruction = """
        Você é um game designer especializado em fluxos de jogo. Crie um fluxo detalhado que inclua:
        1. Onboarding e tutorial
        2. Progressão de níveis/fases
        3. Momentos de decisão
        4. Pontos de checkpoint
        5. Fluxo de monetização (se aplicável)
        6. Experiência do usuário

        Retorne o fluxo em formato JSON estruturado.
        """

        return self.generate_content(
            prompt=f"Crie um fluxo de jogo detalhado para: {game_concept}",
            system_instruction=system_instruction,
            response_schema={
                "type": "object",
                "properties": {
                    "onboarding": {"type": "object", "properties": {
                        "tutorial": {"type": "string"},
                        "primeiros_passos": {"type": "array", "items": {"type": "string"}},
                        "objetivos_iniciais": {"type": "array", "items": {"type": "string"}}
                    }},
                    "progressao": {"type": "object", "properties": {
                        "estrutura_niveis": {"type": "string"},
                        "desbloqueios": {"type": "array", "items": {"type": "string"}},
                        "momentos_chave": {"type": "array", "items": {"type": "string"}}
                    }},
                    "decisoes_jogador": {"type": "array", "items": {"type": "string"}},
                    "checkpoints": {"type": "array", "items": {"type": "string"}},
                    "fluxo_monetizacao": {"type": "array", "items": {"type": "string"}},
                    "experiencia_usuario": {"type": "object", "properties": {
                        "pontos_alto": {"type": "array", "items": {"type": "string"}},
                        "pontos_baixo": {"type": "array", "items": {"type": "string"}},
                        "otimizacoes": {"type": "array", "items": {"type": "string"}}
                    }}
                }
            }
        )