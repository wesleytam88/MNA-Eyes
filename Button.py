# Code by https://www.youtube.com/@BaralTech

class Button():
    def __init__(self, image, pos, font, text_input, base_color, hover_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos))
        
    def update(self, screen):
        '''Displays the text onto the screen'''

        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, mouse_pos):
        '''Returns true/false if button was pressed'''

        if (mouse_pos[0] in range(self.rect.left, self.rect.right) and 
                mouse_pos[1] in range(self.rect.top, self.rect.bottom)):
            return True
        return False

    def changeColor(self, mouse_pos):
        '''Code for changing the button color when hovering over the button'''

        if (mouse_pos[0] in range(self.rect.left, self.rect.right) and 
                mouse_pos[1] in range(self.rect.top, self.rect.bottom)):
            self.text = self.font.render(self.text_input, True, self.hover_color)