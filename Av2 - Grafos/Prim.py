def lerEntrada(arquivoDeEntrada):
    with open(arquivoDeEntrada, 'r') as file:
        linhas = file.readlines()
        n = int(linhas[0])
        matrizAdj = [[float(val) for val in linha.split()] for linha in linhas[1:n+1]]
        r = int(linhas[n+1])
    return n, matrizAdj, r

def prim(matrizAdj, r):
    n = len(matrizAdj)
    chave = [float('inf')] * n
    pai = [-1] * n
    chave[r] = 0
    visitados = [False] * n

    for _ in range(n):
        u = minimoChave(chave, visitados)
        visitados[u] = True
        for v in range(n):
            if matrizAdj[u][v] and not visitados[v] and matrizAdj[u][v] < chave[v]:
                pai[v] = u
                chave[v] = matrizAdj[u][v]
    
    return pai

def minimoChave(chave, visitados):
    minimo = float('inf')
    indiceMinimo = -1
    for i in range(len(chave)):
        if chave[i] < minimo and not visitados[i]:
            minimo = chave[i]
            indiceMinimo = i
    return indiceMinimo

def verificaConexo(pai):
    if -1 in pai[1:]:
        return "FALSO"
    else:
        return "VERDADEIRO"

def main():
    nomeArquivo = "prim.txt"
    n, matrizAdj, r = lerEntrada(nomeArquivo)
    predecessores = prim(matrizAdj, r)
    predecessores[r] = -1
    conexo = verificaConexo(predecessores)
    print(conexo)
    if conexo == "VERDADEIRO":
        print("Predecessores:", predecessores)

if __name__ == "__main__":
    main()
