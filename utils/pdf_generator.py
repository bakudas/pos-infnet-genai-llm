"""
Módulo para geração de PDFs do pitch deck.
Cria apresentações profissionais em PDF 16:9 com layout moderno.
"""

from io import BytesIO
from reportlab.lib.pagesizes import landscape
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Flowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from typing import List
from utils.data_models import PitchDeck

# Dimensões 16:9 em points (1920x1080)
SLIDE_WIDTH = 1920
SLIDE_HEIGHT = 1080
SLIDE_SIZE = (SLIDE_WIDTH, SLIDE_HEIGHT)

class SlideBackground(Flowable):
    """Flowable para desenhar fundo colorido do slide."""
    def __init__(self, color):
        super().__init__()
        self.color = color
    def draw(self):
        self.canv.saveState()
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, SLIDE_WIDTH, SLIDE_HEIGHT, fill=1, stroke=0)
        self.canv.restoreState()

class PitchDeckPDFGenerator:
    """Gerador de PDF para pitch decks de jogos em 16:9."""
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        # Paleta de cores para slides
        self.slide_colors = [colors.whitesmoke, colors.HexColor("#e3f2fd"), colors.HexColor("#f3e5f5"), colors.HexColor("#e8f5e9")]

    def _setup_custom_styles(self):
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=60,
            spaceAfter=40,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0d47a1"),
            fontName='Helvetica-Bold'
        )
        self.slide_title_style = ParagraphStyle(
            'SlideTitle',
            parent=self.styles['Heading2'],
            fontSize=44,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1565c0"),
            fontName='Helvetica-Bold'
        )
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading3'],
            fontSize=32,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1976d2"),
            fontName='Helvetica-Bold'
        )
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=28,
            spaceAfter=18,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        )
        self.bullet_style = ParagraphStyle(
            'CustomBullet',
            parent=self.styles['Normal'],
            fontSize=26,
            spaceAfter=12,
            leftIndent=40,
            fontName='Helvetica'
        )
        self.highlight_style = ParagraphStyle(
            'CustomHighlight',
            parent=self.styles['Normal'],
            fontSize=28,
            spaceAfter=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#388e3c"),
            fontName='Helvetica-Bold'
        )
        self.separator_style = ParagraphStyle(
            'Separator',
            parent=self.styles['Normal'],
            fontSize=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#bdbdbd"),
            spaceAfter=20
        )

    def _create_slide_title(self, title: str) -> Paragraph:
        return Paragraph(f"<b>{title}</b>", self.slide_title_style)

    def _create_bullet_list(self, items: List[str]) -> List[Paragraph]:
        return [Paragraph(f"• {item}", self.bullet_style) for item in items]

    def _separator(self) -> Paragraph:
        return Paragraph("―" * 40, self.separator_style)

    def _slide_background(self, idx: int) -> SlideBackground:
        color = self.slide_colors[idx % len(self.slide_colors)]
        return SlideBackground(color)

    def generate_pitch_deck_pdf(self, pitch_deck: PitchDeck, filename: str = "pitch_deck.pdf") -> BytesIO:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=SLIDE_SIZE,
            rightMargin=100, leftMargin=100, topMargin=80, bottomMargin=80
        )
        story = []
        slide_idx = 0

        # Slide 1: Título
        story.append(self._slide_background(slide_idx)); slide_idx += 1
        story.append(self._create_slide_title("SLIDE 1: TÍTULO E APRESENTAÇÃO"))
        story.append(Paragraph(pitch_deck['slide_titulo']['titulo'], self.title_style))
        story.append(self._separator())
        story.append(Paragraph(pitch_deck['slide_titulo']['conteudo'], self.normal_style))
        if pitch_deck['slide_titulo']['pontos_chave']:
            story.append(Paragraph("Pontos-chave:", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_titulo']['pontos_chave']))
        story.append(PageBreak())

        # Slide 2: Problema/Oportunidade
        story.append(self._slide_background(slide_idx)); slide_idx += 1
        story.append(self._create_slide_title("SLIDE 2: PROBLEMA/OPORTUNIDADE"))
        story.append(Paragraph(pitch_deck['slide_problema']['titulo'], self.subtitle_style))
        story.append(self._separator())
        story.append(Paragraph(pitch_deck['slide_problema']['conteudo'], self.normal_style))
        if pitch_deck['slide_problema']['pontos_chave']:
            story.append(Paragraph("Pontos-chave:", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_problema']['pontos_chave']))
        story.append(PageBreak())

        # Slide 3: Solução/Conceito
        story.append(self._slide_background(slide_idx)); slide_idx += 1
        story.append(self._create_slide_title("SLIDE 3: SOLUÇÃO/CONCEITO DO JOGO"))
        story.append(Paragraph(pitch_deck['slide_solucao']['titulo'], self.subtitle_style))
        story.append(self._separator())
        story.append(Paragraph(pitch_deck['slide_solucao']['conteudo'], self.normal_style))
        if pitch_deck['slide_solucao']['pontos_chave']:
            story.append(Paragraph("Pontos-chave:", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_solucao']['pontos_chave']))
        story.append(PageBreak())

        # Slide 4: Análise de Mercado
        story.append(self._slide_background(slide_idx)); slide_idx += 1
        story.append(self._create_slide_title("SLIDE 4: ANÁLISE DE MERCADO"))
        from reportlab.platypus import Table
        market_data = [
            ["Tamanho do Mercado", pitch_deck['slide_mercado']['tamanho_mercado']],
            ["Crescimento", pitch_deck['slide_mercado']['crescimento_mercado']]
        ]
        market_table = Table(market_data, colWidths=[4*inch, 8*inch])
        market_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#bbdefb")),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 28),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 18),
            ('GRID', (0, 0), (-1, -1), 2, colors.HexColor("#90caf9"))
        ]))
        story.append(market_table)
        story.append(Spacer(1, 30))
        if pitch_deck['slide_mercado']['segmentos_alvo']:
            story.append(Paragraph("Segmentos Alvo:", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_mercado']['segmentos_alvo']))
        if pitch_deck['slide_mercado']['tendencias']:
            story.append(Paragraph("Tendências:", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_mercado']['tendencias']))
        if pitch_deck['slide_mercado']['oportunidades']:
            story.append(Paragraph("Oportunidades:", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_mercado']['oportunidades']))
        story.append(PageBreak())

        # Slide 5: Modelo de Negócio
        story.append(self._slide_background(slide_idx)); slide_idx += 1
        story.append(self._create_slide_title("SLIDE 5: MODELO DE NEGÓCIO"))
        if pitch_deck['slide_modelo_negocio']['estrategia_monetizacao']:
            story.append(Paragraph("Estratégia de Monetização:", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_modelo_negocio']['estrategia_monetizacao']))
        if pitch_deck['slide_modelo_negocio']['fontes_receita']:
            story.append(Paragraph("Fontes de Receita:", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_modelo_negocio']['fontes_receita']))
        if pitch_deck['slide_modelo_negocio']['custos_estimados']:
            story.append(Paragraph("Custos Estimados:", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_modelo_negocio']['custos_estimados']))
        from reportlab.platypus import Table
        projecoes_data = [
            ["Projeção de Receita", pitch_deck['slide_modelo_negocio']['projecao_receita']],
            ["Break-even", pitch_deck['slide_modelo_negocio']['break_even']]
        ]
        projecoes_table = Table(projecoes_data, colWidths=[4*inch, 8*inch])
        projecoes_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#c8e6c9")),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 28),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 18),
            ('GRID', (0, 0), (-1, -1), 2, colors.HexColor("#a5d6a7"))
        ]))
        story.append(projecoes_table)
        story.append(PageBreak())

        # Slide 6: Diferenciação
        story.append(self._slide_background(slide_idx)); slide_idx += 1
        story.append(self._create_slide_title("SLIDE 6: DIFERENCIAÇÃO/COMPETIÇÃO"))
        story.append(Paragraph(pitch_deck['slide_diferencacao']['titulo'], self.subtitle_style))
        story.append(self._separator())
        story.append(Paragraph(pitch_deck['slide_diferencacao']['conteudo'], self.normal_style))
        if pitch_deck['slide_diferencacao']['pontos_chave']:
            story.append(Paragraph("Pontos-chave:", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_diferencacao']['pontos_chave']))
        story.append(PageBreak())

        # Slide 7: Roadmap
        story.append(self._slide_background(slide_idx)); slide_idx += 1
        story.append(self._create_slide_title("SLIDE 7: ROADMAP DE DESENVOLVIMENTO"))
        if pitch_deck['slide_roadmap']['fases']:
            story.append(Paragraph("Fases de Desenvolvimento:", self.subtitle_style))
            for i, fase in enumerate(pitch_deck['slide_roadmap']['fases'], 1):
                story.append(Paragraph(f"Fase {i}: {fase}", self.bullet_style))
        story.append(Paragraph(f"Cronograma: {pitch_deck['slide_roadmap']['cronograma']}", self.subtitle_style))
        if pitch_deck['slide_roadmap']['marcos_principais']:
            story.append(Paragraph("Marcos Principais:", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_roadmap']['marcos_principais']))
        if pitch_deck['slide_roadmap']['riscos']:
            story.append(Paragraph("Riscos Identificados:", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_roadmap']['riscos']))
        story.append(PageBreak())

        # Slide 8: Equipe
        story.append(self._slide_background(slide_idx)); slide_idx += 1
        story.append(self._create_slide_title("SLIDE 8: EQUIPE/RECURSOS"))
        story.append(Paragraph(pitch_deck['slide_equipe']['titulo'], self.subtitle_style))
        story.append(self._separator())
        story.append(Paragraph(pitch_deck['slide_equipe']['conteudo'], self.normal_style))
        if pitch_deck['slide_equipe']['pontos_chave']:
            story.append(Paragraph("Pontos-chave:", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_equipe']['pontos_chave']))
        story.append(PageBreak())

        # Slide 9: Financeiro
        story.append(self._slide_background(slide_idx)); slide_idx += 1
        story.append(self._create_slide_title("SLIDE 9: PROJEÇÕES FINANCEIRAS"))
        story.append(Paragraph(pitch_deck['slide_financeiro']['titulo'], self.subtitle_style))
        story.append(self._separator())
        story.append(Paragraph(pitch_deck['slide_financeiro']['conteudo'], self.normal_style))
        if pitch_deck['slide_financeiro']['pontos_chave']:
            story.append(Paragraph("Pontos-chave:", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_financeiro']['pontos_chave']))
        story.append(PageBreak())

        # Slide 10: Call to Action
        story.append(self._slide_background(slide_idx)); slide_idx += 1
        story.append(self._create_slide_title("SLIDE 10: CALL TO ACTION"))
        story.append(Paragraph(pitch_deck['slide_call_action']['titulo'], self.subtitle_style))
        story.append(self._separator())
        story.append(Paragraph(pitch_deck['slide_call_action']['conteudo'], self.normal_style))
        if pitch_deck['slide_call_action']['pontos_chave']:
            story.append(Paragraph("Pontos-chave:", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['slide_call_action']['pontos_chave']))
        story.append(PageBreak())

        # Informações adicionais
        story.append(self._slide_background(slide_idx)); slide_idx += 1
        story.append(self._create_slide_title("INFORMAÇÕES ADICIONAIS"))
        info_data = [
            ["Público-alvo do Pitch", pitch_deck['publico_alvo_pitch']],
            ["Duração da Apresentação", pitch_deck['duracao_apresentacao']]
        ]
        from reportlab.platypus import Table
        info_table = Table(info_data, colWidths=[4*inch, 8*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#eeeeee")),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 28),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 18),
            ('GRID', (0, 0), (-1, -1), 2, colors.HexColor("#bdbdbd"))
        ]))
        story.append(info_table)
        if pitch_deck['dicas_apresentacao']:
            story.append(Paragraph("Dicas de Apresentação:", self.subtitle_style))
            story.extend(self._create_bullet_list(pitch_deck['dicas_apresentacao']))
        story.append(Spacer(1, 60))
        story.append(Paragraph("<font color='#bdbdbd'>--- Gerado pelo Game Concept Forge ---</font>", self.highlight_style))

        doc.build(story)
        buffer.seek(0)
        return buffer


def generate_pitch_deck_pdf(pitch_deck: PitchDeck, filename: str = "pitch_deck.pdf") -> BytesIO:
    generator = PitchDeckPDFGenerator()
    return generator.generate_pitch_deck_pdf(pitch_deck, filename)