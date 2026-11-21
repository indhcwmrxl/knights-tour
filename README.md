# Passeio do Cavalo — Heuristica de Warnsdorff com Criterio de Desempate de Roth

<p align="center">
  <img src="banner.jpg" alt="Passeio do Cavalo" width="320"/>
</p>

Implementacao em terminal do classico **Problema do Passeio do Cavalo** utilizando uma estrategia gulosa baseada na **heuristica de Warnsdorff** com o **criterio de desempate de Roth**, com visualizacao animada do tabuleiro em ASCII renderizado em perspectiva 3D ou projecao isometrica.

---

## Sobre o Problema

O Passeio do Cavalo e um problema combinatorio classico no qual um cavalo de xadrez deve visitar todas as casas de um tabuleiro N×N exatamente uma vez. A sequencia de movimentos forma um **caminho Hamiltoniano** no grafo de movimentos validos do cavalo.

### Algoritmo

O solucionador utiliza uma **estrategia gulosa** que toma decisoes localmente otimas a cada passo, sem retroceder:

1. A cada posicao, todos os movimentos validos do cavalo sao enumerados.
2. Entre os candidatos, e escolhido o que possui o **menor numero de saidas possiveis** (menor grau) — esta e a regra de Warnsdorff, que direciona o cavalo para longe de casas isoladas.
3. Quando dois ou mais candidatos tem o mesmo grau, o **criterio de desempate de Roth** seleciona o que possui a **maior distancia euclidiana em relacao ao centro** do tabuleiro, priorizando bordas e cantos onde o cavalo tem maior chance de ficar preso.
4. Um fator aleatorio serve como terceiro nivel de desempate, permitindo que o algoritmo repita com ordenacoes diferentes em ate **50 tentativas** ate encontrar um passeio completo.

### Complexidade

| Dimensao | Valor |
|----------|-------|
| Complexidade de tempo | O(N²) |
| Complexidade de espaco | O(N²) |

O algoritmo inicializa uma matriz N×N e executa no maximo N² − 1 passos por tentativa. Cada passo avalia um conjunto fixo de 8 movimentos em O(1). Com ate K = 50 tentativas, o pior caso e O(50 · N²) = O(N²). O uso de memoria e dominado pela matriz do tabuleiro e pela lista do caminho, ambos de tamanho O(N²).

---

## Funcionalidades

- Heuristica de Warnsdorff com criterio de desempate de Roth
- Visualizacao animada passo a passo no terminal
- Renderizacao em perspectiva 3D no terminal
- Suporte a cores ANSI com estetica cyberpunk/retro
- Tamanho do tabuleiro, posicao inicial, velocidade de animacao e altura das celulas configuravéis
- Relatorio de execucao com numero de passos, tempo e total de avaliacoes de grau

---

## Requisitos

- Python 3.7 ou superior
- Terminal com suporte a cores ANSI (Linux, macOS, Windows Terminal)

Nenhuma dependencia externa e necessaria.

---

## Instalacao

```bash
git clone https://github.com/indhcwmrxl/knights-tour.git
cd knights-tour
```

---

## Como Usar

### Basico

```bash
python3 knights_tour.py
```

Executa com a configuracao padrao: tabuleiro 8×8, posicao inicial A1, modo de visualizacao 3D.

### Sintaxe completa

```bash
python3 knights_tour.py [--size N] [--start POS] [--delay SEG] [--tall | --compact]
```

### Opcoes

| Opcao | Abreviacao | Padrao | Descricao |
|-------|------------|--------|-----------|
| `--size N` | `-s` | `8` | Tamanho do tabuleiro (N×N). Minimo recomendado: 5 |
| `--start POS` | `-p` | `a1` | Posicao inicial em notacao de xadrez (ex: `d4`, `b7`) |
| `--delay SEG` | `-d` | `0.06` | Intervalo entre quadros da animacao em segundos |
| `--tall` | | | Forca altura de celula com 3 linhas |
| `--compact` | | | Forca altura de celula com 2 linhas |

### Exemplos

```bash
# Tabuleiro 8x8 iniciando em D4
python3 knights_tour.py --start d4

# Tabuleiro 5x5 iniciando em A3, animacao mais rapida
python3 knights_tour.py --size 5 --start a3 --delay 0.03

# Tabuleiro 10x10 com celulas compactas
python3 knights_tour.py --size 10 --compact

# Argumentos posicionais (sintaxe legada)
python3 knights_tour.py 8 0.05 d4
```

---

## Saida do Programa

Durante a execucao, o terminal exibe:

- Um **painel HUD** com o passo atual, posicao no tabuleiro e barra de progresso
- O **tabuleiro animado** atualizado a cada movimento do cavalo
- Um **relatorio final de execucao** contendo:
  - Status do passeio (completo ou parcial)
  - Dimensoes do tabuleiro
  - Posicoes de inicio e fim
  - Numero de casas visitadas
  - Tempo de calculo em milissegundos
  - Total de avaliacoes de grau (metrica de esforco computacional)

---

## Observacoes sobre o Tabuleiro 5×5

O tabuleiro 5×5 e um caso limite conhecido. Certas posicoes iniciais nao produzem um caminho Hamiltoniano completo sob nenhuma estrategia gulosa deterministica, incluindo a de Warnsdorff. Quando todas as 50 tentativas sao esgotadas sem um passeio completo, o programa reporta um **passeio parcial** com o numero de casas visitadas.

Posicoes proximas ao centro (ex: C3, D3) tendem a produzir passeios parciais mais curtos, enquanto posicoes de borda (ex: A3, B1) tem maior probabilidade de gerar passeios completos.

---

## Contexto Academico

Esta implementacao foi desenvolvida para a disciplina de **Compiladores** da **Universidade do Estado do Rio Grande do Norte (UERN)**, Campus Natal, como exercicio pratico de analise de complexidade algorítmica e projeto de estrategias gulosas.

---

## Referencias

- FEOFILOFF, Paulo. *O paradigma guloso no projeto de algoritmos*. Disponivel em: https://users.ime.usp.br/~pf/analise_de_algoritmos/aulas/guloso.html
- POHL, Ira. A method for finding Hamilton paths and Knight's tours. *Communications of the ACM*, v. 10, n. 7, p. 446–449, 1967. DOI: 10.1145/363427.363463
- ROTH, Arnd. *The Problem of the Knight: A Fast and Simple Algorithm*. Wolfram Library Archive, MathSource, 1992. Disponivel em: https://library.wolfram.com/infocenter/MathSource/909/
- BIGONHA, Roberto S.; BIGONHA, Mariza A. S. *Algoritmos e Estruturas de Dados II*. Disponivel em: https://homepages.dcc.ufmg.br/~bigonha/Cursos/aedii-slides-p4.pdf

---

## Licenca

Este projeto esta licenciado sob a [Licenca MIT](LICENSE).
