import requests
import sys

class Player(object):

	def __init__(self, ident, name, rank, rating):
		self.id = ident
		self.name = name
		self.rank = int(float(rank))
		self.rating = rating

	def get_matches(self, region):
		from match import Match
		matches = []
		matches_as_dicts = requests.get('http://garsh0p.no-ip.biz:5100/' + region + 
										'/matches?player=' + self.id).json()['matches']
		for match in matches_as_dicts:
			matches.append(Match(self, 
						   match['opponent_name'],
						   match['result'], 
						   match['tournament_name']))
		return matches

	def best_win(self, region):
		import extension
		best_win = None
		best_rank = sys.maxsize
		for match in self.get_matches(region):
			opponent = extension.player_by_name(match.player2, region)
			if opponent.rank < best_rank:
				best_rank = opponent.rank
				best_win = match
		return best_win

    def worst_loss(self):
        return

    def __str__(self):
        return "[%s, %s, %s]" % (self.name, self.rank, self.rating)

	def __repr__(self):
		return "[%s, %s, %s]" % (self.name, self.rank, self.rating)
