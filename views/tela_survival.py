import pygame


class TelaSurvival:

    def __init__(
        self,
        largura,
        altura,
        tamanho_bloco
    ):
        self.largura = largura
        self.altura = altura
        self.tamanho_bloco = tamanho_bloco

    def desenhar(
        self,
        superficie,
        corpo_peca
    ):
        if corpo_peca is None:
            return

        if corpo_peca.perdida:
            return

        bloco = self.tamanho_bloco

        formato = corpo_peca.formato

        for y, linha in enumerate(
            formato
        ):

            for x, valor in enumerate(
                linha
            ):

                if not valor:
                    continue

                px = (
                    corpo_peca.x
                    + x * bloco
                )

                py = (
                    corpo_peca.y
                    + y * bloco
                )

                rect = pygame.Rect(
                    int(px),
                    int(py),
                    bloco,
                    bloco
                )

                # Corpo
                pygame.draw.rect(
                    superficie,
                    corpo_peca.cor,
                    rect
                )

                # Borda
                pygame.draw.rect(
                    superficie,
                    (255, 255, 255),
                    rect,
                    1
                )