import numpy

class Site:
	init_resource = 0.0
	resource = 0.0
	recovery_rate = 0.0
	neighborhood = []
	def __init__(self, **kwargs):
		self.init_resource = numpy.random.lognormal(kwargs['resource_mean'], kwargs['resource_sigma'])
		self.resource = numpy.copy(self.init_resource)
		self.recovery_rate = numpy.random.lognormal(kwargs['recovery_mean'], kwargs['recovery_sigma'])
	def exploit(self, skill):
		exploited_resource = min(self.resource, self.resource * skill)
		self.resource -= exploited_resource
		return exploited_resource

class Agent:
	skill = 0.0
	stock = 0.0
	temporary_stock = 0.0
	comsuption = 0.0
	strategy = 0
	efficiency = 0.0
	site = None
	def __init__(self, **kwargs):
		self.skill = numpy.random.lognormal(kwargs['skill_mean'], kwargs['skill_sigma'])
		self.stock = numpy.random.lognormal(kwargs['stock_mean'], kwargs['stock_sigma'])
		self.temporary_stock = 0.0
		self.comsuption = numpy.random.lognormal(kwargs['comsuption_mean'], kwargs['comsuption_sigma'])
		self.strategy = numpy.random.randint(0, 2)
		self.efficiency = numpy.random.lognormal(kwargs['efficiency_mean'], kwargs['efficiency_sigma'])
		self.site = kwargs['site']
	def produce(self):
		if numpy.random.rand() < self.efficiency: self.temporary_stock = site.exploit(self.skill)

def topology(sites, height, width):
	for i in range(height):
		for j in range(width):
			pass

def setup():
	global width, height, sites, N, agents
	width = 20
	height = 20
	site_parameters = { resource_mean: 4.0, resource_sigma: 0.3, recovery_mean: 1.0, recovery_sigma: 0.1 }
	sites = [ Site(site_parameters) for i in range(height * width) ]
	topology(sites, height, width)
	N = 100
	agent_parameters = { skill_mean: 4.0, skill_sigma: 0.1, stock_mean: 1.0, stock_sigma: 0.1, comsuption_mean: 2.0, comsuption_sigma: 0.2, efficiency_mean: 0.1, efficiency_sigma: 0.5 }
	agents = [ Agent(agent_parameters, site = numpy.random.choice(sites)) for i in range(N) ]

