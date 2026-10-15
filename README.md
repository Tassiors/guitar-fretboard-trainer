# 🎸 Guitar Fretboard Trainer (Treinador de Braço de Guitarra)

Treinador interativo de memorização e localização ágil de notas no braço da guitarra para **músicos destros e canhotos**, baseado na escala real de uma guitarra até a 12ª casa (dois pontos), com afinação padrão (E A D G B E), mapeamento do Nut (cordas soltas), foco por transparência suave e suporte a notas repetidas no intervalo.

Disponível em **duas versões**:
1. 🌐 **Versão Web (Navegador)** via GitHub Pages (sem precisar instalar nada!).
2. 💻 **Versão Desktop Standalone** (Python com interface gráfica CustomTkinter).

---

## 🌐 Acesso Online pelo Navegador (GitHub Pages)

Você pode acessar o aplicativo diretamente de qualquer computador, tablet ou celular:
👉 **[https://tassiors.github.io/guitar-fretboard-trainer/](https://tassiors.github.io/guitar-fretboard-trainer/)**

---

## ℹ️ Perspectiva do Instrumentista

> [!NOTE]
> **A posição das notas equivale exatamente à posição real em que tocamos (visão do instrumento em mãos).** A imagem utilizada é uma representação da visão traseira do braço da guitarra, adaptada com transparência para tornar o fretboard e as cordas perfeitamente visíveis sob a perspectiva de quem está tocando.

---

## 🌟 Modos de Treino

1. 🎯 **Modo "Localizar no Braço"**:
   - O aplicativo solicita uma nota musical (ex.: **Lá / A** nas casas 1 a 5).
   - Contabiliza todas as suas ocorrências no intervalo selecionado (`🎯 0 de 3 encontradas`).
   - Cada posição correta brilha em **verde esmeralda com onda de expansão (ripple)** e reproduz o timbre da corda.
   - Avança para a próxima nota somente quando você encontrar **todas as ocorrências** daquele intervalo.

2. 🎹 **Novo Modo "Adivinhar a Nota" (Teclado Cromático)**:
   - O aplicativo sorteia uma posição aleatória no braço da guitarra dentro da região configurada, destacando-a com uma marcação vibrante `?`.
   - Você adivinha a nota clicando nos botões da **escala cromática dispostos no formato de uma oitava de teclado/piano** (teclas brancas naturais embaixo e teclas pretas com acidentes em cima) para máxima ergonomia e tempo de resposta ultra-rápido.
   - Suporte a **atalhos no teclado físico do computador** (teclas `C`, `D`, `E`, `F`, `G`, `A`, `B` e números `1` a `5`).
   - Feedback sonoro e visual instantâneo: se errar, o app indica o erro e mantém a mesma nota; **só avança para a próxima nota quando você acertar**!
   - Opção de alternar entre layout Teclado de Piano e Grade Rápida compacta.

---

## 🌟 Funcionalidades & Configurações

1. **Orientação para Destros e Canhotos**:
   - **Destro (Padrão)**: Nut/pestana à esquerda, casas progredindo para a direita.
   - **Canhoto**: Orientação espelhada horizontalmente, com Nut/pestana à direita e casas progredindo para a esquerda.
   - A ordem das cordas (6ª E no topo até 1ª E embaixo) mantém a perspectiva de toque do músico em ambas as orientações.

2. **Sincronização Inteligente do Nut (Cordas Soltas)**:
   - O Nut (cordas soltas / casa 0) é **ativado automaticamente apenas quando a região começa na 1ª casa em diante** (ex.: `1ª a 5ª = ativado`, `1ª a 8ª = ativado`, `1ª a 12ª = ativado`, `0 a 12 = ativado`).
   - Em regiões intermediárias ou agudas (ex.: `3ª a 5ª = desativado`, `5ª a 9ª = desativado`, `7ª a 12ª = desativado`), o Nut é **automaticamente desativado**, mantendo o foco do instrumentista estritamente na digitação da posição ativa.

3. **Notas Naturais e Acidentes (#) por Padrão**:
   - Por padrão, o treino inclui **todas as notas (naturais e sustenidos/acidentes)** para um aprendizado musical completo.
   - Se desejar, é possível filtrar apenas notas naturais com um clique.

4. **Foco por Transparência Suave**:
   - As casas e regiões fora do intervalo de prática recebem um efeito de transparência esmaecida.
   - A região ativa permanece com 100% de nitidez e contraste, direcionando o foco visual naturalmente.

5. **Botão "👁️ Exibir Notas do Intervalo"**:
   - Permite visualizar instantaneamente todas as notas musicais do intervalo ativo para estudo e memorização visual.

6. **Métricas de Desempenho em Tempo Real**:
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
