class UnionFind:
    def __init__(self, n):
        self.pai = list(range(n))
        self.rank = [0] * n

    def encontrar(self, x):
        if self.pai[x] != x:
            self.pai[x] = self.encontrar(self.pai[x])
        return self.pai[x]

    def unir(self, x, y):
        raiz_x = self.encontrar(x)
        raiz_y = self.encontrar(y)
        if raiz_x == raiz_y:
            return False
        if self.rank[raiz_x] < self.rank[raiz_y]:
            self.pai[raiz_x] = raiz_y
        elif self.rank[raiz_x] > self.rank[raiz_y]:
            self.pai[raiz_y] = raiz_x
        else:
            self.pai[raiz_y] = raiz_x
            self.rank[raiz_x] += 1
        return True


def kruskal(matriz):
    n = len(matriz)
    arestas = []
    for i in range(n):
        for j in range(i + 1, n):
            if matriz[i][j] != 0:
                arestas.append((i, j, matriz[i][j]))
    arestas.sort(key=lambda x: x[2])

    uf = UnionFind(n)
    arestas_arvore = []
    for aresta in arestas:
        u, v, peso = aresta
        if uf.unir(u, v):
            arestas_arvore.append(aresta)
            if len(arestas_arvore) == n - 1:
                return True, arestas_arvore

    return False, []


def ler_grafo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        n = int(arquivo.readline().strip())
        matriz = []
        for _ in range(n):
            linha = list(map(float, arquivo.readline().split()))
            matriz.append(linha)
        return matriz


def main():
    matriz = ler_grafo("kruskal.txt")
    eh_conexo, arestas_arvore = kruskal(matriz)
    if eh_conexo:
        print("VERDADEIRO")
        print(arestas_arvore)
    else:
        print("FALSO")


if __name__ == "__main__":
    main()
