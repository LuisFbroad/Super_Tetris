import pygame
import sys

from config import (
    COLUNAS,
    LINHAS,
    FPS,
    DIFICULDADES,
    LARGURA_BLOCO
)

from models.tabuleiro import Tabuleiro
from models.peca import Peca, SuperPeca
from views.tela import TelaJogo
from views.particula import GerenciadorParticulas


class GerenciadorJogo:

    def __init__(self):
        pygame.init()

        self.tela = TelaJogo()
        self.clock = pygame.time.Clock()

        self.gerenciador_particulas = GerenciadorParticulas()

        # Índice da dificuldade selecionada
        self.indice_dificuldade = 1

        # Estados:
        # MENU
        # JOGANDO
        # PAUSADO
        self.estado = "MENU"

        # Lock Delay
        self.tempo_lock_delay = 500
        self.timer_lock = 0

        # Hold
        self.pode_trocar_hold = True

        # Movimento lateral
        self.tempo_ultimo_mov_x = 0
        self.atraso_mov_x = 120

    # =========================================================
    # CONFIGURAÇÃO DA DIFICULDADE
    # =========================================================

    def _obter_config_dificuldade(self):
        chaves = list(DIFICULDADES.keys())

        chave_atual = chaves[self.indice_dificuldade]

        return DIFICULDADES[chave_atual]

    # =========================================================
    # INICIAR NOVO JOGO
    # =========================================================

    def iniciar_novo_jogo(self):

        config_dif = self._obter_config_dificuldade()

        self.velocidade_queda_ms = config_dif["velocidade_ms"]
        self.chance_super = config_dif["chance_super"]

        # Tabuleiro
        self.tabuleiro = Tabuleiro(
            COLUNAS,
            LINHAS
        )

        # Pontuação
        self.pontuacao = 0

        # Game Over
        self.game_over = False

        # Peças
        self.proxima_peca = self._gerar_peca()
        self.peca_atual = self._gerar_peca()
        self.peca_guardada = None

        # Timers
        agora = pygame.time.get_ticks()

        self.tempo_ultima_queda = agora
        self.timer_lock = 0
        self.tempo_ultimo_mov_x = agora

        # Hold
        self.pode_trocar_hold = True

        # Estado
        self.estado = "JOGANDO"

    # =========================================================
    # GERAR PEÇA
    # =========================================================

    def _gerar_peca(self):

        import random

        x_inicial = COLUNAS // 2 - 1

        if random.random() < self.chance_super:
            return SuperPeca(
                x_inicial,
                0
            )

        return Peca(
            x_inicial,
            0
        )

    # =========================================================
    # PEÇA FANTASMA
    # =========================================================

    def _obter_peca_fantasma(self):

        if not self.peca_atual:
            return None

        import copy

        fantasma = copy.deepcopy(
            self.peca_atual
        )

        while not self.tabuleiro.verificar_colisao(
            fantasma
        ):
            fantasma.y += 1

        fantasma.y -= 1

        return fantasma

    # =========================================================
    # HOLD
    # =========================================================

    def _trocar_peca_hold(self):

        if not self.pode_trocar_hold:
            return

        if self.peca_guardada is None:

            self.peca_guardada = self.peca_atual

            self.peca_atual = self.proxima_peca

            self.proxima_peca = self._gerar_peca()

        else:

            (
                self.peca_guardada,
                self.peca_atual
            ) = (
                self.peca_atual,
                self.peca_guardada
            )

        self.peca_atual.x = COLUNAS // 2 - 1
        self.peca_atual.y = 0

        self.pode_trocar_hold = False

        self.timer_lock = 0

    # =========================================================
    # HARD DROP
    # =========================================================

    def _hard_drop(self):

        if (
            not self.peca_atual
            or self.game_over
        ):
            return

        while not self.tabuleiro.verificar_colisao(
            self.peca_atual
        ):

            self.peca_atual.y += 1

            self.pontuacao += 2

        self.peca_atual.y -= 1

        self._fixar_peca_atual()

    # =========================================================
    # FIXAR PEÇA
    # =========================================================

    def _fixar_peca_atual(self):

        self.tabuleiro.fixar_peca(
            self.peca_atual
        )

        linhas_limpas = (
            self.tabuleiro.limpar_linhas_completas()
        )

        if linhas_limpas > 0:

            self.pontuacao += (
                linhas_limpas ** 2
            ) * 100

        # Próxima peça
        self.peca_atual = self.proxima_peca

        self.proxima_peca = self._gerar_peca()

        # Permite novo Hold
        self.pode_trocar_hold = True

        self.timer_lock = 0

        # Verifica Game Over
        if self.tabuleiro.verificar_colisao(
            self.peca_atual
        ):
            self.game_over = True

    # =========================================================
    # VERIFICAR SE ESTÁ NO CHÃO
    # =========================================================

    def _esta_no_chao(self):

        self.peca_atual.y += 1

        colidiu = (
            self.tabuleiro.verificar_colisao(
                self.peca_atual
            )
        )

        self.peca_atual.y -= 1

        return colidiu

    # =========================================================
    # PROCESSAR EVENTOS
    # =========================================================

    def processar_eventos(self):

        for evento in pygame.event.get():

            # -------------------------------------------------
            # FECHAR JOGO
            # -------------------------------------------------

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            # -------------------------------------------------
            # APENAS EVENTOS DE TECLADO
            # -------------------------------------------------

            if evento.type != pygame.KEYDOWN:
                continue

            tecla = evento.key

            # =================================================
            # MENU
            # =================================================

            if self.estado == "MENU":

                self._processar_menu(tecla)

                continue

            # =================================================
            # GAME OVER
            # =================================================

            if (
                self.estado == "JOGANDO"
                and self.game_over
            ):

                if tecla == pygame.K_r:

                    self.iniciar_novo_jogo()

                elif tecla == pygame.K_ESCAPE:

                    self.estado = "MENU"

                continue

            # =================================================
            # PAUSADO
            # =================================================

            if self.estado == "PAUSADO":

                if tecla == pygame.K_ESCAPE:

                    self.estado = "JOGANDO"

                    # Evita que a peça caia imediatamente
                    # depois de sair da pausa.

                    agora = pygame.time.get_ticks()

                    self.tempo_ultima_queda = agora
                    self.tempo_ultimo_mov_x = agora

                continue

            # =================================================
            # JOGANDO
            # =================================================

            if self.estado == "JOGANDO":

                # ESC = PAUSAR
                if tecla == pygame.K_ESCAPE:

                    self.estado = "PAUSADO"

                    continue

                # Rotação
                if tecla in (
                    pygame.K_UP,
                    pygame.K_w
                ):

                    self.peca_atual.girar(
                        self.tabuleiro
                    )

                # Hard Drop
                elif tecla == pygame.K_SPACE:

                    self._hard_drop()

                # Hold
                elif tecla in (
                    pygame.K_c,
                    pygame.K_LSHIFT,
                    pygame.K_RSHIFT
                ):

                    self._trocar_peca_hold()

    # =========================================================
    # PROCESSAR MENU
    # =========================================================

    def _processar_menu(self, tecla):

        qtd_dificuldades = len(
            DIFICULDADES
        )

        if tecla in (
            pygame.K_UP,
            pygame.K_w
        ):

            self.indice_dificuldade = (
                self.indice_dificuldade - 1
            ) % qtd_dificuldades

        elif tecla in (
            pygame.K_DOWN,
            pygame.K_s
        ):

            self.indice_dificuldade = (
                self.indice_dificuldade + 1
            ) % qtd_dificuldades

        elif tecla in (
            pygame.K_RETURN,
            pygame.K_SPACE
        ):

            self.iniciar_novo_jogo()

    # =========================================================
    # MOVIMENTO CONTÍNUO
    # =========================================================

    def _processar_entradas_continuas(self):

        if (
            not self.peca_atual
            or self.game_over
            or self.estado != "JOGANDO"
        ):
            return

        agora = pygame.time.get_ticks()

        teclas = pygame.key.get_pressed()

        if (
            agora - self.tempo_ultimo_mov_x
            > self.atraso_mov_x
        ):

            # Esquerda
            if (
                teclas[pygame.K_LEFT]
                or teclas[pygame.K_a]
            ):

                self.peca_atual.x -= 1

                if self.tabuleiro.verificar_colisao(
                    self.peca_atual
                ):

                    self.peca_atual.x += 1

                self.tempo_ultimo_mov_x = agora

            # Direita
            elif (
                teclas[pygame.K_RIGHT]
                or teclas[pygame.K_d]
            ):

                self.peca_atual.x += 1

                if self.tabuleiro.verificar_colisao(
                    self.peca_atual
                ):

                    self.peca_atual.x -= 1

                self.tempo_ultimo_mov_x = agora

    # =========================================================
    # ATUALIZAR JOGO
    # =========================================================

    def atualizar(self):

        if (
            self.estado != "JOGANDO"
            or self.game_over
        ):
            return

        agora = pygame.time.get_ticks()

        # Movimento lateral
        self._processar_entradas_continuas()

        # Teclas
        teclas = pygame.key.get_pressed()

        # Soft Drop
        soft_drop_ativo = (
            teclas[pygame.K_DOWN]
            or teclas[pygame.K_s]
        )

        vel_atual = (
            40
            if soft_drop_ativo
            else self.velocidade_queda_ms
        )

        # -------------------------------------------------
        # QUEDA AUTOMÁTICA
        # -------------------------------------------------

        if (
            agora - self.tempo_ultima_queda
            > vel_atual
        ):

            self.peca_atual.y += 1

            if self.tabuleiro.verificar_colisao(
                self.peca_atual
            ):

                self.peca_atual.y -= 1

            else:

                if soft_drop_ativo:
                    self.pontuacao += 1

                self.tempo_ultima_queda = agora

        # -------------------------------------------------
        # LOCK DELAY
        # -------------------------------------------------

        if self._esta_no_chao():

            if self.timer_lock == 0:

                self.timer_lock = agora

            elif (
                agora - self.timer_lock
                >= self.tempo_lock_delay
            ):

                self._fixar_peca_atual()

        else:

            self.timer_lock = 0

    # =========================================================
    # LOOP PRINCIPAL
    # =========================================================

    def executar(self):

        while True:

            self.processar_eventos()

            # =================================================
            # MENU
            # =================================================

            if self.estado == "MENU":

                self.tela.desenhar_menu(
                    DIFICULDADES,
                    self.indice_dificuldade
                )

            # =================================================
            # JOGANDO
            # =================================================

            elif self.estado == "JOGANDO":

                self.atualizar()

                fantasma = (
                    self._obter_peca_fantasma()
                )

                self.tela.desenhar(
                    tabuleiro=self.tabuleiro,
                    peca_atual=self.peca_atual,
                    peca_fantasma=fantasma,
                    proxima_peca=self.proxima_peca,
                    peca_guardada=self.peca_guardada,
                    pontuacao=self.pontuacao,
                    game_over=self.game_over,
                    gerenciador_particulas=(
                        self.gerenciador_particulas
                    ),
                    pausado=False
                )

            # =================================================
            # PAUSADO
            # =================================================

            elif self.estado == "PAUSADO":

                # NÃO chama atualizar()
                #
                # Portanto:
                # - peça não cai
                # - pontuação não muda
                # - lock delay para
                # - movimento para

                fantasma = (
                    self._obter_peca_fantasma()
                )

                self.tela.desenhar(
                    tabuleiro=self.tabuleiro,
                    peca_atual=self.peca_atual,
                    peca_fantasma=fantasma,
                    proxima_peca=self.proxima_peca,
                    peca_guardada=self.peca_guardada,
                    pontuacao=self.pontuacao,
                    game_over=False,
                    gerenciador_particulas=None,
                    pausado=True
                )

            self.clock.tick(FPS)