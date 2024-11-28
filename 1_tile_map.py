import pygame

vector = pygame.math.Vector2

# Initialize Pygame
pygame.init()

# Set up display
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tile Map")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, grass_tiles, water_tiles):
        super().__init__()

        self.move_right_sprites = []
        self.move_left_sprites = []
        self.idle_right_sprites = []
        self.idle_left_sprites = []

        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (1).png"), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (2).png"), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (3).png"), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (4).png"), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (5).png"), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (6).png"), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (7).png"), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("boy/Run (8).png"), (64, 64)))

        self.current_sprite = 0
        self.image = self.move_right_sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        self.starting_x = x
        self.starting_y = y

        self.grass_tiles = grass_tiles
        self.water_tiles = water_tiles

        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

        self.HORIZONTAL_ACCELERATION = 1.5
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCELERATION = 0.5
        self.VERTICAL_JUMP_SPEED = 15

    def update(self):
        self.move()
        self.check_collisions()

    def move(self):
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
        elif keys[pygame.K_RIGHT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right_sprites, .2)

        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        if self.position.x > WINDOW_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WINDOW_WIDTH

        self.rect.bottomleft = self.position

    def check_collisions(self):
        collided_platforms = pygame.sprite.spritecollide(self, self.grass_tiles, False)

        if collided_platforms:
            if self.velocity.y > 0:
                self.position.y = collided_platforms[0].rect.top
                self.velocity.y = 0

        if pygame.sprite.spritecollide(self, self.water_tiles, False):
            self.position = vector(self.starting_x, self.starting_y)
            self.velocity = vector(0, 0)

    def jump(self):
        if pygame.sprite.spritecollide(self, self.grass_tiles, False):
            self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]


main_tile_group = pygame.sprite.Group()
grass_tile_group = pygame.sprite.Group()
water_tile_group = pygame.sprite.Group()
my_player_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image_int, main_group, sub_group=""):
        super().__init__()
        if image_int == 1:
            self.image = pygame.image.load("dirt.png")
        elif image_int == 2:
            self.image = pygame.image.load("grass.png")
            sub_group.add(self)
        elif image_int == 3:
            self.image = pygame.image.load("water.png")
            sub_group.add(self)

        main_group.add(self)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


tile_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1]
]

for row in range(len(tile_map)):
    for col in range(len(tile_map[row])):
        x = col * 32
        y = row * 32
        if tile_map[row][col] == 1:
            Tile(x, y, 1, main_tile_group)
        elif tile_map[row][col] == 2:
            Tile(x, y, 2, main_tile_group, grass_tile_group)
        elif tile_map[row][col] == 3:
            Tile(x, y, 3, main_tile_group, water_tile_group)
        elif tile_map[row][col] == 4:
            my_player = Player(x, y + 32, grass_tile_group, water_tile_group)
            my_player_group.add(my_player)

background_image = pygame.image.load("background.png")
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

# main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.jump()

    # Blit background
    display_surface.blit(background_image, background_rect)

    main_tile_group.draw(display_surface)

    my_player_group.update()
    my_player_group.draw(display_surface)

    # Update
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
