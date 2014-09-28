class Match(object):

    def __init__(self, player1, player2, result, tournament):
        self.player1 = player1
        self.player2 = player2
        self.result = result #'win' if player1 won, 'lose' if player1 lost
        self.tournament = tournament

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
                self.player1.name == other.player2 and \
                self.player2 == other.player1.name and \
                self.result != other.result and \
                self.tournament == other.tournament

    def __str__(self):
        return "%s %s against %s at %s" % (self.player1.name, self.result, 
                                            self.player2, self.tournament)

    def __repr__(self):
        return "%s %s against %s at %s" % (self.player1.name, self.result, 
                                            self.player2, self.tournament)