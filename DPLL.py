def dpll_satisfiable(symbols, clauses, model):
    if len(clauses) == 0:
        return True
    if any(len(clause) == 0 for clause in clauses):
        return False

    unit_clauses = [c for c in clauses if len(c) == 1]
    while unit_clauses:
        unit = unit_clauses[0]
        clauses = [c for c in clauses if unit not in c]
        symbols, model = update_symbols_model(symbols, model, unit)
        unit_clauses = [c for c in clauses if len(c) == 1]

    if any(len(clause) == 0 for clause in clauses):
        return False

    literal = symbols[0]
    remaining_symbols = symbols[1:]

    return (
        dpll_satisfiable(remaining_symbols, [clause for clause in clauses if literal not in clause], model + [(literal, True)]) or
        dpll_satisfiable(remaining_symbols, [clause for clause in clauses if -literal not in clause], model + [(literal, False)])
    )

def update_symbols_model(symbols, model, unit):
    new_symbols = symbols[:]
    new_model = model[:]

    literal = unit[0]
    value = (unit[0] > 0)

    new_symbols.remove(abs(literal))
    new_model.append((abs(literal), value))

    return new_symbols, new_model

def n_queens(n):
    symbols = [i * n + j + 1 for i in range(n) for j in range(n)]
    clauses = []

    # Cada posição deve ter exatamente uma rainha
    for i in range(n):
        clause = [symbols[(i * n) + j] for j in range(n)]

        clauses.append(clause)
        for j in range(i * n + 1, (i + 1) * n + 1):
            for k in range(j + 1, (i + 1) * n + 1):
                clauses.append([-j, -k])

    # Cada rainha deve ser única em cada coluna
    for j in range(1, n + 1):
        clause = [symbols[i] for i in range(j, n * n + 1, n)]
        clauses.append(clause)
        for i in range(j, n * n + 1, n):
            for k in range(i + n, n * n + 1, n):
                clauses.append([-i, -k])

    # Cada rainha deve ser única nas diagonais principais
    for k in range(2 - n, n - 1):
        clause1 = [symbols[i] for i in range(1, n * n + 1) if i % n - i // n == k]
        clause2 = [symbols[i] for i in range(1, n * n + 1) if i % n - i // n == -k]
        if len(clause1) > 1:
            clauses.append(clause1)
            for i in range(len(clause1)):
                for j in range(i + 1, len(clause1)):
                    clauses.append([-clause1[i], -clause1[j]])
        if len(clause2) > 1:
            clauses.append(clause2)
            for i in range(len(clause2)):
                for j in range(i + 1, len(clause2)):
                    clauses.append([-clause2[i], -clause2[j]])

    model = []
    result = dpll_satisfiable(symbols, clauses, model)

    if result:
        queens = [symbol for symbol, value in result if value]
        board = [['Q' if symbol in queens else '.' for symbol in range(i * n + 1, (i + 1) * n + 1)] for i in range(n)]
        for row in board:
            print(' '.join(row))
    else:
        print("Não há solução para N = ", n)


def read_cnf_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    num_clauses, num_atoms = map(int, lines[0].split())

    clauses = []
    for line in lines[1:]:
        clause = list(map(int, line.split()))
        clauses.append(clause)

    return num_clauses, num_atoms, clauses



def main():
    file_path = 'C:/Users/felip/Downloads/N-Queens-with-SAT/arquivo_de_entrada.txt'
    num_clauses, num_atoms, clauses = read_cnf_file(file_path)

    symbols = list(range(1, num_atoms + 1))
    model = []
    result = dpll_satisfiable(symbols, clauses, model)

    if result:
        print("Satisfatível")
        print("Modelo:", result)
    else:
        print("Insatisfatível")

if __name__ == '__main__':
    #n_queens(8)
    main()
