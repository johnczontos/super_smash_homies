import sys
import pygame

from utils.spritesheet import SpriteSheet
from Player import *


'''
Classes
'''

# Platform

# Player






def _load_sprite_sheet():
    """Builds the overall set:
    - Loads images from the sprite sheet.
    - Creates a Piece object, and sets appropriate attributes
      for that piece.
    - Adds each piece to the list self.pieces.
    """
    filename = 'stages/fd_sprite_board.png'
    piece_ss = SpriteSheet(filename)

    # Load all stage images.
    return piece_ss.load_grid_images(20, 24)

class Stage(pygame.sprite.Sprite):
    def __init__(self, filename):
        super(Stage, self).__init__()
        self.images = []
        self.counter = 0
        self.sheet = SpriteSheet(filename).load_grid_images(20, 24)
        for image in self.sheet:
            self.images.append(image)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(0, 0, 960, 540)

    def update(self):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''
        self.counter += 1
        if self.counter % 50 == 0:
            self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

def main():
    pygame.init()
    screen = pygame.display.set_mode((960, 540))

    pygame.display.set_caption("Super Smash Homies")

    stage = Stage('stages/fd_sprite_board.png')
    stage_animation = pygame.sprite.Group(stage)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            

        # Calling the 'my_group.update' function calls the 'update' function of all 
        # its member sprites. Calling the 'my_group.draw' function uses the 'image'
        # and 'rect' attributes of its member sprites to draw the sprite.
        stage_animation.update()
        stage_animation.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()