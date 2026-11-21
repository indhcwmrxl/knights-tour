#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 O PROBLEMA DO CAVALO (KNIGHT'S TOUR) - VISUALIZADOR 3D (ASCII)
=============================================================================
 Demonstração interativa e animada do clássico algoritmo do Passeio do Cavalo
 utilizando a Heurística de Warnsdorff com desempate de Roth e renderização
 3D em perspectiva no terminal com estética cyberpunk/retro.
=============================================================================
"""

import sys
import time
import os
import random
import argparse

# Códigos de Cor ANSI
C_RESET       = "\033[0m"
C_BOLD        = "\033[1m"
C_DIM         = "\033[2m"

# Paleta Cyberpunk / Retro Terminal
C_BORDER      = "\033[38;5;242m"   # Cinza suave para bordas da grade
C_TILE_L      = "\033[48;5;237m"   # Fundo da casa clara
C_TILE_D      = "\033[48;5;234m"   # Fundo da casa escura
C_WALL        = "\033[38;5;239m"   # Contorno do pedestal 3D
C_WALL_F      = "\033[38;5;235m"   # Textura da parede lateral

# Cavalo & Elementos Visuais
C_KNIGHT      = "\033[1;38;5;220m" # Dourado brilhante para o corpo do cavalo
C_KNIGHT_EYE  = "\033[1;38;5;231m" # Branco puro para o olho do cavalo
C_KNIGHT_BASE = "\033[38;5;214m"   # Âmbar para a base do pedestal
C_TRAIL_HOT   = "\033[1;38;5;51m"  # Ciano neon para os passos mais recentes
C_TRAIL_MID   = "\033[38;5;45m"    # Ciano intermediário
C_VISITED     = "\033[38;5;34m"    # Verde esmeralda para casas visitadas
C_HUD         = "\033[1;38;5;75m"   # Azul claro para a interface HUD
C_ACCENT      = "\033[1;38;5;201m"  # Magenta para destaques
C_COORD       = "\033[1;38;5;214m"  # Âmbar para coordenadas (A-H, 1-8)

# Destaque de Início e Fim (Cores marcantes e distintas)
C_START_FG    = "\033[1;38;5;46m"   # Verde Neon brilhante para INÍCIO
C_START_BG    = "\033[48;5;22m"     # Fundo verde floresta para destacar a casa de início
C_END_FG      = "\033[1;38;5;196m"  # Vermelho Neon brilhante para FIM
C_END_BG      = "\033[48;5;52m"     # Fundo vermelho vinho para destacar a casa final

class KnightsTour3D:
    def __init__(self, size=8, delay=0.06, start_pos="a1", cell_height=None):
        self.size = size
        self.delay = delay
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        self.path = []
        self.start_r, self.start_c = self.parse_coord(start_pos)
        self.solve_time_ms = 0.0
        self.heuristics_evals = 0
        
        # Detecção de tamanho do terminal
        try:
            term = os.get_terminal_size()
            term_lines, term_cols = term.lines, term.columns
        except Exception:
            term_lines, term_cols = 24, 80

        if cell_height is not None:
            self.cell_height = cell_height
        else:
            # Auto-detecta: se o terminal tiver espaço suficiente (>= 38 linhas), usa 3 linhas
            self.cell_height = 3 if term_lines >= 38 else 2

    def parse_coord(self, coord_str):
        """Converte coordenadas como 'a1', 'd4', '0,0' para (row, col) na matriz."""
        s = str(coord_str).strip().lower()
        if len(s) >= 2 and s[0].isalpha() and s[1:].isdigit():
            col = ord(s[0]) - ord('a')
            rank = int(s[1:])
            row = self.size - rank
            if 0 <= row < self.size and 0 <= col < self.size:
                return row, col
        # Formato numérico "r,c" ou "r c"
        for sep in [",", " ", ";"]:
            if sep in s:
                parts = s.split(sep)
                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                    r, c = int(parts[0]), int(parts[1])
                    if 0 <= r < self.size and 0 <= c < self.size:
                        return r, c
        # Padrão: a1 (inferior esquerdo)
        return self.size - 1, 0

    def format_coord(self, r, c):
        """Retorna representação de xadrez: 'A1', 'D4', etc."""
        col_letters = "ABCDEFGH"
        col_char = col_letters[c] if c < len(col_letters) else chr(ord('A') + c)
        rank_num = self.size - r
        return f"{col_char}{rank_num}"

    def is_valid(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == 0

    def get_degree(self, r, c):
        self.heuristics_evals += 1
        count = 0
        for dr, dc in self.moves:
            if self.is_valid(r + dr, c + dc):
                count += 1
        return count

    def solve_warnsdorff(self):
        """Resolve o Knight's Tour usando a Heurística de Warnsdorff com desempate de Roth."""
        t_start = time.perf_counter()
        total_squares = self.size * self.size
        
        # Tentativas com desempate de Roth (prioriza bordas) para garantir 100% de sucesso
        for attempt in range(50):
            self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
            self.path = []
            curr_r, curr_c = self.start_r, self.start_c
            step = 1
            self.board[curr_r][curr_c] = step
            self.path.append((curr_r, curr_c))

            while step < total_squares:
                candidates = []
                for dr, dc in self.moves:
                    nr, nc = curr_r + dr, curr_c + dc
                    if self.is_valid(nr, nc):
                        deg = self.get_degree(nr, nc)
                        # Distância Euclidiana do centro (regra de Roth)
                        dist_center = (nr - (self.size - 1) / 2.0)**2 + (nc - (self.size - 1) / 2.0)**2
                        # Prioriza menor grau; em caso de empate, maior distância do centro
                        candidates.append((deg, -dist_center, random.random(), nr, nc))

                if not candidates:
                    break

                candidates.sort()
                _, _, _, next_r, next_c = candidates[0]

                step += 1
                curr_r, curr_c = next_r, next_c
                self.board[curr_r][curr_c] = step
                self.path.append((curr_r, curr_c))

            if step == total_squares:
                break

        self.solve_time_ms = (time.perf_counter() - t_start) * 1000.0
        return len(self.path) == total_squares

    # =========================================================================
    # RENDERIZADOR 1: TABULEIRO 3D EM PERSPECTIVA (ORIENTAÇÃO REAL DE XADREZ)
    # =========================================================================
    def render_perspective_3d(self, current_step):
        """
        Renderiza o tabuleiro com orientação padrão de xadrez:
        - Linha 1 na frente (embaixo), Linha 8 atrás (em cima).
        - Colunas A até H da esquerda para a direita.
        - Casa A1 escura, Casa H1 clara ("Branca na direita").
        - Pedestal 3D chanfrado na base e laterais.
        - Sprite do cavalo detalhado e expressivo.
        """
        curr_pos = self.path[current_step - 1] if current_step > 0 and len(self.path) >= current_step else None
        col_letters = "ABCDEFGH"
        cell_w = 6
        h = self.cell_height

        lines = []

        # Cabeçalho de colunas (A..H)
        header_cols = "      "
        for c in range(self.size):
            char_c = col_letters[c] if c < len(col_letters) else chr(ord('A') + c)
            header_cols += f"  {C_COORD}{char_c}{C_RESET}   "
        lines.append(header_cols)

        # Borda superior do tabuleiro
        top_border = "   " + C_BORDER + "┌" + ("──────┬" * (self.size - 1)) + "──────┐" + C_RESET
        lines.append(top_border)

        for r in range(self.size):
            rank = self.size - r
            
            for line_idx in range(h):
                line_parts = []
                
                # Indicador de linha (Rank) na esquerda
                if line_idx == 0:
                    line_parts.append(f"{C_COORD}{rank:2d}{C_RESET} {C_BORDER}│{C_RESET}")
                else:
                    line_parts.append(f"   {C_BORDER}│{C_RESET}")

                for c in range(self.size):
                    # No xadrez clássico: (r + c) % 2 == 0 é casa clara (a8 é clara, a1 é escura)
                    is_light = (r + c) % 2 == 0
                    val = self.board[r][c]
                    total_squares = self.size * self.size
                    is_start = (val == 1)
                    # O ponto de término só é revelado no fim quando o percurso termina
                    is_end = (val == total_squares and current_step >= total_squares)

                    # Cor de fundo destacada para Início (Verde floresta) e Fim (Vinho)
                    if is_start:
                        bg = C_START_BG
                    elif is_end:
                        bg = C_END_BG
                    else:
                        bg = C_TILE_L if is_light else C_TILE_D

                    is_current = (curr_pos == (r, c))
                    is_visited = (0 < val <= current_step)

                    if is_current:
                        # SPRITE DO CAVALO BEM TRABALHADO
                        base_col = C_START_FG if is_start else (C_END_FG if is_end else C_KNIGHT_BASE)
                        s_val = f"{val:02d}"
                        if h == 3:
                            if line_idx == 0:
                                piece_txt = f"{C_KNIGHT}  _/) {C_RESET}"
                            elif line_idx == 1:
                                piece_txt = f"{C_KNIGHT} /{C_KNIGHT_EYE}●{C_KNIGHT}  \\{C_RESET}"
                            else:
                                piece_txt = f"{base_col}[={C_KNIGHT_EYE}{s_val}{base_col}=]{C_RESET}"
                        else:  # h == 2
                            if line_idx == 0:
                                piece_txt = f"{C_KNIGHT} _/)  {C_RESET}"
                            else:
                                piece_txt = f"{C_KNIGHT}/{C_KNIGHT_EYE}●{base_col}{s_val}{C_KNIGHT}\\{C_RESET}"
                        line_parts.append(bg + piece_txt + C_BORDER + "│" + C_RESET)

                    elif is_start and is_visited:
                        # Casa inicial visitada (passo 01) em Verde Neon destacado
                        if h == 3:
                            if line_idx == 0:
                                cell_txt = f" {C_START_FG}START{C_RESET}"
                            elif line_idx == 1:
                                cell_txt = f" {C_START_FG}{C_BOLD}[01]{C_RESET} "
                            else:
                                cell_txt = "      "
                        else:
                            if line_idx == 0:
                                cell_txt = f" {C_START_FG}START{C_RESET}"
                            else:
                                cell_txt = f" {C_START_FG}{C_BOLD}[01]{C_RESET} "
                        line_parts.append(bg + cell_txt + C_BORDER + "│" + C_RESET)

                    elif is_end:
                        # Casa final (passo final) em Vermelho Neon destacado
                        s_end = f"{total_squares:02d}"
                        if h == 3:
                            if line_idx == 0:
                                cell_txt = f"  {C_END_FG}FIM{C_RESET} "
                            elif line_idx == 1:
                                cell_txt = f" {C_END_FG}{C_BOLD}[{s_end}]{C_RESET} "
                            else:
                                cell_txt = "      "
                        else:
                            if line_idx == 0:
                                cell_txt = f"  {C_END_FG}FIM{C_RESET} "
                            else:
                                cell_txt = f" {C_END_FG}{C_BOLD}[{s_end}]{C_RESET} "
                        line_parts.append(bg + cell_txt + C_BORDER + "│" + C_RESET)

                    elif is_visited:
                        # Rastro de casas já visitadas
                        diff = current_step - val
                        if diff == 1:
                            col = C_TRAIL_HOT + C_BOLD
                        elif diff <= 4:
                            col = C_TRAIL_MID + C_BOLD
                        else:
                            col = C_VISITED
                        s_val = f"{val:02d}"

                        if line_idx == 1:
                            cell_txt = f"  {col}{s_val}{C_RESET}  "
                        else:
                            cell_txt = "      "
                        line_parts.append(bg + cell_txt + C_BORDER + "│" + C_RESET)

                    else:
                        # Casa vazia com ponto sutil
                        dot = "·" if is_light else " "
                        if h == 3:
                            cell_txt = f"  {dot}   " if line_idx == 1 else "      "
                        else:
                            cell_txt = f"  {dot}   " if line_idx == 0 else "      "
                        line_parts.append(bg + cell_txt + C_BORDER + "│" + C_RESET)

                # Indicador de linha (Rank) na direita
                if line_idx == 0:
                    line_parts.append(f" {C_COORD}{rank}{C_RESET}")
                lines.append("".join(line_parts))

            # Divisórias horizontais
            if r < self.size - 1:
                mid_border = "   " + C_BORDER + "├" + ("──────┼" * (self.size - 1)) + "──────┤" + C_RESET
                lines.append(mid_border)
            else:
                bot_border = "   " + C_BORDER + "└" + ("──────┴" * (self.size - 1)) + "──────┘" + C_RESET
                lines.append(bot_border)

        # Rodapé de colunas (A..H)
        lines.append(header_cols)

        # Pedestal 3D na base
        pedestal_len = self.size * 6 + (self.size - 1)
        lines.append("    " + C_WALL + " \\\\" + ("═" * (pedestal_len - 2)) + "\\\\" + C_RESET)
        lines.append("     " + C_WALL + " \\\\" + ("_" * (pedestal_len - 2)) + "\\\\" + C_RESET)

        return "\n".join(lines)

    def render_frame(self, current_step):
        return self.render_perspective_3d(current_step)

    def print_hud(self, step, total_steps):
        curr_pos = self.path[step - 1] if step > 0 and len(self.path) >= step else (0, 0)
        pos_str = self.format_coord(curr_pos[0], curr_pos[1])
        pct = (step / total_steps) * 100.0
        progress_blocks = int((step / total_steps) * 22)
        bar = "█" * progress_blocks + "░" * (22 - progress_blocks)

        start_str = self.format_coord(self.path[0][0], self.path[0][1]) if self.path else "??"
        if step >= total_steps and self.path:
            end_str = self.format_coord(self.path[-1][0], self.path[-1][1])
            end_label = f"{C_END_FG}● FIM: {end_str} (Passo {total_steps:02d}){C_RESET}"
        else:
            end_label = f"{C_DIM}● FIM: ?? (Passo {total_steps:02d}){C_RESET}"

        print(f"{C_HUD}╔══════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_HUD}║  {C_ACCENT}♞ PASSEIO DO CAVALO (KNIGHT'S TOUR) - 3D CHESS VISUALIZER{C_HUD}           ║{C_RESET}")
        print(f"{C_HUD}╠══════════════════════════════════════════════════════════════════════╣{C_RESET}")
        print(f"{C_HUD}║  Passo: {C_BOLD}{step:02d}/{total_steps:02d}{C_RESET}{C_HUD} │ Posição: {C_KNIGHT}{pos_str} (r:{curr_pos[0]}, c:{curr_pos[1]}){C_HUD} │ Progresso: [{C_TRAIL_HOT}{bar}{C_HUD}] {pct:5.1f}% ║{C_RESET}")
        print(f"{C_HUD}║  {C_START_FG}● INÍCIO: {start_str} (Passo 01){C_RESET}{C_HUD}        ───►        {end_label}{C_HUD}   ║{C_RESET}")
        print(f"{C_HUD}╚══════════════════════════════════════════════════════════════════════╝{C_RESET}")

    def animate(self):
        # Limpa tela
        os.system('cls' if os.name == 'nt' else 'clear')
        start_name = self.format_coord(self.start_r, self.start_c)
        print(f"{C_ACCENT}[+] Calculando percurso completo via Warnsdorff a partir de {C_BOLD}{start_name}{C_RESET}...")
        
        success = self.solve_warnsdorff()
        total_steps = len(self.path)
        total_squares = self.size * self.size

        # Oculta cursor do terminal
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

        try:
            for s in range(1, total_steps + 1):
                sys.stdout.write("\033[H")
                self.print_hud(s, total_squares)
                rendered = self.render_frame(s)
                sys.stdout.write(rendered + "\n")
                sys.stdout.flush()
                time.sleep(self.delay)

            # Resumo final acadêmico e técnico (conforme requisitos de CPA / UERN)
            end_name = self.format_coord(self.path[-1][0], self.path[-1][1]) if self.path else "??"
            status_txt = f"{C_BOLD}{C_VISITED}PASSEIO COMPLETO ALCANÇADO (100%){C_RESET}" if success else f"{C_BOLD}\033[31mPASSEIO PARCIAL{C_RESET}"
            print(f"\n{C_HUD}┌──────────────────────── RELATÓRIO DE EXECUÇÃO ────────────────────────┐{C_RESET}")
            print(f"{C_HUD}│{C_RESET} Status: {status_txt}")
            print(f"{C_HUD}│{C_RESET} Dimensão do Tabuleiro: {C_BOLD}{self.size}x{self.size}{C_RESET} ({total_squares} casas)")
            print(f"{C_HUD}│{C_RESET} Posição Inicial: {C_START_FG}{start_name}{C_RESET} (Passo 01 - Linha: {self.start_r}, Coluna: {self.start_c})")
            print(f"{C_HUD}│{C_RESET} Posição Final:   {C_END_FG}{end_name}{C_RESET} (Passo {total_steps:02d} - Linha: {self.path[-1][0]}, Coluna: {self.path[-1][1]})")
            print(f"{C_HUD}│{C_RESET} Casas Visitadas: {C_BOLD}{total_steps}/{total_squares}{C_RESET} ({total_steps/total_squares*100:.1f}%)")
            print(f"{C_HUD}│{C_RESET} Tempo de Cálculo: {C_BOLD}{self.solve_time_ms:.2f} ms{C_RESET}")
            print(f"{C_HUD}│{C_RESET} Avaliações de Grau (Esforço Computacional): {C_BOLD}{self.heuristics_evals}{C_RESET} verificações")
            print(f"{C_HUD}└───────────────────────────────────────────────────────────────────────┘{C_RESET}\n")

        finally:
            # Restaura cursor do terminal
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()


def parse_args():
    parser = argparse.ArgumentParser(description="Passeio do Cavalo (Knight's Tour) - Visualizador 3D ASCII")
    parser.add_argument("pos_size", nargs="?", default=None, help="Tamanho do tabuleiro (ex: 8 ou 5)")
    parser.add_argument("pos_delay", nargs="?", default=None, help="Velocidade da animacao em segundos (ex: 0.05)")
    parser.add_argument("pos_start", nargs="?", default=None, help="Posicao inicial (ex: a1, b1, d4)")

    parser.add_argument("--size", "-s", type=int, default=8, help="Tamanho do tabuleiro (padrao: 8)")
    parser.add_argument("--delay", "-d", type=float, default=0.06, help="Intervalo entre passos (padrao: 0.06s)")
    parser.add_argument("--start", "-p", type=str, default="a1", help="Posicao inicial do cavalo (padrao: a1)")
    parser.add_argument("--tall", action="store_true", help="Forca celulas altas com 3 linhas")
    parser.add_argument("--compact", action="store_true", help="Forca celulas compactas com 2 linhas")

    args = parser.parse_args()

    # Tratamento de argumentos posicionais legados
    size = args.size
    if args.pos_size is not None:
        try:
            size = int(args.pos_size)
        except ValueError:
            pass

    delay = args.delay
    if args.pos_delay is not None:
        try:
            delay = float(args.pos_delay)
        except ValueError:
            pass

    start = args.pos_start if args.pos_start is not None else args.start

    cell_height = None
    if args.tall:
        cell_height = 3
    elif args.compact:
        cell_height = 2

    return size, delay, start, cell_height


if __name__ == "__main__":
    size, delay, start, cell_height = parse_args()
    app = KnightsTour3D(size=size, delay=delay, start_pos=start, cell_height=cell_height)
    app.animate()
