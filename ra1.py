from collections import deque

def inicializarCache(tamanhoCache):
    memoriaCache = {}
    for i in range(tamanhoCache):
        memoriaCache[i] = -1
    return memoriaCache

def imprimirCache(memoriaCache):
    print("Tamanho da memoria cache: ", len(memoriaCache))
    for memoria in memoriaCache.items():
        print("Posição Cache > ", memoria, "< Posição Memória")
    print("--------------------------------------------------")

def buscarValorEmCache(memoriaCache, posicaoMemoria):
    for cache, memoria in memoriaCache.items():
        if memoria == posicaoMemoria:
            return True
    return False

def mapeamentoDireto(tamanhoCache, posMemoria, memoriaCache):
    totalPosicoesAcessadas = 0
    hit = 0
    miss = 0
    for posicaoMemoria in posMemoria:
        totalPosicoesAcessadas += 1
        posicaoCache = posicaoMemoria % tamanhoCache
        print("Posição de memória desejada: ", posicaoMemoria)

        if (buscarValorEmCache(memoriaCache, posicaoMemoria)):
            hit += 1
            print("Linha: ", totalPosicoesAcessadas, " Status: Hit")
        else:
            miss += 1
            print("Linha: ", totalPosicoesAcessadas, " Status: Miss")

        memoriaCache[posicaoCache] = posicaoMemoria

        imprimirCache(memoriaCache)

    print("--------------------------------------------------")
    print("Total de posições acessadas: ", totalPosicoesAcessadas)
    print("Total de hits: ", hit)
    print("Total de miss: ", miss)
    print("Taxa de acertos: ", (hit / totalPosicoesAcessadas) * 100, "%")

def mapeamentoAssociativoFIFO(numConjuntos, tamCache, posMemoria):
    print("-----------------------FIFO-------------------------")

    cache = [[] for _ in range(numConjuntos)]
    filaFifo = [[] for _ in range(numConjuntos)]
    totalPosicoesAcessadas = 0
    hit = 0
    miss = 0
    
    for posicao in posMemoria:
        totalPosicoesAcessadas += 1
        conjunto = posicao % numConjuntos
        if posicao in cache[conjunto]:
            hit += 1
            print("Linha: ", totalPosicoesAcessadas, " Status: Hit")
        else:
            miss += 1
            print("Linha: ", totalPosicoesAcessadas, " Status: Miss")
            if len(cache[conjunto]) == tamCache:
                posicaoRemovida = filaFifo[conjunto].pop(0)

                cache[conjunto].remove(posicaoRemovida)

                print("A posição de memória ", posicaoRemovida, " foi removida da cache.")

            cache[conjunto].append(posicao)
            filaFifo[conjunto].append(posicao)

            print("A posição de memória ", posicao, " foi adicionada à cache.")

        imprimirCacheConjunto(cache)
    
    print("--------------------------------------------------")
    print("Total de posições acessadas: ", totalPosicoesAcessadas)
    print("Total de hits: ", hit)
    print("Total de miss: ", miss)
    print("Taxa de acertos: ", (hit / totalPosicoesAcessadas) * 100, "%")

def mapeamentoAssociativoConjuntoLRU(numConjuntos, tamCache, posMemoria):
    print("-----------------------LRU-------------------------")
    cache = [[] for i in range(numConjuntos)]
    totalPosicoesAcessadas = 0
    hit = 0
    miss = 0
    lru = [[0 for j in range(tamCache // numConjuntos)] for i in range(numConjuntos)]
    for posicaoMemoria in posMemoria:
        totalPosicoesAcessadas += 1
        conjunto = posicaoMemoria % numConjuntos
        print("Posição de memória desejada: ", posicaoMemoria)

        if posicaoMemoria in cache[conjunto]:
            hit += 1
            print("Linha: ", totalPosicoesAcessadas, " Status: Hit")
            lru[conjunto][cache[conjunto].index(posicaoMemoria)] = totalPosicoesAcessadas
        else:
            miss += 1
            print("Linha: ", totalPosicoesAcessadas, " Status: Miss")
            if len(cache[conjunto]) == tamCache // numConjuntos:
                posicaoLRU = lru[conjunto].index(min(lru[conjunto]))
                lru[conjunto].pop(posicaoLRU)
                cache[conjunto].pop(posicaoLRU)
            cache[conjunto].append(posicaoMemoria)
            lru[conjunto].append(totalPosicoesAcessadas)

        imprimirCacheConjunto(cache)

    print("--------------------------------------------------")
    print("Total de posições acessadas: ", totalPosicoesAcessadas)
    print("Total de hits: ", hit)
    print("Total de miss: ", miss)
    print("Taxa de acertos: ", (hit / totalPosicoesAcessadas) * 100, "%")
    

def mapeamentoAssociativoConjuntoLFU(tamanhoCache, numConjuntos, posMemoria):
    print("-----------------------LFU-------------------------")
    totalPosicoesAcessadas = 0
    hit = 0
    miss = 0
    cache = [[] for _ in range(numConjuntos)] 
    frequencia = [[0 for _ in range(tamanhoCache)] for _ in range(numConjuntos)]

    for posicaoMemoria in posMemoria:
        totalPosicoesAcessadas += 1
        conjunto = posicaoMemoria % numConjuntos
        posicaoCache = -1
        for i, bloco in enumerate(cache[conjunto]):
            if bloco == posicaoMemoria:
                hit += 1
                posicaoCache = i
                break
        if posicaoCache == -1:
            miss += 1
            if len(cache[conjunto]) < tamanhoCache:
                posicaoCache = len(cache[conjunto])
                cache[conjunto].append(posicaoMemoria)
            else:
                minFrequencia = min(frequencia[conjunto])
                for i, f in enumerate(frequencia[conjunto]):
                    if f == minFrequencia:
                        posicaoCache = i
                        break
                cache[conjunto][posicaoCache] = posicaoMemoria
            frequencia[conjunto][posicaoCache] = 1
        else:
            frequencia[conjunto][posicaoCache] += 1

        print("Posição de memória desejada: ", posicaoMemoria)
        imprimirCacheConjunto(cache)

    print("--------------------------------------------------")
    print("Total de posições acessadas: ", totalPosicoesAcessadas)
    print("Total de hits: ", hit)
    print("Total de miss: ", miss)
    print("Taxa de acertos: ", (hit / totalPosicoesAcessadas) * 100, "%")

def imprimirCacheConjunto(conjuntos):
    print("Cache:")
    for i in range(len(conjuntos)):
        print("Conjunto", i, ": ", end="")
        for j in range(len(conjuntos[i])):
            print(conjuntos[i][j], end=" ")
        print()
    print()


tamanhoCache = int(input("Digite o tamanho da memoria cache: "))

# memoriaCache1 = inicializarCache(tamanhoCache)

# mapeamentoDireto(tamanhoCache, [1, 2, 1, 2, 4, 3, 2, 9, 12, 1, 2, 22, 23,  1, 2, 3, 2], memoriaCache1)

tamanhosPossiveis = [1, 2, 4 ,8, 16]
tecnicasSubstituicao = ['LRU', 'lru', 'LFU', 'lfu', 'FIFO', 'fifo']
condicao = 0
while condicao < 1:
    tamanhoConjunto = int(input("Digite o tamanho do conjunto: 1, 2, 4, 8 ou 16 blocos: "))
    tecnicaSubstituicao = input("Digite qual tecnica de substituição deseja utilizar (LFU, LRU ou FIFO): ")
    if  tamanhoConjunto not in tamanhosPossiveis:
        print("Tamanho de conjunto não é valido")
    elif tecnicaSubstituicao not in tecnicasSubstituicao:
        print("Digite uma técnica de substituição válida")
    else:
        condicao = 1


        


memoriaCache = inicializarCache(tamanhoCache)
print(memoriaCache)
posMemo = [1, 2, 1, 11, 1,
                 16, 1, 21, 1, 26, 4, 5, 6, 7, 8, 12 ,34 , 45, 45 ,65 ,32, 123]

if tecnicaSubstituicao == "LRU" or tecnicaSubstituicao == "lru":
    mapeamentoAssociativoConjuntoLRU(tamanhoConjunto, tamanhoCache, [1, 2, 1, 2, 4, 3, 2, 9, 12, 1, 2, 22, 23,  1, 2, 3, 2])
elif tecnicaSubstituicao == "LFU" or tecnicaSubstituicao == "lfu":
    mapeamentoAssociativoConjuntoLFU(tamanhoCache, tamanhoCache, [1, 2, 1, 2, 4, 3, 2, 9, 12, 1, 2, 22, 23,  1, 2, 3, 2])
else: 
    mapeamentoAssociativoFIFO(tamanhoConjunto, tamanhoCache, [1, 2, 1, 2, 4, 3, 2, 9, 12, 1, 2, 22, 23,  1, 2, 3, 2])


