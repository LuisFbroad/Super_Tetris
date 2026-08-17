import pygame

from models.peca import Peca
from models.survival.torre import Torre
from physics.corpo_peca import CorpoPeca
from views.tela_survival import TelaSurvival


class ModoSurvival:

    def __init__(self, tela):

        self.tela = tela

        self.largura = tela.get_width()
        self.altura = tela.get_height()

        self.tamanho_bloco = 30

        self.relogio = pygame.time.Clock()

        self.tela_survival = TelaSurvival(
            self.largura,
            self.altura,
            self.tamanho_bloco
        )

        self.opcoes = [
            "INICIAR",
            "DIFICULDADE",
            "CONTROLES",
            "VOLTAR"
        ]

        self.indice = 0

        self.estado = "MENU"

        self.torre = None

        self.rodando = True

    # =========================================================
    # ENTRADA DO MODO SURVIVAL
    # =========================================================

    def executar(self):

        while self.rodando:

            dt = self.relogio.tick(60) / 1000.0

            if self.estado == "MENU":

                resultado = self.processar_menu()

                if resultado == "JOGAR":
                    self.iniciar_jogo()

                elif resultado == "VOLTAR":
                    return "MENU"

                self.desenhar_menu()

            elif self.estado == "JOGO":

                self.processar_jogo()

                self.atualizar_jogo(dt)

                self.desenhar_jogo()

            pygame.display.flip()

        return "MENU"

    # =========================================================
    # MENU SURVIVAL
    # =========================================================

    def processar_menu(self):

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if evento.type != pygame.KEYDOWN:
                continue

            if evento.key == pygame.K_UP:

                self.indice -= 1

                if self.indice < 0:
                    self.indice = len(self.opcoes) - 1

            elif evento.key == pygame.K_DOWN:

                self.indice += 1

                if self.indice >= len(self.opcoes):
                    self.indice = 0

            elif evento.key == pygame.K_RETURN:

                opcao = self.opcoes[self.indice]

                if opcao == "INICIAR":
                    return "JOGAR"

                if opcao == "VOLTAR":
                    return "VOLTAR"

        return None

    # =========================================================
    # INICIAR PARTIDA
    # =========================================================

    def iniciar_jogo(self):

        self.estado = "JOGO"

        self.torre = Torre(
            self.largura,
            self.altura
        )

        self.criar_peca()

    # =========================================================
    # CRIAR PEÇA
    # =========================================================

    def criar_peca(self):

        # Cria uma peça normal do Tetris
        peca = Peca(
            0,
            0
        )

        # Calcula a largura da peça em blocos
        largura_blocos = max(
            len(linha)
            for linha in peca.formato
        )

        largura_peca = (
            largura_blocos *
            self.tamanho_bloco
        )

        # Posição inicial
        x = (
            self.largura -
            largura_peca
        ) / 2

        y = 80

        # Transforma a peça normal
        # em uma peça física
        corpo = CorpoPeca(
            peca,
            self.tamanho_bloco,
            x,
            y
        )

        # Adiciona à torre
        self.torre.adicionar_peca(
            corpo
        )

    # =========================================================
    # EVENTOS DURANTE O JOGO
    # =========================================================

    def processar_jogo(self):

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:

                    self.estado = "MENU"

                    self.torre = None

    # =========================================================
    # FÍSICA
    # =========================================================

    def atualizar_jogo(self, dt):

        if self.torre is None:
            return

        self.torre.atualizar(
            dt
        )

    # =========================================================
    # DESENHAR MENU
    # =========================================================

    def desenhar_menu(self):

        self.tela.fill(
            (10, 10, 18)
        )

        fonte_titulo = pygame.font.Font(
            None,
            70
        )

        fonte = pygame.font.Font(
            None,
            42
        )

        titulo = fonte_titulo.render(
            "MODO SURVIVAL",
            True,
            (255, 255, 255)
        )

        titulo_rect = titulo.get_rect(
            center=(
                self.largura // 2,
                100
            )
        )

        self.tela.blit(
            titulo,
            titulo_rect
        )

        for i, opcao in enumerate(
            self.opcoes
        ):

            selecionada = (
                i == self.indice
            )

            cor = (
                (0, 220, 255)
                if selecionada
                else (180, 180, 180)
            )

            prefixo = (
                "> "
                if selecionada
                else "  "
            )

            texto = fonte.render(
                prefixo + opcao,
                True,
                cor
            )

            rect = texto.get_rect(
                center=(
                    self.largura // 2,
                    250 + i * 60
                )
            )

            self.tela.blit(
                texto,
                rect
            )

    # =========================================================
    # DESENHAR JOGO
    # =========================================================

    def desenhar_jogo(self):

        self.tela.fill(
            (5, 5, 10)
        )

        # Título
        fonte = pygame.font.Font(
            None,
            45
        )

        titulo = fonte.render(
            "SURVIVAL",
            True,
            (255, 255, 255)
        )

        self.tela.blit(
            titulo,
            titulo.get_rect(
                center=(
                    self.largura // 2,
                    35
                )
            )
        )

        # Área do jogo
        pygame.draw.rect(
            self.tela,
            (50, 50, 60),
            (
                0,
                70,
                self.largura,
                self.altura - 70
            ),
            2
        )

        # Desenha todas as peças da torre
        if self.torre is not None:

            for peca in self.torre.obter_pecas():

                self.tela_survival.desenhar(
                    self.tela,
                    peca
                )

        # Informação
        fonte_info = pygame.font.Font(
            None,
            26
        )

        texto = fonte_info.render(
            "ESC - Voltar ao menu",
            True,
            (180, 180, 180)
        )

        self.tela.blit(
            texto,
            (
                15,
                self.altura - 35
            )
        )