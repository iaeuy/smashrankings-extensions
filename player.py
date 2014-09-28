import requests
import sys
from match import Match

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

    def worst_loss(self, region):
        import extension
        worst_loss = None
        worst_rank = 0
        for match in self.get_matches(region):
            if match.result == 'win':
                continue
            opponent = extension.player_by_name(match.player2, region)
            if isinstance(opponent, str):
                continue
            if opponent.rank > worst_rank:
                worst_rank = opponent.rank
                worst_loss = match
        if not worst_loss:
            return 'Player has no losses in ' + region
        return worst_loss

    def head_to_head_record(self, other, region):
        wins = 0
        losses = 0
        for match in self.get_matches(region):
            if match.player2 == other.name:
                if match.result == 'win':
                    wins += 1
                else:
                    losses += 1
        return wins, losses

    def common_results(self, other, region):
        import extension
        p1_matches = self.get_matches(region)
        p2_matches = other.get_matches(region)
        common_players = []
        results = {}
        for match in p1_matches:
            for p2match in p2_matches:
                if match.player2 == p2match.player2:
                    if match.player2 not in common_players:
                        common_players.append(match.player2)
        for player in common_players:
            common_player = extension.player_by_name(player, region)
            if isinstance(common_player, str):
                continue
            results[player] = self.head_to_head_record(common_player, region), \
                                other.head_to_head_record(common_player, region)
        return results  

    def __str__(self):
        return "[%s, %s, %s]" % (self.name, self.rank, self.rating)

    def __repr__(self):
        return "[%s, %s, %s]" % (self.name, self.rank, self.rating)
