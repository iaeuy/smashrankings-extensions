class Player(object):

	def __init__(self, id, name, rank, rating):
		self.id = id
		self.name = name
		self.rank = rank
		self.rating = rating

	def get_matches(self):
		return

	def best_win(self):
		return

	def worst_loss(self):
		return

	def __str__(self):
		return "[%s, %s, %s]" % (self.name, self.rank, self.rating)

	def __repr__(self):
		return "[%s, %s, %s]" % (self.name, self.rank, self.rating)

	def __eq__(self, other):
		return