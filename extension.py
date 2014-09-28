import requests
from player import Player

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

all_regions = get_all_regions() #list of strings
all_players = {} #dictionary mapping regions to list of Player objects
for region in all_regions:
	all_players[region] = get_players_in_region(region)

def player_by_id(ident, region):
	for player in all_players[region]:
		if player.id == ident:
			return player
	return 'Player with id' + ident + ' not found in ' + region

def get_matches_in_region(region):
	return 

all_matches = {} #dictionary mapping regions to list of matches, represented as dictionaries 
for region in all_regions:
	all_matches[region] = get_matches_in_region(region)