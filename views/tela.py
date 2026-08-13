import pygame
from config import (
    LARGURA_BLOCO, COR_FUNDO, COR_GRADE, 
    LARGURA_TELA, ALTURA_TELA, COR_BORDA_SUPER
)

class TelaJogo:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        self.largura_painel = 160
        self.largura_total = LARGURA_TELA + self.largura_painel
        self.altura_total = ALTURA_TELA

        self.superficie = pygame.display.set_mode((self.largura_total, self.altura_total))
        pygame.display.set_caption("Tetris com Super Peça")

        self.fonte_pontos = pygame.font.SysFont("Arial", 22, bold=True)
        self.fonte_titulo = pygame.font.SysFont("Arial", 15)
        self.fonte_game_over = pygame.font.SysFont("Arial", 36, bold=True)

    def desenhar(self, tabuleiro, peca_atual, peca_fantasma=None, proxima_peca=None, peca_guardada=None, pontuacao=0, game_over=False):
        self.superficie.fill(COR_FUNDO)

        # 1. Desenha os blocos fixados no tabuleiro
        for y in range(tabuleiro.linhas):
            for x in range(tabuleiro.colunas):
                cor = tabuleiro.grade[y][x]
                if cor:
                    pygame.draw.rect(
                        self.superficie, cor,
                        (x * LARGURA_BLOCO, y * LARGURA_BLOCO, LARGURA_BLOCO, LARGURA_BLOCO)
                    )

        # 2. Desenha a Peça FANTASMA (com borda cinza bem visível)
        if peca_fantasma and not game_over:
            for x, y in peca_fantasma.obter_posicoes_globais():
                if y >= 0:
                    pygame.draw.rect(
                        self.superficie, (120, 120, 120),  # Borda cinza clara
                        (x * LARGURA_BLOCO, y * LARGURA_BLOCO, LARGURA_BLOCO, LARGURA_BLOCO), 2
                    )

        # 3. Desenha a Peça Atual
        for x, y in peca_atual.obter_posicoes_globais():
            if y >= 0:
                pygame.draw.rect(
                    self.superficie, peca_atual.cor,
                    (x * LARGURA_BLOCO, y * LARGURA_BLOCO, LARGURA_BLOCO, LARGURA_BLOCO)
                )
                if getattr(peca_atual, 'is_super', False):
                    pygame.draw.rect(
                        self.superficie, COR_BORDA_SUPER,
                        (x * LARGURA_BLOCO, y * LARGURA_BLOCO, LARGURA_BLOCO, LARGURA_BLOCO), 2
                    )

        # 4. Grade do Tabuleiro
        for y in range(tabuleiro.linhas):
            for x in range(tabuleiro.colunas):
                pygame.draw.rect(
                    self.superficie, COR_GRADE,
                    (x * LARGURA_BLOCO, y * LARGURA_BLOCO, LARGURA_BLOCO, LARGURA_BLOCO), 1
                )

        # 5. HUD Lateral (Pontos, Próxima e Guardada)
        self._desenhar_hud(pontuacao, proxima_peca, peca_guardada)

        # 6. Game Over
        if game_over:
            self._desenhar_game_over()

        pygame.display.update()

    def _desenhar_hud(self, pontuacao, proxima_peca, peca_guardada):
        x_painel = LARGURA_TELA + 10

        pygame.draw.line(
            self.superficie, COR_GRADE,
            (LARGURA_TELA, 0), (LARGURA_TELA, ALTURA_TELA), 2
        )

        # Pontuação
        txt_pontos_titulo = self.fonte_titulo.render("PONTUAÇÃO:", True, (180, 180, 180))
        self.superficie.blit(txt_pontos_titulo, (x_painel, 15))

        txt_pontos_valor = self.fonte_pontos.render(str(pontuacao), True, (255, 255, 255))
        self.superficie.blit(txt_pontos_valor, (x_painel, 38))

        # Miniatura: PEÇA GUARDADA (HOLD)
        txt_hold = self.fonte_titulo.render("GUARDADA (C):", True, (180, 180, 180))
        self.superficie.blit(txt_hold, (x_painel, 85))
        self._desenhar_miniatura(peca_guardada, x_painel + 15, 110)

        # Miniatura: PRÓXIMA PEÇA
        txt_prox = self.fonte_titulo.render("PRÓXIMA:", True, (180, 180, 180))
        self.superficie.blit(txt_prox, (x_painel, 210))
        self._desenhar_miniatura(proxima_peca, x_painel + 15, 235)

    def _desenhar_miniatura(self, peca, pos_x, pos_y):
        """Método auxiliar para desenhar peças menores na interface lateral."""
        if not peca:
            return

        tamanho_mini = 18
        for i, linha in enumerate(peca.formato):
            for j, bloco in enumerate(linha):
                if bloco == 1:
                    px = pos_x + (j * tamanho_mini)
                    py = pos_y + (i * tamanho_mini)
                    pygame.draw.rect(
                        self.superficie, peca.cor,
                        (px, py, tamanho_mini, tamanho_mini)
                    )
                    if getattr(peca, 'is_super', False):
                        pygame.draw.rect(
                            self.superficie, COR_BORDA_SUPER,
                            (px, py, tamanho_mini, tamanho_mini), 1
                        )

    def _desenhar_game_over(self):
        overlay = pygame.Surface((self.largura_total, self.altura_total), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.superficie.blit(overlay, (0, 0))

        txt_go = self.fonte_game_over.render("GAME OVER", True, (255, 50, 50))
        txt_reiniciar = self.fonte_titulo.render("Pressione R para reiniciar", True, (255, 255, 255))

        rect_go = txt_go.get_rect(center=(self.largura_total // 2, self.altura_total // 2 - 20))
        rect_re = txt_reiniciar.get_rect(center=(self.largura_total // 2, self.altura_total // 2 + 20))

        self.superficie.blit(txt_go, rect_go)
        self.superficie.blit(txt_reiniciar, rect_re)