class Player():
    def __init__(self, name, score, buzzer):
        self.name = name
        self.score = score
        self.buzzer = buzzer

    def __repr__(self):
        return str(self.score) + " " + self.name + ": '" + chr(self.buzzer) + "'"

    def __lt__(self, other):
        if type(other) != type(self):
            raise TypeError
        if other.score == self.score:
            return self.name.lower() < other.name.lower()
        return other.score < self.score