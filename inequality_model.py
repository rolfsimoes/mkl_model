############
## To-do list:
##   * Improve performance on choice routines (_take, _borrow, _migrate)
##   * Create Power-law topology (Barabasi-Albert)
##   * Create a 'save agregate data per simulation' for each class (Site, Debtlink, Agent, Simulation)
##   * Create a 'save agregate data per step' for each class (Site, Debtlink, Agent, Simulation)
##   * Create a plot graphs functions
############

import numpy

"""
O Modelo construído aqui é um do tipo Modelo Baseado em Agentes (MBA).
O código foi desenhado com a estrutura de dados orientada ao objeto. 
Desta forma o código fica mais fácil de compreender, entre outras fazões
por que dois dos três objetos são os agentes do modelo.
Foram definidos quatro objetos: Site, DebtLink, Agent e SImulation.
Sites são os sítios (ou ambientes) pelos quais os agentes podem transitar.
Agents são os agentes que representam as pessoas.
DebtLink são os links que podem ser formados entre os agentes.
Simulation eh a simulacao propriamente dita, a dinamica do modelo.
"""

class Site:
	"""
	A primeira classe do código, ou seja, o primeiro objeto do código é o Site
	nele são descritos os parametros do agente do tipo ambiente (site), como os recursos
	disponiveis, a taxa de recuperacao do recurso e a previsibilidade da taxa de 
	encontro entre agentes e recursos.
    
	Para que estes ambientes possam ser descritos de maneira que sejam de alguma
	forma conectados uns aos outros, de maneira que possamos descrever a sua
	vizinhanca, foi criada uma lista chamada neighbors
    
	Para que estes ambientes possam ser explorados pelos agentes do tipo pessoa
	outra lista chamada agents_in_site foi criada. Nesta lista ficarao armazenados
	os agentes com os quais ela irá interagir.
	"""
	def __init__(self,
				init_resource, 
				resource, 
				recovery_rate,
				predictability):
		"""
		a cada inicio de simulacao a funcao "Simulacao" chama uma outra
		funcao que define todos os ambientes, site, da dinamica.
                 
		a funcao "__init__" eh chamada automaticamente quando a dinamica
		se inicia. eh ela que atribui os valores aos YYY do objeto a
		cada site criado.
		Neste caso, seus recursos iniciais, atuais, a probabilidade de
		recuperacao, a previsibilidade, a lista de vizinhos, e a lista
		de agentes ocupando o site naquele instante.
                 
		a funcao tambem insere o objeto na sua propria lista de vizinhos.
		"""
		self.init_resource = init_resource
		self.resource = resource
		self.recovery_rate = recovery_rate
		self.predictability = predictability
		self.neighbors = []
		self.neighbors.append(self)
		self.agents_in_site = []
	
	def add_agent(self, agent):
		"""
		funcao add_agent tem dois OBJETOS, o self e o agent.
		Isto eh, a funcao add_agent pode orientar a dois objetos.
           
		Primeiro: a funcao pergunta se o agent nao esta na lista
		agents_in_site do self (site).
    
		Segundo: Se o agent de fato nao esta na agents_in_site, 
		o modelo pergunta ao agente se ele esta associado a algum
		site.
   
		Terceiro: Se o agent esta associado a algum site entao
		a funcao remove o agente da lista agents_in_site que 
		ele esta vinculado. Isto significa desassociar este agent
		do antigo site que ele ocupava.
    
		Quarto: o site entao associa o agent da funcao a ele
		colocando o mesmo em sua lista agents_in_site.
    
		Quinto: Por fim a funcao coloca o objeto self (o sitio)
		no site, o YYY do agent da interacao.
    
		Resumo: Esta funcao retira o objeto site da lista 'site'
		do agent da interacao. E desassocia o agent da interacao
		da lista 'agents_in_site' do objeto site.
		"""
		if not (agent in self.agents_in_site):
			if (agent.site != None):
				agent.site.agents_in_site.remove(agent) 
			self.agents_in_site.append(agent)
			agent.site = self

	def recovery(self):
		"""
		a funcao recovery interage apenas com um objeto, o self,
		no caso um agente do tipo ambiente.
        
		esta funca atualiza o recurso do ambiente site. Ela é uma funcao
		de crescimento logístico do tipo:
		R(t+1) = R(t+1) + rate*R(t+1)*(1 - R(t+1)/R(t=0)). 
        
		toda rodada o ambiente soma aos recursos de cada sítio um valor
		igual aa multiplicacao de uma taxa(rate) de recuperacao (recovery_rate)
		com a recurso disponivel naquela rodada (t+1), com um (1) menos a diferenca
		entre a quantidade de recurso da rodada (t+1) dividida pela disponibilidade
		dos recursos naquele mesmo sitio no inicio da dinamica (t = 0).
		"""
		self.resource += self.recovery_rate * self.resource * (1.0 - self.resource / self.init_resource)
		pass
	
	def _exploit(self, agent_skill):
		"""
		a funcao _exploit eh chamada por um objeto do tipo agent e interage com o 
		objeto do tipo self, um site, um agente do tipo ambiente.
                
		primeiro: a funcao declara que a variavel exploited_resource
		sera zerada seja qual for o valor que ela esteja assumindo
		naquele momento.
        
		segundo: a funcao sorteia um numero aleatorio entre 0 e 1 e confere se o
		valor eh menor do que o parametro 'previsibilidade' do objeto ao qual ela
		esta orientada. Se sim, o agente do tipo agent que chamou a funcao tera 
		tido sucesso, isto eh, ele conseguirá obter recursos naquela rodada.
        
		terceiro: o valor de recurso que sera retirado do ambiente sera um valor 
		minimo entre os recursos disponiveis no ambiente naquele naquele
		instante de tempo (t+1) e o resultado do produto da quantidade de
		recursos do site pela habilidade (agent_skill) do agent que esta
		chamando a funcao.
        
		quarto: o valor entao atribuido aa variavel 'exploited_resource' eh
		subtraido da quantidade de recursos que havia disponivel no instante
		t + 1 no objeto ao qual a funcao esta orientada, o site, o ambiente
		explorado pelo agente.
        
		quinto: a funcao retorna o valor 'exploited_resource' que sera processado
		na funcao "produce" do objeto "agent".
		"""
		exploited_resource = 0.0
		if numpy.random.rand() < self.predictability:
			exploited_resource = min(self.resource, self.resource * agent_skill)
			self.resource -= exploited_resource
		return exploited_resource

	def clear_neighbor(self):
		"""
		A funcao 'clear_neighbor' eh uma funcao que altera somente
		parametros do objeto ao qual ela esta orientada (self) o
		agente do tipo ambiente, um site.
        
		primeiro: a funcao retira todos os agentes da lista 'neighbors' do
		objeto.
        
		segundo: a funcao insere o proprio objeto na lista 'neighbors' dele.
        
		resumo: a funcao limpa a lista de vizinhos do ambiente e depois insere
		ele mesmo na lista, de maneira que o ambiente ocupado sempre sera considerado
		em quaisquer buscas feitas pelos agentes que envolvam a vizinhanca dos
		locais nos quais eles se encontram.
		"""
		self.neighbors.clear()
		self.neighbors.append(self)

class DebtLink:
	"""
	a segunda classe eh o objeto 'DebtLink'. ele eh formado por quatro XXX: 
	ele mesmo, o lender, o borrower e o value.
    
	eh atraves deste objeto que os agentes que devem algum valor em recurso
	sao cobrados, pois eh nele que os lenders armazenam os values emprestados
	aos borrowers.
    
	#Pergunta, os XXX sao as variaveis?
	"""
	def __init__(self, 
				 lender, 
				 borrower, 
				 value):
		"""
		quando a dinamica eh iniciada a funcao "__init__" eh chamada
		automaticamente e define que nos XXX do objeto, seu lender 
		sera um lender, seu borrower sera um borrower e seu value
		sera um value.
		"""
		self.lender = lender
		self.borrower = borrower
		self.value = value

class GiftLink:
	"""
	"""
	def __init__(self, 
				 giver, 
				 taker, 
				 value):
		"""
		"""
		self.giver = giver
		self.taker = taker
		self.value = value

class Agent:
	"""
	a terceira classe eh o objeto Agent. eh este objeto que
	define cada um dos agents criados em cada dinamica.
	"""
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
		"""
		quando a simulacao eh iniciado a funcao "__init__" do objeto
		eh chamada automaticamente. uma vez para cada agent criado.
		 
		eh esta funcao que define os XXX (Parametros?) de cada agente.
		sao eles sua lista de agentes, sua habilidade, seu estoque inicial
		seu estoque maximo, sua demanda energetica, a quantidade de
		recursos consumida por rodada, o deficit energetico, sua probabilidade
		de procriacao, seu componente de heranca, sua estrategia, o site em
		que esta vinculado, seus limiares de morte e divida, sua taxa de
		interesse, a quantidade de dadivas oferecidas, sua divida e a sua
		lista de possiveis emprestimos
		"""
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
		self.debt_link = None
		self.loans = []
		self.gift_link = None
		self.gifts = []
		 
	def produce(self):
		"""
		a funcao producao eh chamada pelos agentes e ela
		faz referencia somente ao agente que a chama.
        
		primeiro: a funcao define que o valor atual do estoque do
		agente, isto eh, a quantidade de recursos que aquele agente
		detem no instante t+1 eh igual ao valor minimo entre o valor
		que ele possuia no instante t = 0 e o valor maximo de estoque
		que o agent pode estocar.
        
		segundo: a funcao entao atualiza o estoque do agente adicionando
		ao seu estoque o valor que o agente retorna da funcao "_exploit".
        
		trata-se de um rocedimento que realiza a producao do agente.
		nao existe valor de retorno da funcao "produce".
		"""
		self.stock = min(self.stock, self.stock_max)
		self.stock += self.site._exploit(self.skill)
	
	def consume(self):
		"""
		a funcao consumo faz referencia apenas ao agent que a chama.
		ela eh chamada apos o agente ja ter produzido seus recursos
		e estocado o que conseguiu.
        
		primeiro: a funcao atualiza o valor do XXX (valor consumido)
		do agent que chama a funcao. este valor sera um minimo entre
		o que existe no estoque do agente e sua demanda de consumo.
        
		segundo: o estoque do agente objeto eh subtraido do valor
		consumido pelo agente no primeiro passo (???) da funcao.
        
		terceiro: o deficit de consumo do agente eh adicionado do valor
		da diferenca entra a demanda de energia do agente e o valor
		que ele de fato consumiu nesta rodada.
        
		quarto: caso apos consumir seus recursos o agente ainda tenha
		recursos estocados, isto eh, caso o agente tenha produzido o
		suficiente para consumir e ainda tenha estoque disponivel, ele 
		entao pode recuperar seu deficit (caso tenha um) com o valor
		minimo entre seu estoque e seu deficit de consumo.
                
		quinto: caso o agente tenha mesmo um valor para recuperar o seu
		proprio deficit de consumo, a funcao entao subtrai o valor de 
		recuperacao do agente do seu deficit.
        
		sexto: o valor de recuperacao do deficit de consumo do agente eh
		entao subtraido do seu estoque.
        
		resumo: a funcao consumo subtrai do estoque do agente o seu
		valor consumido naquela rodada. este valor depende do quanto
		o agente dispoe de recursos em seu estoque. minha impressao eh
		de que na realidade aqui temos duas funcoes. uma consome e a 
		outra recupera o deficit de consumo. caso o agente tenha uma.
		a recuperacao do deficit depende do tamanho do deficit e da
		quantidade de recursos no estoque do agente apos ele satisfazer
		sua demanda diaria.
		"""
		self.consumed = min(self.stock, self.consumption_demanded)
		self.stock -= self.consumed
		self.consumption_deficit += self.consumption_demanded - self.consumed
		deficit_recovery = min(self.stock, self.consumption_deficit)
		self.consumption_deficit -= deficit_recovery
		self.stock -= deficit_recovery
	
	def solve_consumption_deficit(self):
		"""
		a funcao "solve_consumption_deficit" pode fazer referencia apenas ao
		agente que chama a funcao, um agent.
        
		eh aqui que a demanda de consumo dos agentes pode ser satisfeita, seja
		atraves de um compartilhamento, uma troca, ou mesmo a morte do agente.
		caso a sua demanda energética tenha se tornado grande demais.
        
		primeiro: a funcao confere se a demanda energetica do agent ja supertou
		o seu limiar de morte. caso sim, o agente chama a funçao "_die" e morre.
        
		segundo: caso o agente nao morra a funcao verifica se a demanda energetica
		do agent eh superior ao limiar da divida, aquele limiar quando a demanda
		energetica do agente ja esta consideravel.
        
		quarto: caso o deficit do agente tenha superado seu limiar de divida, o
		agente chama a funcao "_borrow" e procura por um agente que possa lhe
		ceder recursos.
        
		quinto: apos chamar a funcao "_borrow" o agente chama a funcao "_migrate"
		e verifica se em sua vizinhanca existe um lugar melhor para ele explorar.
        
		sexto: entretanto, se o deficit energetico do agente nao for tao grande
		para ele ceder a uma troca (egoista") a funcao ira conferir se este agente
		tem algum tipo de deficit energetico ou se ele esta produzindo o suficiente
		para se manter nas ultimas rodadas.
        
		setimo: caso exista uma demanda energetica encontrada no passo anterior
		a funcao entao chama a funcao "_take" em que o agente vai procurar em
		sua vizinhanca por um agente (altruista) que possa lhe ceder recursos.
        
		oitavo: a funcao entao chama a funcao "_migrate" para o agente ver se
		no seu entorno, sua vizinhanca, existe um ambiente que tenha mais 
		recursos do que o seu atual.
        
		resumo: esta funcao trabalha a partir do deficit de consumo do agente
		que a chama. caso exista um, o agente vai obter cooperacao, uma troca,
		ou vai morrer. caso seja o caso de uma das duas opcoes, o agente ira
		tentar migrar, buscando ambientes nos quais ele possa tentar satisfazer
		sozinho o seu deficit e a sua demanda.
		"""
		if self.consumption_deficit > self.threshold_death: self._die()
		elif (self.consumption_deficit > self.threshold_debt): 
			self._borrow()
			self._migrate()
		elif (self.consumption_deficit > 0.0): 
			self._migrate()
		
	def _migrate(self):
		"""
		a funcao migrate pode fazer referencia somente ao agente
		objeto da funcao, aquele que a chama.
        
		primeiro: a funcao cria uma lista que sera formada por todos
		os sitios na lista de vizinhos ('neighbors') do sitio ocupado
		pelo agente que chamou a funcao. todos os sitios menos o sitio
		em que o agente esta no instante em que executa o primeiro passo
		da funcao.
        
		segundo: a funcao confere se existe algum ambiente em sua
		vizinhanca. caso sim a funcao ira passar para o seu terceiro
		passo. caso nao ela ira parar.
        
		terceiro: a funcao ira selecionar aleatoriamente um site
		entre os ambientes vizinhos ao ambiente em que o objeto
		esta associado.
        
		quarto: se os recursos disponiveis no site escolhido forem
		maiores do que os recursos disponiveis no ambiente atual do
		agente entao a funcao ira executar o seu quinto passo. se
		nao, a funcao para.
        
		quinto: o ambiente escolhido chama a funcao "add_agent"
		para entao mudar o agente para o seu novo sitio.
        
		resumo: esta eh a funcao na qual o agente pode olhar para
		a sua vizinhanca aleatoriamente e decidir se vai para um
		novo ambiente ou se permanece onde esta.
		"""
		choice_list = [s for s in self.site.neighbors if s != self.site]
		if len(choice_list) > 0: 
			choosed = numpy.random.choice(choice_list)
			if choosed.resource > self.site.resource:
				choosed.add_agent(self)
		
	def _borrow(self):
		"""
		a funcao "_borrow" eh chamada pelo agente cujo deficit
		de consumo tenha sido maior do que o limiar de divida
		na rodada em questao.
        
		nesta funcao o agente objeto ira procurar novamente por
		um agente na vizinhanca que tenha recursos a lhe oferecer.
		porem desta vez o agente ira aceitar recursos tanto de
		altruistas como de egoistas.
        
		primeiro:a funcao confere se o agente que a chamou ja tem
		alguma divida com alguem ou nao. caso nao tenha ele pode
		pedir por uma troca.
        
		segundo: caso o agente objeto ja nao seja um endividado
		ele cria uma lista de possiveis escolhas que sera formada
		por todos os agentes nos sitios vizinhos ao sitio ocupado
		pelo objeto que tenham seu estoque recursos a mais do que
		aqueles que ele precisa para comer na proxima rodada.
        
		terceiro se existe na vizinhanca do objeto ao menos um agente
		que se encaixe nas caracteristicas definidas pela lista do 
		segundo passo, entao a funcao passa ao quarto passo.
        
		quarto: o agente escolhe um agente entre aqueles que se 
		encaixam na sua lista de opcoes.
        
		quinto: o valor do emprestiom sera igual ao valor de retorno
		da funcao "_lend" que eh aqui chamada pelo agente escolhido.
        
		sexto: o objetoconsome a quantidade de recursos que o agente
		egoista disponibilizou.
        
		setimo: o deficit de consumo do objeto eh subtraido do valor
		trocado com o agente egoista.
		"""
		if self.debt_link == None:
			choice_list = [a for s in self.site.neighbors for a in s.agents_in_site if a.stock >= (self.consumption_demanded - self.consumed)]
			if len(choice_list) > 0: 
				choosed = numpy.random.choice(choice_list)
				loan_value = choosed._lend(self, self.consumption_demanded - self.consumed)
				self.consumed += loan_value
				self.consumption_deficit -= loan_value
		
	def _lend(self, 
			   borrower, 
			   asked_value):
		"""
		a funcao "_lend" eh a funcao que define se o agente
		que chamou a funcao "_borrow" vai ou nao ter algum
		retonro da sua proposta de troca.
	       
		SERIA INTERESSANTE abrir a opcao para o agente que
		chamou a funcao "_borrow" ter a chance de escolher
		um altruista e cooperar com ele sem fazer divida.
	       
		primeiro: a funcao confere se o agente escolhido pelo
		agente que chamou a funcao "_borrow" eh egoista.
		se ele nao for a funcao pula para seu passo de numero
		oito. se sim, ela passa para o passo dois.
	       
		segundo: a funcao define que o valor de emprestimo
		sera igual ao minimo entre o estoque do egoista e o
		valor solicitado pelo agente em necessidado.
	       
		terceiro: o estoque do objeto eh subtraido do valor
		que este ira emprestar ao agente em necessidade.
	       
		quarto: o valor de debito sera igual ao valor do
		objeto DebtLink cujo lender eh o objeto da funcao
		"_lend".
	       
		quinto: a divida eh colocada na lista de emprestimos
		do agente.
	       
		sexto: o debito eh colocado para o borrower (NAO ENTENDI ESTE PASSO)
	       
		setimo: a funcao retorna o valor que o egoista disponibilizou.
	       
		oitavo: caso a condicao do passo um nao tenha sido satisfeita,
		a funcao "_lend" retonra o valor zero. Ou seja, o agente que
		chamou a funcao "_borrow" nao conseguiu nenhum recurso emprestado.
	       
		resumo: esta funcao forma o link de debito entre o agente
		que chama a funcao "_borroW" e o agente escolhido que de
		fato eh quem chama a funcao "_lend". Isso se o lender for um
		egoista que tenha recursos em estoque suficientes para nao
		arriscar sua rodada seguinte.
		"""
		if self.strategy == 1:
			loan_value = min(self.stock, asked_value)
			self.stock -= loan_value
			debt_link = DebtLink(self, borrower, loan_value * (1.0 + self.interest_rate))
			self.loans.append(debt_link)
			borrower.debt_link = debt_link
			return loan_value
		else: return 0.0

	def _take(self,
		   giver,
		   offered_value):
		"""
		"""
		self.consumed += offered_value
		self.consumption_deficit -= offered_value
		
	def give(self):
		"""
		"""
		if self.strategy == 0:
			choice_list = [a for s in self.site.neighbors for a in s.agents_in_site if a != self and a.gift_link == None]
			if len(choice_list) > 0:
				choosed = numpy.random.choice(choice_list)
				gift = min(self.stock, choosed.consumption_demanded - choosed.consumed)
				if gift > 0:
					self.stock -= gift
					choosed._take(self, gift)
					gift_link = GiftLink(self, choosed, gift)
					self.gifts.append(gift_link)
					choosed.gift_link = gift_link

	def _die(self):
		"""
		a funcao "_die" eh a funcao que mata os agentes que
		tenham um deficit de recursos tao grande que eles ja
		ultrapassaram o limiar de morte. estes agentes chamam
		a funcao "_die" dentro da funcao "solve_consumption_deficit".
        
		primeiro: a funcao remove o agente que esta morrendo da
		lista de 'agents_in_site' do site em que o objeto se encontra.
        
		segundo: o ambiente eh removido do agente objeto tambem.
        
		terceiro: se o agente tem alguma divida, a funcao passa
		para o passo de numero quatro. se nao a funcao para.
        
		quarto: a funcao remove o debito do objeto da lista de emprestimos
		do agente para o qual o objeto devia.
        
		quinto: a funcao apaga a divida do agente dele mesmo.
        
		sexto: caso o agente que esta morrendo seja um egoista que
		tenha emprestado recursos a outros agentes, a funcao passa
		para o passo de numero sete, caso nao a funcao para.
        
		setimo: as dividas sao apagadas nos agentes endividados.
        
		oitavo: a funcao deleta todos os valores dentro da lista
		de endividados do agente que esta morrendo.
        
		nono: por fim o agente se remove da lista de agentes
		da dinamica.
        
		resumo: todas as relacoes do agente com outros agentes
		sao desfeitas, inclusive aquelas com os agentes do tipo
		ambiente. ao final o agente se exclui da dinamica.
		"""
		self.site.agents_in_site.remove(self)
		self.site = None
		if self.debt_link != None:
			self.debt_link.lender.loans.remove(self.debt_link)
			self.debt_link = None
		for l, loan in enumerate(self.loans):
			loan.borrower.debt_link = None
			del self.loans[l]
		if self.gift_link != None:
			self.gift_link.giver.gifts.remove(self.gift_link)
			self.gift_link = None
		for g, gift in enumerate(self.gifts):
			gift.taker.gift_link = None
			del self.gifts[g]
		self.agents_list.remove(self)

	def charge(self):
		"""
		a funcao "charge" faz referencia apenas ao agente objeto
		que a chamou. trata=se da funcao que permite aos agentes
		egoistas cobrar o emprestimo realizado na troca em que
		algum ou alguns agentes os procuraram atraves da funcao
		"_borrow".
        
		primeiro: a funcao ordena a lista de emprestimos "loans"
		do agente do menor ao maior valor com o comando 'enumerate'.
        
		segundo: a funcao determina que o valor de pagamento sera
		igual ao valor de retorno da funcao "_pay" chamada pelo
		devedor multiplicada pelo juros da divida (interest_rate).
        
		terceiro: se o valor a ser pago for menor ou igual a zero
		a funcao passa para o quarto passo. se nao a funcao vai
		para o passo numero seis.
        
		quarto: sendo o valor de divida menor ou igual a zero, a 
		funcao desfaz o vinculo de divida do agente que pediu.
        
		quinto: a funcao entao deleta esta divida da lista de
		dividas do agente egoista que emprestou recursos.
        
		sexto: o estoque do agente que chamou a funcao charge
		eh acrescido do valor do pagamento realizado pelo agente
		que estava endividado.
        
		resumo: esta funcao cobra as dividas de emprestimo das
		rodadas anteriores e eventualmente quita a relacao de
		divida quando o agente que pediu ajuda consegue pagar
		todo o valor que devia.
		"""
		for l, loan in enumerate(self.loans):
			payment_value = loan.borrower._pay(loan.value)
			loan.value -= payment_value
			if loan.value <= 0.0:
				loan.borrower.debt_link = None
				del self.loans[l]
			self.stock += payment_value

	def _pay(self, asked_value):
		"""
		a funcao "_pay" faz referencia ao agente que a chamou
		a partir da funcao "charge" e tambem ao valor solicitado
		pelo agente para quitar a sua divida.
        
		primeiro: a funcao determina que o valor a ser pago pelo
		agente endividado sera igual ao minimo entre o valor solicitado
		e a quantidade de recursos que o agente tem disponivel em
		seu estoque.
        
		segundo: a funcao retira do estoque do agente que a chamou
		o valor definido no passo de numero um.
        
		terceiro: a funcao retorna o valor retirado do estoque do
		agente para que seja feito o seu pagamento na funcao "charge".
        
		resumo: esta funcao confere se o agente endividado tem recursos
		para quitar sua divida e retorna o valor que o agente tem
		disponivel em seu estoque.
		"""
		payment_value = min(self.stock, asked_value)
		self.stock -= payment_value
		return payment_value
	
	def retribute(self):
		"""
		"""
		if self.gift_link != None:
			retribution_value = min(self.stock, self.gift_link.value * (1.0 + self.interest_rate))
			self.stock -= retribution_value
			self.gift_link.value -= retribution_value
			self.gift_link.giver.stock += retribution_value
			if self.gift_link.value <= 0.0:
				self.gift_link.giver.gifts.remove(self.gift_link)
				self.gift_link = None

	def sprout(self):
		"""
		a funcao "sprout" faz referencia somente ao agente objeto que a chamou.
		trata-se da funcao que simula a reproducao dos agentes do tipo agent.
        
		primeiro: a funcao sorteia um numero aleatorio entre zero e um e confere
		se o numero sorteado eh menor do que a probabilidade de reproducao do 
		objeto. se sim, a funcao passa ao passo numero dois. se nao, a funcao
		encerra.
        
		terceiro: caso o numero sorteado tenha sido menor do que a probabilidade
		reprodutiva do agente objeto, a funcao adiciona um novo agente aa lista
		de agentes em simulacao no modelo. a funcao passa os proximos doze 
		passos atribuindo valores aos parametros e variaveis do novo agente.
		como, por exemplo, sua habilidade, estoque herdado, estoque maximo, 
		demanda energetica de cada rodada, probabilidade reprodutiva, sua
		porcentagem de heranca, sua estrategia, o seu site associado, e seus
		limiares de morte, divida e seu interest_rate.
        
		decimo sexto: a funcao por fim adiciona todas as caracteristicas
		recebidas pelo agente nos passos anteriores aa lista 'agent_list'
		do modelo.
        
		resumo: a funcao "sprout" cria um novo agente e o adiciona no mesmo
		site em que esta o seu agente pai.
		"""
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

class Simulation:
	"""
	o ultimo objeto do codigo eh o 'Simulation'. eh aqui que sao
	gerados todos os agentes, aqui tambem sao atribuidos todos os
	valores das suas propriedades.
    
	neste objeto tambem sao definidas as funcoes que criam as 
	diferentes topologias que podem ser simuladas, o "step", o
	"simulation" e o "save_data"
	"""
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
		"""
		quando eh iniciada a simulacao a funcao "__init__" eh
		chamada automaticamente pelo objeto 'Simulation'. esta
		funcao faz referencia apenas ao objeto Simulation e aas
		propriedades do proprio que nela sao gerados . sao entao
		gerados todos os sites dentro do valor maximo de 
		sites definidos pelo parametro 'sites_count' inserido
		manualmente.
	       
		a funcao tambem cria todos os agentes definidos pelo
		valor 'agents_count' inserido manualmente como a populacao
		inicial da simulacao. aqui sao atribuidos aos agents todas
		as suas propriedades.
		"""
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
		"""
		a funcao "topology_grid" faz referencia ao Simulationo
		enquanto objeto direcionado e cria uma malha quadrada
		em ambientes com a vizinhanca de distancia um.
		isto eh, cada site tera quatro vizinhos e mais
		ele mesmo na sua lista 'neighbors'. um vizinho
		ao norte um ao sul um a leste e outro a oeste.
        
		primeiro: a funcao cria um for para cada sitio existente.
        
		segundo: a funcao limpa a lista de vizinhos de todos os
		sites criados.
        
		terceiro: a funcao pega cada sitio criado atraves do seu
		indice na lista de sites.
        
		quarto: se o modulo da divisao do indice do sitio pelo 
		lado do grid mais um for menor do que o valor do lado
		do grid,a funcao passa para o quinto passo. se nao ela
		vai para o setimo.
        
		quinto: se a condicao do passo quatro tiver sido satisfeita
		a funcao adiciona o proximo membro da lista de sites como o
		vizinho do objeto.
        
		sexto: a funcao adiciona o objeto na lista de vizinhos do 
		membro da lista i + 1.
        
		sexto: se a condicao do passo quatro nao for satisfeita a
		funcao confere se o numero inteiro da divisao do indice do
		site pelo lado do grid, mais um, eh menor do que o valor do
		lado do grid. se sim, a funcao passa para o setimo passo. se
		nao ela para.
        
		setimo: a funcao adiciona o vizinho de baixo (sul) do grid aa
		vizinhanca do objeto.
        
		oitavo: a funcao adiciona o objeto aa vizinhanca do agente 
		que esta ao sul deste.
        
		resumo: esta funcao cria a vizinhanca leste e sul de cada
		agente e os coloca inversamente como vizinhos dos mesmos.
		"""
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
		"""
		a funcao "topology_circle" faz referencia apenas ao Simulation
		enquanto objeto e ao radius que nada mais eh do que o alcance
		da vizinhanca circular que pode ser definida manualmente na
		inicializacao do modelo.
		"""
		for s in self.sites:
			s.clear_neighbor()
		for i in range(len(self.sites)):
			for r in range(radius):
				self.sites[i].neighbors.append(self.sites[(i + r + 1) % len(self.sites)])
				self.sites[(i + r + 1) % len(self.sites)].neighbors.append(self.sites[i])
			
	def topology_complete(self):
		"""
		a funcao "topology_complete" faz referencia ao Simulation
		enquanto objeto direcionado da funcao. ela cria uma lista de
		vizinhanca para cada agente do tipo site. nesta lista sao 
		inseridos todos os sitios que foram criados na inicializacao
		do modelo, fazendo com que cada site seja vizinho de todos os
		outros sites do modelo.
		"""
		for i in range(len(self.sites) - 1):
			for j in range(i + 1, len(self.sites)):
				self.sites[i].neighbors.append(self.sites[j])
				self.sites[j].neighbors.append(self.sites[i])
			
	def topology_random_connect(self, probability):
		"""
		a funcao "topoplogy_random_connect" faz referencia ao Simulation
		enquanto objeto da funcao e aa probabilidade de conexao que 
		foi definida manualmente na inicializacao do modelo.
        
		o modelo cria uma lista com todos os sites do modelo menos o
		proprio sitio em questao e com a probabilidade definida liga
		os agentes um a um.
		"""
		for i in range(len(self.sites) - 1):
			for j in range(i + 1, len(self.sites)):
				if not (self.sites[j] in self.sites[i].neighbors):
					if numpy.random.rand() < probability:
						self.sites[i].neighbors.append(self.sites[j])
						self.sites[j].neighbors.append(self.sites[i])
					
	def topology_random_reconnect(self, probability):
		"""
		a funcao "topology_random_reconnect" faz referencia ao Simulation
		enquanto objeto da funcao e aa probabilidade de reconexao definida
		manualmente. esta funcao foi criada para gerarmos as redes do tipo
		small world seja no grid seja na topologia circular.
        
		essa lista percorre as listas de vizinhos de cada sitio e com
		uma probabilidade de reconexao definida desfaz a vizinhanca e
		reconecta o link aleatoriamente em outro agente.
		"""
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
		"""
		a funcao step faz referencia apenas ao objeto Simulation.
		esta eh a funcao que chama todas as funcoes simuladas a
		cada time step do modelo.
        
		primeiro: a funcao embaralha aleatoriamente a lista de
		agentes do modelo, o 'agents_list' para que a cada rodada
		a ordem de agentes que executa suas funcoes seja alterada
		de maneira a nao privilegiar nenhum agente.
        
		segundo: para todos os agentes na lista:
			terceiro: cada agente chama a funcao "produce"
            
		quarto: para todos os agentes na lista:
			quinto: cada agente chama a funcao "charge"
            
		sexto: para todos os agentes na lista:
			setimo: cada agente chama a funcao "consume"
            
		oitavo: para todos os agentes na lista:
			nono: cada agente chama a funcao "solve_consumption_deficit"
            
		decimo: para todos os agentes na lista:
			decimo primeiro: cada agente chama a funcao "recovery"
            
		decimo segundo: para todos os agentes na lista:
			decimo terceiro: cada agente chama a funcao "sprout"
            
		resumo: a funcao "step" define a ordem de cada step da
		simulacao.
		"""
		numpy.random.shuffle(self.agents_list)
		for agent in self.agents_list:
			agent.produce()
		for agent in self.agents_list:
			agent.charge()
		for agent in self.agents_list:
			if agent.strategy == 0: 
				agent.retribute()
		for agent in self.agents_list:
			if agent.strategy == 0: 
				agent.give()
		for agent in self.agents_list:
			agent.consume()
		for agent in self.agents_list:
			agent.solve_consumption_deficit()
		for site in self.sites:
			site.recovery()
		for agent in self.agents_list:
			agent.sprout()
	
	def simulation(self, max_time, realizations = 1):
		"""
		a funcao "simulation"  faz referencia aa "Simulation" e aa
		propriedade max_time. esta eh a funcao que chama os steps
		dentro do 'max_time' definido manualmente no começo da
		interacao.
        
		primeiro: a funcao chama cada passo dentro do 'max_time'.
        
		segundo: para cada passo dentro do max_time o objeto chama
		a funcao "step".
        
		terceiro: o objeto chama a funcao "save_data".
		"""
		save_data_begin(self)
		for i in range(realizations):
			for t in range(max_time):
				self.step()
				save_data_step(self, t)
			save_data_realization(self, i)
		save_data_end(self)


def save_data_begin(simulation):
	pass
	pass

def save_data_step(simulation, step):
	pass
	pass

def save_data_realization(simulation, realization):
	"""
	a funcao "save_data"...
	"""
	pass
	pass

def save_data_end(simulation):
	pass
	pass