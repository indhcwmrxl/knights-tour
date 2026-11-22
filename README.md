# Passeio do Cavalo — Heurística de Warnsdorff com Critério de Desempate de Roth

<p align="center">
  <img src="banner.jpg" alt="Passeio do Cavalo" width="320"/>
</p>

Implementação em terminal do clássico **Problema do Passeio do Cavalo** utilizando uma estratégia gulosa baseada na **heurística de Warnsdorff** com o **critério de desempate de Roth**, com visualização animada e saída em cores ANSI.

---

## Sobre o Problema

O Passeio do Cavalo é um problema combinatório clássico no qual um cavalo de xadrez deve visitar todas as casas de um tabuleiro N×N exatamente uma vez. A sequência de movimentos forma um **caminho Hamiltoniano** sobre o grafo das casas do tabuleiro.

### Algoritmo

O solucionador utiliza uma **estratégia gulosa** que toma decisões localmente ótimas a cada passo, sem retroceder:

1. A cada posição, todos os movimentos válidos do cavalo são enumerados.
2. Entre os candidatos, é escolhido o que possui o **menor número de saídas possíveis** (menor grau) — esta é a regra de Warnsdorff, que direciona o cavalo para longe de casas isoladas.
3. Quando dois ou mais candidatos têm o mesmo grau, o **critério de desempate de Roth** seleciona o que possui a **maior distância euclidiana em relação ao centro** do tabuleiro, priorizando bordas e cantos.
4. Um fator aleatório serve como terceiro nível de desempate, permitindo que o algoritmo repita com ordenações diferentes em até **50 tentativas** até encontrar um passeio completo.

### Complexidade

| Dimensão | Valor |
|----------|-------|
| Complexidade de tempo | O(N²) |
| Complexidade de espaço | O(N²) |

O algoritmo inicializa uma matriz N×N e executa no máximo N² − 1 passos por tentativa. Cada passo avalia um conjunto fixo de 8 movimentos em O(1). Com até K = 50 tentativas, o pior caso é O(K·N²).

---

## Funcionalidades

- Heurística de Warnsdorff com critério de desempate de Roth
- Visualização animada passo a passo no terminal
- Renderização em perspectiva 3D no terminal
- Suporte a cores ANSI com estética cyberpunk/retro
- Tamanho do tabuleiro, posição inicial, velocidade de animação e altura das células configuráveis
- Relatório de execução com número de passos, tempo e total de avaliações de grau

---

## Requisitos

- Python 3.7 ou superior
- Terminal com suporte a cores ANSI (Linux, macOS, Windows Terminal)

Nenhuma dependência externa é necessária.

---

## Instalação

```bash
git clone https://github.com/indhcwmrxl/knights-tour.git
cd knights-tour
```

---

## Como Usar

### Básico

```bash
python3 knights_tour.py
```

Executa com a configuração padrão: tabuleiro 8×8, posição inicial A1, modo de visualização 3D.

### Sintaxe completa

```bash
python3 knights_tour.py [--size N] [--start POS] [--delay SEG] [--tall | --compact]
```

### Opções

| Opção | Abreviação | Padrão | Descrição |
|-------|------------|--------|-----------|
| `--size N` | `-s` | `8` | Tamanho do tabuleiro (N×N). Mínimo recomendado: 5 |
| `--start POS` | `-p` | `a1` | Posição inicial em notação de xadrez (ex: `d4`, `b7`) |
| `--delay SEG` | `-d` | `0.06` | Intervalo entre quadros da animação em segundos |
| `--tall` | | | Força altura de célula com 3 linhas |
| `--compact` | | | Força altura de célula com 2 linhas |

### Exemplos

```bash
# Tabuleiro 8×8 iniciando em D4
python3 knights_tour.py --start d4

# Tabuleiro 5×5 iniciando em A3, animação mais rápida
python3 knights_tour.py --size 5 --start a3 --delay 0.03

# Tabuleiro 10×10 com células compactas
python3 knights_tour.py --size 10 --compact

# Argumentos posicionais (sintaxe legada)
python3 knights_tour.py 8 0.05 d4
```

---

## Saída do Programa

Durante a execução, o terminal exibe:

- Um **painel HUD** com o passo atual, posição no tabuleiro e barra de progresso
- O **tabuleiro animado** atualizado a cada movimento do cavalo
- Um **relatório final de execução** contendo:
  - Status do passeio (completo ou parcial)
  - Dimensões do tabuleiro
  - Posições de início e fim
  - Número de casas visitadas
  - Tempo de cálculo em milissegundos
  - Total de avaliações de grau (métrica de esforço computacional)

---

## Observações sobre o Tabuleiro 5×5

O tabuleiro 5×5 é um caso limite conhecido. Certas posições iniciais não produzem um caminho Hamiltoniano completo sob nenhuma estratégia gulosa determinística, incluindo a de Warnsdorff. Quando isso ocorre, o programa tenta outras ordenações aleatórias até atingir o limite de 50 tentativas.

Posições próximas ao centro (ex: C3, D3) tendem a produzir passeios parciais mais curtos, enquanto posições de borda (ex: A3, B1) têm maior probabilidade de gerar passeios completos.

---

## Contexto Acadêmico

Esta implementação foi desenvolvida para a disciplina de **Compiladores** da **Universidade do Estado do Rio Grande do Norte (UERN)**, Campus Natal, como exercício prático de análise de complexidade algorítmica e implementação de heurísticas.

---

## Referências

- FEOFILOFF, Paulo. *O paradigma guloso no projeto de algoritmos*. Disponível em: https://users.ime.usp.br/~pf/analise_de_algoritmos/aulas/guloso.html
- POHL, Ira. A method for finding Hamilton paths and Knight's tours. *Communications of the ACM*, v. 10, n. 7, p. 446–449, 1967. DOI: 10.1145/363427.363463
- ROTH, Arnd. *The Problem of the Knight: A Fast and Simple Algorithm*. Wolfram Library Archive, MathSource, 1992. Disponível em: https://library.wolfram.com/infocenter/MathSource/909/
- BIGONHA, Roberto S.; BIGONHA, Mariza A. S. *Algoritmos e Estruturas de Dados II*. Disponível em: https://homepages.dcc.ufmg.br/~bigonha/Cursos/aedii-slides-p4.pdf

---

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
