import pygame
from pygame.locals import *
import sys
import random

# Global variable for game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))  # initialising display for game
GROUND_Y = SCREENHEIGHT * 0.8
GAME_SPRITES = {}  # this is use to store images
GAME_SOUNDS = {}  # this is use to store sound
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'


def welcome_screen():
    """
    It will use to show images on initial screen
    """
    # player_position_at_x = int(SCREENWIDTH/5)
    # player_position_at_y = int(SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2  # (H-h)/2
    message_screen_at_x = int(SCREENWIDTH - GAME_SPRITES['message'].get_height())/2+40
    # 40 is offset value which I have set after running game
    message_screen_at_y = int(SCREENHEIGHT * 0.25)
    base_at_x = 0

    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # If the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                # SCREEN.blit(GAME_SPRITES['player'], (player_position_at_x, player_position_at_y))
                SCREEN.blit(GAME_SPRITES['message'], (message_screen_at_x, message_screen_at_y))
                SCREEN.blit(GAME_SPRITES['base'], (base_at_x, GROUND_Y))
                pygame.display.update()
                FPS_CLOCK.tick(FPS)


def start_game():
    score = 0
    player_position_at_x = int(SCREENWIDTH/5)
    player_position_at_y = int(SCREENHEIGHT/2)
    base_position_at_x = 0

    new_pipe1 = random_pipe()
    new_pipe2 = random_pipe()

    upper_pipes = [
        {'x': SCREENWIDTH+200, 'y': new_pipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': new_pipe1[0]['y']}
    ]
    lower_pipes = [
        {'x': SCREENWIDTH+200, 'y': new_pipe2[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': new_pipe2[1]['y']}
    ]
    pipe_velocity_at_x = -4
    player_velocity_y = -9
    player__max_velocity_y = 10
    player_min_velocity_y = -8
    player_acceleration_y = -1
    player_flap_velocity = -8
    is_player_flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_LEFT):
                if player_position_at_y > 0:
                    player_velocity_y = player_flap_velocity
                    is_player_flapped = True
                    GAME_SOUNDS['wing'].play()

        crash_test = is_collide(player_position_at_x, player_position_at_y, upper_pipes, lower_pipes)
        if crash_test:
            return
        # check for score
        player_mid_position = player_position_at_x + GAME_SPRITES['player'].get_width()/2
        for pipe in upper_pipes:
            pipe_mid_pos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipe_mid_pos <= player_mid_position <pipe_mid_pos + 4:
                score += 1
                print(f'your score is {score}')
                GAME_SOUNDS['point'].play()

        if player_velocity_y < player__max_velocity_y and not is_player_flapped:
            player_velocity_y += player_acceleration_y

        if is_player_flapped:
            is_player_flapped = False

        player_height = GAME_SPRITES['player'].get_height()
        player_position_at_y = player_position_at_y + min(player_velocity_y, GROUND_Y - player_position_at_y - player_height)

        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            upper_pipe['x'] += pipe_velocity_at_x
            lower_pipe['x'] += pipe_velocity_at_x
        # adding new pipe
        if 0 < upper_pipes[0]['x'] < 5:
            new_pipe = random_pipe()
            upper_pipes.append(new_pipe[0])
            lower_pipes.append(new_pipe[1])


        # Removing pipe when they are out of display
        if upper_pipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upper_pipe['x'], upper_pipe['x']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lower_pipe['x'], lower_pipe['x']))

        SCREEN.blit(GAME_SPRITES['base'], (base_position_at_x, GROUND_Y))
        SCREEN.blit(GAME_SPRITES['player'], (player_position_at_x, player_position_at_y))
        my_digits = [int(x) for x in list(str(score))]
        width = 0
        for digit in my_digits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        x_offset = (SCREENWIDTH - width)/2
        for digit in my_digits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (x_offset, SCREENWIDTH * 0.12))
            x_offset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def is_collide(player_position_at_x, player_position_at_y, upper_pipes, lower_pipes):
    return False


def random_pipe():
    """
    Generate random position of pipe for upper and lower one's
    """
    pipe_height = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    position_for_lower_pipe_at_y = random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipe_x = SCREENWIDTH * 10
    position_for_upper_pipe_at_y = pipe_height - position_for_lower_pipe_at_y + offset
    pipe = [
        {'x': pipe_x, 'y': position_for_upper_pipe_at_y},
        {'x': pipe_x, 'y': position_for_lower_pipe_at_y}
    ]
    return pipe

if __name__ == '__main__':
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird design by Rahul')
    # adding number into sprites to blit score on screen
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )
    # adding message image in sprite to blit on screen
    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )
    # loading sound in dictionary
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    while True:
        welcome_screen()
        start_game()


