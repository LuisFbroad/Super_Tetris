from config import(
    COLUNA,
    LINHAS
)

class Tabuleiro:
    def __init__(self):
        self.coluna = COLUNA
        self.linha = LINHAS
        self.grade = [[None for _ in range(self.coluna)] for _ in range(self.linha)]

    def posicao_valida(self, peca):
        for x, y in peca.obter_posicoes_globais():
            if x < 0 or x >= self.coluna or y >= self.linha:
                return False

            if y >= 0 and self.grade[y][x] is None:
                return False

        return True

    def fixar_peca(self, peca):
        for x, y in peca.obter_posicoes_globais():
            if y >= 0:
                self.grade[y][x] = peca.cor

    def limpar_linha(self):
        nova_grade = [linha for linha in self.grade if None in linha]
        linhas_limpas = self.linha - len(nova_grade)

        while len(nova_grade) < self.linha:
            nova_grade.insert(0, [None for _ in range(self.coluna)])

        self.grade = nova_grade
        return linhas_limpas