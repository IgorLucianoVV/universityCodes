def knapsack_solver(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    n = int(lines[0].strip())
    c = list(map(int, lines[1].strip().split()))
    w = list(map(int, lines[2].strip().split()))
    M = list(map(int, lines[3].strip().split()))
    m = list(map(int, lines[4].strip().split()))
    W = int(lines[5].strip())

    # Função de lucro
    def f(x):
        return sum(ci * xi for ci, xi in zip(c, x))

    # Verifica se o conjunto factível é vazio
    def is_feasible(x):
        return all(mi <= xi <= Mi for xi, mi, Mi in zip(x, m, M)) and sum(xi * wi for xi, wi in zip(x, w)) <= W

    # Inicializa a solução
    best_solution = None
    best_profit = float('-inf')

    # Gera todas as combinações possíveis de 0 a M[i]
    for x1 in range(M[0] + 1):
        for x2 in range(M[1] + 1):
            for x3 in range(M[2] + 1):
                for x4 in range(M[3] + 1):
                    x = [x1, x2, x3, x4]
                    if is_feasible(x):
                        profit = f(x)
                        if profit > best_profit:
                            best_profit = profit
                            best_solution = x

    if best_solution is None:
        print("Solução Inviável")
    else:
        print("Solução Ótima:", best_solution)

# Chamada da função principal
knapsack_solver("knapsack.txt")