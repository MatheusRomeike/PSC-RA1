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


tamanhoCache = int(input("Digite o tamanho da memoria cache: "))
memoriaCache = inicializarCache(tamanhoCache)

mapeamentoDireto(tamanhoCache, [1, 6, 1, 11, 1,
                 16, 1, 21, 1, 26], memoriaCache)
