import pygame, config, sys, random
# from pygame.sprite import _Group

class Level:
    def __init__(self):
        self.name = "level"
        self.score = 0
        
        self.images = {}
        self.sounds = {}

        self.to_blit = []

    def level(self):
        raise Exception("Level is not implemented.")

    def play_level(self):
        self.level()


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.fonts = {}
        self.images = {}
        self.sounds = {}

        self.icon  = pygame.image.load("assets/sprites/player.png")
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Пригоди Шайлушая")
        self.screen = pygame.display.set_mode(config.SIZE)
        self.clock = pygame.time.Clock()

        self.music_on = True

    def play_level(self, level: Level, **kwargs):
        vel = 4
        while True:
            self.clock.tick(60)
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_m:
                        if self.music_on:
                            # pygame.mixer.music.set_volume(0)
                            pygame.mixer.music.pause()
                            self.music_on == False
                        else:
                            # pygame.mixer.music.set_volume(0.2)
                            pygame.mixer.music.play()
                            self.music_on == True

                    if event.key == pygame.K_LEFT and not player_looks_left:
                        player = pygame.transform.flip(player, True, False)
                        player_looks_left == True

                    if event.key == pygame.K_RIGHT and player_looks_left:
                        player = pygame.transform.flip(player, True, False)
                        player_looks_left = False

            # Read controls
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_rect = player_rect.move(-vel, 0)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_rect = player_rect.move(vel, 0)
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player_rect = player_rect.move(0, vel)
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player_rect = player_rect.move(0, -vel)

            # Build the frame
            for sprite in level.to_blit:
                self.screen.blit()
            self.clock.tick()
            pygame.display.flip()


class Entity(pygame.sprite.Sprite):
    def __init__(self, image, img_scale=1, vector=[0, 0], *groups) -> None:
        super().__init__(*groups)
        if type(image) is str:
            self.image = pygame.transform.scale_by(pygame.image.load(image), img_scale)
        else:
            self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = 100
        self.rect.y = 100

        self.true_x = 100.
        self.true_y = 100.

        self.vec = vector
        self.vel = 3
        self.acl = 1
        self.health = 20

        self.projectiles = []

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

        self.true_x = float(x)
        self.true_y = float(y)
        return self

    def random_spawn(self):
        self.true_x = random.randint(0, config.SIZE[0] - self.rect.right)
        self.true_y = random.randint(0, config.SIZE[1] - self.rect.bottom)
        self.rect.x = self.true_x
        self.rect.y = self.true_y
        return self
    
    def random_spawn_outborders(self):
        self.rect.x = random.randint(0, config.SIZE[0] - self.rect.right)
        self.rect.y = random.randint(0, config.SIZE[1] - self.rect.bottom)
        return self
    
    def move_byvec(self, vector):
        try:
            self.true_x += vector[0] / max(abs(vector[0]), abs(vector[1])) * self.vel
            self.true_y += vector[1] / max(abs(vector[0]), abs(vector[1])) * self.vel
            # self.rect = self.rect.move(self.true_x, self.true_y)
            self.rect.x = self.true_x
            self.rect.y = self.true_y
        except ZeroDivisionError:
            pass
        return self

    def moveai(self, to_position):
        try:
            vector = (to_position.x - self.rect.x, to_position.y - self.rect.y)
        except AttributeError:
            vector = (to_position[0] - self.rect.x, to_position[1] - self.rect.y)

        return self.move_byvec(vector=vector)


class Player(Entity):
    def __init__(self, image_path, *groups) -> None:
        super().__init__(image_path, *groups)
        self.image = pygame.transform.scale_by(self.image, 0.1)

        self.can_shoot = False
        self.shoot_cooldown = 0
        self.can_sprint = False
        self.on_click = None

    
    def input_controls(self, keys):
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT and not player_looks_left:
                    player = pygame.transform.flip(player, True, False)
                    player_looks_left == True

                if event.key == pygame.K_RIGHT and player_looks_left:
                    player = pygame.transform.flip(player, True, False)
                    player_looks_left = False

        # Read controls
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect = self.rect.move(-self.vel, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect = self.rect.move(self.vel, 0)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect = self.rect.move(0, self.vel)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect = self.rect.move(0, -self.vel)

        # Read mouse
        if pygame.mouse.get_pressed()[0]:
            mousepos = pygame.mouse.get_pos()
            bullet = Entity("assets\sprites\snails\snailgold.png", 0.1)
            bullet.vel = 10
            bullet.set_pos(self.rect.x, self.rect.y)

            bullet.vec = [mousepos[0] - self.rect.x, mousepos[1] - self.rect.y]
            self.projectiles.append(bullet)

        if self.projectiles:
            for proj in self.projectiles:
                proj.move_byvec(proj.vec)


# def BaseAI(**kwargs):
#     move = {}
#     vec_x =
#     if abs(kwargs["dest_x"]) > abs(kwargs['dest_y']):
#         move["move": (kwargs["vel"], 0)]


if __name__ == "__main__":
    print("Wrong module buddy")