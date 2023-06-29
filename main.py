!pip install python-sat

#exemplo de uso glucose
from pysat.solvers import Glucose3
g = Glucose3()
g.add_clause([1, 2])
g.add_clause([-1, 2])
g.add_clause([1, -2])
g.add_clause([-1, -2])
print(g.solve())
print(g.get_model())


#mapear os simbolos proposicionais (atomos)
N = 5
counter = 1
mapping_to_int = {}
mapping_to_int_inv = {}
positions = [[i,j] for i in range(1,N+1) for j in range(1,N+1)]
for position in positions:
  key = f"Q_{position[0]}_{position[1]}"
  mapping_to_int[key] = counter
  mapping_to_int_inv[counter] = key
  counter = counter + 1

dict(zip(["a","b","c","d"], range(4)))

#gerando uma instancia do solver (DPLL)
g = Glucose3()

#cada linha possui PELO MENOS UMA rainha
for i in range(1,N+1):
  line = []
  for j in range(1, N+1):
    line.append(mapping_to_int[f"Q_{i}_{j}"])
  g.add_clause(line)

#implementar cada linha possui NO MAXIMO UMA RAINHA


#implementar cada coluna possui PELO MENOS UMA RAINHA

#cada coluna possui NO MAXIMO uma rainha
for j in range(1,N+1):
  for i in range(1, N+1):
    other_indexes = list(range(1,N+1))
    other_indexes.remove(i)
    for other in other_indexes:
      #Q_i_j -> ~Q_k_j === ~Q_i_j v ~Q_k_j
      clause = [-mapping_to_int[f"Q_{i}_{j}"], -mapping_to_int[f"Q_{other}_{j}"]]
      g.add_clause(clause)


print(g.solve())
print(g.get_model())

#diagonais primarias
diff = -1
a = [[i,j] for i in range(1, N+1) for j in range(1,N+1) if i-j == diff]
a

#sugestao
#implementar que cada diagonal (primaria ou secundaria)
#possui NO MAXIMO UMA RAINHA