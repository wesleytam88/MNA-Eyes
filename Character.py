class Character():
    def __init__(self, full_name, first_name, last_name, alt_names, img_url, anime):
        self.full_name = full_name
        self.first_name = first_name
        self.last_name = last_name
        self.alt_names = alt_names
        self.img_url = img_url
        self.anime = anime

    def __repr__(self):
        return self.name + " from " + self.anime