# 🎸 Guitar Fretboard Trainer (Treinador de Braço de Guitarra)

Treinador interativo de memorização e localização ágil de notas no braço da guitarra para **músicos destros**, baseado na escala real de uma guitarra até a 12ª casa (dois pontos), com afinação padrão (E A D G B E), mapeamento do Nut (cordas soltas), foco por transparência suave e suporte a notas repetidas no intervalo.

Disponível em **duas versões**:
1. 🌐 **Versão Web (Navegador)** via GitHub Pages (sem precisar instalar nada!).
2. 💻 **Versão Desktop Standalone** (Python com interface gráfica).

---

## 🌐 Acesso Online pelo Navegador (GitHub Pages)

Você pode acessar o aplicativo diretamente de qualquer computador, tablet ou celular:
👉 **[https://tassiors.github.io/guitar-fretboard-trainer/](https://tassiors.github.io/guitar-fretboard-trainer/)**

---

## 🌟 Funcionalidades

1. **Imagem e Escala Real**:
   - Braço com o fundo branco original, recortado do headstock até a **12ª casa** (marcação de dois pontos).
   - Cordas na ordem real (de cima para baixo):
     - **6ª corda: E (Bordão mais grosso)**
     - **5ª corda: A**
     - **4ª corda: D**
     - **3ª corda: G**
     - **2ª corda: B**
     - **1ª corda: E (Prima mais fina)**

2. **Mapeamento Completo do Nut (Cordas Soltas / Casa 0)**:
   - Ampla área de clique para cada corda solta no Nut.
   - Opção para incluir ou ignorar as cordas soltas no treino.

3. **Treino de Todas as Ocorrências Repetidas**:
   - Quando uma nota é solicitada (ex.: **Lá / A** nas casas 1 a 5), o aplicativo contabiliza todas as suas posições no intervalo selecionado (`🎯 0 de 3 encontradas`).
   - Cada posição acertada brilha com uma **aura verde esmeralda e onda de expansão (ripple)** e permanece fixada.
   - O app só avança para a próxima nota quando você encontrar **todas as ocorrências** daquele intervalo!

4. **Foco por Transparência (Sem Linhas Azuis)**:
   - As casas e regiões fora do intervalo de prática recebem um efeito de transparência esmaecida.
   - A região ativa permanece com 100% de nitidez e contraste, direcionando o foco visual naturalmente.

5. **Botão "👁️ Exibir Notas do Intervalo"**:
   - Permite visualizar instantaneamente todas as notas musicais do intervalo ativo para estudo e memorização visual.

6. **Métricas de Desempenho**:
   - ⏱️ **Tempo Médio de Resposta** (em segundos)
   - ⏱️ **Cronômetro ao vivo** da nota atual
   - ✅ **Total de Acertos**
   - ❌ **Total de Erros**
   - 🎯 **Taxa de Precisão (%)**
   - 🔥 **Sequência Atual de Acertos (Streak)** e Recorde

---

## 💻 Como Rodar a Versão Desktop (Python)

### Pelo inicializador em lote (Windows):
Dê dois cliques em:
```cmd
run.bat
```

### Pelo Terminal:
```powershell
python app.py
```
