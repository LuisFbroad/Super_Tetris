import pygame
import random
from config import FPS, DIFICULDADES, LARGURA_BLOCO, LARGURA_TELA
from models.peca import Peca, SuperPeca
from models.tabuleiro import Tabuleiro
from views.tela import TelaJogo
from views.particula import GerenciadorParticulas

class GerenciadorJogo:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.tela = TelaJogo()
        self.gerenciador_particulas = GerenciadorParticulas()

        # Controle de Estados: "MENU" ou "JOGANDO"
        self.estado = "MENU"

        # Configuração das Opções de Dificuldade
        self.chaves_dificuldade = list(DIFICULDADES.keys())
        self.indice_dificuldade = 1  # Inicia no "MEDIO"
        self.dificuldade_atual = DIFICULDADES[self.chaves_dificuldade[self.indice_dificuldade]]

        # Variáveis do Jogo
        self.tabuleiro = None
        self.pontuacao = 0
        self.game_over = False
        self.velocidade_atual = self.dificuldade_atual["velocidade_ms"]
        self.chance_super = self.dificuldade_atual["chance_super"]
        self.tempo_ultima_queda = 0

        self.peca_atual = None
        self.proxima_peca = None
        self.peca_guardada = None
        self.pode_trocar_hold = True

        # DAS (Fluidez nos Controles)
        self.delay_das = 140
        self.intervalo_das = 35
        self.tempo_ultimo_mov = 0
        self.tecla_pressionada = None
        self.tempo_inicio_tecla = 0

    def iniciar_novo_jogo(self):
        """Prepara o jogo com a dificuldade selecionada."""
        self.tabuleiro = Tabuleiro()
        self.pontuacao = 0
        self.game_over = False
        self.velocidade_atual = self.dificuldade_atual["velocidade_ms"]
        self.chance_super = self.dificuldade_atual["chance_super"]
        self.tempo_ultima_queda = pygame.time.get_ticks()

        self.peca_atual = self._gerar_nova_peca()
        self.proxima_peca = self._gerar_nova_peca()
        self.peca_guardada = None
        self.pode_trocar_hold = True
        self.estado = "JOGANDO"

    def _gerar_nova_peca(self):
        if random.random() < self.chance_super:
            return SuperPeca()
        return Peca()

    def _criar_fantasma(self):
        if getattr(self.peca_atual, 'is_super', False):
            fantasma = SuperPeca()
        else:
            fantasma = Peca()

        fantasma.x = self.peca_atual.x
        fantasma.y = self.peca_atual.y
        fantasma.formato = [linha[:] for linha in self.peca_atual.formato]

        while self.tabuleiro.posicao_valida(fantasma):
            fantasma.y += 1
        fantasma.y -= 1

        return fantasma

    def _armazenar_peca(self):
        if not self.pode_trocar_hold:
            return

        peca_temp = self.peca_atual
        peca_temp.x = 3
        peca_temp.y = 0

        if self.peca_guardada is None:
            self.peca_guardada = peca_temp
            self.peca_atual = self.proxima_peca
            self.proxima_peca = self._gerar_nova_peca()
        else:
            self.peca_atual = self.peca_guardada
            self.peca_guardada = peca_temp

        self.pode_trocar_hold = False

    def processar_eventos(self):
        agora = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            if evento.type == pygame.KEYDOWN:
                # --- EVENTOS NO MENU ---
                if self.estado == "MENU":
                    if evento.key == pygame.K_UP:
                        self.indice_dificuldade = (self.indice_dificuldade - 1) % len(self.chaves_dificuldade)
                    elif evento.key == pygame.K_DOWN:
                        self.indice_dificuldade = (self.indice_dificuldade + 1) % len(self.chaves_dificuldade)
                    elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                        chave = self.chaves_dificuldade[self.indice_dificuldade]
                        self.dificuldade_atual = DIFICULDADES[chave]
                        self.iniciar_novo_jogo()

                # --- EVENTOS DURANTE A PARTIDA ---
                elif self.estado == "JOGANDO":
                    if self.game_over:
                        if evento.key == pygame.K_r:
                            self.iniciar_novo_jogo()
                        elif evento.key == pygame.K_ESCAPE:
                            self.estado = "MENU"
                    else:
                        if evento.key == pygame.K_UP:
                            self._rotacionar_peca()
                        elif evento.key == pygame.K_SPACE:
                            self._cair_instantaneo()
                        elif evento.key in (pygame.K_c, pygame.K_LSHIFT):
                            self._armazenar_peca()

                        if evento.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN):
                            self.tecla_pressionada = evento.key
                            self.tempo_inicio_tecla = agora
                            self.tempo_ultimo_mov = agora
                            self._executar_movimento(evento.key)

            if evento.type == pygame.KEYUP:
                if evento.key == self.tecla_pressionada:
                    self.tecla_pressionada = None

        if self.estado == "JOGANDO" and self.tecla_pressionada and not self.game_over:
            tempo_segurando = agora - self.tempo_inicio_tecla
            if tempo_segurando > self.delay_das:
                if agora - self.tempo_ultimo_mov > self.intervalo_das:
                    self._executar_movimento(self.tecla_pressionada)
                    self.tempo_ultimo_mov = agora

        return True

    def _executar_movimento(self, tecla):
        if tecla == pygame.K_LEFT:
            self._mover(-1, 0)
        elif tecla == pygame.K_RIGHT:
            self._mover(1, 0)
        elif tecla == pygame.K_DOWN:
            self._mover(0, 1)

    def _mover(self, dx, dy):
        self.peca_atual.x += dx
        self.peca_atual.y += dy
        
        if not self.tabuleiro.posicao_valida(self.peca_atual):
            self.peca_atual.x -= dx
            self.peca_atual.y -= dy
            return False
        return True

    def _rotacionar_peca(self):
        self.peca_atual.rotacionar()
        if not self.tabuleiro.posicao_valida(self.peca_atual):
            for _ in range(3):
                self.peca_atual.rotacionar()

    def _cair_instantaneo(self):
        while self._mover(0, 1):
            pass
        self._fixar_e_proxima()

    def _fixar_e_proxima(self):
        self.tabuleiro.fixar_peca(self.peca_atual)
        
        if getattr(self.peca_atual, 'is_super', False):
            self.pontuacao += 50

        linhas_para_limpar = []
        for y in range(self.tabuleiro.linhas):
            if all(self.tabuleiro.grade[y]):
                linhas_para_limpar.append(y)

        linhas_limpas = self.tabuleiro.limpar_linhas()
        if linhas_limpas > 0:
            for y in linhas_para_limpar:
                self.gerenciador_particulas.criar_explosao_linha(
                    y * LARGURA_BLOCO + LARGURA_BLOCO // 2, 
                    LARGURA_TELA, 
                    self.peca_atual.cor
                )

            tabela_pontos = {1: 100, 2: 300, 3: 500, 4: 800}
            self.pontuacao += tabela_pontos.get(linhas_limpas, linhas_limpas * 200)

        self.peca_atual = self.proxima_peca
        self.proxima_peca = self._gerar_nova_peca()
        self.pode_trocar_hold = True

        if not self.tabuleiro.posicao_valida(self.peca_atual):
            self.game_over = True

    def atualizar(self):
        if self.estado != "JOGANDO" or self.game_over:
            return

        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultima_queda > self.velocidade_atual:
            if not self._mover(0, 1):
                self._fixar_e_proxima()
            self.tempo_ultima_queda = agora

    def executar(self):
        rodando = True
        while rodando:
            rodando = self.processar_eventos()
            self.atualizar()
            
            if self.estado == "MENU":
                self.tela.desenhar_menu(DIFICULDADES, self.indice_dificuldade)
            elif self.estado == "JOGANDO":
                peca_fantasma = self._criar_fantasma() if not self.game_over else None

                self.tela.desenhar(
                    tabuleiro=self.tabuleiro, 
                    peca_atual=self.peca_atual,
                    peca_fantasma=peca_fantasma,
                    proxima_peca=self.proxima_peca,
                    peca_guardada=self.peca_guardada,
                    pontuacao=self.pontuacao, 
                    game_over=self.game_over,
                    gerenciador_particulas=self.gerenciador_particulas
                )
                
            self.clock.tick(FPS)

        pygame.quit()