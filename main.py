import random

class GrafMacierzowy():
    def __init__(self, rozmiar: int, plik: str = None):
        self.liczba_krawedzi = 0
        self.wierzcholki = set()

        if plik:
            with open(plik, "r") as f:
                self.rozmiar = int(next(f))
                self.macierz = [[0] * self.rozmiar for _ in range(self.rozmiar)]
                for linia in f:
                    v, w = map(int, linia.split())
                    self.dodaj_krawedz(v, w)
        else:
            self.macierz = [[0] * rozmiar for _ in range(rozmiar)]
            self.rozmiar = rozmiar

    def dodaj_krawedz(self, v: int, w: int):
        if self.macierz[v][w] == 0:
            self.macierz[v][w] = 1
            self.macierz[w][v] = 1
            self.liczba_krawedzi += 1
            self.wierzcholki.add(v)
            self.wierzcholki.add(w)

# parametr p to prawdopodobieństwo pojawienia się każdej możliwej krawędzi między dwoma wierzchołkami
# 0 - rzadki, 1 - gęsty
    def generuj_graf(self, p: float):
        for i in range(self.rozmiar):
            for j in range(i + 1, self.rozmiar):
                if random.random() < p:
                    self.dodaj_krawedz(i, j)

    def zapisz(self, plik: str):
        with open(plik, "w") as f:
            f.write(str(self.rozmiar) + "\n")
            for i in range(self.rozmiar):
                for j in range(i + 1, self.rozmiar):
                    if self.macierz[i][j] == 1:
                        f.write(f"{i + 1} {j + 1}\n")


