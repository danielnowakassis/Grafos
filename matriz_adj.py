import numpy as np

class Grafo:
  #construtor
    def __init__(self, n_vertices, direcionado, ponderado):
      self.ordem = n_vertices
      self.tamanho = 0
      self.matriz_adjacencias = np.ones((n_vertices,n_vertices)) * np.inf
      self.direcionado = direcionado
      self.ponderado = ponderado
    #metodos 
    def adiciona_aresta(self, u , v, peso):
      if u > self.ordem or v > self.ordem:
        print("out of bound")
      else:
        if self.direcionado:
          if not self.tem_aresta(u,v):
            self.tamanho += 1
            if not self.ponderado:
              peso = 1
            self.matriz_adjacencias[u][v] = peso
        else:
          if not self.tem_aresta(u,v)  and not self.tem_aresta(v,u):
            self.tamanho += 1
            if not self.ponderado:
              peso = 1
            self.matriz_adjacencias[u][v] = peso
            self.matriz_adjacencias[v][u] = peso

    def retorna_adjacentes(self, u):
      adjacentes = []
      if u > self.ordem:
        print("out of bound")
        return False
      else:
        for i in range(self.ordem):
            if self.matriz_adjacencias[u][i] != np.inf:
              adjacentes.append(i)  
        return adjacentes
        

    def remove_aresta(self, u,v):
      if self.direcionado:
        if self.tem_aresta(u,v):
          self.tamanho -= 1  
          self.matrix_adjacencias[u][v] = np.inf
      if not self.direcionado:
        if self.tem_aresta(u,v):
          self.tamanho -= 1
          self.matrix_adjacencias[u][v] = np.inf
          self.matrix_adjacencias[v][u] = np.inf

    def tem_aresta(self , u , v):
      if self.matriz_adjacencias[u][v] == np.inf:
          return False
      else:
          return True
        

    def grau_entrada(self, u):
      if not self.direcionado:
        print("O Grafo não é direcionado, então não possui grau de entrada")
        return
      grau_entrada = 0
      for i in range(self.ordem):
        if self.matriz_adjacencias[i][u] != np.inf:
          grau_entrada += 1
      print(f"O grau de entrada do vértice {u} é {grau_entrada}")
      return grau_entrada

    def grau_saida(self, u):
      if not self.direcionado:
        print("O Grafo não é direcionado, então não possui grau de saída")
        return
      grau_saida = 0
      for i in range(self.ordem):
        if self.matriz_adjacencias[u][i] != np.inf:
          grau_saida += 1
      print(f"O grau de saida do vértice {u} é {grau_saida}")
      return grau_saida
    
    def grau(self, u):
      grau = 0
      if self.direcionado:
        for i in range(self.ordem):
          # if u != i
            if self.matriz_adjacencias[i][u] != np.inf:
              grau += 1
            if self.matriz_adjacencias[u][i] != np.inf:
              grau += 1
        print(f"O grau  do vértice {u} é {grau}")
        return grau
      if not self.direcionado:
        for i in range(self.ordem):
          # if u != i
            if self.matriz_adjacencias[u][i] != np.inf:
              grau += 1
        print(f"O grau  do vértice {u} é {grau}")
        return grau

    def eh_denso(self):
      if self.tamanho > self.max_arestas() * 0.9:
        return True
      else:
        return False 
    def max_arestas(self):
      if self.direcionado:
        return (self.ordem * (self.ordem - 1))
      if not self.direcionado:
        return ( self.ordem * ( self.ordem - 1 ) ) / 2

    def imprime_matriz_adjacencias(self):
      print("========== Matriz de Adjacências =========")
      for i in range(self.ordem):
        print(f"{i}: {self.matriz_adjacencias[i]}")

    def warshall(self):
        #transformar matriz de pesos em matriz binária 
        matriz = np.zeros((self.ordem, self.ordem))
        for i in range(self.ordem):
            for k in range(self.ordem):
                if self.matriz_adjacencias[i][k] != np.inf:
                    matriz[i][k] = 1
                else:
                    matriz[i][k] = 0
        print(matriz)
        for k in range(self.ordem):
            for i in range(self.ordem):
                for j in range(self.ordem):
                    matriz[i][j] = matriz[i][j] or (matriz[i][k] and matriz[k][j])
            print(matriz)
    
    def Dijkstra(self, u, v):
        nos_visitados = []  
        custo = [[np.inf, "-"] for i in range(self.ordem)]
        custo[u][0] = 0
        no_atual = u
        while len(nos_visitados) < self.ordem:
            nos_adjacentes = self.retorna_adjacentes(no_atual)
            for adj in nos_adjacentes:
                if adj not in nos_visitados:
                    custo_acumulativo = custo[no_atual][0] + self.matriz_adjacencias[no_atual][adj]
                    if(custo[adj][0] == np.inf or (custo_acumulativo < custo[adj][0])):
                        custo[adj][0] = custo_acumulativo
                        custo[adj][1] = no_atual
            nos_visitados.append(no_atual)
            menor = np.inf
            for j in range(len(custo)):
                if(j not in nos_visitados):
                    if(menor == np.inf):
                        menor = custo[j][0]
                        no_atual = j
                    else:
                        if(menor > custo[j][0]):
                            menor = custo[j][0]
                            no_atual = j
        caminho = []
        caminho_peso = custo[v][0]
        print(custo)
        while v != '-':
            caminho.append(v)
            v = custo[v][1]
        return(caminho[::-1],caminho_peso)
        
"""
g = Grafo(n_vertices = 5, direcionado =  True , ponderado = True)
g.adiciona_aresta(3,2,6)
g.imprime_matriz_adjacencias()
g.adiciona_aresta(1,2,9)
g.adiciona_aresta(0,4,10)
g.adiciona_aresta(1,3,1)
g.adiciona_aresta(4,0,10)
g.adiciona_aresta(4,2,3)
g.adiciona_aresta(4,1,10)
print(g.retorna_adjacentes(4))
g.imprime_matriz_adjacencias()
g.warshall()"""
"""
g = Grafo(n_vertices = 3, direcionado =  True , ponderado = True)
g.adiciona_aresta(0,1,1)
g.adiciona_aresta(0,2,3)
g.adiciona_aresta(1,2,2)
g.Dijkstra(0,1)


g = Grafo(n_vertices = 4, direcionado =  True , ponderado = False)
g.adiciona_aresta(0,1,1)
g.adiciona_aresta(1,1,1)
g.adiciona_aresta(1,2,1)
g.adiciona_aresta(2,0,1)
g.adiciona_aresta(3,1,1)
g.adiciona_aresta(3,2,1)    
g.warshall()
print(g.Dijkstra(0,3))
"""

