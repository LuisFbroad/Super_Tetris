import pygame
import sys
from config import (
    COLUNAS, LINHAS, FPS, DIFICULDADES, LARGURA_BLOCO
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
        self.indice_dificuldade = 1  # Médio por padrão
        self.estado = "MENU"  # MENU ou JOGANDO

        # Controles de QoL e Movimento
        self.tempo_lock_delay = 500  # 500ms de tolerância no chão
        self.timer_lock = 0
        self.pode_trocar_hold = True

        # Timers para movimentação contínua (DAS/ARR)
        self.tempo_ultimo_mov_x = 0
        self.atraso_mov_x = 120  # Intervalo (ms) para mover pros lados ao segurar

    def _obter_config_dificuldade(self):
        chaves = list(DIFICULDADES.keys())
        chave_atual = chaves[self.indice_dificuldade]
        return DIFICULDADES[chave_atual]

    def iniciar_novo_jogo(self):
        config_dif = self._obter_config_dificuldade()
        self.velocidade_queda_ms = config_dif["velocidade_ms"]
        self.chance_super = config_dif["chance_super"]

        self.tabuleiro = Tabuleiro(COLUNAS, LINHAS)
        self.pontuacao = 0
        self.game_over = False

        self.proxima_peca = self._gerar_peca()
        self.peca_atual = self._gerar_peca()
        self.peca_guardada = None

        self.tempo_ultima_queda = pygame.time.get_ticks()
        self.timer_lock = 0
        self.pode_trocar_hold = True
        self.estado = "JOGANDO"

    def _gerar_peca(self):
        import random
        x_inicial = COLUNAS // 2 - 1
        if random.random() < self.chance_super:
            return SuperPeca(x_inicial, 0)
        return Peca(x_inicial, 0)

    def _obter_peca_fantasma(self):
        if not self.peca_atual:
            return None
        
        import copy
        fantasma = copy.deepcopy(self.peca_atual)
        while not self.tabuleiro.verificar_colisao(fantasma):
            fantasma.y += 1
        fantasma.y -= 1
        return fantasma

    def _trocar_peca_hold(self):
        if not self.pode_trocar_hold:
            return

        if self.peca_guardada is None:
            self.peca_guardada = self.peca_atual
            self.peca_atual = self.proxima_peca
            self.proxima_peca = self._gerar_peca()
        else:
            self.peca_guardada, self.peca_atual = self.peca_atual, self.peca_guardada

        self.peca_atual.x = COLUNAS // 2 - 1
        self.peca_atual.y = 0
        self.pode_trocar_hold = False
        self.timer_lock = 0

    def _hard_drop(self):
        if not self.peca_atual or self.game_over:
            return

        while not self.tabuleiro.verificar_colisao(self.peca_atual):
            self.peca_atual.y += 1
            self.pontuacao += 2

        self.peca_atual.y -= 1
        self._fixar_peca_atual()

    def _fixar_peca_atual(self):
        self.tabuleiro.fixar_peca(self.peca_atual)

        linhas_limpas = self.tabuleiro.limpar_linhas_completas()
        if linhas_limpas > 0:
            self.pontuacao += (linhas_limpas ** 2) * 100

        self.peca_atual = self.proxima_peca
        self.proxima_peca = self._gerar_peca()
        self.pode_trocar_hold = True
        self.timer_lock = 0

        if self.tabuleiro.verificar_colisao(self.peca_atual):
            self.game_over = True

    def _esta_no_chao(self):
        self.peca_atual.y += 1
        colidiu = self.tabuleiro.verificar_colisao(self.peca_atual)
        self.peca_atual.y -= 1
        return colidiu

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if self.estado == "MENU":
                    self._processar_menu(evento.key)
                elif self.estado == "JOGANDO":
                    # Ações pontuais no clique único
                    if self.game_over:
                        if evento.key == pygame.K_r:
                            self.iniciar_novo_jogo()
                        elif evento.key == pygame.K_ESCAPE:
                            self.estado = "MENU"
                    else:
                        if evento.key in (pygame.K_UP, pygame.K_w):
                            self.peca_atual.girar(self.tabuleiro)
                        elif evento.key == pygame.K_SPACE:
                            self._hard_drop()
                        elif evento.key in (pygame.K_c, pygame.K_LSHIFT, pygame.K_RSHIFT):
                            self._trocar_peca_hold()
                        elif evento.key == pygame.K_ESCAPE:
                            self.estado = "MENU"

    def _processar_menu(self, tecla):
        qtd_dificuldades = len(DIFICULDADES)
        if tecla in (pygame.K_UP, pygame.K_w):
            self.indice_dificuldade = (self.indice_dificuldade - 1) % qtd_dificuldades
        elif tecla in (pygame.K_DOWN, pygame.K_s):
            self.indice_dificuldade = (self.indice_dificuldade + 1) % qtd_dificuldades
        elif tecla in (pygame.K_RETURN, pygame.K_SPACE):
            self.iniciar_novo_jogo()

    def _processar_entradas_continuas(self):
        """Processa movimento contínuo ao segurar teclas."""
        if not self.peca_atual or self.game_over:
            return

        agora = pygame.time.get_ticks()
        teclas = pygame.key.get_pressed()

        # Movimentação Lateral Contínua (Esquerda / Direita)
        if agora - self.tempo_ultimo_mov_x > self.atraso_mov_x:
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                self.peca_atual.x -= 1
                if self.tabuleiro.verificar_colisao(self.peca_atual):
                    self.peca_atual.x += 1
                self.tempo_ultimo_mov_x = agora

            elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                self.peca_atual.x += 1
                if self.tabuleiro.verificar_colisao(self.peca_atual):
                    self.peca_atual.x -= 1
                self.tempo_ultimo_mov_x = agora

    def atualizar(self):
        if self.estado != "JOGANDO" or self.game_over:
            return

        agora = pygame.time.get_ticks()

        # Processa movimentação contínua das teclas seguradas
        self._processar_entradas_continuas()

        # Soft Drop: Acelera muito a queda ao segurar DOWN ou S
        teclas = pygame.key.get_pressed()
        soft_drop_ativo = teclas[pygame.K_DOWN] or teclas[pygame.K_s]
        vel_atual = 40 if soft_drop_ativo else self.velocidade_queda_ms

        # Queda por gravidade
        if agora - self.tempo_ultima_queda > vel_atual:
            self.peca_atual.y += 1
            if self.tabuleiro.verificar_colisao(self.peca_atual):
                self.peca_atual.y -= 1
            else:
                if soft_drop_ativo:
                    self.pontuacao += 1  # Pontuação extra por Soft Drop
                self.tempo_ultima_queda = agora

        # Lógica de Lock Delay (Tolerância no chão)
        if self._esta_no_chao():
            if self.timer_lock == 0:
                self.timer_lock = agora
            elif agora - self.timer_lock >= self.tempo_lock_delay:
                self._fixar_peca_atual()
        else:
            self.timer_lock = 0

    def executar(self):
        while True:
            self.processar_eventos()

            if self.estado == "MENU":
                self.tela.desenhar_menu(DIFICULDADES, self.indice_dificuldade)
            elif self.estado == "JOGANDO":
                self.atualizar()
                fantasma = self._obter_peca_fantasma()
                self.tela.desenhar(
                    tabuleiro=self.tabuleiro,
                    peca_atual=self.peca_atual,
                    peca_fantasma=fantasma,
                    proxima_peca=self.proxima_peca,
                    peca_guardada=self.peca_guardada,
                    pontuacao=self.pontuacao,
                    game_over=self.game_over,
                    gerenciador_particulas=self.gerenciador_particulas
                )

            self.clock.tick(FPS)