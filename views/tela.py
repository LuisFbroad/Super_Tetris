import pygame
from config import (
    LARGURA_BLOCO,
    COR_FUNDO, COR_GRADE,
    LARGURA_TELA,
    ALTURA_TELA
)

class TelaJogo:
    def __init__(self):
        pygame.init()
        self.superficie = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Tetris - Módulos Separados")

    def desenhar(self, tabuleiro, peca_atual):
        self.superficie.fill(COR_FUNDO)

        # 1. Desenha blocos fixos
        for y in range(tabuleiro.linhas):
            for x in range(tabuleiro.colunas):
                cor = tabuleiro.grade[y][x]
                if cor:
                    pygame.draw.rect(
                        self.superficie, cor,
                        (x * LARGURA_BLOCO, y * LARGURA_BLOCO, LARGURA_BLOCO, LARGURA_BLOCO)
                    )

        # 2. Desenha a peça em movimento
        for x, y in peca_atual.obter_posicoes_globais():
            if y >= 0:
                pygame.draw.rect(
                    self.superficie, peca_atual.cor,
                    (x * LARGURA_BLOCO, y * LARGURA_BLOCO, LARGURA_BLOCO, LARGURA_BLOCO)
                )

        # 3. Desenha as linhas da grade
        for y in range(tabuleiro.linhas):
            for x in range(tabuleiro.colunas):
                pygame.draw.rect(
                    self.superficie, COR_GRADE,
                    (x * LARGURA_BLOCO, y * LARGURA_BLOCO, LARGURA_BLOCO, LARGURA_BLOCO), 1
                )

        pygame.display.update()

        def _desenhar_hud(self, pontuacao):
            x_painel = LARGURA_TELA + 10

            # Linha divisória da área de jogo
            pygame.draw.line(
                self.superficie, COR_GRADE,
                (LARGURA_TELA, 0), (LARGURA_TELA, ALTURA_TELA), 2
            )

            # Texto de Pontuação
            txt_pontos_titulo = self.fonte_titulo.render("PONTUAÇÃO:", True, (180, 180, 180))
            self.superficie.blit(txt_pontos_titulo, (x_painel, 30))

            txt_pontos_valor = self.fonte_pontos.render(str(pontuacao), True, (255, 255, 255))
            self.superficie.blit(txt_pontos_valor, (x_painel, 55))

            # Legenda da Super Peça
            txt_super = self.fonte_titulo.render("SUPER PEÇA:", True, (255, 215, 0))
            self.superficie.blit(txt_super, (x_painel, 120))
            
            txt_dica = self.fonte_titulo.render("+50 pts bônus", True, (150, 150, 150))
            self.superficie.blit(txt_dica, (x_painel, 142))

    def _desenhar_game_over(self):
        overlay = pygame.Surface((self.largura_total, self.altura_total), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200)) # Preto transparente
        self.superficie.blit(overlay, (0, 0))

        txt_go = self.fonte_game_over.render("GAME OVER", True, (255, 50, 50))
        txt_reiniciar = self.fonte_titulo.render("Pressione R para reiniciar", True, (255, 255, 255))

        # Centraliza o texto
        rect_go = txt_go.get_rect(center=(self.largura_total // 2, self.altura_total // 2 - 20))
        rect_re = txt_reiniciar.get_rect(center=(self.largura_total // 2, self.altura_total // 2 + 20))

        self.superficie.blit(txt_go, rect_go)
        self.superficie.blit(txt_reiniciar, rect_re)