import inequality_model

"""
a variavel "sim" define os valores iniciais de sites_count, agents_count
e todas as variaveis 'mean' e 'sigma' das funcoes de sorteio de valores
das propriedades dos sites e dos agents.
"""
sim = Simulation(sites_count=1024, 
		 sites_init_resource_mean = 4.0,
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
#sim.topology_grid(width=32, height=32)
#sim.topology_circle(radius=2)
#sim.topology_random_reconnect(0.02)
#sim.topology_random_connect(probability=0.05)
#sim.topology_complete()

"""
sim. simluation chama a funcao "simulation" dentro do objeto 'Simulation'.
eh aqui que de fato comeca a simulacao, por isso no parenteses eh colocado
o valor referente ao 'max_time'.
"""
#sim.simulation(1000)
