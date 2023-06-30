# Exemplo de uso do Glucose
from pysat.solvers import Glucose3

g = Glucose3()
g.add_clause([1, 2])
g.add_clause([-1, 2])
g.add_clause([1, -2])
g.add_clause([-1, -2])
print(g.solve())
print(g.get_model())

# Mapear os símbolos proposicionais (átomos)
N = 8
contador = 1
mapeamento_para_int = {}
mapeamento_para_int_inv = {}
posicoes = [[i, j] for i in range(1, N+1) for j in range(1, N+1)]
for posicao in posicoes:
    chave = f"R_{posicao[0]}_{posicao[1]}"
    mapeamento_para_int[chave] = contador
    mapeamento_para_int_inv[contador] = chave
    contador = contador + 1

dict(zip(["a", "b", "c", "d"], range(4)))

# Gerando uma instância do solver (DPLL)
g = Glucose3()

# Cada linha possui PELO MENOS uma rainha
for i in range(1, N+1):
    linha = []
    for j in range(1, N+1):
        linha.append(mapeamento_para_int[f"R_{i}_{j}"])
    g.add_clause(linha)

# Implementar: cada linha possui NO MÁXIMO uma rainha
for j in range(1, N+1):
    for i in range(1, N+1):
        outros_indices = list(range(1, N+1))
        outros_indices.remove(i)
        for outro2 in outros_indices:
            # R_i_j -> ~R_k_j === ~R_i_j v ~R_k_j
            maxLinha = [-mapeamento_para_int[f"R_{j}_{i}"], -mapeamento_para_int[f"R_{j}_{outro2}"]]
            g.add_clause(maxLinha)

# Implementar: cada coluna possui PELO MENOS uma rainha
for i in range(1, N+1):
    coluna = []
    for j in range(1, N+1):
        coluna.append(mapeamento_para_int[f"R_{j}_{i}"])
    g.add_clause(coluna)

# Cada coluna possui NO MÁXIMO uma rainha
for j in range(1, N+1):
    for i in range(1, N+1):
        outros_indices = list(range(1, N+1))
        outros_indices.remove(i)
        for outro in outros_indices:
            # R_i_j -> ~R_k_j === ~R_i_j v ~R_k_j
            maxColuna = [-mapeamento_para_int[f"R_{i}_{j}"], -mapeamento_para_int[f"R_{outro}_{j}"]]
            g.add_clause(maxColuna)

# Sugestão: implementar que cada diagonal (primária ou secundária)
# possui NO MÁXIMO uma rainha

# Diagonais primárias
for diferenca in range(2 - N, N - 1):
    diagonal = [[i, j] for i in range(1, N+1) for j in range(1, N+1) if i - j == diferenca]
    if len(diagonal) > 1:
        for k in range(len(diagonal) - 1):
            for l in range(k + 1, len(diagonal)):
                # ~R_i_j v ~R_k_l
                diagonal_primaria = [-mapeamento_para_int[f"R_{diagonal[k][0]}_{diagonal[k][1]}"],
                                     -mapeamento_para_int[f"R_{diagonal[l][0]}_{diagonal[l][1]}"]]
                g.add_clause(diagonal_primaria)

# Diagonais secundárias
for soma_val in range(3, 2*N):
    diagonal = [[i, j] for i in range(1, N+1) for j in range(1, N+1) if i + j == soma_val]
    if len(diagonal) > 1:
        for k in range(len(diagonal) - 1):
            for l in range(k + 1, len(diagonal)):
                # ~R_i_j v ~R_k_l
                diagonal_secundaria = [-mapeamento_para_int[f"R_{diagonal[k][0]}_{diagonal[k][1]}"],
                                       -mapeamento_para_int[f"R_{diagonal[l][0]}_{diagonal[l][1]}"]]
                g.add_clause(diagonal_secundaria)

print(g.solve())
print(g.get_model())

for i in range(1, N+1):
    linha = []
    for j in range(1, N+1):
        variavel = mapeamento_para_int[f"R_{i}_{j}"]
        if variavel in g.get_model():
            linha.append("X")
        else:
            linha.append("O")
    print(" ".join(linha))
