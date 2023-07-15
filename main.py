def simplify(clauses):
    unit_clauses = []
    pure_literals = set()
    
    while True:
        # Passo 1: Identificar cláusulas unitárias e literais puros
        for clause in clauses:
            if len(clause) == 1:
                unit_clauses.append(clause[0])
            for literal in clause:
                if -literal not in clause:
                    pure_literals.add(abs(literal))
        
        # Passo 2: Propagação unitária
        while unit_clauses:
            unit_literal = unit_clauses.pop()
            clauses = [clause for clause in clauses if unit_literal not in clause]
            for clause in clauses:
                if -unit_literal in clause:
                    clause.remove(-unit_literal)
        
        # Passo 3: Remover cláusulas satisfeitas
        clauses = [clause for clause in clauses if clause]
        
        # Passo 4: Atualizar literais puros
        pure_literals = set(literal for literal in pure_literals if all(literal not in clause for clause in clauses))
        
        if not unit_clauses and not pure_literals:
            break
    
    return clauses



def dpll(clausulas, atribuicao):
    # simplify(clausulas)
    if all(len(c) == 0 for c in clausulas):
        return True  # Todas as cláusulas são satisfeitas, encontramos uma solução válida
    
    if any(len(c) == 0 for c in clausulas):
        return False  # Alguma cláusula está vazia, a atribuição atual não é válida
    
    variaveis_nao_atribuidas = set()
    for clausula in clausulas:
        for literal in clausula:
            variavel = abs(literal)
            if variavel not in atribuicao:
                variaveis_nao_atribuidas.add(variavel)
    
    if len(variaveis_nao_atribuidas) == 0:
        return False  # Todas as variáveis estão atribuídas, não encontramos uma solução
    
    variavel = variaveis_nao_atribuidas.pop()
    clausulas_restantes = []
    
    for clausula in clausulas:
        if variavel in clausula:
            continue  # Variável já está satisfeita, ignorar cláusula
        if -variavel in clausula:
            clausula_restante = [literal for literal in clausula if literal != -variavel]
            clausulas_restantes.append(clausula_restante)
        else:
            clausulas_restantes.append(clausula)
    
    atribuicao[variavel] = True
    if dpll(clausulas_restantes, atribuicao):
        return True
    
    atribuicao[variavel] = False
    return dpll(clausulas_restantes, atribuicao)



# Mapear os símbolos proposicionais (átomos)
n = 4
contador = 1
mapeamento_para_int = {}
mapeamento_para_int_inv = {}
posicoes = [[i, j] for i in range(1, n+1) for j in range(1, n+1)]
for posicao in posicoes:
    chave = f"R_{posicao[0]}_{posicao[1]}"
    mapeamento_para_int[chave] = contador
    mapeamento_para_int_inv[contador] = chave
    contador = contador + 1

# lista de clausulas
clausulas = []

# Cada linha possui PELO MENOS uma rainha
for i in range(1, n+1):
    linha = []
    for j in range(1, n+1):
        linha.append(mapeamento_para_int[f"R_{i}_{j}"])
    clausulas.append(linha)

# Implementar: cada linha possui NO MÁXIMO uma rainha
for j in range(1, n+1):
    for i in range(1, n+1):
        outros_indices = list(range(1, n+1))
        outros_indices.remove(i)
        for outro2 in outros_indices:
            # R_i_j -> ~R_k_j === ~R_i_j v ~R_k_j
            maxLinha = [-mapeamento_para_int[f"R_{j}_{i}"], -mapeamento_para_int[f"R_{j}_{outro2}"]]
            clausulas.append(maxLinha)

# Implementar: cada coluna possui PELO MENOS uma rainha
for i in range(1, n+1):
    coluna = []
    for j in range(1, n+1):
        coluna.append(mapeamento_para_int[f"R_{j}_{i}"])
    clausulas.append(coluna)

# Cada coluna possui NO MÁXIMO uma rainha
for j in range(1, n+1):
    for i in range(1, n+1):
        outros_indices = list(range(1, n+1))
        outros_indices.remove(i)
        for outro in outros_indices:
            # R_i_j -> ~R_k_j === ~R_i_j v ~R_k_j
            maxColuna = [-mapeamento_para_int[f"R_{i}_{j}"], -mapeamento_para_int[f"R_{outro}_{j}"]]
            clausulas.append(maxColuna)

# Sugestão: implementar que cada diagonal (primária ou secundária)
# possui NO MÁXIMO uma rainha

# Diagonais primárias
for diferenca in range(2 - n, n - 1):
    diagonal = [[i, j] for i in range(1, n+1) for j in range(1, n+1) if i - j == diferenca]
    if len(diagonal) > 1:
        for k in range(len(diagonal) - 1):
            for l in range(k + 1, len(diagonal)):
                # ~R_i_j v ~R_k_l
                diagonal_primaria = [-mapeamento_para_int[f"R_{diagonal[k][0]}_{diagonal[k][1]}"],
                                     -mapeamento_para_int[f"R_{diagonal[l][0]}_{diagonal[l][1]}"]]
                clausulas.append(diagonal_primaria)

# Diagonais secundárias
for soma_val in range(3, 2*n):
    diagonal = [[i, j] for i in range(1, n+1) for j in range(1, n+1) if i + j == soma_val]
    if len(diagonal) > 1:
        for k in range(len(diagonal) - 1):
            for l in range(k + 1, len(diagonal)):
                # ~R_i_j v ~R_k_l
                diagonal_secundaria = [-mapeamento_para_int[f"R_{diagonal[k][0]}_{diagonal[k][1]}"],
                                       -mapeamento_para_int[f"R_{diagonal[l][0]}_{diagonal[l][1]}"]]
                clausulas.append(diagonal_secundaria)

print(clausulas)

# Executar o algoritmo com as cláusulas fornecidas
assignment = {}
satisfiable = dpll(clausulas, assignment)

if satisfiable:
    print("Encontrada uma solução válida:")
    for var, value in assignment.items():
        if value:
            print(mapeamento_para_int_inv[var])
else:
    print("Não foi encontrada uma solução válida.")


for i in range(1, n+1):
    linha = []
    for j in range(1, n+1):
        variavel = mapeamento_para_int[f"R_{i}_{j}"]
        if variavel in clausulas:
            linha.append("X")
        else:
            linha.append("O")
    print(" ".join(linha))
