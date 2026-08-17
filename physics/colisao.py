import pygame


class Colisor:

    @staticmethod
    def obter_rect(objeto):
        return pygame.Rect(
            int(objeto.x),
            int(objeto.y),
            int(objeto.largura),
            int(objeto.altura)
        )

    @staticmethod
    def retangulos_colidem(
        objeto_a,
        objeto_b
    ):
        rect_a = Colisor.obter_rect(
            objeto_a
        )

        rect_b = Colisor.obter_rect(
            objeto_b
        )

        return rect_a.colliderect(
            rect_b
        )

    @staticmethod
    def colisao_com_chao(
        objeto,
        altura_tela
    ):
        limite = (
            altura_tela
            - objeto.altura
        )

        if objeto.y >= limite:

            objeto.y = limite

            objeto.parar_verticalmente()

            return True

        return False

    @staticmethod
    def pousar_sobre(
        objeto,
        suporte
    ):
        """
        Verifica se um objeto que está caindo
        pode pousar sobre outro.
        """

        if objeto.velocidade_y < 0:
            return False

        rect_objeto = Colisor.obter_rect(
            objeto
        )

        rect_suporte = Colisor.obter_rect(
            suporte
        )

        # Verifica se existe sobreposição horizontal
        sobreposicao_horizontal = (
            rect_objeto.right > rect_suporte.left
            and
            rect_objeto.left < rect_suporte.right
        )

        if not sobreposicao_horizontal:
            return False

        # Parte inferior do objeto
        parte_inferior = rect_objeto.bottom

        # Parte superior do suporte
        parte_superior = rect_suporte.top

        distancia = (
            parte_inferior
            - parte_superior
        )

        # Pequena tolerância para evitar atravessar
        if 0 <= distancia <= 20:

            objeto.y = (
                suporte.y
                - objeto.altura
            )

            objeto.parar_verticalmente()

            return True

        return False