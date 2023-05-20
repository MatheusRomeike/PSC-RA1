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

# def mapeamentoAssociativoFIFO(posMemoria, numConjuntos, tamCache):
#     totalPosicoesAcessadas = 0
#     hit = 0
#     miss = 0
#     posicaoCache = 0
#     for posicaoMemoria in posMemoria:
#         totalPosicoesAcessadas += 1
#         print("Posição de memória desejada: ", posicaoMemoria)

#         if (buscarValorEmCache(memoriaCache, posicaoMemoria)):
#             hit += 1
#             print("Linha: ", totalPosicoesAcessadas, " Status: Hit")
#         else:
#             miss += 1
#             print("Linha: ", totalPosicoesAcessadas, " Status: Miss")

#             if posicaoCache > len(memoriaCache) - 1:
#                 posicaoCache = 0
#             memoriaCache[posicaoCache] = posicaoMemoria
#             posicaoCache += 1
#         imprimirCache(memoriaCache)

#     print("--------------------------------------------------")
#     print("Total de posições acessadas: ", totalPosicoesAcessadas)
#     print("Total de hits: ", hit)
#     print("Total de miss: ", miss)
#     print("Taxa de acertos: ", (hit / totalPosicoesAcessadas) * 100, "%")

def mapeamentoAssociativoFIFO(numConjuntos, tamCache, posMemoria):
    totalPosicoesAcessadas = 0
    hit = 0
    miss = 0
    memoriaCache = [[] for _ in range(tamCache)]
    conjuntoCache = [[] for _ in range(numConjuntos)]

    for posicaoMemoria in posMemoria:
        totalPosicoesAcessadas += 1
        print("Posição de memória desejada:", posicaoMemoria)

        conjuntoIndex = posicaoMemoria % numConjuntos
        cacheIndex = conjuntoCache[conjuntoIndex].index(posicaoMemoria) if posicaoMemoria in conjuntoCache[conjuntoIndex] else -1

        if cacheIndex != -1:
            hit += 1
            print("Linha:", totalPosicoesAcessadas, "Status: Hit")
        else:
            miss += 1
            print("Linha:", totalPosicoesAcessadas, "Status: Miss")

            if len(conjuntoCache[conjuntoIndex]) < tamCache:
                conjuntoCache[conjuntoIndex].append(posicaoMemoria)
            else:
                posicaoSubstituir = conjuntoCache[conjuntoIndex].pop(0)
                conjuntoCache[conjuntoIndex].append(posicaoMemoria)
                cacheIndex = memoriaCache.index(posicaoSubstituir)
                memoriaCache[cacheIndex] = posicaoMemoria

    #imprimirCacheConjunto(memoriaCache)

    print("--------------------------------------------------")
    print("Total de posições acessadas:", totalPosicoesAcessadas)
    print("Total de hits:", hit)
    print("Total de miss:", miss)
    print("Taxa de acertos:", (hit / totalPosicoesAcessadas) * 100, "%")


def mapeamentoAssociativoConjuntoLRU(numConjuntos, tamCache, posMemoria):
    conjuntos = [[] for i in range(numConjuntos)]
    totalPosicoesAcessadas = 0
    hit = 0
    miss = 0
    lru = [[0 for j in range(tamCache // numConjuntos)] for i in range(numConjuntos)]
    for posicaoMemoria in posMemoria:
        totalPosicoesAcessadas += 1
        conjunto = posicaoMemoria % numConjuntos
        print("Posição de memória desejada: ", posicaoMemoria)

        # Verifica se o valor está na cache
        if posicaoMemoria in conjuntos[conjunto]:
            hit += 1
            print("Linha: ", totalPosicoesAcessadas, " Status: Hit")
            # Atualiza a matriz LRU
            lru[conjunto][conjuntos[conjunto].index(posicaoMemoria)] = totalPosicoesAcessadas
        else:
            miss += 1
            print("Linha: ", totalPosicoesAcessadas, " Status: Miss")
            # Verifica se a cache do conjunto está cheia
            if len(conjuntos[conjunto]) == tamCache // numConjuntos:
                # Obtém a posição da cache que foi acessada menos recentemente
                posicaoLRU = lru[conjunto].index(min(lru[conjunto]))
                # Remove o valor da cache e atualiza a matriz LRU
                lru[conjunto].pop(posicaoLRU)
                conjuntos[conjunto].pop(posicaoLRU)
            # Adiciona o valor à cache do conjunto e atualiza a matriz LRU
            conjuntos[conjunto].append(posicaoMemoria)
            lru[conjunto].append(totalPosicoesAcessadas)

        imprimirCacheConjunto(conjuntos)

    print("--------------------------------------------------")
    print("Total de posições acessadas: ", totalPosicoesAcessadas)
    print("Total de hits: ", hit)
    print("Total de miss: ", miss)
    print("Taxa de acertos: ", (hit / totalPosicoesAcessadas) * 100, "%")
    

def mapeamentoAssociativoConjuntoLFU(tamanhoCache, numConjuntos, posMemoria):
    totalPosicoesAcessadas = 0
    hit = 0
    miss = 0
    conjuntos = [[] for _ in range(numConjuntos)] # cria uma lista de listas para representar os conjuntos
    frequencia = [[0 for _ in range(tamanhoCache)] for _ in range(numConjuntos)] # cria uma matriz de frequência

    for posicaoMemoria in posMemoria:
        totalPosicoesAcessadas += 1
        conjunto = posicaoMemoria % numConjuntos
        posicaoCache = -1
        # busca na cache
        for i, bloco in enumerate(conjuntos[conjunto]):
            if bloco == posicaoMemoria:
                hit += 1
                posicaoCache = i
                break
        # se não encontrou, adiciona na cache
        if posicaoCache == -1:
            miss += 1
            # verifica se há espaço no conjunto
            if len(conjuntos[conjunto]) < tamanhoCache:
                posicaoCache = len(conjuntos[conjunto])
                conjuntos[conjunto].append(posicaoMemoria)
            # se não há espaço, substitui o bloco menos frequente
            else:
                # encontra o bloco menos frequente
                minFrequencia = min(frequencia[conjunto])
                for i, f in enumerate(frequencia[conjunto]):
                    if f == minFrequencia:
                        posicaoCache = i
                        break
                # substitui o bloco menos frequente
                conjuntos[conjunto][posicaoCache] = posicaoMemoria
            # inicializa a frequência do novo bloco
            frequencia[conjunto][posicaoCache] = 1
        else:
            # incrementa a frequência do bloco
            frequencia[conjunto][posicaoCache] += 1

        print("Posição de memória desejada: ", posicaoMemoria)
        if posicaoCache == -1:
            print("Linha: ", totalPosicoesAcessadas, " Status: Miss")
        else:
            print("Linha: ", totalPosicoesAcessadas, " Status: Hit")
        imprimirCacheConjunto(conjuntos)

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


tamanhosPossiveis = [1, 2, 4 ,8, 16]
condicao = 0
while condicao < 1:
    tamanhoConjunto = int(input("Digite o tamanho do conjunto: 1, 2, 4, 8 ou 16 blocos: "))
    if  tamanhoConjunto not in tamanhosPossiveis:
        print("Tamanho de conjunto não é valido")
    else:
        condicao = 1
        


memoriaCache = inicializarCache(tamanhoCache)
print(memoriaCache)
# mapeamentoAssociativoConjuntoLRU(tamanhoConjunto, tamanhoCache, [1, 2, 1, 11, 1,
#                  16, 1, 21, 1, 26, 4, 5, 6, 7, 8, 12 ,34 , 45, 45 ,65 ,32, 123])

# mapeamentoAssociativoConjuntoLFU(tamanhoCache, tamanhoCache, [1, 2, 1, 11, 1,
#                  16, 1, 21, 1, 26, 4, 5, 6, 7, 8, 12 ,34 , 45, 45 ,65 ,32, 123])


mapeamentoAssociativoFIFO(tamanhoConjunto, tamanhoCache, [1, 2, 1, 11, 1,
                 16, 1, 21, 1, 26, 4, 5, 6, 7, 8, 12 ,34 , 45, 45 ,65 ,32, 123])


