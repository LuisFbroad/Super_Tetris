import pygame

from config import (
    LARGURA_BLOCO,
    COR_FUNDO,
    COR_GRADE,
    COR_PAINEL,
    COR_TEXTO,
    COR_TEXTO_MUTED,
    LARGURA_TELA,
    ALTURA_TELA,
    COR_BORDA_SUPER
)


class TelaJogo:

    # =========================================================
    # CORES DA INTERFACE
    # =========================================================

    COR_CYAN = (0, 240, 255)
    COR_CYAN_DARK = (0, 150, 180)

    COR_BRANCO = (245, 248, 255)
    COR_PRETO = (8, 10, 18)

    COR_CARD = (18, 21, 34)
    COR_CARD_HOVER = (28, 32, 50)

    COR_BORDA_CARD = (48, 54, 78)

    COR_PERIGO = (255, 50, 80)

    # =========================================================
    # CONSTRUTOR
    # =========================================================

    def __init__(self):

        self.largura_painel = 180

        self.largura_total = (
            LARGURA_TELA
            + self.largura_painel
        )

        self.altura_total = ALTURA_TELA

        self.superficie = pygame.display.set_mode(
            (
                self.largura_total,
                self.altura_total
            )
        )

        pygame.display.set_caption(
            "Tetris - Neon Edition"
        )

        pygame.font.init()

        self.fonte = pygame.font.SysFont(
            "Segoe UI",
            24,
            bold=True
        )

        self.fonte_titulo = pygame.font.SysFont(
            "Segoe UI",
            16,
            bold=True
        )

        self.fonte_grande = pygame.font.SysFont(
            "Segoe UI",
            40,
            bold=True
        )

        self.fonte_normal = pygame.font.SysFont(
            "Segoe UI",
            20,
            bold=True
        )

        self.fonte_pequena = pygame.font.SysFont(
            "Segoe UI",
            14
        )

    # =========================================================
    # DESENHAR JOGO
    # =========================================================

    def desenhar(
        self,
        tabuleiro,
        peca_atual,
        peca_fantasma,
        proxima_peca,
        peca_guardada,
        pontuacao,
        game_over,
        gerenciador_particulas=None,
        pausado=False
    ):

        self.superficie.fill(
            COR_FUNDO
        )

        # -----------------------------------------------------
        # GRADE
        # -----------------------------------------------------

        self._desenhar_grade()

        # -----------------------------------------------------
        # TABULEIRO
        # -----------------------------------------------------

        if tabuleiro:

            for y in range(
                tabuleiro.linhas
            ):

                for x in range(
                    tabuleiro.colunas
                ):

                    cor = tabuleiro.grade[y][x]

                    if cor:

                        self._desenhar_bloco(
                            x,
                            y,
                            cor
                        )

        # -----------------------------------------------------
        # PEÇA FANTASMA
        # -----------------------------------------------------

        if (
            peca_fantasma
            and not game_over
        ):

            self._desenhar_peca_fantasma(
                peca_fantasma
            )

        # -----------------------------------------------------
        # PEÇA ATUAL
        # -----------------------------------------------------

        if (
            peca_atual
            and not game_over
        ):

            self._desenhar_peca(
                peca_atual
            )

        # -----------------------------------------------------
        # PARTÍCULAS
        # -----------------------------------------------------

        if (
            gerenciador_particulas
            and not pausado
        ):

            gerenciador_particulas.atualizar_e_desenhar(
                self.superficie
            )

        # -----------------------------------------------------
        # PAINEL LATERAL
        # -----------------------------------------------------

        self._desenhar_painel_lateral(
            proxima_peca,
            peca_guardada,
            pontuacao
        )

        # -----------------------------------------------------
        # GAME OVER
        # -----------------------------------------------------

        if game_over:

            self._desenhar_game_over()

        # -----------------------------------------------------
        # PAUSA
        # -----------------------------------------------------

        elif pausado:

            self._desenhar_pause()

        # -----------------------------------------------------
        # ATUALIZAR DISPLAY
        # -----------------------------------------------------

        pygame.display.update()

    # =========================================================
    # DESENHAR BLOCO
    # =========================================================

    def _desenhar_bloco(
        self,
        x,
        y,
        cor,
        alpha=255
    ):

        rect = pygame.Rect(
            x * LARGURA_BLOCO,
            y * LARGURA_BLOCO,
            LARGURA_BLOCO,
            LARGURA_BLOCO
        )

        if alpha < 255:

            superficie = pygame.Surface(
                (
                    LARGURA_BLOCO,
                    LARGURA_BLOCO
                ),
                pygame.SRCALPHA
            )

            superficie.fill(
                (
                    *cor[:3],
                    alpha
                )
            )

            self.superficie.blit(
                superficie,
                rect.topleft
            )

        else:

            pygame.draw.rect(
                self.superficie,
                cor,
                rect
            )

            pygame.draw.rect(
                self.superficie,
                (255, 255, 255),
                rect,
                width=1
            )

    # =========================================================
    # DESENHAR PEÇA
    # =========================================================

    def _desenhar_peca(
        self,
        peca
    ):

        for y, linha in enumerate(
            peca.formato
        ):

            for x, valor in enumerate(
                linha
            ):

                if valor:

                    px = peca.x + x
                    py = peca.y + y

                    if py >= 0:

                        self._desenhar_bloco(
                            px,
                            py,
                            peca.cor
                        )

                        if getattr(
                            peca,
                            "is_super",
                            False
                        ):

                            rect = pygame.Rect(
                                px * LARGURA_BLOCO,
                                py * LARGURA_BLOCO,
                                LARGURA_BLOCO,
                                LARGURA_BLOCO
                            )

                            pygame.draw.rect(
                                self.superficie,
                                COR_BORDA_SUPER,
                                rect,
                                width=2
                            )

    # =========================================================
    # PEÇA FANTASMA
    # =========================================================

    def _desenhar_peca_fantasma(
        self,
        fantasma
    ):

        for y, linha in enumerate(
            fantasma.formato
        ):

            for x, valor in enumerate(
                linha
            ):

                if valor:

                    px = fantasma.x + x
                    py = fantasma.y + y

                    if py >= 0:

                        self._desenhar_bloco(
                            px,
                            py,
                            fantasma.cor,
                            alpha=60
                        )

    # =========================================================
    # GRADE
    # =========================================================

    def _desenhar_grade(self):

        for x in range(
            0,
            LARGURA_TELA,
            LARGURA_BLOCO
        ):

            pygame.draw.line(
                self.superficie,
                COR_GRADE,
                (x, 0),
                (x, ALTURA_TELA)
            )

        for y in range(
            0,
            ALTURA_TELA,
            LARGURA_BLOCO
        ):

            pygame.draw.line(
                self.superficie,
                COR_GRADE,
                (0, y),
                (LARGURA_TELA, y)
            )

    # =========================================================
    # PAINEL LATERAL
    # =========================================================

    def _desenhar_painel_lateral(
        self,
        proxima_peca,
        peca_guardada,
        pontuacao
    ):

        x_painel = LARGURA_TELA

        rect_painel = pygame.Rect(
            x_painel,
            0,
            self.largura_painel,
            self.altura_total
        )

        pygame.draw.rect(
            self.superficie,
            COR_PAINEL,
            rect_painel
        )

        pygame.draw.line(
            self.superficie,
            self.COR_BORDA_CARD,
            (x_painel, 0),
            (
                x_painel,
                self.altura_total
            ),
            width=2
        )

        # -----------------------------------------------------
        # PONTUAÇÃO
        # -----------------------------------------------------

        txt_titulo_pts = (
            self.fonte_titulo.render(
                "PONTUAÇÃO",
                True,
                COR_TEXTO_MUTED
            )
        )

        txt_pts = self.fonte.render(
            str(pontuacao),
            True,
            COR_TEXTO
        )

        self.superficie.blit(
            txt_titulo_pts,
            (
                x_painel + 20,
                30
            )
        )

        self.superficie.blit(
            txt_pts,
            (
                x_painel + 20,
                55
            )
        )

        # -----------------------------------------------------
        # HOLD
        # -----------------------------------------------------

        txt_hold = (
            self.fonte_titulo.render(
                "GUARDADA (C)",
                True,
                COR_TEXTO_MUTED
            )
        )

        self.superficie.blit(
            txt_hold,
            (
                x_painel + 20,
                110
            )
        )

        if peca_guardada:

            self._desenhar_miniatura(
                peca_guardada,
                x_painel + 30,
                140
            )

        # -----------------------------------------------------
        # PRÓXIMA PEÇA
        # -----------------------------------------------------

        txt_prox = (
            self.fonte_titulo.render(
                "PRÓXIMA PEÇA",
                True,
                COR_TEXTO_MUTED
            )
        )

        self.superficie.blit(
            txt_prox,
            (
                x_painel + 20,
                240
            )
        )

        if proxima_peca:

            self._desenhar_miniatura(
                proxima_peca,
                x_painel + 30,
                270
            )

    # =========================================================
    # MINIATURA
    # =========================================================

    def _desenhar_miniatura(
        self,
        peca,
        offset_x,
        offset_y
    ):

        tamanho = LARGURA_BLOCO // 2

        for y, linha in enumerate(
            peca.formato
        ):

            for x, valor in enumerate(
                linha
            ):

                if valor:

                    rect = pygame.Rect(
                        offset_x + x * tamanho,
                        offset_y + y * tamanho,
                        tamanho,
                        tamanho
                    )

                    pygame.draw.rect(
                        self.superficie,
                        peca.cor,
                        rect
                    )

                    pygame.draw.rect(
                        self.superficie,
                        (255, 255, 255),
                        rect,
                        width=1
                    )

    # =========================================================
    # PAUSA
    # =========================================================

    def _desenhar_pause(self):

        # -----------------------------------------------------
        # OVERLAY
        # -----------------------------------------------------

        overlay = pygame.Surface(
            (
                self.largura_total,
                self.altura_total
            ),
            pygame.SRCALPHA
        )

        overlay.fill(
            (
                5,
                7,
                15,
                205
            )
        )

        self.superficie.blit(
            overlay,
            (0, 0)
        )

        # -----------------------------------------------------
        # CARD
        # -----------------------------------------------------

        largura_card = 380
        altura_card = 210

        x_card = (
            self.largura_total
            - largura_card
        ) // 2

        y_card = (
            self.altura_total
            - altura_card
        ) // 2

        rect_card = pygame.Rect(
            x_card,
            y_card,
            largura_card,
            altura_card
        )

        pygame.draw.rect(
            self.superficie,
            self.COR_CARD,
            rect_card,
            border_radius=14
        )

        pygame.draw.rect(
            self.superficie,
            self.COR_CYAN,
            rect_card,
            width=2,
            border_radius=14
        )

        # -----------------------------------------------------
        # TÍTULO
        # -----------------------------------------------------

        titulo = self.fonte_grande.render(
            "PAUSADO",
            True,
            self.COR_CYAN
        )

        rect_titulo = titulo.get_rect(
            center=(
                self.largura_total // 2,
                y_card + 55
            )
        )

        self.superficie.blit(
            titulo,
            rect_titulo
        )

        # -----------------------------------------------------
        # CONTINUAR
        # -----------------------------------------------------

        texto = self.fonte_normal.render(
            "ESC  •  Continuar",
            True,
            COR_TEXTO
        )

        rect_texto = texto.get_rect(
            center=(
                self.largura_total // 2,
                y_card + 115
            )
        )

        self.superficie.blit(
            texto,
            rect_texto
        )

        # -----------------------------------------------------
        # TEXTO SECUNDÁRIO
        # -----------------------------------------------------

        texto_secundario = (
            self.fonte_pequena.render(
                "O jogo está pausado",
                True,
                COR_TEXTO_MUTED
            )
        )

        rect_secundario = (
            texto_secundario.get_rect(
                center=(
                    self.largura_total // 2,
                    y_card + 155
                )
            )
        )

        self.superficie.blit(
            texto_secundario,
            rect_secundario
        )

    # =========================================================
    # GAME OVER
    # =========================================================

    def _desenhar_game_over(self):

        overlay = pygame.Surface(
            (
                self.largura_total,
                self.altura_total
            ),
            pygame.SRCALPHA
        )

        overlay.fill(
            (
                10,
                10,
                20,
                210
            )
        )

        self.superficie.blit(
            overlay,
            (0, 0)
        )

        txt_go = self.fonte_grande.render(
            "GAME OVER",
            True,
            self.COR_PERIGO
        )

        txt_restart = (
            self.fonte_titulo.render(
                "[R] Reiniciar  |  [ESC] Menu",
                True,
                COR_TEXTO
            )
        )

        rect_go = txt_go.get_rect(
            center=(
                self.largura_total // 2,
                self.altura_total // 2 - 20
            )
        )

        rect_res = txt_restart.get_rect(
            center=(
                self.largura_total // 2,
                self.altura_total // 2 + 35
            )
        )

        self.superficie.blit(
            txt_go,
            rect_go
        )

        self.superficie.blit(
            txt_restart,
            rect_res
        )

    # =========================================================
    # MENU
    # =========================================================

    def desenhar_menu(
        self,
        opcoes,
        indice_selecionado
    ):

        self.superficie.fill(
            COR_FUNDO
        )

        # -----------------------------------------------------
        # TÍTULO
        # -----------------------------------------------------

        fonte_titulo_grande = (
            pygame.font.SysFont(
                "Segoe UI",
                42,
                bold=True
            )
        )

        txt_titulo = (
            fonte_titulo_grande.render(
                "TETRIS",
                True,
                self.COR_CYAN
            )
        )

        txt_sub = (
            self.fonte_titulo.render(
                "NEON EDITION",
                True,
                COR_TEXTO_MUTED
            )
        )

        rect_tit = txt_titulo.get_rect(
            center=(
                self.largura_total // 2,
                80
            )
        )

        rect_sub = txt_sub.get_rect(
            center=(
                self.largura_total // 2,
                125
            )
        )

        self.superficie.blit(
            txt_titulo,
            rect_tit
        )

        self.superficie.blit(
            txt_sub,
            rect_sub
        )

        # -----------------------------------------------------
        # INSTRUÇÃO
        # -----------------------------------------------------

        txt_instrucao = (
            self.fonte_titulo.render(
                "Selecione a Dificuldade:",
                True,
                COR_TEXTO
            )
        )

        rect_inst = txt_instrucao.get_rect(
            center=(
                self.largura_total // 2,
                180
            )
        )

        self.superficie.blit(
            txt_instrucao,
            rect_inst
        )

        # -----------------------------------------------------
        # BOTÕES
        # -----------------------------------------------------

        y_inicial = 230

        for i, (
            chave,
            dados
        ) in enumerate(
            opcoes.items()
        ):

            selecionado = (
                i == indice_selecionado
            )

            largura_btn = 200
            altura_btn = 45

            x_btn = (
                self.largura_total
                - largura_btn
            ) // 2

            y_btn = (
                y_inicial
                + i * 55
            )

            rect_btn = pygame.Rect(
                x_btn,
                y_btn,
                largura_btn,
                altura_btn
            )

            if selecionado:

                pygame.draw.rect(
                    self.superficie,
                    dados["cor"],
                    rect_btn,
                    border_radius=8
                )

                cor_texto = (
                    self.COR_PRETO
                )

            else:

                pygame.draw.rect(
                    self.superficie,
                    self.COR_CARD,
                    rect_btn,
                    border_radius=8
                )

                pygame.draw.rect(
                    self.superficie,
                    self.COR_BORDA_CARD,
                    rect_btn,
                    width=1,
                    border_radius=8
                )

                cor_texto = COR_TEXTO

            txt_opcao = (
                self.fonte_titulo.render(
                    dados["nome"].upper(),
                    True,
                    cor_texto
                )
            )

            rect_op = txt_opcao.get_rect(
                center=rect_btn.center
            )

            self.superficie.blit(
                txt_opcao,
                rect_op
            )

        # -----------------------------------------------------
        # DICA
        # -----------------------------------------------------

        txt_dica = (
            self.fonte_titulo.render(
                "↑/↓ NAVEGAR  |  ENTER CONFIRMAR",
                True,
                COR_TEXTO_MUTED
            )
        )

        rect_dica = txt_dica.get_rect(
            center=(
                self.largura_total // 2,
                self.altura_total - 40
            )
        )

        self.superficie.blit(
            txt_dica,
            rect_dica
        )

        pygame.display.update()