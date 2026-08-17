class CorpoFisico:
    """
    Corpo físico básico utilizado pelo modo Survival.
    """

    def __init__(
        self,
        x,
        y,
        largura,
        altura,
        massa=1.0
    ):
        self.x = float(x)
        self.y = float(y)

        self.largura = largura
        self.altura = altura

        self.massa = massa

        # Velocidade
        self.velocidade_x = 0.0
        self.velocidade_y = 0.0

        # Aceleração
        self.aceleracao_x = 0.0
        self.aceleracao_y = 0.0

        # Rotação
        self.angulo = 0.0
        self.velocidade_angular = 0.0

        # Estado
        self.no_chao = False
        self.ativo = True

    def aplicar_forca(
        self,
        forca_x,
        forca_y
    ):
        self.aceleracao_x += (
            forca_x / self.massa
        )

        self.aceleracao_y += (
            forca_y / self.massa
        )

    def aplicar_impulso(
        self,
        impulso_x,
        impulso_y
    ):
        self.velocidade_x += (
            impulso_x / self.massa
        )

        self.velocidade_y += (
            impulso_y / self.massa
        )

    def atualizar(
        self,
        dt,
        gravidade=1500.0
    ):
        if not self.ativo:
            return

        # Gravidade
        self.aceleracao_y += gravidade

        # Velocidade
        self.velocidade_x += (
            self.aceleracao_x * dt
        )

        self.velocidade_y += (
            self.aceleracao_y * dt
        )

        # Posição
        self.x += (
            self.velocidade_x * dt
        )

        self.y += (
            self.velocidade_y * dt
        )

        # Rotação
        self.angulo += (
            self.velocidade_angular * dt
        )

        # Limpar aceleração
        self.aceleracao_x = 0.0
        self.aceleracao_y = 0.0

    def parar_verticalmente(self):
        self.velocidade_y = 0.0
        self.aceleracao_y = 0.0
        self.no_chao = True

    def aplicar_atrito(
        self,
        fator=0.90
    ):
        self.velocidade_x *= fator

        if abs(self.velocidade_x) < 0.01:
            self.velocidade_x = 0.0

    def aplicar_rotacao(
        self,
        velocidade
    ):
        self.velocidade_angular = velocidade