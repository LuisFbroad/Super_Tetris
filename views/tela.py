import pygame
from config import LARGURA_BLOCO, COR_FUNDO, COR_GRADE, LARGURA_TELA, ALTURA_TELA

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