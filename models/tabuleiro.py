from config import COLUNAS, LINHAS

class Tabuleiro:
    def __init__(self):
        self.colunas = COLUNAS
        self.linhas = LINHAS
        self.grade = [[None for _ in range(self.colunas)] for _ in range(self.linhas)]

    def posicao_valida(self, peca):
        """Verifica se a peça está dentro dos limites da grade e sem colisões."""
        for x, y in peca.obter_posicoes_globais():
            if x < 0 or x >= self.colunas or y >= self.linhas:
                return False
            if y >= 0 and self.grade[y][x] is not None:
                return False
        return True

    def fixar_peca(self, peca):
        """Fixa a cor da peça nas coordenadas correspondentes da grade."""
        for x, y in peca.obter_posicoes_globais():
            if y >= 0:
                self.grade[y][x] = peca.cor

    def limpar_linhas(self):
        """Remove linhas completas e adiciona novas linhas vazias no topo."""
        nova_grade = [linha for linha in self.grade if None in linha]
        linhas_limpas = self.linhas - len(nova_grade)

        while len(nova_grade) < self.linhas:
            nova_grade.insert(0, [None for _ in range(self.colunas)])

        self.grade = nova_grade
        return linhas_limpas