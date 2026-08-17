from physics.colisao import Colisor


class Torre:

    def __init__(
        self,
        largura,
        altura
    ):
        self.largura = largura
        self.altura = altura

        self.pecas = []

    def adicionar_peca(
        self,
        peca
    ):
        if peca not in self.pecas:
            self.pecas.append(
                peca
            )

    def remover_peca(
        self,
        peca
    ):
        if peca in self.pecas:
            self.pecas.remove(
                peca
            )

    def atualizar(
        self,
        dt
    ):
        """
        Atualiza a física das peças.
        """

        for peca in self.pecas:

            # Peças fixadas não continuam caindo
            if peca.fixada:
                continue

            # Física
            peca.atualizar_fisica(
                dt
            )

            # --------------------------------------------
            # CHÃO
            # --------------------------------------------

            if Colisor.colisao_com_chao(
                peca,
                self.altura
            ):
                peca.fixar()
                continue

            # --------------------------------------------
            # OUTRAS PEÇAS
            # --------------------------------------------

            for suporte in self.pecas:

                if suporte is peca:
                    continue

                if not suporte.fixada:
                    continue

                if Colisor.pousar_sobre(
                    peca,
                    suporte
                ):
                    peca.fixar()
                    break

    def obter_pecas(self):
        return self.pecas

    def quantidade_pecas(self):
        return len(
            self.pecas
        )

    def obter_pecas_fixas(self):
        return [
            peca
            for peca in self.pecas
            if peca.fixada
        ]

    def limpar(self):
        self.pecas.clear()