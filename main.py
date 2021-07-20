import sys
import os
import pygame

from utils.spritesheet import SpriteSheet

BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)

worldx = 960
worldy = 540
fps = 40
ani = 4

'''
Classes
'''

# x location, y location, img width, img height, img file
class Platform(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', img)).convert()
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc

# Player
class Player(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.health = 10
        self.images = []
        for i in range(1, 5):
            img = pygame.image.load(os.path.join('images', 'mario.png')).convert_alpha()
            img.convert_alpha()
            img.set_colorkey(ALPHA)
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()
            self.rect.x = worldx / 2

    def gravity(self):
        self.movey += 1.2
        if self.rect.y > 275 and self.movey >= 0:
            self.movey = 0
            self.rect.y = 275
            # self.rect.y = worldy-ty-ty

    def jump(self, h):
        self.movey = h

    def control(self, x, y):
        """
        control player movement
        """
        self.movex += x
        self.movey += y

    def update(self):
        """
        Update sprite position
        """

        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

        # moving left
        if self.movex < 0:
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[self.frame // ani], True, False)

        # moving right
        if self.movex > 0:
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0
            self.image = self.images[self.frame // ani]

        # hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        # for enemy in hit_list:
        #     self.health -= 1
        #     print(self.health)
    





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
        self.rect = pygame.Rect(0, 0, worldx, worldy)

    def update(self):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''
        self.counter += 1
        if self.counter % 5 == 0:
            self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]


gloc = []
tx = 64
ty = 64

def main():
    pygame.init()
    screen = pygame.display.set_mode((worldx, worldy))

    pygame.display.set_caption("Super Smash Homies")

    stage = Stage('stages/fd_sprite_board.png')
    stage_animation = pygame.sprite.Group(stage)

    clock = pygame.time.Clock()

    plat = Platform(148, 340, 'platform.png')
    plat_list = pygame.sprite.Group()
    plat_list.add(plat)

    player = Player()
    player_list = pygame.sprite.Group()
    player_list.add(player)
    steps = 7.5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == ord('w'):
                    print('jump')
                    player.jump(-19)
                if event.key == ord('a'):
                    print('left')
                    player.control(-steps, 0)
                if event.key == ord('s'):
                    print('down')
                if event.key == ord('d'):
                    print('right')
                    player.control(steps, 0)
            if event.type == pygame.KEYUP:
                if event.key == ord('a'):
                    player.control(steps, 0)
                if event.key == ord('d'):
                    player.control(-steps, 0)


        # Calling the 'my_group.update' function calls the 'update' function of all 
        # its member sprites. Calling the 'my_group.draw' function uses the 'image'
        # and 'rect' attributes of its member sprites to draw the sprite.
        stage_animation.update()
        stage_animation.draw(screen)

        player.gravity()
        player.update()

        plat_list.draw(screen)
        player_list.draw(screen)
        
        pygame.display.flip()
        clock.tick(fps)

if __name__ == '__main__':
    main()