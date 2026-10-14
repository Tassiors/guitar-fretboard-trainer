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

## 🌟 Funcionalidades

1. **Orientação para Destros e Canhotos**:
   - **Destro (Padrão)**: Nut/pestana à esquerda, casas progredindo para a direita.
   - **Canhoto**: Orientação espelhada horizontalmente, com Nut/pestana à direita e casas progredindo para a esquerda.
   - A ordem das cordas (6ª E no topo até 1ª E embaixo) mantém a perspectiva de toque do músico em ambas as orientações.

2. **Notas Naturais e Acidentes (#) por Padrão**:
   - Por padrão, o treino inclui **todas as notas (naturais e sustenidos/acidentes)** para um aprendizado musical completo.
   - Se desejar, é possível filtrar apenas notas naturais com um clique.

3. **Mapeamento Completo do Nut (Cordas Soltas / Casa 0)**:
   - Ampla área de clique para cada corda solta no Nut.
   - Opção para incluir ou ignorar as cordas soltas no treino.

4. **Treino de Todas as Ocorrências Repetidas**:
   - Quando uma nota é solicitada (ex.: **Lá / A** nas casas 1 a 5), o aplicativo contabiliza todas as suas posições no intervalo selecionado (`🎯 0 de 3 encontradas`).
   - Cada posição acertada brilha com uma **aura verde esmeralda e onda de expansão (ripple)** e permanece fixada.
   - O app só avança para a próxima nota quando você encontrar **todas as ocorrências** daquele intervalo!

5. **Foco por Transparência (Sem Linhas Azuis)**:
   - As casas e regiões fora do intervalo de prática recebem um efeito de transparência esmaecida.
   - A região ativa permanece com 100% de nitidez e contraste, direcionando o foco visual naturalmente.

6. **Botão "👁️ Exibir Notas do Intervalo"**:
   - Permite visualizar instantaneamente todas as notas musicais do intervalo ativo para estudo e memorização visual.

7. **Métricas de Desempenho**:
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
