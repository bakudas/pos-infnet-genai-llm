"""
Módulo para geração de PDFs do pitch deck.
Cria apresentações profissionais em PDF com os 10 slides.
"""

import os
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from typing import Dict, Any, List
from utils.data_models import PitchDeck


class PitchDeckPDFGenerator:
    """Gerador de PDF para pitch decks de jogos."""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Configura estilos personalizados para o PDF."""

        # Título principal
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )

        # Subtítulo
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )

        # Título de slide
        self.slide_title_style = ParagraphStyle(
            'SlideTitle',
            parent=self.styles['Heading2'],
            fontSize=20,
            spaceAfter=15,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )

        # Conteúdo normal
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        )

        # Lista
        self.bullet_style = ParagraphStyle(
            'CustomBullet',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            leftIndent=20,
            fontName='Helvetica'
        )

        # Destaque
        self.highlight_style = ParagraphStyle(
            'CustomHighlight',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            alignment=TA_CENTER,
            textColor=colors.darkgreen,
            fontName='Helvetica-Bold'
        )

    def _create_slide_title(self, title: str) -> Paragraph:
        """Cria o título de um slide."""
        return Paragraph(f"<b>{title}</b>", self.slide_title_style)

    def _create_bullet_list(self, items: List[str]) -> List[Paragraph]:
        """Cria uma lista com bullets."""
        bullet_items = []
        for item in items:
            bullet_items.append(Paragraph(f"• {item}", self.bullet_style))
        return bullet_items

    def _create_metric_table(self, title: str, value: str) -> Table:
        """Cria uma tabela para métricas."""
        data = [[title, value]]
        table = Table(data, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        return table

    def generate_pitch_deck_pdf(self, pitch_deck: PitchDeck, filename: str = "pitch_deck.pdf") -> BytesIO:
        """Gera o PDF completo do pitch deck."""

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=72)

        story = []

        # Slide 1: Título
        story.append(self._create_slide_title("SLIDE 1: TÍTULO E APRESENTAÇÃO"))
        story.append(Paragraph(pitch_deck['slide_titulo']['titulo'], self.title_style))
        story.append(Spacer(1, 20))
        story.append(Paragraph(pitch_deck['slide_titulo']['conteudo'], self.normal_style))
        story.append(Spacer(1, 15))

        if pitch_deck['slide_titulo']['pontos_chave']:
            story.append(Paragraph("<b>Pontos-chave:</b>", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_titulo']['pontos_chave']))

        story.append(PageBreak())

        # Slide 2: Problema/Oportunidade
        story.append(self._create_slide_title("SLIDE 2: PROBLEMA/OPORTUNIDADE"))
        story.append(Paragraph(pitch_deck['slide_problema']['titulo'], self.subtitle_style))
        story.append(Spacer(1, 15))
        story.append(Paragraph(pitch_deck['slide_problema']['conteudo'], self.normal_style))
        story.append(Spacer(1, 15))

        if pitch_deck['slide_problema']['pontos_chave']:
            story.append(Paragraph("<b>Pontos-chave:</b>", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_problema']['pontos_chave']))

        story.append(PageBreak())

        # Slide 3: Solução/Conceito
        story.append(self._create_slide_title("SLIDE 3: SOLUÇÃO/CONCEITO DO JOGO"))
        story.append(Paragraph(pitch_deck['slide_solucao']['titulo'], self.subtitle_style))
        story.append(Spacer(1, 15))
        story.append(Paragraph(pitch_deck['slide_solucao']['conteudo'], self.normal_style))
        story.append(Spacer(1, 15))

        if pitch_deck['slide_solucao']['pontos_chave']:
            story.append(Paragraph("<b>Pontos-chave:</b>", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_solucao']['pontos_chave']))

        story.append(PageBreak())

        # Slide 4: Análise de Mercado
        story.append(self._create_slide_title("SLIDE 4: ANÁLISE DE MERCADO"))

        # Métricas de mercado
        market_data = [
            ["Tamanho do Mercado", pitch_deck['slide_mercado']['tamanho_mercado']],
            ["Crescimento", pitch_deck['slide_mercado']['crescimento_mercado']]
        ]

        market_table = Table(market_data, colWidths=[2*inch, 3*inch])
        market_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(market_table)
        story.append(Spacer(1, 15))

        # Segmentos alvo
        if pitch_deck['slide_mercado']['segmentos_alvo']:
            story.append(Paragraph("<b>Segmentos Alvo:</b>", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_mercado']['segmentos_alvo']))
            story.append(Spacer(1, 10))

        # Tendências
        if pitch_deck['slide_mercado']['tendencias']:
            story.append(Paragraph("<b>Tendências:</b>", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_mercado']['tendencias']))
            story.append(Spacer(1, 10))

        # Oportunidades
        if pitch_deck['slide_mercado']['oportunidades']:
            story.append(Paragraph("<b>Oportunidades:</b>", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_mercado']['oportunidades']))

        story.append(PageBreak())

        # Slide 5: Modelo de Negócio
        story.append(self._create_slide_title("SLIDE 5: MODELO DE NEGÓCIO"))

        # Estratégia de monetização
        if pitch_deck['slide_modelo_negocio']['estrategia_monetizacao']:
            story.append(Paragraph("<b>Estratégia de Monetização:</b>", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_modelo_negocio']['estrategia_monetizacao']))
            story.append(Spacer(1, 10))

        # Fontes de receita
        if pitch_deck['slide_modelo_negocio']['fontes_receita']:
            story.append(Paragraph("<b>Fontes de Receita:</b>", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_modelo_negocio']['fontes_receita']))
            story.append(Spacer(1, 10))

        # Custos estimados
        if pitch_deck['slide_modelo_negocio']['custos_estimados']:
            story.append(Paragraph("<b>Custos Estimados:</b>", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_modelo_negocio']['custos_estimados']))
            story.append(Spacer(1, 15))

        # Projeções
        projecoes_data = [
            ["Projeção de Receita", pitch_deck['slide_modelo_negocio']['projecao_receita']],
            ["Break-even", pitch_deck['slide_modelo_negocio']['break_even']]
        ]

        projecoes_table = Table(projecoes_data, colWidths=[2*inch, 3*inch])
        projecoes_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgreen),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(projecoes_table)

        story.append(PageBreak())

        # Slide 6: Diferenciação
        story.append(self._create_slide_title("SLIDE 6: DIFERENCIAÇÃO/COMPETIÇÃO"))
        story.append(Paragraph(pitch_deck['slide_diferencacao']['titulo'], self.subtitle_style))
        story.append(Spacer(1, 15))
        story.append(Paragraph(pitch_deck['slide_diferencacao']['conteudo'], self.normal_style))
        story.append(Spacer(1, 15))

        if pitch_deck['slide_diferencacao']['pontos_chave']:
            story.append(Paragraph("<b>Pontos-chave:</b>", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_diferencacao']['pontos_chave']))

        story.append(PageBreak())

        # Slide 7: Roadmap
        story.append(self._create_slide_title("SLIDE 7: ROADMAP DE DESENVOLVIMENTO"))

        # Fases de desenvolvimento
        if pitch_deck['slide_roadmap']['fases']:
            story.append(Paragraph("<b>Fases de Desenvolvimento:</b>", self.subtitle_style))
            for i, fase in enumerate(pitch_deck['slide_roadmap']['fases'], 1):
                story.append(Paragraph(f"<b>Fase {i}:</b> {fase}", self.bullet_style))
            story.append(Spacer(1, 10))

        # Cronograma
        story.append(Paragraph(f"<b>Cronograma:</b> {pitch_deck['slide_roadmap']['cronograma']}", self.subtitle_style))
        story.append(Spacer(1, 10))

        # Marcos principais
        if pitch_deck['slide_roadmap']['marcos_principais']:
            story.append(Paragraph("<b>Marcos Principais:</b>", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_roadmap']['marcos_principais']))
            story.append(Spacer(1, 10))

        # Riscos
        if pitch_deck['slide_roadmap']['riscos']:
            story.append(Paragraph("<b>Riscos Identificados:</b>", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_roadmap']['riscos']))

        story.append(PageBreak())

        # Slide 8: Equipe
        story.append(self._create_slide_title("SLIDE 8: EQUIPE/RECURSOS"))
        story.append(Paragraph(pitch_deck['slide_equipe']['titulo'], self.subtitle_style))
        story.append(Spacer(1, 15))
        story.append(Paragraph(pitch_deck['slide_equipe']['conteudo'], self.normal_style))
        story.append(Spacer(1, 15))

        if pitch_deck['slide_equipe']['pontos_chave']:
            story.append(Paragraph("<b>Pontos-chave:</b>", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_equipe']['pontos_chave']))

        story.append(PageBreak())

        # Slide 9: Financeiro
        story.append(self._create_slide_title("SLIDE 9: PROJEÇÕES FINANCEIRAS"))
        story.append(Paragraph(pitch_deck['slide_financeiro']['titulo'], self.subtitle_style))
        story.append(Spacer(1, 15))
        story.append(Paragraph(pitch_deck['slide_financeiro']['conteudo'], self.normal_style))
        story.append(Spacer(1, 15))

        if pitch_deck['slide_financeiro']['pontos_chave']:
            story.append(Paragraph("<b>Pontos-chave:</b>", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_financeiro']['pontos_chave']))

        story.append(PageBreak())

        # Slide 10: Call to Action
        story.append(self._create_slide_title("SLIDE 10: CALL TO ACTION"))
        story.append(Paragraph(pitch_deck['slide_call_action']['titulo'], self.subtitle_style))
        story.append(Spacer(1, 15))
        story.append(Paragraph(pitch_deck['slide_call_action']['conteudo'], self.normal_style))
        story.append(Spacer(1, 15))

        if pitch_deck['slide_call_action']['pontos_chave']:
            story.append(Paragraph("<b>Pontos-chave:</b>", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_call_action']['pontos_chave']))

        story.append(PageBreak())

        # Informações adicionais
        story.append(self._create_slide_title("INFORMAÇÕES ADICIONAIS"))

        info_data = [
            ["Público-alvo do Pitch", pitch_deck['publico_alvo_pitch']],
            ["Duração da Apresentação", pitch_deck['duracao_apresentacao']]
        ]

        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(info_table)
        story.append(Spacer(1, 15))

        # Dicas de apresentação
        if pitch_deck['dicas_apresentacao']:
            story.append(Paragraph("<b>Dicas de Apresentação:</b>", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['dicas_apresentacao']))

        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph("--- Gerado pelo Game Concept Forge ---", self.highlight_style))

        # Gerar PDF
        doc.build(story)
        buffer.seek(0)
        return buffer


def generate_pitch_deck_pdf(pitch_deck: PitchDeck, filename: str = "pitch_deck.pdf") -> BytesIO:
    """Função conveniente para gerar PDF do pitch deck."""
    generator = PitchDeckPDFGenerator()
    return generator.generate_pitch_deck_pdf(pitch_deck, filename)