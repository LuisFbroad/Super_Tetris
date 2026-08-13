from config import COLUNAS, LINHAS

class Tabuleiro:
    def __init__(self, colunas=COLUNAS, linhas=LINHAS):
        self.colunas = colunas
        self.linhas = linhas
        # Matriz cheia de None representando posições vazias
        self.grade = [[None for _ in range(self.colunas)] for _ in range(self.linhas)]

    def verificar_colisao(self, peca):
        """Retorna True se a peça estiver fora do tabuleiro ou colidindo com blocos fixos."""
        for y, linha in enumerate(peca.formato):
            for x, valor in enumerate(linha):
                if valor:
                    px = peca.x + x
                    py = peca.y + y

                    # Colisão com limites das paredes laterais ou fundo
                    if px < 0 or px >= self.colunas or py >= self.linhas:
                        return True

                    # Colisão com blocos já fixados (ignora posições acima do topo da tela py < 0)
                    if py >= 0 and self.grade[py][px] is not None:
                        return True

        return False

    def fixar_peca(self, peca):
        """Fixa as células da peça no tabuleiro permanentemente."""
        for y, linha in enumerate(peca.formato):
            for x, valor in enumerate(linha):
                if valor:
                    px = peca.x + x
                    py = peca.y + y
                    if 0 <= py < self.linhas and 0 <= px < self.colunas:
                        self.grade[py][px] = peca.cor

    def limpar_linhas_completas(self):
        """Remove linhas cheias e desce as linhas acima, retornando a quantidade limpa."""
        linhas_limpas = 0
        y = self.linhas - 1

        while y >= 0:
            # Verifica se todas as células da linha contêm uma cor
            if all(celula is not None for celula in self.grade[y]):
                linhas_limpas += 1
                del self.grade[y]
                # Insere uma nova linha vazia no topo
                self.grade.insert(0, [None for _ in range(self.colunas)])
            else:
                y -= 1

        return linhas_limpas