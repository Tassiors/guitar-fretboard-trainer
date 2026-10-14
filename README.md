# 🎸 Guitar Fretboard Trainer (Treinador de Braço de Guitarra)

Um aplicativo moderno e interativo em Python para treino acelerado de memorização e localização de notas no braço da guitarra, com **orientação para destros**, divisões físicas reais das casas, textura realista de jacarandá/rosewood, cordas com calibre proporcional e síntese de áudio imediata.

---

## 🌟 Principais Funcionalidades

1. **Orientação para Destros**:
   - Nut/Pestana à esquerda, casas progredindo para a direita.
   - Alternância em um clique entre **Visão Tablatura** (1ª corda no topo) e **Visão Músico** (6ª corda no topo).

2. **Braço Realista com Física Precisa**:
   - Divisões exatas das casas baseadas na **regra dos 18 ($2^{1/12}$)**.
   - Trastes metálicos em níquel-prata com relevo e brilho 3D.
   - Marcações em madrepérola (inlays) nas casas 3, 5, 7, 9, 12 (duplo), 15, 17, 19, 21 e 24.
   - Cordas bordão com textura enrolada (wound) e primas em aço liso, com calibres físicos graduais.

3. **Treino por Região Customizável**:
   - Presets imediatos:
     - **1ª à 5ª casa** (Posição aberta / primeiros passos)
     - **5ª à 9ª casa** (Região média)
     - **7ª à 12ª casa** (Oitava)
     - **9ª à 15ª casa** (Solos e escalas agudas)
     - **0 à 12 (Metade do braço)**
     - **Braço Completo (0 a 22 casas)**
   - Sliders deslizantes para definir qualquer intervalo inicial e final que desejar.
   - Opção de **Zoom na Região** para ampliar a área de treino na tela inteira.

4. **Métricas de Desempenho em Tempo Real**:
   - ⏱️ **Tempo Médio de Acerto** (em segundos)
   - ⏱️ **Cronômetro ao vivo** da nota atual
   - ✅ **Total de Acertos**
   - ❌ **Total de Erros**
   - 🎯 **Taxa de Precisão** (%)
   - 🔥 **Sequência Atual de Acertos (Streak)** e Recorde (Best Streak)
   - 🔄 Botão para zerar métricas a qualquer momento.

5. **Modos e Recursos Extras**:
   - **Áudio Realista Instantâneo**: Sintetizador em memória que reproduz o timbre de corda dedilhada com harmônicos físicos reais.
   - **Notação Dupla**: Escolha entre **Cifra** (C, D, E, F, G, A, B) ou **Solfejo** (Dó, Ré, Mi, Fá, Sol, Lá, Si).
   - **Filtro de Acidentes**: Treine apenas com notas naturais ou inclua sustenidos (#) e bemóis (b).
   - **Botão Dica / Revelar**: Mostra com anéis dourados onde estão as ocorrências da nota solicitada.
   - **Modo Explorador Livre**: Clique livremente em qualquer corda/casa para ouvir e identificar a nota.

---

## 🚀 Como Executar

### Opção 1: Pelo executável em lote (Windows)
Basta dar dois cliques no arquivo:
```cmd
run.bat
```

### Opção 2: Pelo Terminal / Prompt de Comando
```powershell
python app.py
```

### Dependências
O aplicativo utiliza apenas bibliotecas leves já instaladas:
- `customtkinter`
- `pillow`
- `winsound` (nativo do Windows)
