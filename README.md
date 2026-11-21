# Knight's Tour — Warnsdorff's Heuristic with Roth's Tiebreaker

A terminal-based implementation of the **Knight's Tour problem** using a greedy strategy based on **Warnsdorff's heuristic** with **Roth's tiebreaking criterion**, featuring an animated ASCII board rendered in 3D perspective or isometric projection.

---

## About the Problem

The Knight's Tour is a classic combinatorial problem in which a chess knight must visit every square of an N×N board exactly once. The sequence of moves forms a **Hamiltonian path** on the graph of valid knight moves.

### Algorithm

The solver uses a **greedy strategy** that makes locally optimal decisions at each step without backtracking:

1. At each position, all valid knight moves are enumerated.
2. Among the candidates, the one with the **fewest onward moves** (lowest degree) is chosen — this is Warnsdorff's rule, which steers the knight away from isolated squares.
3. When two or more candidates share the same degree, **Roth's tiebreaker** selects the one with the **greatest Euclidean distance from the center** of the board, favoring edges and corners where the knight is most likely to get trapped.
4. A random factor serves as a third-level tiebreaker, allowing the algorithm to retry with different orderings across up to **50 attempts** until a complete tour is found.

### Complexity

| Dimension | Value |
|-----------|-------|
| Time complexity | O(N²) |
| Space complexity | O(N²) |

The algorithm initializes an N×N board and executes at most N² − 1 steps per attempt. Each step evaluates a fixed set of 8 moves in O(1). With up to K = 50 retries, the worst-case time is O(50 · N²) = O(N²). Memory usage is dominated by the board matrix and the path list, both of size O(N²).

---

## Features

- Warnsdorff's heuristic with Roth's tiebreaking criterion
- Animated step-by-step visualization in the terminal
- Two rendering modes: **3D perspective** and **isometric projection**
- ANSI color support with a cyberpunk/retro aesthetic
- Configurable board size, starting position, animation speed, and cell height
- Execution report with step count, timing, and total degree evaluations

---

## Requirements

- Python 3.7 or higher
- A terminal with ANSI color support (Linux, macOS, Windows Terminal)

No external dependencies are required.

---

## Installation

```bash
git clone https://github.com/indhcwmrxl/knights-tour.git
cd knights-tour
```

---

## Usage

### Basic

```bash
python3 knights_tour.py
```

Runs the default configuration: 8×8 board, starting at A1, 3D perspective view.

### Full syntax

```bash
python3 knights_tour.py [--size N] [--start POS] [--delay SEC] [--view MODE] [--tall | --compact]
```

### Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--size N` | `-s` | `8` | Board size (N×N). Minimum recommended: 5 |
| `--start POS` | `-p` | `a1` | Starting position in chess notation (e.g., `d4`, `b7`) |
| `--delay SEC` | `-d` | `0.06` | Delay between animation frames in seconds |
| `--view MODE` | `-v` | `3d` | Rendering mode: `3d` or `iso` |
| `--tall` | | | Force 3-line cell height |
| `--compact` | | | Force 2-line cell height |

### Examples

```bash
# 8x8 board starting at D4 with isometric view
python3 knights_tour.py --start d4 --view iso

# 5x5 board starting at A3, faster animation
python3 knights_tour.py --size 5 --start a3 --delay 0.03

# 10x10 board with compact cells
python3 knights_tour.py --size 10 --compact

# Positional arguments (legacy syntax)
python3 knights_tour.py 8 0.05 d4 3d
```

---

## Output

During execution, the terminal displays:

- A **HUD panel** with the current step, board position, and a progress bar
- The **animated board** updated at each knight move
- A **final execution report** including:
  - Tour status (complete or partial)
  - Board dimensions
  - Start and end positions
  - Number of squares visited
  - Computation time in milliseconds
  - Total degree evaluations (computational effort metric)

---

## Notes on the 5×5 Board

The 5×5 board is a known edge case. Certain starting positions do not yield a complete Hamiltonian path under any deterministic greedy strategy, including Warnsdorff's. When all 50 retry attempts are exhausted without a complete tour, the program reports a **partial tour** with the number of squares visited.

Starting positions near the center (e.g., C3, D3) tend to produce shorter partial tours, while edge positions (e.g., A3, B1) are more likely to produce complete tours.

---

## Academic Context

This implementation was developed for the **Compilers** course at the **Universidade do Estado do Rio Grande do Norte (UERN)**, Campus Natal, as a practical exercise on algorithmic complexity analysis and greedy strategy design.

---

## References

- FEOFILOFF, Paulo. *O paradigma guloso no projeto de algoritmos*. Available at: https://users.ime.usp.br/~pf/analise_de_algoritmos/aulas/guloso.html
- POHL, Ira. A method for finding Hamilton paths and Knight's tours. *Communications of the ACM*, v. 10, n. 7, p. 446–449, 1967. DOI: 10.1145/363427.363463
- ROTH, Arnd. *The Problem of the Knight: A Fast and Simple Algorithm*. Wolfram Library Archive, MathSource, 1992. Available at: https://library.wolfram.com/infocenter/MathSource/909/
- BIGONHA, Roberto S.; BIGONHA, Mariza A. S. *Algoritmos e Estruturas de Dados II*. Available at: https://homepages.dcc.ufmg.br/~bigonha/Cursos/aedii-slides-p4.pdf

---

## License

This project is released under the [MIT License](LICENSE).
