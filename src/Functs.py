import pygame                                                                                   # Import libraries
import random
import os

from pygame import draw

WIDTH  = 1280                                                                                   # Width of the game window
HEIGHT = 960                                                                                    # Height of the game window
FPS    = 60                                                                                     # Frames per second

# Create the game and window

SIZE_Y              = 120                                                                       # Height of the apartment
SIZE_X              = 240                                                                       # Width of the apartment
LOWER_Y_BORDER      = 500                                                                       # Boundary where previous apartments stand
X_PIVOT_OF_NEW_FLAT = 300                                                                       # X coordinate where apartments appear
Y_PIVOT_OF_NEW_FLAT = 180                                                                       # Y coordinate where apartments appear
CENTER              = 520                                                                       # Coordinate where the building is centered
DOWN_MOVE           = 4                                                                         # Speed of downward movement
xMOVE               = -10                                                                       # Speed of movement along the X coordinate
BUILD_DOWN_MOVE     = 0.2                                                                       # Speed of the whole building moving down

FLAT_NUM            = 0
FIRST_FLOOR         = 1
SECOND_FLOOR        = 2
THIERD_FLOOR        = 3
FOURTH_FLOOR        = 4
FIFTH_FLOOR         = 5

COORDS_Y_1_FLAT     = 620                                                                       # Y coordinate of the 1st floor (the floor that is already in the building)
COORDS_Y_2_FLAT     = 740                                                                       # Y coordinate of the 2nd floor (the floor that is already in the building)
COORDS_Y_3_FLAT     = 860                                                                       # Y coordinate of the 3rd floor (the floor that is already in the building)

global coords_x,     coords_y                                                                   # Declare which variables are global
global flat_size_x,  flat_size_y, flats_arr 
global score,        score_text,  text_surf

pygame.init ()                                                                                  # Initialize the game

pygame.mixer.init ()                                                                            # Initialize sound

screen = pygame.display.set_mode ((WIDTH, HEIGHT))                                              # Create the window

pygame.display.set_caption ("Build your home!")                                                 # Title of the game

clock = pygame.time.Clock ()                                                                    # To ensure the game runs at a specified frame rate

backfront  = pygame.image.load ("inc/Imgs/backgraund.png").convert ()                           # Load the background

screen.blit (backfront, (0, 0))                                                                 # Draw the background

def CheckIvent ():                                                                              # Function checks what the user pressed and if they pressed anything at all
    for event in pygame.event.get():                                                            # Iterate through each event, that is, each key pressed, mouse click
        if event.type == pygame.QUIT:                                                           # If the user entered QUIT, then exit
            os.abort ()
        if event.type == pygame.KEYDOWN:                                                        # If the user pressed Escape, then exit
            if event.key == pygame.K_ESCAPE:    
                os.abort ()
            elif event.key == pygame.K_SPACE:                                                   # If the user pressed space, return True, True is also = 1
                return True
            elif event.key == pygame.K_r:                                                       # If the user pressed "R", return -1
                return -1
            elif event.key == pygame.K_1:                                                       # If you press 1, it will pause the music
                pygame.mixer.music.pause()
            elif event.key == pygame.K_2:                                                       # If you press 2, it will unpause, lower the volume
                pygame.mixer.music.unpause()
                pygame.mixer.music.set_volume(0.5)  
            elif event.key == pygame.K_3:                                                       # If you press 3, it will unpause, increase the volume
                pygame.mixer.music.unpause()    
                pygame.mixer.music.set_volume(1)
    return False                                                                                # If none of the conditions fit, return False = 0

def FlatCut():                                                                    # Function that handles the falling floor
    global coords_x, flat_size_x                                                               # Declare which variables are global

    if coords_x[FLAT_NUM] < coords_x[FIRST_FLOOR]:
        flat_size_x = flat_size_x - (coords_x[FIRST_FLOOR] - coords_x[FLAT_NUM])                                # Determines where the house fell. If it's slightly closer to the start of the tower, this applies
        coords_x[FLAT_NUM] = coords_x[FIRST_FLOOR]
    elif coords_x[FLAT_NUM] > coords_x[FIRST_FLOOR]:                                                            # If it's past the start of the tower, then this applies
        flat_size_x = flat_size_x - (coords_x[FLAT_NUM] - coords_x[FIRST_FLOOR])
    
def GameOver():                                                                                 # Function that is called at the end of the game when the player loses
    game_is_vse     = pygame.font.Font ("inc/Texts/CubicPixel.otf", 150)                             # Initialize the font. The path 'inc' is the file path, the rest is the size
    vse_surf        = game_is_vse.render (f"Game Over!", False, (255, 13, 10))                         # Now set the text, antialiasing = False, color

    over_score_text = pygame.font.Font ("inc/Texts/CubicPixel.otf", 100)
    text_surf       = over_score_text.render (f"Your score: {score}", False, (255, 255, 255))

    retry_text_surf = pygame.font.Font ("inc/Texts/CubicPixel.otf", 50)
    text_retry      = retry_text_surf.render ("To play again press \"R\"", False, (255, 255, 255))

    screen.blit (backfront,  (0, 0))                                                              # Clear the screen of everything that was there before

    screen.blit (vse_surf,   (300, 300))                                                           # Render "Game Over" on the screen
    screen.blit (text_surf,  (350, 500))                                                          # Render Score on the screen                                                         
    screen.blit (text_retry, (400, 700))                                                         # Render "To play press R" on the screen

    pygame.display.flip ()                                                                       # Update the screen for the user

    while True:                                                                                 # Continuously check if the user pressed something
        res = CheckIvent ()

        if res == -1:
            GameCtor ()                                                                             # If pressed, call main where the game starts
            StartGame ()
            return

def GameCtor ():
    global coords_x,     coords_y,    xMOVE                                                                # Declare which variables are global
    global flat_size_x,  flat_size_y, flats_arr
    global flats_arr,    score, text_surf,   score_text

    pygame.mixer.music.load ("inc/Sounds/Subway.mp3")                                            # Loads audio
    pygame.mixer.music.play (-1)                                                                 # Loops the audio, as -1 is specified

    flat_size_x = SIZE_X                                                                        # Size of the flat image on X
    flat_size_y = SIZE_Y                                                                        # Size of the flat image on Y

    score = 0                                                                                   # Player's score

    score_text = pygame.font.Font("inc/Texts/CubicPixel.otf", 75)                               # Text, as mentioned earlier
    text_surf  = score_text.render(f"Your score: {score}", False, (255, 255, 255))

    coords_x = [X_PIVOT_OF_NEW_FLAT, CENTER, CENTER, CENTER]
    coords_y = [Y_PIVOT_OF_NEW_FLAT, COORDS_Y_1_FLAT, COORDS_Y_2_FLAT, COORDS_Y_3_FLAT]

    flat1 = Flats ("inc/Imgs/flat1.png", flat_size_x, flat_size_y)
    flat2 = Flats ("inc/Imgs/flat2.jpg", flat_size_x, flat_size_y)
    flat3 = Flats ("inc/Imgs/flat3.jpg", flat_size_x, flat_size_y)
    flat4 = Flats ("inc/Imgs/flat4.jpg", flat_size_x, flat_size_y)
    flat5 = Flats ("inc/Imgs/flat5.jpg", flat_size_x, flat_size_y)

    floor = Flats ("inc/Imgs/flat1.png", flat_size_x, flat_size_y)

    flats_arr = [floor, flat1, flat2, flat3, flat4, flat5]

def ScreenPrint (screen_flat, screen_flat_1, screen_flat_2, screen_flat_3, text_surf):
    screen.blit (backfront, (0, 0))                                                             # Clear the screen

    # This is the function This is what is displayed These are the coordinates of what is displayed
    screen.blit (screen_flat_1, (coords_x[FIRST_FLOOR],  coords_y[FIRST_FLOOR]))                # Render the flats on the screen
    screen.blit (screen_flat_2, (coords_x[SECOND_FLOOR], coords_y[SECOND_FLOOR]))
    screen.blit (screen_flat_3, (coords_x[THIERD_FLOOR], coords_y[THIERD_FLOOR]))

    screen.blit (screen_flat,   (coords_x[FLAT_NUM],  coords_y[FLAT_NUM]))

    screen.blit (text_surf, (430, 100))                                                         # Place the text

    pygame.display.flip ()                                                          # Show the result of this iteration to the user

def DropTheFlat ():
    coords_x[THIERD_FLOOR] = coords_x[SECOND_FLOOR]                                                 # Change 2 -> 3, 1 -> 2, the flat that is falling -> becomes the first floor
    coords_x[SECOND_FLOOR] = coords_x[FIRST_FLOOR]
    coords_x[FIRST_FLOOR]  = coords_x[FLAT_NUM]

    coords_y[FIRST_FLOOR]  = COORDS_Y_1_FLAT                                                # Align the Y coordinates of the flats
    coords_y[SECOND_FLOOR] = COORDS_Y_2_FLAT
    coords_y[THIERD_FLOOR] = COORDS_Y_3_FLAT

    coords_y[FLAT_NUM] = Y_PIVOT_OF_NEW_FLAT                                             # Reset the coordinates of the moving floor to the standard ones
    coords_x[FLAT_NUM] = X_PIVOT_OF_NEW_FLAT

    num = random.randint (1, 5)                                                     # Randomly choose a number from 1 to 5 to select a new skin for the floor

    if num == 1:
        flats_arr[FLAT_NUM].surf = pygame.transform.scale(flats_arr[FIRST_FLOOR].surf,  (flat_size_x, flat_size_y))
    elif num == 2:
        flats_arr[FLAT_NUM].surf = pygame.transform.scale(flats_arr[SECOND_FLOOR].surf, (flat_size_x, flat_size_y))
    elif num == 3:
        flats_arr[FLAT_NUM].surf = pygame.transform.scale(flats_arr[THIERD_FLOOR].surf, (flat_size_x, flat_size_y))
    elif num == 4:
        flats_arr[FLAT_NUM].surf = pygame.transform.scale(flats_arr[FOURTH_FLOOR].surf, (flat_size_x, flat_size_y))
    elif num == 5:
        flats_arr[FLAT_NUM].surf = pygame.transform.scale(flats_arr[FIFTH_FLOOR].surf,  (flat_size_x, flat_size_y))
    
    return False

class Flats:

    def __init__ (self, file_directory, flat_size_x, flat_size_y):
        self.ctor = pygame.image.load(file_directory).convert ()                                                        # Load images of flat variants
        self.surf = pygame.transform.scale(self.ctor, (flat_size_x, flat_size_y))                                       # Set the initial size of each flat  

def StartGame ():
    global coords_x,     coords_y,    xMOVE                                                                             # Declare which variables are global
    global flat_size_x,  flat_size_y, flats_arr
    global flats_arr,    score, text_surf,   score_text

    flat = flats_arr[FLAT_NUM].surf                                                                                     # Our flat - it can change, so its skin is a variable

    screen_flat_1 = flats_arr[THIERD_FLOOR].surf                                                                        # These are variables. They will change when your block falls
    screen_flat_2 = flats_arr[FIRST_FLOOR].surf                                                                         # The reason they have these values now is just the initial value set randomly
    screen_flat_3 = flats_arr[FIFTH_FLOOR].surf

    key_pressed = False                                                                                                 # Boolean variable (can be only True = 1 or False = 0), indicates if the user has pressed a key
    go_down     = False                                                                                                 # Indicates if the entire column of flats is moving down, also a boolean

    ScreenPrint (flat, screen_flat_1, screen_flat_2, screen_flat_3, text_surf)

    while True:                                                                                 # Enter the loop
        if go_down:                                                                             # Marker for when your flat is falling
            if coords_y[SECOND_FLOOR] >= COORDS_Y_3_FLAT:                                               # If the coordinate of the second floor has become that of the third floor, then
                go_down = DropTheFlat ()

                screen_flat_3 = screen_flat_2                                                   # Change the values of the variables
                screen_flat_2 = screen_flat_1

                screen_flat_1 = pygame.transform.scale(flat, (flat_size_x, flat_size_y))        # Draw our new first floor on the screen

                flat = flats_arr[FLAT_NUM].surf
                
                continue                                                                        # Next iteration of the loop
            else:
                ScreenPrint (flat, screen_flat_1, screen_flat_2, screen_flat_3, text_surf)

                coords_y[FIRST_FLOOR]  += BUILD_DOWN_MOVE                                               # Move all floors slightly down the screen
                coords_y[SECOND_FLOOR] += BUILD_DOWN_MOVE
                coords_y[THIERD_FLOOR] += BUILD_DOWN_MOVE
                coords_y[FLAT_NUM]  += BUILD_DOWN_MOVE


                continue
        elif key_pressed == True:                                                               # If the user pressed the spacebar
            if coords_y[FLAT_NUM] >= LOWER_Y_BORDER:                                                     # If our floor has already dropped to the level of the upper standing floor, enter if
                key_pressed = False                                                             # Remove the marker indicating the user pressed a key

                FlatCut ()                                   # Cut the image

                if flat_size_x <= 0:                                                            # If the size of the flat has become 0, the user loses
                    GameOver ()
                    return 0
                    
                flat = pygame.transform.scale (flat, (flat_size_x, flat_size_y))                # Otherwise change the size to the one that has been cut

                score += 1                                                               # +1 to the score
                text_surf  = score_text.render (f"Your score: {score}", False, (255, 255, 255)) # Display the score

                screen.blit (flat, (coords_x[FLAT_NUM], coords_y[FLAT_NUM]))                             # Display the new floor of the flat on the screen

                go_down = True                                                                  # Indicate that our building will now be descending

                continue                                                                        # Next iteration
                
            coords_y[FLAT_NUM] += DOWN_MOVE                                                              # If the flat has not yet reached the building, lower it down
        else:
            key_pressed = CheckIvent ()                                                         # If none of the above conditions are true, check what the user is inputting

        if key_pressed  == False:                                                               # If the user hasn't pressed any useful keys, move the flat horizontally
            coords_x[FLAT_NUM]   += xMOVE        

        if coords_x[FLAT_NUM] >= WIDTH - flat_size_x:                                                    # If the flat has reached the edge of the screen, change the direction of movement
            xMOVE = -xMOVE
        elif coords_x[FLAT_NUM] <= 0:
            xMOVE = abs (xMOVE) 

        ScreenPrint (flat, screen_flat_1, screen_flat_2, screen_flat_3, text_surf)

        clock.tick (FPS)                                                                        # Controls the number of FPS (frames per second, the number of screen updates per second)