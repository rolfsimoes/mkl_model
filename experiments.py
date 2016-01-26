import inequality_model as im
import numpy as np
import sys

def personal_data_begin():
	#global realizations_stock_mean, realizations_stock_std_dev, realizations_num_gifts, \
	#		realizations_num_loans, realizations_num_altruists, realizations_num_egoists, \
	#		realizations_num_population
	#realizations_stock_mean = []
	#realizations_stock_std_dev = []
	#realizations_num_gifts = []
	#realizations_num_loans = []
	#realizations_num_altruists = []
	#realizations_num_egoists = []
	#realizations_num_population = []
	pass
	pass

def personal_data_step(simulation, parameter, realization, step):
	pass
	pass

def personal_data_realization(simulation, parameter, realization):
	#realizations_stock_mean.append(np.mean([a.stock for a in simulation.agents_list]))
	#realizations_stock_std_dev.append(np.std([a.stock for a in simulation.agents_list]))
	#realizations_num_gifts.append(np.sum([len(a.gifts) for a in simulation.agents_list]))
	#realizations_num_loans.append(np.sum([len(a.loans) for a in simulation.agents_list]))
	#realizations_num_altruists.append(len([0 for a in simulation.agents_list if a.strategy == 0]))
	#realizations_num_egoists.append(len([0 for a in simulation.agents_list if a.strategy == 1]))
	#realizations_num_population.append(len(simulation.agents_list))
	if realization == 0: print('.', file=sys.stderr)
	print(str(parameter), str(realization), np.mean([a.stock for a in simulation.agents_list]), np.std([a.stock for a in simulation.agents_list]),
	   np.sum([len(a.gifts) for a in simulation.agents_list]), np.sum([len(a.loans) for a in simulation.agents_list]),
	   len([0 for a in simulation.agents_list if a.strategy == 0]), len([0 for a in simulation.agents_list if a.strategy == 1]),
	   len(simulation.agents_list), sep='\t')


def personal_data_end():
	#print(np.mean(realizations_stock_mean), np.mean(realizations_stock_std_dev), np.mean(realizations_num_gifts), np.mean(realizations_num_loans), 
	#   np.mean(realizations_num_altruists), np.mean(realizations_num_egoists), np.mean(realizations_num_population), sep='\t')
	pass
	pass

im.save_data_step = personal_data_step
im.save_data_realization = personal_data_realization

print('parameter', 'realization', 'stock_mean', 'stock_std_dev', 'num_gifts', 'num_loans', 'num_altruists', 'num_egoists', 'num_population', sep='\t')

"""
o range do i eh a variacao do valor dos parametros i que eu vou testar
"""
for i in range(1):
	parameter = i
	personal_data_begin()
	for realization in range(1):
		"""
		a variavel "sim" define os valores iniciais de sites_count, agents_count
		e todas as variaveis 'mean' e 'sigma' das funcoes de sorteio de valores
		das propriedades dos sites e dos agents.
		"""
		sim = im.Simulation(sites_count=1024, 
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
		sim.topology_grid(width=32, height=32)
		#sim.topology_circle(radius=2)
		#sim.topology_random_reconnect(0.02)
		#sim.topology_random_connect(probability=0.05)
		#sim.topology_complete()

		"""
		sim.simluation chama a funcao "simulation" dentro do objeto 'Simulation'.
		eh aqui que de fato comeca a simulacao, por isso no parenteses eh colocado
		o valor referente ao 'max_time' e 'realizations' que indica quantas
		realizacoes serao executadas para a o objeto 'Simulation' criado.
		"""
		sim.simulation(max_time=2000, parameter=parameter, realization=realization)
	personal_data_end()
