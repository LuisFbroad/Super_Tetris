import pygame


class GerenciadorMenu:

    def __init__(self, tela):
        self.tela = tela

        self.opcoes = [
            "MODO CLÁSSICO",
            "MODO SURVIVAL",
            "SAIR"
        ]

        self.indice = 0

    def executar(self):
        rodando = True

        while rodando:

            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    return "SAIR"

                if evento.type == pygame.KEYDOWN:

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

                        if opcao == "MODO CLÁSSICO":
                            return "CLASSIC"

                        elif opcao == "MODO SURVIVAL":
                            return "SURVIVAL"

                        elif opcao == "SAIR":
                            return "SAIR"

            self.desenhar()

            pygame.display.flip()

        return "SAIR"

    def desenhar(self):

        self.tela.fill((15, 15, 25))

        fonte_titulo = pygame.font.Font(None, 80)
        fonte_menu = pygame.font.Font(None, 45)

        titulo = fonte_titulo.render(
            "SUPER TETRIS",
            True,
            (255, 255, 255)
        )

        titulo_rect = titulo.get_rect(
            center=(self.tela.get_width() // 2, 100)
        )

        self.tela.blit(titulo, titulo_rect)

        for i, opcao in enumerate(self.opcoes):

            selecionada = i == self.indice

            cor = (0, 220, 255) if selecionada else (180, 180, 180)

            texto = fonte_menu.render(
                ("> " if selecionada else "  ") + opcao,
                True,
                cor
            )

            rect = texto.get_rect(
                center=(
                    self.tela.get_width() // 2,
                    260 + i * 60
                )
            )

            self.tela.blit(texto, rect)