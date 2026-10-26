"""
Coração de "eu te amo" em 20 idiomas, desenhado com turtle.

Como rodar:
    python coracao_idiomas.py

Não precisa instalar nada: o turtle já vem junto com o Python.

Como o desenho acontece:
  O coração é montado em linhas, como um parágrafo justificado.
  1. Primeiro aparecem as frases da borda, em ordem, como uma caneta:
     começa no "vale" de cima, desce pela direita até a ponta e volta
     pela esquerda.
  2. Depois o miolo vai sendo preenchido aos poucos.
"""

import math
import random
import turtle
import tkinter.font as tkfont

# ------------------------------------------------------------
# 1. Configurações (mexa aqui pra mudar o resultado)
# ------------------------------------------------------------
LARGURA, ALTURA = 900, 860
ESCALA = 23                 # tamanho do coração
DESLOCAMENTO_Y = 45         # sobe o coração um pouco
FUNDO = "black"
COR = "#e3122b"             # um vermelho só, como na inspiração
FONTE = "Arial"
TAMANHO = 9                 # tamanho da letra
ESPACO_ENTRE_PALAVRAS = 8   # em pixels
ESPACO_ENTRE_LINHAS = 2     # em pixels

# Velocidade (aumente os tempos pra ficar mais devagar)
MS_POR_FRASE_CONTORNO = 70
MS_POR_FRASE_RECHEIO = 35
PAUSA_ENTRE_ETAPAS_MS = 500

# A "piscada": a frase nasce nesta cor e vai esfriando até a COR
COR_DA_PISCADA = "#ffffff"
PASSOS_DA_PISCADA = 10      # mais passos = transição mais suave
MS_POR_PASSO_DA_PISCADA = 35

FRASES = [
    "I love you",              # inglês
    "Eu te amo",               # português
    "Te amo",                  # espanhol
    "Je t'aime",               # francês
    "Ti amo",                  # italiano
    "Ich liebe dich",          # alemão
    "Ik hou van jou",          # holandês
    "Jag älskar dig",          # sueco
    "Kocham cię",              # polonês
    "Я тебя люблю",            # russo
    "Seni seviyorum",          # turco
    "Σ'αγαπώ",                 # grego
    "愛してる",                 # japonês
    "사랑해",                   # coreano
    "我爱你",                   # chinês
    "मैं तुमसे प्यार करता हूँ",       # hindi
    "Aku cinta kamu",          # indonésio
    "Anh yêu em",              # vietnamita
    "Te iubesc",               # romeno
    "Mahal kita",              # filipino
]


# ------------------------------------------------------------
# 2. A matemática do coração
# ------------------------------------------------------------
def ponto_do_coracao(t, encolher=1.0):
    """Fórmula clássica do coração. t vai de 0 a 2π.
    'encolher' (0 a 1) aproxima o ponto do centro do coração."""
    x = 16 * math.sin(t) ** 3
    y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
    centro_y = 2  # centro aproximado da forma, em unidades da fórmula
    x *= encolher
    y = centro_y + (y - centro_y) * encolher
    return x * ESCALA, y * ESCALA + DESLOCAMENTO_Y


def contorno(encolher=1.0, pontos=600):
    return [ponto_do_coracao(2 * math.pi * i / pontos, encolher) for i in range(pontos)]


def cortes_na_altura(poligono, y):
    """Onde uma linha horizontal na altura y cruza o contorno.
    Devolve pares (x_inicio, x_fim) dos trechos que ficam DENTRO do coração.
    Perto do topo são dois trechos (um em cada 'bochecha')."""
    xs = []
    n = len(poligono)
    for i in range(n):
        x1, y1 = poligono[i]
        x2, y2 = poligono[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
    xs.sort()
    return [(xs[i], xs[i + 1]) for i in range(0, len(xs) - 1, 2)]


# ------------------------------------------------------------
# 3. Planejar as posições (sem desenhar ainda)
# ------------------------------------------------------------
def planejar(medir, altura_linha):
    """Monta o coração em linhas de texto, como um parágrafo justificado.
    medir(texto) devolve a largura real do texto em pixels.
    Devolve (borda, miolo): as frases da borda vêm na ordem de um traço
    contínuo; as do miolo vêm embaralhadas."""
    forma = contorno(encolher=0.99)
    ys = [p[1] for p in forma]
    borda, miolo = [], []

    y = max(ys) - altura_linha
    while y > min(ys):
        for inicio, fim in cortes_na_altura(forma, y + altura_linha / 2):
            disponivel = fim - inicio
            linha, usado = [], 0
            for _ in range(60):  # tenta encaixar frases até encher a linha
                texto = random.choice(FRASES)
                w = medir(texto)
                extra = ESPACO_ENTRE_PALAVRAS if linha else 0
                if usado + extra + w <= disponivel:
                    linha.append((texto, w))
                    usado += extra + w
            if not linha:
                continue
            # justificar: espalha a sobra entre as palavras, pra borda ficar redonda
            sobra = disponivel - usado
            if len(linha) > 1 and sobra / (len(linha) - 1) < ESPACO_ENTRE_PALAVRAS * 3:
                gap = ESPACO_ENTRE_PALAVRAS + sobra / (len(linha) - 1)
                x = inicio
            else:  # linha curta (ponta de baixo): só centraliza
                gap = ESPACO_ENTRE_PALAVRAS
                x = inicio + sobra / 2
            for k, (texto, w) in enumerate(linha):
                frase = (x + w / 2, y, texto)
                if k == 0 or k == len(linha) - 1:
                    borda.append(frase)
                else:
                    miolo.append(frase)
                x += w + gap
        y -= altura_linha + ESPACO_ENTRE_LINHAS

    # Ordem da borda: como uma caneta, do "vale" de cima, sentido horário
    centro_y = 2 * ESCALA + DESLOCAMENTO_Y
    def angulo(frase):
        x, y, _ = frase
        return math.atan2(x, y - centro_y) % (2 * math.pi)
    borda.sort(key=angulo)

    random.shuffle(miolo)   # o miolo aparece espalhado, não linha por linha
    return borda, miolo


# ------------------------------------------------------------
# 4. Desenhar: cada frase nasce branca e esfria até o vermelho
# ------------------------------------------------------------
def degrade(cor_inicio, cor_fim, passos):
    """Lista de cores intermediárias entre duas cores no formato '#rrggbb'."""
    r1, g1, b1 = (int(cor_inicio[i:i + 2], 16) for i in (1, 3, 5))
    r2, g2, b2 = (int(cor_fim[i:i + 2], 16) for i in (1, 3, 5))
    cores = []
    for k in range(1, passos + 1):
        t = k / passos
        cores.append("#%02x%02x%02x" % (round(r1 + (r2 - r1) * t),
                                         round(g1 + (g2 - g1) * t),
                                         round(b1 + (b2 - b1) * t)))
    return cores


def main():
    tela = turtle.Screen()
    tela.setup(LARGURA, ALTURA)
    tela.bgcolor(FUNDO)
    tela.title("Eu te amo em 20 idiomas")
    tela.tracer(0)

    # Em vez da caneta do turtle, escrevemos direto no canvas do Tk.
    # Assim cada frase vira um objeto que dá pra mudar de cor depois.
    canvas = tela.getcanvas()
    fonte = tkfont.Font(family=FONTE, size=TAMANHO, weight="bold")

    borda, miolo = planejar(fonte.measure, fonte.metrics("linespace"))
    fila = [(f, MS_POR_FRASE_CONTORNO) for f in borda]
    fila.append((None, PAUSA_ENTRE_ETAPAS_MS))
    fila += [(f, MS_POR_FRASE_RECHEIO) for f in miolo]

    cores_da_piscada = degrade(COR_DA_PISCADA, COR, PASSOS_DA_PISCADA)

    def esfriar(item, passo=0):
        """Troca a cor da frase, um passo por vez, do branco até o vermelho."""
        if passo < len(cores_da_piscada):
            canvas.itemconfig(item, fill=cores_da_piscada[passo])
            canvas.after(MS_POR_PASSO_DA_PISCADA, lambda: esfriar(item, passo + 1))

    def proxima(i=0):
        if i >= len(fila):
            return
        frase, espera = fila[i]
        if frase:
            x, y, texto = frase
            # o canvas do Tk tem o eixo y invertido em relação ao turtle
            item = canvas.create_text(x, -y, text=texto, anchor="s",
                                      fill=COR_DA_PISCADA, font=fonte)
            esfriar(item)
        canvas.after(espera, lambda: proxima(i + 1))

    proxima()
    turtle.done()


if __name__ == "__main__":
    main()
    