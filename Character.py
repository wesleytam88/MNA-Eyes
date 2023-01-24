class Character():
    def __init__(self, name, alt_names, char_img, anime):
        self.name = name
        self.alt_names = alt_names
        self.char_img = char_img
        self.anime = anime

    def __repr__(self):
        return self.name + " from " + self.anime