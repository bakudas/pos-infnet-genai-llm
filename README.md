# Game Concept Forge

Uma aplicação web multipáginas (Streamlit) que utiliza a API gratuita do Gemini para transformar ideias iniciais em conceitos de jogos estruturados. O app oferece uma suíte completa de ferramentas para desenvolvimento de conceitos de jogos, desde a geração inicial até análises detalhadas de mercado e fluxos de jogo.

## 🚀 Funcionalidades Disponíveis

### 📝 **Concept Generator**
- Gera conceitos de jogos a partir de ideias iniciais
- Cria One-Page GDD estruturado com core loop, mecânicas e monetização
- Sugere arte conceitual baseada na premissa do jogo
- Interface moderna e fácil de usar

### 🔍 **Competitor Analysis**
- Analisa concorrentes diretos e similares
- Identifica oportunidades de diferenciação
- Examina tendências de mercado
- Fornece recomendações estratégicas

### 🔄 **Core Loop Developer**
- Desenvolve core loops detalhados e balanceados
- Cria sistemas de recompensas (imediatas e de longo prazo)
- Define feedback loops e mecânicas de retenção
- Balanceia dificuldade e progressão

### 🎯 **Game Flow Creator**
- Cria fluxos de jogo completos
- Define onboarding e tutorial detalhados
- Mapeia progressão de níveis e momentos chave
- Otimiza experiência do usuário

### 📊 **Pitch Deck Creator**
- Gera apresentações de 10 slides
- Foca em investidores e publishers
- Inclui análise de mercado e finanças
- Cria call-to-action profissional
- **Exporta PDF profissional** para apresentações

## 🔮 Funcionalidades em Desenvolvimento

- **GDD de 10 Páginas**: Documento completo de game design
- **Art Concept Generator**: Gera conceitos visuais e mood boards
- **Market Validation**: Análise de viabilidade e estimativas de receita

## 🏗️ Arquitetura

```
pos-infnet-genai-llm/
├── app.py                 # Página principal e navegação
├── pages/                 # Páginas da aplicação
│   ├── 01_concept_generator.py
│   ├── 02_competitor_analysis.py
│   ├── 03_core_loop_developer.py
│   ├── 04_game_flow_creator.py
│   └── 05_pitch_deck_creator.py
├── utils/                 # Módulos utilitários
│   ├── __init__.py
│   ├── gemini_client.py   # Cliente centralizado para API Gemini
│   ├── data_models.py     # Estruturas de dados (TypedDict)
│   ├── sidebar.py         # Sidebar modular
│   └── pdf_generator.py   # Gerador de PDFs profissionais
├── requirements.txt       # Dependências
├── .gitignore            # Arquivos ignorados pelo Git
└── README.md             # Este arquivo
```

## 🛠️ Como usar

### 1. **Instalação**
```bash
git clone <url-do-repo>
cd pos-infnet-genai-llm
pip install -r requirements.txt
```

### 2. **Configuração da API**
- Acesse [Google AI Studio](https://aistudio.google.com/app/apikey) e gere sua chave gratuita
- Configure a variável de ambiente:
  ```bash
  export GEMINI_API_KEY="sua-chave-aqui"
  ```

### 3. **Execução**
```bash
streamlit run app.py
```

### 4. **Navegação**
- Acesse [http://localhost:8501](http://localhost:8501)
- Use o menu lateral para navegar entre as páginas
- As páginas compartilham dados automaticamente via sessão

## 📋 Fluxo de Trabalho Recomendado

1. **Gere um conceito** na página Concept Generator
2. **Analise concorrentes** para identificar oportunidades
3. **Desenvolva o core loop** para criar engajamento
4. **Crie o fluxo de jogo** para otimizar a experiência
5. **Crie um pitch deck** para apresentar a investidores

## 💡 Dicas para Melhores Resultados

### Para Conceitos:
- Seja específico sobre gênero e mecânicas
- Mencione inspirações e jogos similares
- Defina claramente o público-alvo
- Pense na experiência do jogador

### Para Análises:
- Considere diferentes plataformas
- Analise tendências de mercado
- Identifique lacunas de oportunidade
- Foque na diferenciação

## 🔧 Tecnologias Utilizadas

- **Streamlit**: Interface web e multipáginas
- **Google Generative AI**: API do Gemini para geração de conteúdo
- **Python**: Linguagem principal
- **TypedDict**: Estruturas de dados tipadas
- **ReportLab**: Geração de PDFs profissionais

## 📊 Estrutura de Dados

A aplicação utiliza estruturas de dados bem definidas (TypedDict) para:
- One-Page GDD
- Análise de Concorrentes
- Core Loop Detalhado
- Fluxo de Jogo
- Pitch Deck (10 slides)
- GDD Completo (futuro)

## 🚨 Observações Importantes

- O app utiliza apenas a API gratuita do Gemini (não requer Google Cloud)
- Não compartilhe sua chave de API publicamente
- Para melhores resultados, descreva sua ideia de jogo de forma clara e objetiva
- As páginas compartilham dados via `st.session_state`

## 📄 Exportação de PDF

O **Pitch Deck Creator** inclui funcionalidade completa de exportação para PDF:

### ✨ Características do PDF:
- **10 slides estruturados** seguindo padrões profissionais
- **Layout responsivo** com cores e tipografia consistentes
- **Tabelas organizadas** para métricas e dados financeiros
- **Listas com bullets** para pontos-chave
- **Quebras de página** automáticas entre slides
- **Footer personalizado** com marca do Game Concept Forge

### 📥 Como exportar:
1. Gere um pitch deck na página "Pitch Deck Creator"
2. Clique no botão "📄 Download PDF"
3. O arquivo será baixado automaticamente
4. Nome do arquivo: `pitch_deck_[titulo_do_jogo].pdf`

### 🎯 Uso recomendado:
- **Apresentações para investidores**
- **Reuniões com publishers**
- **Documentação de projeto**
- **Compartilhamento com equipe**

## 📝 Licença

Desenvolvido para fins educacionais como parte do projeto da disciplina de IA generativa para linguagem (Large Language Model) [25E2_3].

---

**🎮 Transforme suas ideias em jogos viáveis com Game Concept Forge!**
