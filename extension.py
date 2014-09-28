import requests
from player import Player
from match import Match
from tournament import Tournament

#returns list of all regions as strings
def get_all_regions():
	return requests.get('http://garsh0p.no-ip.biz:5100/regions').json()['regions']

def get_players_in_region(region):
	players = []
	players_as_dicts = requests.get('http://garsh0p.no-ip.biz:5100/' + region + 
									'/rankings').json()['ranking']
	for player_dict in players_as_dicts:
		players.append(Player(player_dict['id'], 
							  player_dict['name'],
							  player_dict['rank'],
							  player_dict['rating']))
	return players

def get_tournaments_in_region(region):
	tournaments = []
	tournaments_as_dicts = requests.get('http://garsh0p.no-ip.biz:5100/' + region + 
									'/tournaments').json()['tournaments']
	for tournament in tournaments_as_dicts:
		tournaments.append(Tournament(tournament['id'],
									  tournament['date'],
									  tournament['name']))
	return tournaments

all_regions = get_all_regions() #list of strings
all_players = {} #dictionary mapping regions to list of Player objects
all_tournaments = {}
for region in all_regions:
	all_players[region] = get_players_in_region(region)
	all_tournaments[region] = get_tournaments_in_region(region)

def player_by_id(ident, region):
	for player in all_players[region]:
		if player.id == ident:
			return player
	return 'Player with id' + ident + ' not found in ' + region

def player_by_name(name, region):
	for player in all_players[region]:
		if player.name.lower() == name.lower():
			return player
	return 'Player with name' + name + ' not found in ' + region

def tournament_by_id(ident, region):
	for tournament in all_tournaments[region]:
		if tournament.id == ident:
			return tournament
	return 'Tournament with id' + ident + ' not found in ' + region

def get_matches_in_region(region):
	matches = []
	for player in all_players[region]:
		matches_as_dicts = requests.get('http://garsh0p.no-ip.biz:5100/' + region + 
										'/matches?player=' + player.id).json()['matches']
		for match in matches_as_dicts:
			to_add = Match(player, 
						   match['opponent_name'],
						   match['result'], 
						   match['tournament_name'])
			if to_add not in matches:
				matches.append(to_add)
	return matches

# all_matches = {} #dictionary mapping regions to list of matches, represented as dictionaries 
# for region in all_regions:
# 	all_matches[region] = get_matches_in_region(region)