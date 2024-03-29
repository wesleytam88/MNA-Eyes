import pygame
import sys
import time
import os
import random
from PIL import Image
from Button import *
from Player import *
from ordered_list_iterative import *

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE) # Width, height

# Program Title and Icon
pygame.display.set_caption("Anime Eyes")
icon = pygame.image.load("assets/temporarily_not_available.png")
pygame.display.set_icon(icon)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
grey = (90, 90, 90)
darkTurquoise = (0, 206, 209)
red = (255, 0, 0)
BACKGROUND_COLOR = black

# Fonts
title_font_size = 150
title_font = pygame.font.SysFont("cambria", title_font_size)
button_font_size = 100
button_font = pygame.font.SysFont("cambria", button_font_size)
user_input_font_size = 46
user_input_font = pygame.font.SysFont("cambria", user_input_font_size)

# Player List
players = OrderedList()

# Image variables
num_imgs = len([name for name in os.listdir("./images")])
img_list = os.listdir("./images")
random_img_indx = 0    # Which random image are we on
random_img_list = []
for i in random.sample(range(num_imgs), num_imgs):
    random_img_list.append(img_list[i])

# Pixelation constants
INITIAL_PIXELATION = 0.0125
PIXELATION_INCREMENT = 0.001

# Game constants
practice_mode = False
char_list = []
char_dict = {}
TIME_TO_GUESS = 10
TIME_TO_UNPIXELATE = 15

def display_text(text, font, color, coords):
    '''Takes a String to display, font, color, and coordinates. Displays the
       text with the desired attributes on the screen at the coordinates'''

    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect(center = coords)
    screen.blit(textSurface, textRect)

def make_textbox(screen, text, pos, height, color):
    '''Makes a textbox with dynamic length and ability to save user input'''

    TEXTBOX_LEN = 1000
    TEXTBOX_BORDER = 4

    text_box = pygame.Rect(pos[0], pos[1], TEXTBOX_LEN, height)
    text_box.center = (pos[0], pos[1])
    pygame.draw.rect(screen, color, text_box, TEXTBOX_BORDER)

    # Handle text
    text_surface = user_input_font.render(text, True, white)
    text_rect = text_surface.get_rect(center = (pos[0], pos[1]))
    text_box.width = max(TEXTBOX_LEN, text_surface.get_width() + 20)
    screen.blit(text_surface, text_rect)
    # text_box.width = max(TEXTBOX_LEN, text_surface.get_width() + 20)
    return text_box

def make_timer_bar(screen, pos, length, height, color):
    '''Makes a timer bar that decreases length as time progresses'''

    timer_bar = pygame.Rect(pos[0], pos[1], length, height)
    timer_bar.center = (pos[0], pos[1])
    pygame.draw.rect(screen, color, timer_bar)
    return timer_bar

def pixelate(img_name, size):
    '''Pixelates images by scaling down the size then scaling back up again.
       Size variable is a ratio of the original size from 0 < size < 1.000
       Returns path to the pixelated image'''

    rescale_ratio = None
    image = Image.open("./images/" + img_name)

    rescale_ratio = fit_screen_ratio(screen, image)
    image = image.resize(((int)(image.width * rescale_ratio), (int)(image.height * rescale_ratio)), Image.BILINEAR)

    small_img = image.resize(((int)(image.height * size), (int)(image.width * size)), Image.BILINEAR)
    pixelated = small_img.resize(image.size, Image.NEAREST)
    pixelated_path = "./manipulations/" + img_name
    pixelated.save(pixelated_path)
    return pixelated_path

def fit_screen_ratio(screen, image):
    '''Takes in the screen and the image, returns the ratio to which
       the image needs to fit on the screen'''

    if image.width < screen.get_width() and image.height < screen.get_height():
        # Image smaller than screen
        rescale_ratio = min(screen.get_width()/image.width, screen.get_height()/image.height)
    elif image.width < screen.get_width() and image.height > screen.get_height():
        # Image taller but slimmer than screen
        rescale_ratio = screen.get_height()/image.height
    elif image.width > screen.get_width() and image.height < screen.get_height():
        # Image wider but shorter than screen
        rescale_ratio = screen.get_width()/image.width
    else:
        # Image wider and taller than screen
        rescale_ratio = max(image.width/screen.get_width(), image.height/screen.get_height())
    return rescale_ratio

def clear_manips_dir():
    '''Remove all files in manipulations directory'''

    dir = "./manipulations"
    for file in os.listdir(dir):
        os.remove(os.path.join(dir, file))


def main_menu():
    '''Displays the main menu screen'''

    while True:
        half_width = screen.get_width()/2
        ninth_height = screen.get_height()/9
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(BACKGROUND_COLOR)
        display_text("Anime Eyes", title_font, white, (half_width, ninth_height*2))

        party_mode_button = Button(image=None, pos=(half_width, ninth_height*5), font=button_font, text_input="Party Mode (1)", base_color=white, hover_color=grey)
        options_button = Button(image=None, pos=(half_width, ninth_height*6), font=button_font, text_input="OPTIONS (O)", base_color=white, hover_color=grey)
        quit_button = Button(image=None, pos=(half_width, ninth_height*7), font=button_font, text_input="QUIT (Q)", base_color=white, hover_color=grey)
        for button in [party_mode_button, options_button, quit_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if party_mode_button.checkForInput(mouse_pos):
                    party_setup()
                if options_button.checkForInput(mouse_pos):
                    options()
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    party_setup()
                if event.key == pygame.K_o:
                    options()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()

def options():
    '''Displays the options screen'''

    while True:
        half_width = screen.get_width()/2
        eighth_height = screen.get_height()/8
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(BACKGROUND_COLOR)
        # display_text("Options", title_font, white, (screen.get_width()/2, screen.get_height()/8*2))

        menu_button = Button(image=None, pos=(half_width, eighth_height), font=button_font, text_input="Back to Menu", base_color=white, hover_color=grey)
        for button in [menu_button]:
            button.changeColor(mouse_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.checkForInput(mouse_pos):
                    main_menu()

        pygame.display.update()

def party_setup():
    '''Displays the set-up screen for party mode'''

    while True:
        quarter_width = screen.get_width()/4
        eighth_height = screen.get_height()/8
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(BACKGROUND_COLOR)

        add_new_player_button = Button(image=None, pos=(quarter_width, eighth_height*3), font=button_font, text_input="Add new Player (N)", base_color=white, hover_color=grey)
        start_game_button = Button(image=None, pos=(quarter_width, eighth_height*4), font=button_font, text_input="Start Game (Space)", base_color=white, hover_color=grey)
        menu_button = Button(image=None, pos=(quarter_width, eighth_height*5), font=button_font, text_input="Back to Menu (Esc)", base_color=white, hover_color=grey)
        for button in [add_new_player_button, start_game_button, menu_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        # Make and display player buttons
        player_buttons = []
        for i in range(players.size()):
            player_buttons.append(Button(image=None, pos=(quarter_width*3, (screen.get_height()/20)*(i + 1)), font=user_input_font, text_input=players.get_item(i).name, base_color=white, hover_color=red))
            player_buttons[i].changeColor(mouse_pos)
            player_buttons[i].update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if add_new_player_button.checkForInput(mouse_pos):
                    add_new_player()
                if start_game_button.checkForInput(mouse_pos) and players.length > 0:
                    countdown()
                if menu_button.checkForInput(mouse_pos):
                    main_menu()
                for button in player_buttons:
                    if button.checkForInput(mouse_pos):
                        players_list = players.python_list()
                        for i in range(players.size()):
                            if players_list[i].name == button.text_input:
                                players.remove(players_list[i])
                                break
                            i += 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    add_new_player()
                if event.key == pygame.K_SPACE and players.length > 0:
                    countdown()
                if event.key == pygame.K_ESCAPE:
                    players.clear()
                    main_menu()

        pygame.display.update()

def add_new_player():
    '''Displays the screen to add players to the game'''

    NAME_MAX_LEN = 30
    name = ""
    while True:
        half_width = screen.get_width()/2
        third_width = screen.get_width()/3
        eighth_height = screen.get_height()/8
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(BACKGROUND_COLOR)
        display_text("Enter Name", title_font, white, (half_width, eighth_height*3))
        make_textbox(screen, name, (half_width, eighth_height*4), user_input_font_size + 20, white)

        cancel_button = Button(image=None, pos=(third_width, eighth_height*5), font=button_font, text_input="Cancel (Esc)", base_color=white, hover_color=grey)
        submit_button = Button(image=None, pos=(third_width*2, eighth_height*5), font=button_font, text_input="Submit (Enter)", base_color=white, hover_color=grey)
        for button in [cancel_button, submit_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cancel_button.checkForInput(mouse_pos):
                    party_setup()
                if submit_button.checkForInput(mouse_pos) and name != "":
                    buzzer_setup(name)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    party_setup()
                elif event.key == pygame.K_RETURN and name != "":
                    buzzer_setup(name)
                else:
                    if (len(name) <= NAME_MAX_LEN) and event.unicode != '\r':
                        # Fix ENTER being a valid name
                        name += event.unicode

        pygame.display.update()

def buzzer_setup(name):
    '''Displays the screen to map buttons to each player'''
    while True:
        half_width = screen.get_width()/2
        fifth_height = screen.get_height()/5
        same_buzzer = False

        screen.fill(BACKGROUND_COLOR)
        display_text(name, title_font, white, (half_width, fifth_height*2))
        display_text("Hit your buzzer", title_font, white, (half_width, fifth_height*3))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                player_list = players.python_list()
                for player in player_list:
                    if player.buzzer == event.key:
                        same_buzzer = True
                        break
                if not same_buzzer:
                    players.add(Player(name, 0, event.key))
                    party_setup()
        
        pygame.display.update()

def countdown():
    '''Displays the countdown timer (3 seconds)'''

    start = time.time()
    while True:
        half_width = screen.get_width()/2
        half_height = screen.get_height()/2
        screen.fill(BACKGROUND_COLOR)
        if (time.time() - start < 1):
            # 0-1 seconds have passed
            display_text("3", title_font, white, (half_width, half_height))
        elif (time.time() - start < 2):
            # 1-2 seconds have passed
            display_text("2", title_font, white, (half_width, half_height))
        elif (time.time() - start < 3):
            # 2-3 seconds have passed
            display_text("1", title_font, white, (half_width, half_height))
        else:
            play()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()

def play(pixelation=INITIAL_PIXELATION):
    '''Game screen with pixelated images'''

    global random_img_indx
    player_list = players.python_list()
    buzzers = {}    # Hashmap of buzzers and their respective players
    for player in player_list:
        buzzers[player.buzzer] = player
    rand_pic_name = random_img_list[random_img_indx]

    start = time.time()

    while True:
        half_width = screen.get_width()/2
        half_height = screen.get_height()/2
        screen.fill(BACKGROUND_COLOR)

        if pixelation < 0.25:
            pixel_img = pixelate(rand_pic_name, pixelation)
            pixelation += PIXELATION_INCREMENT * 2
        elif pixelation < 0.5:
            pixel_img = pixelate(rand_pic_name, pixelation)
            pixelation += PIXELATION_INCREMENT * 5
        elif pixelation < 0.75:
            pixel_img = pixelate(rand_pic_name, pixelation)
            pixelation += PIXELATION_INCREMENT * 10
        elif pixelation < 1:
            pixel_img = pixelate(rand_pic_name, pixelation)
            pixelation += PIXELATION_INCREMENT * 20

        background = pygame.image.load(pixel_img)
        rect = background.get_rect(center = (half_width, half_height))
        screen.blit(background, rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                clear_manips_dir()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                for buzzer in buzzers:
                    if event.key == buzzer:
                        guess(buzzers[buzzer], rand_pic_name, pixelation)

        pygame.display.update()

def guess(player, img_name, pixelation):
    '''Guessing page of the game. Takes in a Player object, the name of the
       image, and the current pixelation level'''
    global random_img_indx

    guesser = players.remove(player)

    img_name = img_name[0:img_name.rfind('.')]      # Name of image before '.'
    print("Image name: " + img_name)
    start = time.time()

    while True:
        half_width = screen.get_width()/2
        eighth_height = screen.get_height()/8
        screen.fill(BACKGROUND_COLOR)
        display_text(player.name, title_font, white, (half_width, eighth_height*3))

        make_timer_bar(screen, (half_width, eighth_height*5), ((start + TIME_TO_GUESS - time.time()) * 100), user_input_font_size, red)

        if time.time() - start >= TIME_TO_GUESS:
            # Guesser out of time
            guesser.score -= (int)((1 - pixelation) * 100)
            players.add(guesser)
            play(pixelation)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                clear_manips_dir()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    # Press 'y' for correct guess
                    random_img_indx += 1
                    guesser.score += (int)((1 - pixelation) * 100)
                    players.add(guesser)
                    show_original_image()
                elif event.key == pygame.K_n:
                    # Press 'n' for incorrect guess
                    guesser.score -= (int)((1 - pixelation) * 100)
                    players.add(guesser)
                    play(pixelation)

        pygame.display.update()

def show_original_image():
    '''Reveals the original image after a correct guess'''

    while True:
        half_width = screen.get_width()/2
        half_height = screen.get_height()/2
        screen.fill(BACKGROUND_COLOR)
        image = Image.open("./images/" + random_img_list[random_img_indx - 1])
        resize_ratio = fit_screen_ratio(screen, image)
        resized_image = image.resize(((int)(image.width * resize_ratio), (int)(image.height * resize_ratio)), Image.BILINEAR)
        path = "./manipulations/Resized " + random_img_list[random_img_indx - 1]
        resized_image.save(path)

        background = pygame.image.load(path)
        rect = background.get_rect(center = (half_width, half_height))
        screen.blit(background, rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                clear_manips_dir()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    scoreboard()

        pygame.display.update()

def scoreboard():
    '''Displays the scoreboard of the game'''

    global random_img_indx
    global random_img_list
    global practice_mode
    game_over = random_img_indx >= num_imgs

    while True:
        half_width = screen.get_width()/2
        twentieth_height = screen.get_height()/20
        screen.fill(BACKGROUND_COLOR)
        if game_over:
            display_text("End of Game!", title_font, red, (half_width, twentieth_height))
        else:
            display_text("Scoreboard", title_font, white, (half_width, twentieth_height))

        for i in range(players.size()):
            player = players.get_item(i)
            display_text(player.name + ": " + str(player.score), user_input_font, white, (half_width, twentieth_height*(i + 3)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                clear_manips_dir()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_BACKSPACE, pygame.K_RETURN]:
                    if not game_over:
                        play(INITIAL_PIXELATION)
                    else:
                        players.clear()
                        # Clear manipulations directory
                        clear_manips_dir()
                        # Reset rand_img_list and rand_img_indx
                        random_img_indx = 0
                        random_img_list = []
                        for i in random.sample(range(num_imgs), num_imgs):
                            random_img_list.append(img_list[i])
                        practice_mode = False
                        main_menu()

        pygame.display.update()

main_menu()