class Tournament(object):

    def __init__(self, ident, date, name):
        self.id = ident
        self.date = date
        self.name = name

    def __str__(self):
        return "%s on %s" % (self.name, self.date)

    def __repr__(self):
        return "%s on %s" % (self.name, self.date)