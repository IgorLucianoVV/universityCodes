def bellmanFord(arquivoDeEntrada):
    with open(arquivoDeEntrada, 'r') as arquivo:
        linhas = arquivo.readlines()

    # Obtendo o número de vértices
    numVertices = int(linhas[0])

    # Inicializando matrizes de adjacência e distâncias
    matrizAdjacencia = []
    for i in range(1, numVertices + 1):
        linha = list(map(float, linhas[i].split()))
        matrizAdjacencia.append(linha)

    # Obtendo o vértice fonte
    raiz = int(linhas[numVertices + 1])

    # Inicializando os arrays de predecessores e distâncias
    predecessores = [-1] * numVertices
    distancias = [1000000] * numVertices
    distancias[raiz] = 0

    # Algoritmo de Bellman-Ford
    for _ in range(numVertices - 1):
        for u in range(numVertices):
            for v in range(numVertices):
                if matrizAdjacencia[u][v] != 0:
                    if distancias[u] + matrizAdjacencia[u][v] < distancias[v]:
                        distancias[v] = distancias[u] + matrizAdjacencia[u][v]
                        predecessores[v] = u

    # Verificação de ciclos negativos
    for u in range(numVertices):
        for v in range(numVertices):
            if matrizAdjacencia[u][v] != 0:
                if distancias[u] + matrizAdjacencia[u][v] < distancias[v]:
                    print("O grafo contém um ciclo negativo")
                    return None, None

    return predecessores, distancias

predecessores, distancias = bellmanFord("bf.txt")
if predecessores is not None and distancias is not None:
    print("Predecessores:", predecessores)
    print("Distâncias:", distancias)
