def knapsackSolver(knapsack):
    with open(knapsack, 'r') as file:
        lines = file.readlines()

    n = int(lines[0].strip())
    c = list(map(int, lines[1].strip().split()))
    w = list(map(int, lines[2].strip().split()))
    M = list(map(int, lines[3].strip().split()))
    m = list(map(int, lines[4].strip().split()))
    W = int(lines[5].strip())

    # Verifica se as condições são satisfeitas
    def isFeasible(x):
        return all(mi <= xi <= Mi for xi, mi, Mi in zip(x, m, M)) and sum(xi * wi for xi, wi in zip(x, w)) <= W

    # Inicializa a solução ótima e o melhor lucro
    bestSolution = None
    bestProfit = float('-inf')

    # Gera todas as combinações possíveis de valores para as variáveis
    def generateCombinations(currentIndex, currentCombination):
        nonlocal bestSolution, bestProfit
        if currentIndex == n:
            if isFeasible(currentCombination):
                profit = sum(ci * xi for ci, xi in zip(c, currentCombination))
                if profit > bestProfit:
                    bestProfit = profit
                    bestSolution = currentCombination
            return
        for value in range(m[currentIndex], M[currentIndex] + 1):
            generateCombinations(currentIndex + 1, currentCombination + [value])

    # Inicia a geração de combinações
    generateCombinations(0, [])

    if bestSolution is None:
        print("Solução Inviável")
    else:
        print("Solução Ótima:", bestSolution)

knapsackSolver("knapsack.txt")
