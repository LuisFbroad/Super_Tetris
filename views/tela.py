import pygame
from config import (
    LARGURA_BLOCO, COR_FUNDO, COR_GRADE, COR_PAINEL,
    COR_TEXTO, COR_TEXTO_MUTED, LARGURA_TELA, ALTURA_TELA, COR_BORDA_SUPER
)

class TelaJogo:
    def __init__(self):
        # Aumenta a largura total para acomodar o painel lateral de status
        self.largura_painel = 180
        self.largura_total = LARGURA_TELA + self.largura_painel
        self.altura_total = ALTURA_TELA

        self.superficie = pygame.display.set_mode((self.largura_total, self.altura_total))
        pygame.display.set_caption("Tetris - Neon Edition")

        pygame.font.init()
        self.fonte = pygame.font.SysFont("Segoe UI", 24, bold=True)
        self.fonte_titulo = pygame.font.SysFont("Segoe UI", 16, bold=True)

    def desenhar(self, tabuleiro, peca_atual, peca_fantasma, proxima_peca, peca_guardada, pontuacao, game_over, gerenciador_particulas=None):
        self.superficie.fill(COR_FUNDO)

        # 1. Desenhar a Grade do Tabuleiro
        self._desenhar_grade()

        # 2. Desenhar Peças Fixadas no Tabuleiro
        if tabuleiro:
            for y in range(tabuleiro.linhas):
                for x in range(tabuleiro.colunas):
                    cor = tabuleiro.grade[y][x]
                    if cor:
                        self._desenhar_bloco(x, y, cor)

        # 3. Desenhar Peça Fantasma (Sombra)
        if peca_fantasma and not game_over:
            self._desenhar_peca_fantasma(peca_fantasma)

        # 4. Desenhar Peça Atual em Queda
        if peca_atual and not game_over:
            self._desenhar_peca(peca_atual)

        # 5. Desenhar Efeitos de Partículas
        if gerenciador_particulas:
            gerenciador_particulas.atualizar_e_desenhar(self.superficie)

        # 6. Desenhar Painel Lateral (UI)
        self._desenhar_painel_lateral(proxima_peca, peca_guardada, pontuacao)

        # 7. Tela de Game Over
        if game_over:
            self._desenhar_game_over()

        pygame.display.update()

    def _desenhar_bloco(self, x, y, cor, alpha=255):
        rect = pygame.Rect(x * LARGURA_BLOCO, y * LARGURA_BLOCO, LARGURA_BLOCO, LARGURA_BLOCO)
        
        if alpha < 255:
            s = pygame.Surface((LARGURA_BLOCO, LARGURA_BLOCO), pygame.SRCALPHA)
            s.fill((*cor[:3], alpha))
            self.superficie.blit(s, rect.topleft)
        else:
            pygame.draw.rect(self.superficie, cor, rect)
            pygame.draw.rect(self.superficie, (255, 255, 255), rect, width=1)

    def _desenhar_peca(self, peca):
        for y, linha in enumerate(peca.formato):
            for x, valor in enumerate(linha):
                if valor:
                    px = peca.x + x
                    py = peca.y + y
                    if py >= 0:
                        self._desenhar_bloco(px, py, peca.cor)
                        if getattr(peca, 'is_super', False):
                            rect = pygame.Rect(px * LARGURA_BLOCO, py * LARGURA_BLOCO, LARGURA_BLOCO, LARGURA_BLOCO)
                            pygame.draw.rect(self.superficie, COR_BORDA_SUPER, rect, width=2)

    def _desenhar_peca_fantasma(self, fantasma):
        for y, linha in enumerate(fantasma.formato):
            for x, valor in enumerate(linha):
                if valor:
                    px = fantasma.x + x
                    py = fantasma.y + y
                    if py >= 0:
                        self._desenhar_bloco(px, py, fantasma.cor, alpha=60)

    def _desenhar_grade(self):
        for x in range(0, LARGURA_TELA, LARGURA_BLOCO):
            pygame.draw.line(self.superficie, COR_GRADE, (x, 0), (x, ALTURA_TELA))
        for y in range(0, ALTURA_TELA, LARGURA_BLOCO):
            pygame.draw.line(self.superficie, COR_GRADE, (0, y), (LARGURA_TELA, y))

    def _desenhar_painel_lateral(self, proxima_peca, peca_guardada, pontuacao):
        x_painel = LARGURA_TELA
        rect_painel = pygame.Rect(x_painel, 0, self.largura_painel, self.altura_total)
        pygame.draw.rect(self.superficie, COR_PAINEL, rect_painel)
        pygame.draw.line(self.superficie, COR_GRADE, (x_painel, 0), (x_painel, self.altura_total), width=2)

        # Pontuação
        txt_titulo_pts = self.fonte_titulo.render("PONTUAÇÃO", True, COR_TEXTO_MUTED)
        txt_pts = self.fonte.render(str(pontuacao), True, COR_TEXTO)
        self.superficie.blit(txt_titulo_pts, (x_painel + 20, 30))
        self.superficie.blit(txt_pts, (x_painel + 20, 55))

        # Peça Guardada (Hold)
        txt_hold = self.fonte_titulo.render("GUARDADA (C)", True, COR_TEXTO_MUTED)
        self.superficie.blit(txt_hold, (x_painel + 20, 110))
        if peca_guardada:
            self._desenhar_miniatura(peca_guardada, x_painel + 30, 140)

        # Próxima Peça
        txt_prox = self.fonte_titulo.render("PRÓXIMA PEÇA", True, COR_TEXTO_MUTED)
        self.superficie.blit(txt_prox, (x_painel + 20, 240))
        if proxima_peca:
            self._desenhar_miniatura(proxima_peca, x_painel + 30, 270)

    def _desenhar_miniatura(self, peca, offset_x, offset_y):
        for y, linha in enumerate(peca.formato):
            for x, valor in enumerate(linha):
                if valor:
                    rect = pygame.Rect(
                        offset_x + x * (LARGURA_BLOCO // 1.5),
                        offset_y + y * (LARGURA_BLOCO // 1.5),
                        LARGURA_BLOCO // 1.5,
                        LARGURA_BLOCO // 1.5
                    )
                    pygame.draw.rect(self.superficie, peca.cor, rect)
                    pygame.draw.rect(self.superficie, (255, 255, 255), rect, width=1)

    def _desenhar_game_over(self):
        overlay = pygame.Surface((self.largura_total, self.altura_total), pygame.SRCALPHA)
        overlay.fill((10, 10, 20, 210))
        self.superficie.blit(overlay, (0, 0))

        txt_go = self.fonte.render("GAME OVER", True, (255, 50, 80))
        txt_restart = self.fonte_titulo.render("[R] Reiniciar  |  [ESC] Menu", True, COR_TEXTO)

        rect_go = txt_go.get_rect(center=(self.largura_total // 2, self.altura_total // 2 - 20))
        rect_res = txt_restart.get_rect(center=(self.largura_total // 2, self.altura_total // 2 + 20))

        self.superficie.blit(txt_go, rect_go)
        self.superficie.blit(txt_restart, rect_res)

    def desenhar_menu(self, opcoes, indice_selecionado):
        self.superficie.fill(COR_FUNDO)

        fonte_titulo_grande = pygame.font.SysFont("Segoe UI", 42, bold=True)
        txt_titulo = fonte_titulo_grande.render("TETRIS", True, (0, 240, 255))
        txt_sub = self.fonte_titulo.render("NEON EDITION", True, COR_TEXTO_MUTED)

        rect_tit = txt_titulo.get_rect(center=(self.largura_total // 2, 80))
        rect_sub = txt_sub.get_rect(center=(self.largura_total // 2, 125))

        self.superficie.blit(txt_titulo, rect_tit)
        self.superficie.blit(txt_sub, rect_sub)

        txt_instrucao = self.fonte_titulo.render("Selecione a Dificuldade:", True, COR_TEXTO)
        rect_inst = txt_instrucao.get_rect(center=(self.largura_total // 2, 180))
        self.superficie.blit(txt_instrucao, rect_inst)

        y_inicial = 230
        for i, (chave, dados) in enumerate(opcoes.items()):
            selecionado = (i == indice_selecionado)
            
            largura_btn = 200
            altura_btn = 45
            x_btn = (self.largura_total - largura_btn) // 2
            y_btn = y_inicial + (i * 55)

            rect_btn = pygame.Rect(x_btn, y_btn, largura_btn, altura_btn)

            if selecionado:
                pygame.draw.rect(self.superficie, dados["cor"], rect_btn, border_radius=8)
                cor_texto = (10, 10, 20)
            else:
                pygame.draw.rect(self.superficie, (25, 25, 40), rect_btn, border_radius=8)
                pygame.draw.rect(self.superficie, (50, 50, 80), rect_btn, width=1, border_radius=8)
                cor_texto = COR_TEXTO

            txt_opcao = self.fonte_titulo.render(dados["nome"].upper(), True, cor_texto)
            rect_op = txt_opcao.get_rect(center=rect_btn.center)
            self.superficie.blit(txt_opcao, rect_op)

        txt_dica = self.fonte_titulo.render("↑/↓ NAVEGAR  |  ENTER CONFIRMAR", True, COR_TEXTO_MUTED)
        rect_dica = txt_dica.get_rect(center=(self.largura_total // 2, self.altura_total - 40))
        self.superficie.blit(txt_dica, rect_dica)

        pygame.display.update()