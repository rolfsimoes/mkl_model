# -*- coding: cp1252 -*-
import numpy as np
import pylab as PLAB
import random as RD

#Parametros
N = 20
M = 1000
T = N * 10
persistencia = 10

consumo = 2
limiar_empregado = 2*consumo
limiar_empregador = 4*consumo
#limiar_empregado = 6
#limiar_empregador = 160
epsilon = 0.8
velocidade_recuperacao = 1 # velocidade de recuperacao do ambiente
votewithfeet = 0.5 #probabilidade de mudar de ambiente ou pedir ajuda

# variaveis do modelo
habilidade = np.zeros(N, dtype=np.float_) # h - habilidade dos agentes. é multiplicado por recurso_ambiente para obter a producao;
eficiencia = np.zeros(N, dtype=np.float_) # taxa de acertos na procura/busca/produção dos recursos
fome = np.zeros(N, dtype=np.float_) # f - fome dos agentes
mudou = np.zeros(N, dtype=np.float_) # mudou - medir agentes que trocam de ambiente
recurso_ambiente = np.zeros(M, dtype=np.float_) # A - recurso do ambiente. é multiplicado por habilidade para obter a producao do agente; é regenerado por regeneracao_ambiente;
recurso_ambiente_k = np.zeros(M, dtype=np.float_) # K - capacidade de suporte do recurso do ambiente.
regeneracao_ambiente = np.zeros(M, dtype=np.float_) # rec - regeneracao do ambiente. incrementa o recurso do ambiente;
estoque = np.zeros(N, dtype=np.float_) # St - estoque do agente na rodada atual;
ambiente_do = np.zeros(N, dtype=np.int_) # lista de ambientes ocupados pelo agente
agente_do = np.zeros(M, dtype=np.int_) # lista dos agentes com seus ambientes ocupados
producao = np.zeros(N, dtype=np.float_) # P - producao do agente na rodada atual;
producao_recebida = np.zeros(N, dtype=np.float_) # Q - é a producao recebida pelo empregador na rodada atual (caso o agente nao seja um, é igual a producao do proprio agente);
empregador = np.arange(N, dtype=np.int_) # e - é o empregador do agente;
conectividade = np.ones(N, dtype=np.int_)
vida = np.ones(N, dtype=np.bool_)
urna_agentes = range(N)

# listas para o Plot
lista_estoque = [[] for i in xrange(N)]
lista_ambiente = [[] for i in xrange(N)]
lista_producao = [[] for i in xrange(N)]
lista_links = [[] for i in xrange(N)]
lista_fome = [[] for i in xrange(N)]
lista_nomadismo = [[] for i in xrange(N)]

#########################################################################
def configuracao_inicial():
    #for agente in xrange(N):
   	#habilidade[agente] = RD.normalvariate(0.5, 0.01)
   	#recurso_ambiente[agente] = RD.lognormvariate(5.1, 0.02)
   	#regeneracao_ambiente[agente] = RD.normalvariate(1.0, 0.02)
   	#estoque[agente] = RD.lognormvariate(20.0, 1.0)
    global habilidade, recurso_ambiente, regeneracao_ambiente, estoque, recurso_ambiente_k, resiliencia, eficiencia
    habilidade = np.random.normal(3.0, 0.5, N) / 100
    eficiencia = np.random.normal(0.5, 0.1, N) #introduz o efeito estocástico na busca por recursos
    recurso_ambiente = np.random.lognormal(4.0, 0.5, M) #+ 4
    recurso_ambiente_k = np.copy(recurso_ambiente)
    #resiliencia = recurso_ambiente * 0.25 #PRECISO aprender a definir a resiliência AQUI está dando pau nesta multiplicação
    #regeneracao_ambiente = np.random.lognormal(0.5, 0.5, M) #não está sendo usado na função de regeneracao()
    #estoque = np.random.lognormal(2.5, 0.5, N)
    estoque = 0
    agente = 0
    while agente < N:
        ambiente_sorteado = RD.randint(0, M - 1)
        if agente_do[ambiente_sorteado] == 0:
            agente_do[ambiente_sorteado] = agente
            ambiente_do[agente] = ambiente_sorteado
            agente += 1
    #print habilidade, recurso_ambiente, regeneracao_ambiente, estoque

def iniciar_rodada():
    #for agente in xrange(N):
    #    producao_recebida[agente] = 0.0
    global producao_recebida
    producao_recebida *= 0

def produzir():
    global producao, habilidade, recurso_ambiente, eficiencia
#OPÇÃO DE PRODUÇÃO ESTOCÁSTICA - ainda em teste - abaixo
    for agente in xrange(N):
        if RD.random() <= eficiencia[agente]:
            producao[agente] = habilidade[agente] * recurso_ambiente[ambiente_do[agente]]
        else: producao[agente] = 0
        recurso_ambiente[ambiente_do[agente]] -= producao[agente]
#OPÇÃO TRADICIONAL DE PRODUÇÃO - consolidada - abaixo                        
        #producao[agente] = habilidade[agente] * recurso_ambiente[ambiente_do[agente]]
        #recurso_ambiente[ambiente_do[agente]] -= producao[agente]


def distribuir():
    for agente in xrange(N):
        if (empregador[agente] <> agente):
            producao_recebida[empregador[agente]] += producao[agente] * epsilon
            producao_recebida[agente] = producao[agente] * (1 - epsilon)
        else:
            producao_recebida[agente] = producao[agente]

def estocar():
    #for agente in xrange(N):
    #    estoque[agente] += producao_recebida[agente]
    global estoque, producao_recebida
    estoque += producao_recebida

def consumir():
    #for agente in xrange(N):
    #    estoque[agente] -= min(consumo, estoque[agente])
    global estoque, consumo, estoque, fome
    for agente in xrange(N):
        if estoque[agente] < consumo:
            fome[agente] += 1
            estoque[agente] = 0
        else: 
			estoque[agente] -= consumo
			fome[agente] = 0

def morrer():
    for agente in xrange(N):
        vida[agente] = (fome[agente] < 4)
        if not vida[agente]:
            while(True):
                try: urna_agentes.remove[agente]
                except: break
            habilidade[agente] = 0
            #recurso_ambiente[ambiente_do[agente]] = 0
            #regeneracao_ambiente[agente] = 0
            agente_do[ambiente_do[agente]] = 0
            estoque[agente] = 0
            empregador[agente] = agente

def associar():
    
    for agente in xrange(N):
        if (empregador[agente] <> agente) and ((not vida[empregador[agente]]) or (estoque[empregador[agente]] < limiar_empregado) or (estoque[agente] > limiar_empregador)): 
            conectividade[empregador[agente]] -= 1
            empregador[agente] = agente
    for agente in xrange(N):
        if (empregador[agente] == agente) and (estoque[agente] < limiar_empregado) and (vida[empregador[agente]]):
            if RD.random() < votewithfeet:
                ambiente_sorteado = RD.randint(0, M-1)
                if agente_do[ambiente_sorteado] == 0:
                    agente_do[ambiente_do[agente]] = 0
                    agente_do[ambiente_sorteado] = agente
                    ambiente_do[agente] = ambiente_sorteado
                    #fome[agente] += 1
                    mudou[agente] += 1
            else:
                for tentativa in xrange(persistencia):
                    agente_sorteado = urna_agentes[RD.randint(0, len(urna_agentes) - 1)]
                    if estoque[agente_sorteado] < limiar_empregador: continue
                    if producao[agente]*epsilon >= consumo-estoque[agente]: #se o preço que o empregado irá pagar for maior ou igual ao que o empregador emprestaria
                        empregador[agente] = agente_sorteado
           	        urna_agentes.append(agente_sorteado)
           	        conectividade[agente_sorteado] += 1
           	        estoque[empregador[agente]] -= consumo-estoque[agente]
           	        estoque[agente] = consumo
          		break

def regenerar():
    #for agente in xrange(N):
    #    recurso_ambiente[agente] += regeneracao_ambiente[agente]
    global recurso_ambiente, regeneracao_ambiente, recurso_ambiente_k, velocidade_recuperacao, resiliencia
    recurso_ambiente += velocidade_recuperacao*recurso_ambiente*(1-recurso_ambiente/recurso_ambiente_k)
    for agente in xrange(N):
        if recurso_ambiente[ambiente_do[agente]] <= 2:
            recurso_ambiente[ambiente_do[agente]] = 0
            ambiente_sorteado = RD.randint(0, M-1) #adicionei a mudança de amb depois do colapso
            if agente_do[ambiente_sorteado] == 0:
				agente_do[ambiente_do[agente]] = 0
				agente_do[ambiente_sorteado] = agente
				ambiente_do[agente] = ambiente_sorteado
				#fome[agente] += 1
				mudou[agente] += 1
                


def salvar_dados():
    for agente in xrange(N):
        if vida[agente]:
            lista_ambiente[agente].append(recurso_ambiente[ambiente_do[agente]])
            lista_estoque[agente].append(estoque[agente])
            lista_producao[agente].append(producao[agente])
            lista_links[agente].append(conectividade[agente])
            lista_fome[agente].append(fome[agente])
            lista_nomadismo[agente].append(mudou[agente])

def simular():
    configuracao_inicial()
    print habilidade
    for t in xrange(T):
        iniciar_rodada()
        produzir()
        distribuir()
        estocar()
        morrer()
        associar()
        consumir()
        regenerar()
        salvar_dados()


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

simular()

_plot()
