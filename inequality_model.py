import numpy

class Site:
	init_resource = 0.0
	resource = 0.0
	recovery_rate = 0.0
	neighbors = []
	agents = []
	def __init__(self, **kwargs):
		self.init_resource = numpy.random.lognormal(kwargs['resource_mean'], kwargs['resource_sigma'])
		self.resource = numpy.copy(self.init_resource)
		self.recovery_rate = numpy.random.lognormal(kwargs['recovery_mean'], kwargs['recovery_sigma'])
		self.neighbors.append(self)
	def add_agent(self, agent):
		if not (agent in self.agents):
			if agent.site != None:
				agent.site.agents.remove(agent) 
			self.agents.append(agent)
			agent.site = self
	def recovery(self):
		self.resource += self.recovery_rate * self.resource * (1.0 - self.resource / self.init_resource)
	def _exploit(self, skill):
		exploited_resource = min(self.resource, self.resource * skill)
		self.resource -= exploited_resource
		return exploited_resource

class DebtLink:
	lender = None
	borrower = None
	value = 0.0
	def __init__(self, lender, borrower, value):
		self.lender = lender
		self.borrower = borrower
		self.value = value

class Agent:
	agents = []
	dying = False
	skill = 0.0
	stock = 0.0
	stock_max = 0.0
	consumption_demanded = 0.0
	consumed = 0.0
	consumption_deficit = 0.0
	threshold_migrate = 0.0
	threshold_debt = 0.0
	threshold_death = 0.0
	reproduction_prob = 0.0
	inheritance = 0.0
	strategy = 0
	efficiency = 0.0
	site = None
	gift_gived = 0
	debt = None
	loans = []
	def __init__(self, **kwargs):
		self.agents_list = kwargs['agents_list']
		self.dying = False
		self.skill = kwargs['skill']
		self.stock = kwargs['stock']
		self.stock_max = kwargs['stock_max']
		self.consumed = 0.0
		self.consumption_deficit = 0.0
		self.threshold_migrate = kwargs['threshold_migrate']
		self.threshold_debt = kwargs['threshold_debt']
		self.threshold_death = kwargs['threshold_death']
		self.reproduction_prob = kwargs['reproduction_prob']
		self.inheritance = kwargs['inheritance']
		self.strategy = kwargs['strategy']
		self.efficiency = kwargs['efficiency']
		kwargs['site'].add_agent(self)
	def produce(self):
		self.stock = min(self.stock, self.stock_max)
		if numpy.random.rand() < self.efficiency: 
			self.stock = site._exploit(self.skill)
	def consume(self):
		self.consumed = min(self.stock, self.consumption_demanded)
		self.stock -= self.consumed
		self.consumption_deficit += self.consumption_demanded - self.consumed
		deficit_recovery = min(self.stock, self.consumption_deficit)
		self.consumption_deficit -= deficit_recovery
		self.stock -= deficit_recovery
	def solve_consumption_deficit(self):
		if consumption_deficit > self.threshold_death: self._die()
		elif (consumption_deficit > self.threshold_debt) and (self.stock == 0): 
			self._borrow()
			self._migrate()
		elif (self.consumption_deficit > 0.0) and (self.stock == 0): 
			self._take()
			self._migrate()
	def _take(self):
		choosed = numpy.random.choice([a for s in self.site.neighbors for a in s.agents])
		gift = choosed._give(self, self.consumption_demanded - self.consumed)
		self.consumed += gift
		self.consumption_deficit -= gift
	def _give(self, taker, asked_value):
		if self.strategy == 0:
			gift = min(self.stock, asked_value)
			self.stock -= gift
			self.gift_gived += 1
			return gift
		else: return 0.0
	def _migrate(self):
		choosed = numpy.random.choice([s for s in self.neighbors])
		if choosed.resource > self.site.resource:
			choosed.add_agent(self)
	def _borrow(self):
		if debt == None:
			choosed = numpy.random.choice([a for s in self.site.neighbors for a in s.agents])
			debt = choosed._lend(self, self.consumption_demanded - self.consumed)
			self.consumed += debt
			self.consumption_deficit -= debt
	def _lend(self, borrower, asked_value):
		if self.strategy == 1:
			loan = min(self.stock, asked_value)
			self.stock -= loan
			debt = DebtLink(self, borrower, loan)
			self.loans.append(debt)
			borrower.debt = debt
			return loan
		else: return 0.0
	def _die():
		self.dying = True
		self.site.agents.remove(self)
		self.site = None
		if self.debt != None:
			self.debt.lender.loans.remove(self.debt)
			self.debt = None
		for loan in agent.loans:
			loan.borrower.debt = None
			del loan
	def charge(self):
		for loan in loans:
			payment = loan.borrower._pay(loan.value)
			loan.value -= payment
			if loan.value == 0.0:
				loan.borrower.debt = None
				del loan
			self.stock += payment
	def _pay(self, asked_value):
		payment = min(self.stock, asked_value)
		self.stock -= payment
		return payment
	def sprout(self):
		if numpy.random.rand() < self.reproduction_prob: 
			agent_parameters = {}
			agent_parameters['agents_list'] = self.agents_list
			agent_parameters['skill'] = numpy.random.normal(self.skill, 0.1)
			agent_parameters['stock'] = self.stock * self.inheritance
			self.stock -= agent_paramenters['stock']
			agent_parameters['stock_max'] = self.stock_max
			agent_parameters['consumption_demanded'] = numpy.random.normal(self.consumption_demanded, 0.1)
			agent_parameters['reproduction_prob'] = self.reproduction_prob
			agent_parameters['inheritance'] = self.inheritance
			agent_parameters['strategy'] = self.strategy
			agent_parameters['efficiency'] = numpy.random.normal(self.efficiency, 0.1)
			agent_parameters['site'] = self.sites
			agent_parameters['threshold_migrate'] = self.threshold_migrate
			agent_parameters['threshold_debt'] = self.threshold_debt
			agent_parameters['threshold_death'] = self.threshold_death
			agents.append(Agent(agent_parameters))

def topology(sites, height, width):
	for i in range(height):
		for j in range(width):
			pass

def setup():
	global width, height, sites, N
	width = 20
	height = 20
	site_parameters = { resource_mean: 4.0, resource_sigma: 0.3, recovery_mean: 1.0, recovery_sigma: 0.1 }
	sites = [ Site(site_parameters) for i in range(height * width) ]
	topology(sites, height, width)

	N = 100
	agents_list = []
	agent_parameters = {}
	agent_parameters['agents_list'] = agents_list
	agent_parameters['skill'] = numpy.random.lognormal(4.0, 0.1)
	agent_parameters['stock'] = 0.0
	agent_parameters['stock_max'] = 0.0
	agent_parameters['consumption_demanded'] = numpy.random.lognormal(2.0, 0.2)
	agent_parameters['strategy'] = numpy.random.randint(0, 2)
	agent_parameters['efficiency'] = numpy.random.lognormal(0.1, 0.5)
	agent_parameters['site'] = numpy.random.choice(sites)
	agent_parameters['threshold_migrate'] = 2.0 * agent_parameters['consumption_demanded']
	agent_parameters['threshold_debt'] = 5.0 * agent_parameters['consumption_demanded']
	agent_parameters['threshold_death'] = 10.0 * agent_parameters['consumption_demanded']
	for i in range(N):
		agents_list.append(Agent(agent_parameters))

def step():
	numpy.random.shuffle(agents)
	for agent in agents:
		agent.produce()
	for agent in agents:
		agent.charge()
	for agent in agents:
		agent.consume()
	for agent in agents:
		agent.solve_consumption_deficit()
	for dead_agent in agents:
		if dead_agent.dying: del dead_agent
	for site in sites:
		site.recovery()

def simulation(max_time):
	setup()
	for t in max_time:
		step()
	save_data()

def save_data():
	pass