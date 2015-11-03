# -*- coding: cp1252 -*-
import numpy as np
import pylab as PLAB
import random as RD


#Parametros

M = 1000 #ambientes disponíveis para serem ocupados
N = 200 #tamanho inicial da população
pop = N #medida de indivíduos vivos ao longo da dinamica, começa igual a 'N', mas decai com as mortes
Nmax = 1200 #tamanho máximo da população
T = N * 10 #número de rodadas
persistencia = 10 #busca por auxílio/ajuda/empréstimo/cooperação
consumo = 2.0 #consumo dos agentes
limiar_empregado = 2*consumo #para entrar na dinâmica de empréstimos
limiar_empregador = 4*consumo #para entrar na dinâmica de emprestémos
#epsilon = 0.8 #taxa/imposto/dívida - porcentagem a pagar
velocidade_recuperacao = 1 # velocidade de recuperacao do ambiente
votewithfeet = 0.5 #probabilidade de mudar de ambiente ou pedir ajuda
#link = 0 #link inicial dos agentes ... (!!!) não sei se ainda precisa ficar aqui
limite_reprodutivo = 4 #TEM QUE SER NÚMERO PAR AQUI!!!
fome_maxima = 4 #fome máxima para morte dos agentes


# variaveis do modelo
agente_do = np.zeros(M, dtype=np.int_) # lista dos agentes com seus ambientes ocupados
ambiente_do = np.zeros(Nmax, dtype=np.int_) # lista de ambientes ocupados pelo agente
conectividade = np.ones(Nmax, dtype=np.int_)
contador_populacional = np.ones(Nmax, dtype=np.float_)
eficiencia = np.zeros(Nmax, dtype=np.float_) # taxa de acertos na procura/busca/produção dos recursos
empregador = np.arange(Nmax, dtype=np.int_) # e - é o empregador do agente;
estoque = np.zeros(Nmax, dtype=np.float_) # St - estoque do agente na rodada atual;
fome = np.zeros(Nmax, dtype=np.float_) # f - fome dos agentes
habilidade = np.zeros(Nmax, dtype=np.float_) # h - habilidade dos agentes. é multiplicado por recurso_ambiente para obter a producao;
mudou = np.zeros(Nmax, dtype=np.float_) # mudou - medir agentes que trocam de ambiente
producao = np.zeros(Nmax, dtype=np.float_) # P - producao do agente na rodada atual;
producao_recebida = np.zeros(Nmax, dtype=np.float_) # Q - é a producao recebida pelo empregador na rodada atual (caso o agente nao seja um, é igual a producao do proprio agente);
recurso_ambiente = np.zeros(M, dtype=np.float_) # A - recurso do ambiente. é multiplicado por habilidade para obter a producao do agente; é regenerado por regeneracao_ambiente;
recurso_ambiente_k = np.zeros(M, dtype=np.float_) # K - capacidade de suporte do recurso do ambiente.
regeneracao_ambiente = np.zeros(M, dtype=np.float_) # rec - regeneracao do ambiente. incrementa o recurso do ambiente;
urna_agentes = range(N)
vida = np.ones(Nmax, dtype=np.bool_)

# listas para o Plot
lista_ambiente = [[] for i in xrange(Nmax)]
lista_conectividade = [[] for i in xrange(Nmax)]
lista_estoque = [[] for i in xrange(Nmax)]
lista_fome = [[] for i in xrange(Nmax)]
lista_links = [[] for i in xrange(Nmax)]
lista_nomadismo = [[] for i in xrange(Nmax)]
lista_producao = [[] for i in xrange(Nmax)]


#########################################################################
def configuracao_inicial():
    global N, pop, M, T, persistencia, consumo, limiar_empregado, limiar_empregador, epsilon, velocidade_recuperacao, votewithfeet, \
    habilidade, eficiencia, fome, mudou, recurso_ambiente, recurso_ambiente_k, regeneracao_ambiente, estoque, ambiente_do, agente_do, \
    producao, producao_recebida, empregador, conectividade, vida, urna_agentes, lista_estoque, lista_ambiente, lista_producao, lista_links, \
    lista_fome, lista_nomadismo, link, contador_populacional
    
    habilidade = np.random.lognormal(0.4, 0.5, Nmax) #/ 100 #(!!!)essa divisão por cem aqui, não sei o que é...
    eficiencia = np.random.lognormal(0.5, 0.2, Nmax) #introduz o efeito estocástico na busca por recursos
    recurso_ambiente = np.random.lognormal(0.8, 0.5, M) #+ 4
    recurso_ambiente_k = np.copy(recurso_ambiente)
    #resiliencia = recurso_ambiente * 0.25 #PRECISO aprender a definir a resiliência AQUI está dando pau nesta multiplicação
    #regeneracao_ambiente = np.random.lognormal(0.5, 0.5, M) #não está sendo usado na função de regeneracao()
    #estoque = np.random.lognormal(2.5, 0.5, N)
    estoque = 0
    agente = 0 #ENTENDER O QUE É ESTE PARAMETRO
    link = 0

    while agente < N: #associam-se, aqui, cada agente a um dos 'M' ambientes disponíveis
        ambiente_sorteado = RD.randint(0, M - 1)
        if agente_do[ambiente_sorteado] == 0:
            agente_do[ambiente_sorteado] = agente
            ambiente_do[agente] = ambiente_sorteado
            agente += 1 #(!!!) Precisa deste contador aqui???

def iniciar_rodada():
    global N, pop, M, T, persistencia, consumo, limiar_empregado, limiar_empregador, epsilon, velocidade_recuperacao, votewithfeet, \
    habilidade, eficiencia, fome, mudou, recurso_ambiente, recurso_ambiente_k, regeneracao_ambiente, estoque, ambiente_do, agente_do, \
    producao, producao_recebida, empregador, conectividade, vida, urna_agentes, lista_estoque, lista_ambiente, lista_producao, lista_links, \
    lista_fome, lista_nomadismo, link, contador_populacional
    
    for agente in xrange(N):
        producao_recebida[agente] *= 0

def produzir():
    global N, pop, M, T, persistencia, consumo, limiar_empregado, limiar_empregador, epsilon, velocidade_recuperacao, votewithfeet, \
    habilidade, eficiencia, fome, mudou, recurso_ambiente, recurso_ambiente_k, regeneracao_ambiente, estoque, ambiente_do, agente_do, \
    producao, producao_recebida, empregador, conectividade, vida, urna_agentes, lista_estoque, lista_ambiente, lista_producao, lista_links, \
    lista_fome, lista_nomadismo, link, contador_populacional
    
    #OPÇÃO TRADICIONAL DE PRODUÇÃO - consolidada - abaixo  
    #for agente in xrange(N):
        #producao[agente] = habilidade[agente] * recurso_ambiente[ambiente_do[agente]]
        #recurso_ambiente[ambiente_do[agente]] -= producao[agente]
    
    #OPÇÃO DE PRODUÇÃO ESTOCÁSTICA - ainda em teste - abaixo
    for agente in xrange(N):
        if RD.random() <= eficiencia[agente]:
            producao[agente] = habilidade[agente] * recurso_ambiente[ambiente_do[agente]] * contador_populacional[agente]
        else: producao[agente] = 0
        recurso_ambiente[ambiente_do[agente]] -= producao[agente]
                        
def distribuir(parametros):
    global N, pop, M, T, persistencia, consumo, limiar_empregado, limiar_empregador, epsilon, velocidade_recuperacao, votewithfeet, \
    habilidade, eficiencia, fome, mudou, recurso_ambiente, recurso_ambiente_k, regeneracao_ambiente, estoque, ambiente_do, agente_do, \
    producao, producao_recebida, empregador, conectividade, vida, urna_agentes, lista_estoque, lista_ambiente, lista_producao, lista_links, \
    lista_fome, lista_nomadismo, link, contador_populacional    
    
    for agente in xrange(N):
        if (empregador[agente] <> agente):
            producao_recebida[empregador[agente]] += producao[agente] * parametros[0]
            producao_recebida[agente] = producao[agente] * (1 - parametros[0])
	else:
	    producao_recebida[agente] = producao[agente]

def estocar():
    global N, pop, M, T, persistencia, consumo, limiar_empregado, limiar_empregador, epsilon, velocidade_recuperacao, votewithfeet, \
    habilidade, eficiencia, fome, mudou, recurso_ambiente, recurso_ambiente_k, regeneracao_ambiente, estoque, ambiente_do, agente_do, \
    producao, producao_recebida, empregador, conectividade, vida, urna_agentes, lista_estoque, lista_ambiente, lista_producao, lista_links, \
    lista_fome, lista_nomadismo, link, contador_populacional
    
    #for agente in xrange(N):
    #    estoque[agente] += producao_recebida[agente]
    estoque += producao_recebida   

	

def morrer():
    global N, pop, M, T, persistencia, consumo, limiar_empregado, limiar_empregador, epsilon, velocidade_recuperacao, votewithfeet, \
    habilidade, eficiencia, fome, mudou, recurso_ambiente, recurso_ambiente_k, regeneracao_ambiente, estoque, ambiente_do, agente_do, \
    producao, producao_recebida, empregador, conectividade, vida, urna_agentes, lista_estoque, lista_ambiente, lista_producao, lista_links, \
    lista_fome, lista_nomadismo, link, contador_populacional    
    
    for agente in xrange(N):
        if vida[agente]:
            vida[agente] = (fome[agente] < fome_maxima)
            if not vida[agente]:
                while(True):
                    try: urna_agentes.remove[agente] #(!!!) Será que está funcionando isto aqui?
                    except: break
                    habilidade[agente] = 0
                    #recurso_ambiente[ambiente_do[agente]] = 0
                    #regeneracao_ambiente[agente] = 0
                    agente_do[ambiente_do[agente]] = 0
                    estoque[agente] = 0
                    empregador[agente] = agente
                    pop -= contador_populacional[agente]
                    contador_populacional[agente] = 0

def associar(parametros):
    global N, pop, M, T, persistencia, consumo, limiar_empregado, limiar_empregador, epsilon, velocidade_recuperacao, votewithfeet, \
    habilidade, eficiencia, fome, mudou, recurso_ambiente, recurso_ambiente_k, regeneracao_ambiente, estoque, ambiente_do, agente_do, \
    producao, producao_recebida, empregador, conectividade, vida, urna_agentes, lista_estoque, lista_ambiente, lista_producao, lista_links, \
    lista_fome, lista_nomadismo, link, contador_populacional    
    
    for agente in xrange(N):
        if (empregador[agente] <> agente) and ((not vida[empregador[agente]]) or (estoque[empregador[agente]] < limiar_empregador) or (estoque[agente] > limiar_empregado)): 
            conectividade[empregador[agente]] -= 1
            empregador[agente] = agente
            #link[agente] -= 1
            link -= 1
            
    for agente in xrange(N): #Aqui desconecta todo mundo! Assim buscam um empregador novo a toda rodada, sem fidelizar
        if empregador[agente] <> agente:
            empregador[agente] = agente
            
    for agente in xrange(N):
        if (empregador[agente] == agente) and (estoque[agente] < limiar_empregado) and (vida[empregador[agente]]) and (vida[agente]):
            if RD.random() < votewithfeet:
                ambiente_sorteado = RD.randint(0, M-1)
                if agente_do[ambiente_sorteado] == 0:
                    agente_do[ambiente_do[agente]] = 0
                    agente_do[ambiente_sorteado] = agente
                    ambiente_do[agente] = ambiente_sorteado
                    #fome[agente] += 1
                    mudou[agente] += 1
            else: #(!!!)preciso adicionar aqui o fator do "contador_populacional"
                for tentativa in xrange(persistencia):
                    agente_sorteado = urna_agentes[RD.randint(0, len(urna_agentes) - 1)]
                    if estoque[agente_sorteado] < limiar_empregador: continue #(!!!) Esse 'continue' é para ele continuar buscando???
                    if producao[agente]*parametros[0] >= consumo - estoque[agente]:
                        empregador[agente] = agente_sorteado
                        #link[empregador[agente]] += 1
                        link += 1
                    urna_agentes.append(agente_sorteado)
                    conectividade[agente_sorteado] += 1
                    estoque[empregador[agente]] -= consumo-estoque[agente]
                    estoque[agente] = consumo
                    break


def consumir():
    global N, pop, M, T, persistencia, consumo, limiar_empregado, limiar_empregador, epsilon, velocidade_recuperacao, votewithfeet, \
    habilidade, eficiencia, fome, mudou, recurso_ambiente, recurso_ambiente_k, regeneracao_ambiente, estoque, ambiente_do, agente_do, \
    producao, producao_recebida, empregador, conectividade, vida, urna_agentes, lista_estoque, lista_ambiente, lista_producao, lista_links, \
    lista_fome, lista_nomadismo, link, contador_populacional    
    
    for agente in xrange(N):
        if vida[empregador[agente]]:
            if estoque[agente] < consumo * contador_populacional[agente]:
                fome[agente] += 1.0 - estoque[agente] / (consumo * contador_populacional[agente])
                estoque[agente] = 0
            else: 
                estoque[agente] -= consumo * contador_populacional[agente]
                fome[agente] = 0
                
                

def regenerar():
    global N, pop, M, T, persistencia, consumo, limiar_empregado, limiar_empregador, epsilon, velocidade_recuperacao, votewithfeet, \
    habilidade, eficiencia, fome, mudou, recurso_ambiente, recurso_ambiente_k, regeneracao_ambiente, estoque, ambiente_do, agente_do, \
    producao, producao_recebida, empregador, conectividade, vida, urna_agentes, lista_estoque, lista_ambiente, lista_producao, lista_links, \
    lista_fome, lista_nomadismo, link, contador_populacional    
    
    recurso_ambiente += velocidade_recuperacao*recurso_ambiente*(1-recurso_ambiente/recurso_ambiente_k)
    for agente in xrange(N): #medida de resiliência do ambiente, se AMB < 2, então: COLAPSO
        if recurso_ambiente[ambiente_do[agente]] <= 2:
            recurso_ambiente[ambiente_do[agente]] = 0
            ambiente_sorteado = RD.randint(0, M-1) #adicionei a mudança de amb depois do colapso
            if agente_do[ambiente_sorteado] == 0:
                agente_do[ambiente_do[agente]] = 0
                agente_do[ambiente_sorteado] = agente
                ambiente_do[agente] = ambiente_sorteado
                #fome[agente] += 1
                mudou[agente] += 1

def dinamica_populacional_1(): #consumo precisa virar uma variável global
    global N, pop, M, T, persistencia, consumo, limiar_empregado, limiar_empregador, epsilon, velocidade_recuperacao, votewithfeet, \
    habilidade, eficiencia, fome, mudou, recurso_ambiente, recurso_ambiente_k, regeneracao_ambiente, estoque, ambiente_do, agente_do, \
    producao, producao_recebida, empregador, conectividade, vida, urna_agentes, lista_estoque, lista_ambiente, lista_producao, lista_links, \
    lista_fome, lista_nomadismo, link, contador_populacional
    
    for agente in xrange(N):
        if vida[agente]: #para os agentes vivos
            if contador_populacional[agente] < limite_reprodutivo:
                if estoque[agente] > consumo*limite_reprodutivo: #o limiar vai variar com o número de indivíduos em determinado agente
                    contador_populacional[agente] += 1 #nova variável: contador
                    pop += 1 #atualização geral do tamanho populacional


def dinamica_populacional_2(): #se crescer demais deveria bipartir?
    global N, pop, M, T, persistencia, consumo, limiar_empregado, limiar_empregador, epsilon, velocidade_recuperacao, votewithfeet, \
    habilidade, eficiencia, fome, mudou, recurso_ambiente, recurso_ambiente_k, regeneracao_ambiente, estoque, ambiente_do, agente_do, \
    producao, producao_recebida, empregador, conectividade, vida, urna_agentes, lista_estoque, lista_ambiente, lista_producao, lista_links, \
    lista_fome, lista_nomadismo, link, contador_populacional
    
    for agente in xrange(N):
        if N < Nmax:
            if vida[agente]:
                if contador_populacional[agente] == limite_reprodutivo:
                    N += 1
                    habilidade[N-1] = habilidade[agente]
                    contador_populacional[N-1] = contador_populacional[agente] / 2
                    contador_populacional[agente] = contador_populacional[agente] / 2
                    estoque[N-1] = estoque[agente] / 2
                    estoque[agente] = estoque[agente] / 2
                    ambiente_sorteado = RD.randint(0, M-1) #estou tentando duplicar o agente - não sei se este método funciona
                    if agente_do[ambiente_sorteado] == 0:
                        agente_do[ambiente_sorteado] = N-1
                        ambiente_do[N-1] = ambiente_sorteado


def salvar_dados():
    global N, pop, M, T, persistencia, consumo, limiar_empregado, limiar_empregador, epsilon, velocidade_recuperacao, votewithfeet, \
    habilidade, eficiencia, fome, mudou, recurso_ambiente, recurso_ambiente_k, regeneracao_ambiente, estoque, ambiente_do, agente_do, \
    producao, producao_recebida, empregador, conectividade, vida, urna_agentes, lista_estoque, lista_ambiente, lista_producao, lista_links, \
    lista_fome, lista_nomadismo, link, contador_populacional
    
    for agente in xrange(N):
        if vida[agente]:
            lista_ambiente[agente].append(recurso_ambiente[ambiente_do[agente]])
            lista_estoque[agente].append(estoque[agente])
            lista_producao[agente].append(producao[agente])
            #lista_conectividade[agente] = conectividade[agente] #podeser que não dê pra plotar porque cada rodada tem um N diferente          
            lista_fome[agente].append(fome[agente])
            lista_nomadismo[agente].append(mudou[agente])

def simular(parametros):
    configuracao_inicial()
    for t in xrange(T):
        iniciar_rodada()
        produzir()
        distribuir(parametros)
        estocar()
        morrer()
        associar(parametros)
        consumir()
        dinamica_populacional_1()
        dinamica_populacional_2()
        regenerar()
        salvar_dados()
        print pop


def _plot():
    for i in xrange(0, N, 1):
        PLAB.figure(1)
        PLAB.subplot(211)
        PLAB.plot(lista_estoque[i])
        PLAB.ylabel('lista_estoque')
        PLAB.subplot(212)
        PLAB.plot(lista_ambiente[i])
        PLAB.ylabel('ambientes')
        PLAB.figure(2)
        PLAB.subplot(211)
        PLAB.plot(lista_producao[i])
        PLAB.ylabel('lista_producao')
        PLAB.subplot(212)
        PLAB.plot(lista_links[i])
        PLAB.ylabel('Links')
        PLAB.figure(3)
        PLAB.subplot(211)
        PLAB.plot(lista_fome[i])
        PLAB.ylabel('lista_fome')
        PLAB.subplot(212)
        PLAB.plot(lista_nomadismo[i])
        PLAB.ylabel('nomadismo')
    PLAB.show()
    
    
####################################################################


#AQUI - listas para arquivar médias de parâmetros estudados (pop, link, conectividade)
lista_medias_pop = []
lista_std_dev_pop = []
lista_medias_link = []
lista_std_dev_link = []
lista_mean_do_std_conectividade = []
lista_mean_do_mean_conectividade = []

#file = open("controle.txt", "w")   
for z in xrange(0, 11):
    lista_geral_de_conexoes = []
    lista_pop = []
    lista_mean_da_conectividade = []
    lista_std_da_conectividade = []
    
    for y in xrange(0, 50):
        #Parametros
        N = 200
        pop = N
        M = 1000
        T = N * 10
        Nmax = 1000
        persistencia = 10
        consumo = 2.0
        limiar_empregado = 2*consumo
        limiar_empregador = 4*consumo
        #epsilon = 0.8
        velocidade_recuperacao = 1 # velocidade de recuperacao do ambiente
        votewithfeet = 0.5 #probabilidade de mudar de ambiente ou pedir ajuda
        link = 0
        limite_reprodutivo = 4 #só pode ser par!!!
        fome_maxima = 4
        
        # variaveis do modelo
        agente_do = np.zeros(M, dtype=np.int_) # lista dos agentes com seus ambientes ocupados
        ambiente_do = np.zeros(Nmax, dtype=np.int_) # lista de ambientes ocupados pelo agente
        conectividade = np.ones(Nmax, dtype=np.int_)
        contador_populacional = np.ones(Nmax, dtype=np.float_)
        eficiencia = np.zeros(Nmax, dtype=np.float_) # taxa de acertos na procura/busca/produção dos recursos
        empregador = np.arange(Nmax, dtype=np.int_) # e - é o empregador do agente;
        estoque = np.zeros(Nmax, dtype=np.float_) # St - estoque do agente na rodada atual;
        fome = np.zeros(Nmax, dtype=np.float_) # f - fome dos agentes
        habilidade = np.zeros(Nmax, dtype=np.float_) # h - habilidade dos agentes. é multiplicado por recurso_ambiente para obter a producao;
        mudou = np.zeros(Nmax, dtype=np.float_) # mudou - medir agentes que trocam de ambiente
        producao = np.zeros(Nmax, dtype=np.float_) # P - producao do agente na rodada atual;
        producao_recebida = np.zeros(Nmax, dtype=np.float_) # Q - é a producao recebida pelo empregador na rodada atual (caso o agente nao seja um, é igual a producao do proprio agente);
        recurso_ambiente = np.zeros(M, dtype=np.float_) # A - recurso do ambiente. é multiplicado por habilidade para obter a producao do agente; é regenerado por regeneracao_ambiente;
        recurso_ambiente_k = np.zeros(M, dtype=np.float_) # K - capacidade de suporte do recurso do ambiente.
        regeneracao_ambiente = np.zeros(M, dtype=np.float_) # rec - regeneracao do ambiente. incrementa o recurso do ambiente;
        urna_agentes = range(N)
        vida = np.ones(Nmax, dtype=np.bool_)

        
        # listas para o Plot
        lista_estoque = [[] for i in xrange(Nmax)]
        lista_ambiente = [[] for i in xrange(Nmax)]
        lista_producao = [[] for i in xrange(Nmax)]
        lista_conectividade = [[] for i in xrange(Nmax)]
        lista_fome = [[] for i in xrange(Nmax)]
        lista_nomadismo = [[] for i in xrange(Nmax)]
        
        simular([z/10.0])
        
        lista_pop.append(pop)
        lista_medias_pop.append(np.mean(lista_pop))
        lista_std_dev_pop.append(np.std(lista_pop))
        
        #lista_geral_de_conexoes.append(link)
        #lista_medias_link.append(np.mean(lista_geral_de_conexoes))
        #lista_std_dev_link.append(np.std(lista_geral_de_conexoes))
                
        #lista_mean_da_conectividade.append(np.mean(conectividade))
        #lista_std_da_conectividade.append(np.std(conectividade)) #talvez não dê pra rodar, porque cada rodada tem um N diferente
        #lista_mean_do_mean_conectividade.append(np.mean(lista_mean_da_conectividade))
        #lista_mean_do_std_conectividade.append(np.mean(lista_std_da_conectividade))

	
	

#PLAB.errorbar([i/10.0 for i in xrange(0, 11)], lista_mean_do_mean_conectividade, yerr=lista_mean_do_std_conectividade)
PLAB.errorbar([i/10.0 for i in xrange(0, 11)], lista_medias_pop, yerr=lista_std_dev_pop)
PLAB.ylabel('Populacao Final')
PLAB.xlabel('Epsilon')
#PLAB.plot(range(0, 11), lista_pop)
PLAB.show()


#_plot()
