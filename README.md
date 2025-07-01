# Game Concept Forge

Uma aplicação web (Streamlit) que utiliza a API gratuita do Gemini para transformar ideias iniciais em conceitos de jogos estruturados. O app gera automaticamente um documento de One-Page GDD (Game Design Document) com core loop, mecânicas, monetização e diferenciais, além de sugerir uma arte conceitual para o jogo.

## Funcionalidades
- Geração automática de conceitos de jogos a partir de uma ideia simples
- Estruturação do conceito em formato de One-Page GDD
- Sugestão de arte conceitual baseada na premissa do jogo
- Interface moderna e fácil de usar

## Como usar

1. **Clone o repositório e instale as dependências:**
   ```bash
   git clone <url-do-repo>
   cd pos-infnet-genai-llm
   pip install -r requirements.txt
   ```

2. **Obtenha sua chave de API gratuita do Gemini:**
   - Acesse [Google AI Studio](https://aistudio.google.com/app/apikey) e gere sua chave.

3. **Defina a variável de ambiente com sua chave:**
   ```bash
   export GEMINI_API_KEY="sua-chave-aqui"
   ```

4. **Execute o aplicativo:**
   ```bash
   streamlit run app.py
   ```

5. **Acesse no navegador:**
   - O app estará disponível em [http://localhost:8501](http://localhost:8501)

6. **Como funciona:**
   - Digite sua ideia de jogo no campo indicado e clique em "Enviar".
   - O app irá gerar um conceito estruturado, exibir o GDD e sugerir uma arte conceitual.

## Observações
- O app utiliza apenas a API gratuita do Gemini (não requer Google Cloud).
- Não compartilhe sua chave de API publicamente.
- Para melhores resultados, descreva sua ideia de jogo de forma clara e objetiva.

---

Desenvolvido para fins educacionais como parte do projeto da disciplina de IA generativa para linguagem (Large Language Model) [25E2_3].
