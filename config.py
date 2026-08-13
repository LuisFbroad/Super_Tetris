import random

## DIMENSÕES DA GRADE ##

LARGURA_BLOCO = 30
COLUNA = 10
LINHAS = 20

LARGURA_TELA = COLUNA * LARGURA_BLOCO
ALTURA_TELA = LINHAS * LARGURA_BLOCO

FPS = 120
VELOCIDADE_QUEDA_MS = 350   

##  CORES ##

COR_FUNDO = (0, 0, 0)
COR_GRADE = (40, 40, 40)

## FORMAÇÃO E CORES DAS PEÇAS ##

FORMATOS = [
    [[1, 1, 1, 1]],        
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1], [1, 1]],      
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 0], [1, 1, 1]] 
]

CORES_PECAS = [
    (0, 255, 255),  # Ciano
    (255, 165, 0),  # Laranja
    (0, 0, 255),    # Azul
    (255, 255, 0),  # Amarelo
    (0, 255, 0),    # Verde
    (255, 0, 0),    # Vermelho
    (128, 0, 128)   # Roxo
]

## CONFIG DA SUPER PEÇA ##

CHANCE_SUPER_PECA = 0.15
COR_SUPER_PECA = (255, 215, 0)
COR_BORDA_SUPER = (255, 255, 255)
MIN_BLOCOS_SUPER = 5
MAX_BLOCOS_SUPER = 6