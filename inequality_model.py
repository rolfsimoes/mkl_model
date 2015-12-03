############
## To-do list:
##   * Comment code with 'docstring'.
##   * Improve performance on choice routines (_take, _borrow, _migrate)
##   * Create Power-law topology (Barabasi-Albert)
##   * Create a 'save agregate data per simulation' for each class (Site, Debtlink, Agent, Simulation)
##   * Create a 'save agregate data per step' for each class (Site, Debtlink, Agent, Simulation)
##   * Create a plot graphs functions
############

import numpy

class Site:
	def __init__(self, 
			     init_resource, 
			     resource, 
			     recovery_rate,
			     predictability):
		self.init_resource = init_resource
		self.resource = resource
		self.recovery_rate = recovery_rate
		self.predictability = predictability
		self.neighbors = []
		self.neighbors.append(self)
		self.agents_in_site = []
	def add_agent(self, agent):
		if not (agent in self.agents_in_site):
			if (agent.site != None):
				agent.site.agents_in_site.remove(agent) 
			self.agents_in_site.append(agent)
			agent.site = self
	def recovery(self):
		self.resource += self.recovery_rate * self.resource * (1.0 - self.resource / self.init_resource)
		pass
	def _exploit(self, agent_skill):
		exploited_resource = 0.0
		if numpy.random.rand() < self.predictability:
			exploited_resource = min(self.resource, self.resource * agent_skill)
			self.resource -= exploited_resource
		return exploited_resource
	def clear_neighbor(self):
		self.neighbors.clear()
		self.neighbors.append(self)

class DebtLink:
	def __init__(self, 
			     lender, 
			     borrower, 
			     value):
		self.lender = lender
		self.borrower = borrower
		self.value = value

class Agent:
	def __init__(self, 
			     agents_list, 
			     skill, 
			     stock, 
			     stock_max, 
			     consumption_demanded, 
			     reproduction_prob,
			     inheritance, 
			     strategy,
			     site, 
			     threshold_debt, 
			     threshold_death,
			     interest_rate):
		self.agents_list = agents_list
		self.skill = skill
		self.stock = stock
		self.stock_max = stock_max
		self.consumption_demanded = consumption_demanded
		self.consumed = 0.0
		self.consumption_deficit = 0.0
		self.reproduction_prob = reproduction_prob
		self.inheritance = inheritance
		self.strategy = strategy
		self.site = None
		site.add_agent(self)
		self.threshold_debt = threshold_debt
		self.threshold_death = threshold_death
		self.interest_rate = interest_rate
		self.gift_gived = 0
		self.debt = None
		self.loans = []
	def produce(self):
		"""Procedimento que realiza a producao do agente.
		Sem valor de retorno."""
		self.stock = min(self.stock, self.stock_max)
		self.stock += self.site._exploit(self.skill)
	def consume(self):
		self.consumed = min(self.stock, self.consumption_demanded)
		self.stock -= self.consumed
		self.consumption_deficit += self.consumption_demanded - self.consumed
		deficit_recovery = min(self.stock, self.consumption_deficit)
		self.consumption_deficit -= deficit_recovery
		self.stock -= deficit_recovery
	def solve_consumption_deficit(self):
		if self.consumption_deficit > self.threshold_death: self._die()
		elif (self.consumption_deficit > self.threshold_debt): 
			self._borrow()
			self._migrate()
		elif (self.consumption_deficit > 0.0): 
			self._take()
			self._migrate()
	def _take(self):
		choice_list = [a for s in self.site.neighbors for a in s.agents_in_site if a != self]
		if len(choice_list) > 0:
			choosed = numpy.random.choice(choice_list)
			gift = choosed._give(self, self.consumption_demanded - self.consumed)
			self.consumed += gift
			self.consumption_deficit -= gift
	def _give(self, 
		   taker, 
		   asked_value):
		if self.strategy == 0:
			gift = min(self.stock, asked_value)
			self.stock -= gift
			self.gift_gived += 1
			return gift
		else: return 0.0
	def _migrate(self):
		choice_list = [s for s in self.site.neighbors if s != self.site]
		if len(choice_list) > 0: 
			choosed = numpy.random.choice(choice_list)
			if choosed.resource > self.site.resource:
				choosed.add_agent(self)
	def _borrow(self):
		if self.debt == None:
			choice_list = [a for s in self.site.neighbors for a in s.agents_in_site if a.stock >= (self.consumption_demanded - self.consumed)]
			if len(choice_list) > 0: 
				choosed = numpy.random.choice(choice_list)
				loan_value = choosed._lend(self, self.consumption_demanded - self.consumed)
				self.consumed += loan_value
				self.consumption_deficit -= loan_value
	def _lend(self, 
		   borrower, 
		   asked_value):
		if self.strategy == 1:
			loan_value = min(self.stock, asked_value)
			self.stock -= loan_value
			debt = DebtLink(self, borrower, loan_value)
			self.loans.append(debt)
			borrower.debt = debt
			return loan_value
		else: return 0.0
	def _die(self):
		self.site.agents_in_site.remove(self)
		self.site = None
		if self.debt != None:
			self.debt.lender.loans.remove(self.debt)
			self.debt = None
		for l, loan in enumerate(self.loans):
			loan.borrower.debt = None
			del self.loans[l]
		self.agents_list.remove(self)
	def charge(self):
		for l, loan in enumerate(self.loans):
			payment_value = loan.borrower._pay(loan.value * (1.0 + self.interest_rate))
			loan.value -= payment_value
			if loan.value <= 0.0:
				loan.borrower.debt = None
				del self.loans[l]
			self.stock += payment_value
	def _pay(self, asked_value):
		payment_value = min(self.stock, asked_value)
		self.stock -= payment_value
		return payment_value
	def sprout(self):
		if numpy.random.rand() < self.reproduction_prob: 
			sprout_agents_list = self.agents_list
			sprout_skill = self.skill
			sprout_stock = self.stock * self.inheritance
			self.stock -= sprout_stock
			sprout_stock_max = self.stock_max
			sprout_consumption_demanded = self.consumption_demanded
			sprout_reproduction_prob = self.reproduction_prob
			sprout_inheritance = self.inheritance
			sprout_strategy = self.strategy
			sprout_site = self.site
			sprout_threshold_debt = self.threshold_debt
			sprout_threshold_death = self.threshold_death
			sprout_interest_rate = self.interest_rate
			self.agents_list.append(Agent(sprout_agents_list, 
										  sprout_skill, 
										  sprout_stock, 
										  sprout_stock_max, 
										  sprout_consumption_demanded, 
										  sprout_reproduction_prob,
										  sprout_inheritance, 
										  sprout_strategy,
										  sprout_site, 
										  sprout_threshold_debt, 
										  sprout_threshold_death,
										  sprout_interest_rate))

class Simulation():
	def __init__(self, 
			     sites_count, 
			     sites_init_resource_mean, 
			     sites_init_resource_sigma, 
			     sites_recovery_rate_mean, 
			     sites_recovery_rate_sigma, 
			     sites_predictability_mean, 
			     sites_predictability_sigma,
			     agents_count,
			     agents_skill_mean,
			     agents_skill_sigma,
			     agents_stock_max,
			     agents_consumption_demanded_mean,
			     agents_consumption_demanded_sigma,
			     agents_reproduction_prob,
			     agents_inheritance,
			     agents_interest_rate):
		site_parameters = {}
		self.sites = []
		for i in range(sites_count):
			sites_init_resource = abs(numpy.random.normal(sites_init_resource_mean, sites_init_resource_sigma))
			sites_resource = sites_init_resource
			sites_recovery_rate = abs(numpy.random.normal(sites_recovery_rate_mean, sites_recovery_rate_sigma))
			sites_predictability = abs(numpy.random.normal(sites_predictability_mean, sites_predictability_sigma))
			self.sites.append(Site(sites_init_resource, 
								   sites_resource, 
								   sites_recovery_rate,
								   sites_predictability))
		self.agents_list = []
		agent_parameters = {}
		for i in range(agents_count):
			agents_list = self.agents_list
			agents_skill = abs(numpy.random.normal(agents_skill_mean, agents_skill_sigma))
			agents_stock = 0.0
			agents_stock_max = agents_stock_max
			agents_consumption_demanded = abs(numpy.random.normal(agents_consumption_demanded_mean, agents_consumption_demanded_sigma))
			agents_reproduction_prob = agents_reproduction_prob
			agents_inheritance = agents_inheritance
			agents_strategy = numpy.random.randint(0, 2)
			agents_site = numpy.random.choice(self.sites)
			agents_threshold_debt = 5.0 * agents_consumption_demanded
			agents_threshold_death = 10.0 * agents_consumption_demanded
			agents_interest_rate = agents_interest_rate
			self.agents_list.append(Agent(agents_list, 
										  agents_skill, 
										  agents_stock, 
										  agents_stock_max, 
										  agents_consumption_demanded, 
										  agents_reproduction_prob,
										  agents_inheritance, 
										  agents_strategy,
										  agents_site, 
										  agents_threshold_debt, 
										  agents_threshold_death,
										  agents_interest_rate))
	def topology_grid(self, width, height):
		for s in self.sites:
			s.clear_neighbor()
		for i in range(len(self.sites)):
			if (i % width) + 1 < width:
				self.sites[i].neighbors.append(self.sites[i + 1])
				self.sites[i + 1].neighbors.append(self.sites[i])
			if int(i / width) + 1 < height:
				self.sites[i].neighbors.append(self.sites[i + width])
				self.sites[i + width].neighbors.append(self.sites[i])
	def topology_circle(self, radius):
		for s in self.sites:
			s.clear_neighbor()
		for i in range(len(self.sites)):
			for r in range(radius):
				self.sites[i].neighbors.append(self.sites[(i + r + 1) % len(self.sites)])
				self.sites[(i + r + 1) % len(self.sites)].neighbors.append(self.sites[i])
	def topology_complete(self):
		for i in range(len(self.sites) - 1):
			for j in range(i + 1, len(self.sites)):
				self.sites[i].neighbors.append(self.sites[j])
				self.sites[j].neighbors.append(self.sites[i])
	def topology_random_connect(self, probability):
		for i in range(len(self.sites) - 1):
			for j in range(i + 1, len(self.sites)):
				if not (self.sites[j] in self.sites[i].neighbors):
					if numpy.random.rand() < probability:
						self.sites[i].neighbors.append(self.sites[j])
						self.sites[j].neighbors.append(self.sites[i])
	def topology_random_reconnect(self, probability):
		for i in range(len(self.sites)):
			for j in range(len(self.sites)):
				if (i != j) and (self.sites[j] in self.sites[i].neighbors):
					if numpy.random.rand() < probability / 2.0:
						choice_list = [s for s in self.sites if not (s in self.sites[i].neighbors)]
						if len(choice_list) > 0:
							choosed = numpy.random.choice(choice_list)
							self.sites[i].neighbors.remove(self.sites[j])
							self.sites[j].neighbors.remove(self.sites[i])
							self.sites[i].neighbors.append(choosed)
							choosed.neighbors.append(self.sites[i])
	def step(self):
		numpy.random.shuffle(self.agents_list)
		for agent in self.agents_list:
			agent.produce()
		for agent in self.agents_list:
			agent.charge()
		for agent in self.agents_list:
			agent.consume()
		for agent in self.agents_list:
			agent.solve_consumption_deficit()
		for site in self.sites:
			site.recovery()
		for agent in self.agents_list:
			agent.sprout()
	def simulation(self, max_time):
		for t in range(max_time):
			self.step()
			print(t, len(self.agents_list), sum([a.gift_gived for a in self.agents_list]), len([l for a in self.agents_list for l in a.loans ]))
		self.save_data()
	def save_data(self):
		pass
		pass

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

#sim.topology_grid(width=32, height=32)
#sim.topology_circle(radius=2)
#sim.topology_random_reconnect(0.02)
sim.topology_random_connect(probability=0.05)
#sim.topology_complete()
sim.simulation(1000)
