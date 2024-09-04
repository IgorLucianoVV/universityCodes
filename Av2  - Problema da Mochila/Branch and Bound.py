class KnapsackBranchBoundSolver:
    def __init__(self, knapsackFile):
        with open(knapsackFile, 'r') as file:
            lines = file.readlines()

        self.n = int(lines[0].strip())
        self.c = list(map(int, lines[1].strip().split()))
        self.w = list(map(int, lines[2].strip().split()))
        self.M = list(map(int, lines[3].strip().split()))
        self.m = list(map(int, lines[4].strip().split()))
        self.W = int(lines[5].strip())

        self.bestSolution = None
        self.bestProfit = float('-inf')

    def isFeasible(self, x):
        return all(mi <= xi <= Mi for xi, mi, Mi in zip(x, self.m, self.M)) and sum(xi * wi for xi, wi in zip(x, self.w)) <= self.W

    def branchAndBound(self, currentIndex, currentCombination):
        if currentIndex == self.n:
            if self.isFeasible(currentCombination):
                profit = sum(ci * xi for ci, xi in zip(self.c, currentCombination))
                if profit > self.bestProfit:
                    self.bestProfit = profit
                    self.bestSolution = currentCombination
            return

        # Branch para cada possível valor (0 ou 1) da variável atual
        for value in range(2):
            newCombination = currentCombination[:] + [value]
            print("Solução parcial:", newCombination)  # Imprime a solução parcial
            if not self.isFeasible(newCombination):
                print("Poda de bound por Inviabilidade")
                continue
            elif self.bestSolution and sum(ci * xi for ci, xi in zip(self.c, newCombination)) <= self.bestProfit:
                print("Poda de bound por Optimalidade")
                break
            self.branchAndBound(currentIndex + 1, newCombination)

    def solve(self):
        self.branchAndBound(0, [])
        if self.bestSolution is None:
            print("Solução Inviável")
        else:
            print("Solução Ótima:", self.bestSolution)

solver = KnapsackBranchBoundSolver("knapsack.txt")
solver.solve()

# Professor, para casos futuros, vale colocar um arquivo com exemplos de entrada e saída para podermos validar o código.