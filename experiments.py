import inequality_model as im


def personal_data_step(simulation, step):
	pass
	#if step == 0:
		#print('%step', '%pop', '%debt', '%gift', '\n', sep='\t')
	#print(step,
		#len(simulation.agents_list),
		#len([l for a in simulation.agents_list for l in a.loans ]),
		#len([g for a in simulation.agents_list for g in a.gifts ]), sep='\t')

def personal_data(simulation):

	print(len(simulation.agents_list))

	#print('%edge list of lend-borrower relation')
	#for a in simulation.agents_list:
		#for n in a.loans:
			#print(id(a), id(n), sep=',')
	#print('%edge list of giver-taker relation')
	#for a in simulation.agents_list:
		#for n in a.gifts:
			#print(id(a), id(n), sep=',')

im.save_data_step = personal_data_step
im.save_data = personal_data

"""
o range do i eh a variacao do valor dos parametros i que eu vou testar
"""



for i in range(0, 2):
	k = i/10.0
	print("resource_mean =", k)
	"""
	a variavel "sim" define os valores iniciais de sites_count, agents_count
	e todas as variaveis 'mean' e 'sigma' das funcoes de sorteio de valores
	das propriedades dos sites e dos agents.
	"""
	sim = im.Simulation(sites_count=1024, 
			 sites_init_resource_mean = k,
			 sites_init_resource_sigma = 0.1,
			 sites_recovery_rate_mean = 1.1,
			 sites_recovery_rate_sigma = 0.1,
			 sites_predictability_mean = 0.8,
			 sites_predictability_sigma = 0.1,
			 agents_count=200,
			 agents_skill_mean = 0.2,
			 agents_skill_sigma = 0.01,
			 agents_stock_max = 0.0,
			 agents_consumption_demanded_mean = 0.8,
			 agents_consumption_demanded_sigma = 0.1,
			 agents_reproduction_prob = 0.01,
			 agents_inheritance = 0.1,
			 agents_interest_rate = 0.1)

	"""
	sim.topology chama a funcao topology dentro do objeto 'Simulation'
	"""
	sim.topology_grid(width=32, height=32)
	#sim.topology_circle(radius=2)
	#sim.topology_random_reconnect(0.02)
	#sim.topology_random_connect(probability=0.05)
	#sim.topology_complete()

	"""
	sim. simluation chama a funcao "simulation" dentro do objeto 'Simulation'.
	eh aqui que de fato comeca a simulacao, por isso no parenteses eh colocado
	o valor referente ao 'max_time'.
	"""
	for j in range(100):
		print("Simulacao =", j)
		"""
		o range aqui eh o numero de vezes que a simulacao vai realizar cada i dos parametros.
		"""
		sim.simulation(2000,)
