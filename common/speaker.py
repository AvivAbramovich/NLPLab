class Speaker(object):
    def __init__(self, name, stand_for, description, bio):
        self.name = name
        self.stand_for = stand_for
        self.description = description
        self.bio = bio

    def __str__(self):
        return '%s (stand %s)' % (self.name, 'for' if self.stand_for else 'against')

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name and self.stand_for == other.stand_for and self.description == other.description and self.bio == other.bio
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)