from collections import defaultdict
import os
import time
import matplotlib.pyplot as plt
import numpy as np
import random

class Grafo:
    #construtor 
    @classmethod
    def le_net (cls, arquivo):
      file = open(arquivo,"r")
      vertices = []
      vertice = True
      clase = None
      for i in file:
        if i[0] != "*" and vertice:
          quebrado = i.split("\"")
          vertices.append(quebrado[1])
        if vertice and i[0] == "*":
          vertice = False
          if i[1] == "a":
            print("direcionado")
            clase = cls(True)
          else: 
            clase = cls(False)
          for j in vertices:
            clase.adiciona_vertice(j)
          continue
        if not vertice:
          quebrado = i.split(" ")
          clase.adiciona_aresta(vertices[int(quebrado[0])-1],vertices[int(quebrado[1])-1],int(quebrado[2]))  
      file.close()
      return clase   

    
    def __init__(self,direcionado):
        self.lista_adjacencia = defaultdict(list)
        self.vertices = []
        self.ordem = 0
        self.tamanho = 0
        self.direcionado = direcionado
    
      

    @classmethod
    def grafo_aleatorio(cls,n_vertices,n_arestas,direcionado):
      self = cls(direcionado)
      for i in range(n_vertices):
        self.adiciona_vertice(i)
      while n_arestas > 0:
        a = random.choice(self.vertices)
        b = random.choice(self.vertices)
        if  a != b:
          if  not self.tem_aresta(a,b):
             n_arestas -= 1 
          self.adiciona_aresta(a,b,random.randrange(1,101))
      return self

    @classmethod
    def sfn_le_users(cls,n_vertices_init, prob, n_vertices_max, n_arestas_max, k, direcionado, arquivo):
      if k < n_vertices_max:
        file = open(arquivo)
        cont = 0
        classe = cls(direcionado)
        for vert in file:
            print(cont)
            if cont < n_vertices_init:
                classe.adiciona_vertice(vert)
                for j in classe.lista_adjacencia:
                    if vert != j:
                        num_aleatorio = np.random.random()
                        if num_aleatorio > prob:         
                            classe.adiciona_aresta(vert,j,random.randrange(1,101))
                #print(classe.lista_graus_n_direcionado())
            elif cont < n_vertices_max:
                #len(classe.lista_adjacencia[i]) grau
                # (2 * classe.tamanho) soma dos graus
                classe.adiciona_vertice(vert)
                cont_add = 0
                adicionados = []
                if(classe.tamanho < n_arestas_max):
                    while(k > cont_add):
                        for i in classe.lista_adjacencia:
                            n = random.random()
                            soma_graus = 0
                            if classe.direcionado:
                                soma_graus = np.sum(classe.lista_graus())
                            else:
                                soma_graus = 2 * classe.tamanho
                            if vert != i and k > cont_add and (n < classe.grau_saida_int(j) / soma_graus) and i not in adicionados:
                                classe.adiciona_aresta(vert,i,random.randrange(1,101))
                                adicionados.append(i)
                                cont_add += 1
            else:
                break
            cont += 1
      
        file.close()
      return classe
    

    #verifica se u e v são adjacêntes
    def tem_aresta(self, u, v):
        #verifica se u e v já são vertices adicionados
        if all(x in self.vertices for x in [u, v]):
            #verifica se u e v são adjacentes
            for adj in self.lista_adjacencia[u]:
                if adj[0] == v:
                    return True
            return False
        else:
            #print(f"os vértices {u} ou {v} não foram adicionados")
            return False
    #adiciona um vértice u 
    def adiciona_vertice(self, u):
        #se u não foi adicionado, então pode ser adicionado 
        if u not in self.vertices:
            self.ordem += 1
            self.vertices.append(u)
            self.lista_adjacencia[u] = []
        #else:
            #print(u + " já é um vértice")
    #adiciona uma aresta entre u e v 
    def adiciona_aresta(self, u, v, peso):
        nao_achou = not self.tem_aresta(u,v)
        # verifica se os vertices existem
        # se não existe, ele adiciona, caso contrário, ele atualiza o peso
        if (nao_achou):
            self.tamanho += 1
            self.lista_adjacencia[u].append((v, peso))
            if not self.direcionado:
              self.lista_adjacencia[v].append((u, peso))
        else:
            for i in range(len(self.lista_adjacencia[u])):
                if self.lista_adjacencia[u][i][0] == v:
                    self.lista_adjacencia[u].remove(self.lista_adjacencia[u][i])
                    self.lista_adjacencia[u].append((v, peso))
                    break
            
            if not self.direcionado:
              for i in range(len(self.lista_adjacencia[v])):
                if self.lista_adjacencia[v][i][0] == u:
                  self.lista_adjacencia[v].remove(self.lista_adjacencia[v][i])
                  self.lista_adjacencia[v].append((u, peso))
                  break

    def remove_aresta(self, u, v):
        remover = None
        #verifica se u e v são adjacêntes  
        if self.tem_aresta(u, v):
            #procura pela adjacência
            for adj in range(len(self.lista_adjacencia[u])):
                if self.lista_adjacencia[u][adj][0] == v:
                    remover = self.lista_adjacencia[u][adj]
                    self.tamanho -= 1
            #remove a adjacência
            self.lista_adjacencia[u].remove(remover)
            if not self.direcionado:
              self.lista_adjacencia[v].remove((u, remover[1]))
        #else:
            #print("Aresta não removida")
    def remove_vertice(self, u):
        #verifica se u é um vértice adicionado 
        if u in self.vertices:
          #remove o vértice
            self.lista_adjacencia.pop(u)
            self.vertices.remove(u)
            #remove adjacências existentes entre outros vértices e u
            for vertice in self.lista_adjacencia:
                for adj in self.lista_adjacencia[vertice]:
                    if adj[0] == u:
                        self.lista_adjacencia[vertice].remove(adj)
        #else:
            #print(f"os vértice {u} não foi adicionado")
    def peso(self, u, v):
        achou = False
        #verifica se u e v são vértices
        if all(x in self.vertices for x in [u, v]):
            # procura a a adjacência
            for adj in self.lista_adjacencia[u]:
                # printa o peso entre os 2
                if adj[0] == v:
                    print(f'o peso entre {u} e {v} é {adj[1]}')
                    achou = True
            # caso não há adjacência, printa que não existe adjacência
            if not achou:
                print(f"{u} e {v} não são adjacentes")
        else:
            print(f"os vértices {u} ou {v} não foram adicionados")
    def grau(self, u):
        #verifica se u é vértice
        if u in self.vertices:
            #verifica grau de saida
            grau_saida = len(self.lista_adjacencia[u])
            #print(f'{u} tem grau de saida {grau_saida}')
            grau_entrada = 0
            #verifica grau de saida
            if self.direcionado:
              for vertice in self.lista_adjacencia:
                  if vertice != u:
                      for adj in self.lista_adjacencia[vertice]:
                          if adj[0] == u:
                              grau_entrada += 1
            #print(f'{u} tem grau de entrada {grau_entrada}')
            #print(f'{u} tem grau {grau_entrada + grau_saida}')
            if self.direcionado:
              return grau_entrada, grau_saida, grau_entrada + grau_saida
            return grau_saida
        else:
            print(f"os vértice {u} não foi adicionado")
    def num_vertices(self):
        print("Número de vertices : ", end = '')
        print(self.ordem)
    
    def num_arestas(self):
        print("Número de arestas : ", end = '')
        print(self.tamanho)  
  
    def imprime_lista_adjacencias(self):
        #imprime vertice
        for vertice in self.lista_adjacencia:
            print(f'{vertice} -> ', end='')
            #imprime adjacências
            for adj in self.lista_adjacencia[vertice]:
                print(f'{adj} - ', end='')
            print(' ')
    
    def escreve_net_Grafo(self):
      if os.path.exists("teste.net"):
        os.remove("teste.net")
      file = open("teste.net","a")
      count = 1
      index = defaultdict(list)
      for i in self.lista_adjacencia:
        file.write(str(count)+" \""+str(i)+"\" \n")
        index[i] = count
        count += 1
      if self.direcionado:
        file.write("*arcs\n")
      else:
        file.write("*edges\n")
      for i in self.lista_adjacencia:
        for j in self.lista_adjacencia[i]:
          file.write(str(index[i])+" "+str(index[j[0]])+" "+str(j[1])+"\n")
      file.close()

    def dfs_kosaraju(self, v, visitados):   
      visitados[v]= True
      print(v, end = ' ')
      for i in self.lista_adjacencia[v]:
        if not visitados[i[0]]:
          self.dfs_kosaraju(i[0],visitados)

    def dfs_n_direcionado(self, v, visitados):   
      visitados[v]= True
      print(v, end = ' ')
      for i in self.lista_adjacencia[v]:
        if not visitados[i[0]]:
          self.dfs_n_direcionado(i[0], visitados)

    def pilhando(self,v,visitados, pilha):
        visitados[v]= True
        for i in self.lista_adjacencia[v]:
            if not visitados[i[0]]:
                self.pilhando(i[0], visitados, pilha)
        pilha = pilha.append(v)

    def transposta(self):
        g = Grafo(True)
        for u in self.lista_adjacencia:
            for v in self.lista_adjacencia[u]:
                g.adiciona_aresta(v[0],u, v[1])
        return g
      

    def numero_componentes_direcionado(self):
        print("Componentes: ")
        n_componentes = 0
        pilha = []
        visitados = defaultdict(list)
        for i in self.lista_adjacencia:
          visitados[i] = False
        for j in self.lista_adjacencia:
            if not visitados[j]:
              self.pilhando(j, visitados, pilha)
        grafo_trans = self.transposta()
        for i in self.lista_adjacencia:
          visitados[i] = False
        while pilha:
            i = pilha.pop()
            if not visitados[i]:
              grafo_trans.dfs_kosaraju(i, visitados)
              print()
              n_componentes += 1
        print("Numero de Componentes: " + str(n_componentes))
    
    def numero_componentes_n_direcionado(self):
        n_componentes = 0
        visitados = defaultdict(list)
        for i in self.lista_adjacencia:
          visitados[i] = False
        for v in self.lista_adjacencia:
          if not visitados[v]:
            self.dfs_n_direcionado(v, visitados)
            print()
            n_componentes += 1
        print("Numero de Componentes: " + str(n_componentes))


    def bfs(self, u):
      visitados = []
      lista = []
      lista.append(u)
      while lista:
        s = lista.pop(0)
        if s not in visitados:
          visitados.append(s)
          for x in self.lista_adjacencia[s]:
            if x not in visitados:
              lista.append(x[0])
      return visitados  

    def bfs_parada(self, u, destino):
      visitados = []
      lista = []
      lista.append(u)
      while lista:
        s = lista.pop(0)
        if s not in visitados:
          visitados.append(s)
          for x in self.lista_adjacencia[s]:
            if x not in visitados:
              lista.append(x[0])
              if x[0] == destino:
                for i in range(len(lista)):
                    if lista[i] not in visitados:
                        visitados.append(lista[i])
                return visitados
      return False

    def Dijkstra(self, u, v):
        if self.bfs_parada(u,v):
            custo = defaultdict(list)
            nos_visitados = []  
            for i in self.bfs(u):
                custo[i] = [np.inf, "-"] 
            custo[u][0] = 0
            no_atual = u
            while len(nos_visitados) < self.ordem:
                for adj in self.lista_adjacencia[no_atual]:
                    if adj[0] not in nos_visitados:
                        custo_acumulativo = custo[no_atual][0] + 1
                        if(custo[adj[0]][0] == np.inf or (custo_acumulativo < custo[adj[0]][0])):
                            custo[adj[0]][0] = custo_acumulativo
                            custo[adj[0]][1] = no_atual
                nos_visitados.append(no_atual)
                menor = np.inf
                for j in custo:
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
            while v != '-':
                caminho.append(v)
                v = custo[v][1]
            return(caminho[::-1],caminho_peso)
        else:
            return([],0)

    def todos_menores_caminhos(self):
        menores_caminhos = []
        for i in range(len(self.vertices)):
            for j in range(i+1,len(self.vertices)):
              vertice1 = self.vertices[i]
              vertice2 = self.vertices[j]
              menor = self.Dijkstra(vertice1,vertice2)[0]
              menores_caminhos.append(menor)
                #self.bfs_alcancavel(str(i),str(j))
        return menores_caminhos

    def ehCiclico(self):
      self.finished = []
      lista = self.lista_adjacencia 
      for i in lista:
        if not i in self.finished:
          if self.visit(i,[],lista,""):
            return True 
      return False

    def visit(self,vert, visitados, lista, anterior):
      copy_visitados = visitados.copy()
      if not vert in copy_visitados:
        vizinhos = []
        for i in lista[vert]:
          vizinhos.append(i[0])
        copy_visitados.append(vert)
        for vizinho in vizinhos:
          if vizinho in copy_visitados:
            if vizinho == anterior and (not self.direcionado):
              continue
            else:
              return True
          if not vizinho in self.finished:
            if self.visit(vizinho,copy_visitados,lista,vert):
              return True
        self.finished.append(vert)
        return False
      return False

    def transforma_DAG(self):
      if not self.direcionado:
        print("Grafo não direcionado")
        return self
      if self.ehCiclico():
        self.tamanho = 0
        ex_lista_adjacencia = sorted(self.lista_adjacencia.items(), key=lambda a: len(a[1]), reverse=True)
        for i in self.lista_adjacencia:
           self.lista_adjacencia[i] = []
       
        self.lista_adjacencia[ex_lista_adjacencia[0][0]] = ex_lista_adjacencia[0][1]

        visitados = [ex_lista_adjacencia[0][0]]
        for i in range(1, len(ex_lista_adjacencia)):
            visitados.append(ex_lista_adjacencia[i][0])
            for j in range(len(ex_lista_adjacencia[i][1])):
                if ex_lista_adjacencia[i][1][j][0] not in visitados:
                    self.adiciona_aresta(ex_lista_adjacencia[i][0], ex_lista_adjacencia[i][1][j][0], ex_lista_adjacencia[i][1][j][1])            
      else:
        return self

    def lista_graus(self):
        graus = []
        
        for vertice in self.lista_adjacencia:
            graus.append(self.grau_saida_int(vertice))
        return graus
   

    def todos_menores_caminhos_grafico(self):
        menores_caminhos = []
        for i in range(len(self.vertices) - 1):
            print(i)
            for j in range(i+1, len(self.vertices)):
                menor = len(self.Dijkstra(self.vertices[i],self.vertices[j])[0])
                if menor != 0:
                    menores_caminhos.append(menor)
                #self.bfs_alcancavel(str(i),str(j))
        return menores_caminhos

    def histograma_menor_caminho(self):
        menor_caminho = self.todos_menores_caminhos_grafico()
        plt.hist(menor_caminho)
        media = np.mean(menor_caminho)
        plt.axvline(media, color='k', linestyle='dashed', linewidth=1)

        min_ylim, max_ylim = plt.ylim()
        plt.text(media*1.1, max_ylim*0.9, 'Média: {:.2f}'.format(media))
        plt.xlabel("menores caminhos")
        plt.ylabel("quantidade de duplas")
        plt.show()
 
    def histograma_graus(self):
        graus = self.lista_graus()
        plt.hist(graus)
        media = np.mean(graus)
        plt.axvline(media, color='k', linestyle='dashed', linewidth=1)

        min_ylim, max_ylim = plt.ylim()
        plt.text(media*1.1, max_ylim*0.9, 'Média: {:.2f}'.format(media))
        plt.xlabel("Graus")
        plt.ylabel("número de nós")
        plt.show()
 


    def Vertice_Central_Intermediacao(self):
      menor_caminhos = self.todos_menores_caminhos()
      dict_vertices = defaultdict(list)
      for i in self.vertices:
        dict_vertices[i] = 0
      for caminho in menor_caminhos:
        for indice in range(1,len(caminho)-1):
          vertice = caminho[indice]
          dict_vertices[vertice] += 1
      central = ["",0]
      for vertice in dict_vertices:
        print(vertice + ": "+str(dict_vertices[vertice]))
        if central[1] < dict_vertices[vertice]:
          central = [vertice, dict_vertices[vertice]]
      return central
    
    def Menores_Caminhos_Vertice(self,vertice):
      caminhos = []
      for i in self.vertices:
        if i != vertice:
          caminhos.append(self.Dijkstra(vertice,i)[0])
      return caminhos
    
    def Vertice_Central_Proximidade(self):
      dict_vertices = defaultdict(list)
      for i in self.vertices:
        dict_vertices[i] = [self.Menores_Caminhos_Vertice(i),0]
      for vertice in dict_vertices:
        for caminho in dict_vertices[vertice][0]:
          if  len(caminho) == 0:
            dict_vertices[vertice][1] += 0
          else:
            dict_vertices[vertice][1] += len(caminho)-1
      central = ["",0]
      for vertice in dict_vertices:
        if  dict_vertices[vertice][1] > 0:
          proximidade = (len(dict_vertices[vertice][0]))/dict_vertices[vertice][1]
          print(vertice + ":  " +str(proximidade))
          if central[1] < proximidade:
            central = [vertice,proximidade]
      return central

    def Transforma_em_Conexo(self):
       if not self.direcionado:
         conectados = self.bfs(self.vertices[0])
         while (len(conectados) != len(self.vertices)):
           for vertice in self.vertices:
             if not (vertice in conectados):
               self.adiciona_aresta(random.choice(conectados),vertice,random.randrange(1,101))
               conectados = self.bfs(self.vertices[0])
    
    def Arvore_Minima(self,grafo):
      if grafo.direcionado:
        print("Grafo direcionado")
        return grafo
      menor_caminhos = grafo.todos_menores_caminhos()
      for caminho in menor_caminhos:
        if caminho == []:
          print("Grafo não conexo")
          return grafo
      arestas = grafo.lista_adjacencia
      arvore = Grafo(False)
      for vertice in grafo.vertices:
        arvore.adiciona_vertice(vertice)
      while (arvore.tamanho != (arvore.ordem-1)): 
        menor_aresta = ["","",101]
        for vertice in arestas:
          for adjacencia in arestas[vertice]:
            if adjacencia[1] < menor_aresta[2] or menor_aresta[2] == 101:
              menor_aresta = [vertice,adjacencia[0],adjacencia[1]]
              if adjacencia[1] == 1:
                break
          else:
            continue
          break
        grafo.remove_aresta(menor_aresta[0],menor_aresta[1])
        arvore.adiciona_aresta(menor_aresta[0],menor_aresta[1],menor_aresta[2])
        if arvore.ehCiclico():
          arvore.remove_aresta(menor_aresta[0],menor_aresta[1])
      return arvore

#g = Grafo.le_net("teste.net")
#g = Grafo.sfn_le_users(n_vertices_init = 100, prob = 0.8, n_vertices_max = 10, n_arestas_max = 15000, k = 1, direcionado = True, arquivo = "Users.txt")
#print(g.lista_graus())
#g.imprime_lista_adjacencias()

#g.escreve_net_Grafo("SFN_PAJEK.net")
#g.imprime_lista_adjacencias()
#print(g.Vertice_Central_Intermediacao())
#print(g.Vertice_Central_Proximidade())
#print(g.bfs(g.vertices[0]))
g = Grafo.grafo_aleatorio(n_vertices = 100,n_arestas= 10,direcionado= False)
g.numero_componentes_n_direcionado()


g = Grafo.grafo_aleatorio(n_vertices = 100,n_arestas= 300,direcionado= True)
g.numero_componentes_direcionado()
g.num_vertices()
g.num_arestas()

print("é ciclico " + str(g.ehCiclico()))
g.transforma_DAG()
print("Transformou DAG")
print("é ciclico " + str(g.ehCiclico()))
g.num_vertices()
g.num_arestas()
#print("-=-=-=-=-=-")
"""
print("DAG:")
g.transforma_DAG()
g.num_arestas()
g.num_vertices()
#g.imprime_lista_adjacencias()
g.histograma_graus()
"""
#g.histograma_menor_caminho()



