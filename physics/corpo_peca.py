from physics.fisica import CorpoFisico


class CorpoPeca(CorpoFisico):
    """
    Representa uma Peca do Tetris no sistema físico
    do modo Survival.
    """

    def __init__(
        self,
        peca,
        tamanho_bloco,
        x,
        y
    ):
        self.peca = peca
        self.tamanho_bloco = tamanho_bloco

        self.formato = peca.formato
        self.cor = peca.cor

        self.fixada = False
        self.perdida = False

        # Calcula dimensões da matriz
        largura_blocos = 0

        for linha in self.formato:
            if len(linha) > largura_blocos:
                largura_blocos = len(linha)

        altura_blocos = len(
            self.formato
        )

        largura = (
            largura_blocos
            * tamanho_bloco
        )

        altura = (
            altura_blocos
            * tamanho_bloco
        )

        massa = self._calcular_massa()

        super().__init__(
            x=x,
            y=y,
            largura=largura,
            altura=altura,
            massa=massa
        )

    def _calcular_massa(self):
        quantidade = 0

        for linha in self.formato:

            for bloco in linha:

                if bloco:
                    quantidade += 1

        return max(
            1.0,
            quantidade
        )

    def atualizar_fisica(
        self,
        dt,
        gravidade=1500.0
    ):
        if self.fixada or self.perdida:
            return

        super().atualizar(
            dt,
            gravidade
        )

    def fixar(self):
        self.fixada = True
        self.no_chao = True

        self.velocidade_x = 0.0
        self.velocidade_y = 0.0
        self.velocidade_angular = 0.0

    def marcar_como_perdida(self):
        self.perdida = True
        self.ativo = False