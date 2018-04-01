class Speaker(object):
    def __init__(self, name, stand_for, description, bio):
        self.name = name
        self.stand_for = stand_for
        self.description = description
        self.bio = bio

    def __str__(self):
        return '%s (stand %s)' % (self.name, 'for' if self.stand_for else 'against')