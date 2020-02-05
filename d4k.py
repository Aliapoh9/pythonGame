# Chinnakrit M. 61090006 Python Final Project

import pygame
import os
import abc
import random


class Character(abc.ABC):

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.hitbox = None
        self.hitboxRect = None
        self.hurtbox = None
        self.hurtboxRect = None
        self.idle_frames = []   # Can be put in a dict or 2D list.
        self.idleL_frames = []
        self.attacking_frames = []
        self.attackingL_frames = []
        self.run_frames = []
        self.runL_frames = []
        self.jumping_frames = []
        self.jumpingL_frames = []
        self.hurt_frames = []
        self.hurtL_frames = []
        self.die_frames = []
        self.dieL_frames = []
        self.idle = 1
        self.attacking = 0
        self.currentFrames = 0
        self.hurt = 0
        self.die = 0
        self.jumping = 0
        self.name = ""
        self.level = 1
        self.poise = 0

        self.health = 100

    def update_anim(self):

        if self.is_alive():
            self.check_valid_anim()
            self.update_hitboxes()

            if self.idle == 1:
                self.currentFrames += 1
                self.heading = "right"

                if self.currentFrames == len(self.idle_frames):
                    self.currentFrames = 0

                self.image = self.idle_frames[self.currentFrames]

            elif self.idle == 2:  # IDLE LEFT
                self.currentFrames += 1
                self.heading = "left"
                if self.currentFrames == len(self.idleL_frames):
                    self.currentFrames = 0

                self.image = self.idleL_frames[self.currentFrames]

            elif self.attacking == 1:
                self.image = self.attacking_frames[self.currentFrames]
                self.currentFrames += 1
                if self.currentFrames == len(self.attacking_frames):
                    self.currentFrames = 0
                    self.attacking = 0
                    self.idle = 1

            elif self.attacking == 2:  # attacking Left
                self.image = self.attackingL_frames[self.currentFrames]
                self.currentFrames += 1
                if self.currentFrames == len(self.attackingL_frames):
                    self.currentFrames = 0
                    self.attacking = 0
                    self.idle = 2

            elif self.run == 1:   # Run right
                self.currentFrames += 1
                self.heading = "right"
                if self.currentFrames == len(self.run_frames):
                    self.currentFrames = 0
                    self.idle = 1

                self.image = self.run_frames[self.currentFrames]

            elif self.run == 2:   # Run left
                self.currentFrames += 1
                self.heading = "left"
                if self.currentFrames == len(self.runL_frames):
                    self.currentFrames = 0
                    self.idle = 2

                self.image = self.runL_frames[self.currentFrames]

            elif self.jumping == 1:
                self.currentFrames += 1
                if self.currentFrames == len(self.jumping_frames):
                    self.currentFrames = 0
                    self.idle = 1

                self.image = self.jumping_frames[self.currentFrames]

            elif self.jumping == 2: # Jumping Left
                self.currentFrames += 1
                if self.currentFrames == len(self.jumpingL_frames):
                    self.currentFrames = 0
                    self.idle = 2

                self.image = self.jumpingL_frames[self.currentFrames]

            elif self.hurt == 1:
                self.currentFrames += 1
                if self.currentFrames >= len(self.hurt_frames):
                    self.currentFrames = 0
                    self.idle = 1
                    self.hurt = 0

                self.image = self.hurt_frames[self.currentFrames]

            elif self.hurt == 2:
                self.currentFrames += 1
                if self.currentFrames >= len(self.hurtL_frames):
                    self.currentFrames = 0
                    self.idle = 2
                    self.hurt = 0

                self.image = self.hurtL_frames[self.currentFrames]
        else:

            self.animation_kill()
            self.health = 0
            if self.currentFrames >= len(self.die_frames):
                self.currentFrames = 0

            if self.heading == "right":
                self.die = 1
                self.currentFrames += 1
                if self.currentFrames >= len(self.die_frames):
                    self.currentFrames -= 1
                    self.die = 3

                self.image = self.die_frames[self.currentFrames]
            else:
                self.die = 2
                self.currentFrames += 1
                if self.currentFrames >= len(self.dieL_frames):
                    self.currentFrames -= 1
                    self.die = 3

                self.image = self.dieL_frames[self.currentFrames]

    def check_valid_anim(self):

        if self.idle and self.attacking:
            self.attacking = 0
        if self.attacking and self.hurt or self.jumping and self.hurt:
            self.hurt = 0
        if not self.idle and not self.attacking and not self.run and not self.jumping and not self.hurt:
            self.currentFrames = 0
            self.idle = 1

    def draw_hitbox(self):
        pygame.draw.rect(self.image, (255, 0, 0), self.hitbox, 1)

    def draw_hurtbox(self):
        pygame.draw.rect(self.image, (255, 0, 0), ((10, 0), self.hurtbox), 1)

    def take_damage(self, kb, damage):
        self.idle = 0
        self.run = 0

        if not self.poise:

            if self.heading == "right" or self.idle == 1:
                self.hurt = 1
            elif self.heading == "left" or self.idle == 2:
                self.hurt = 2


            if kb == 1 and self.x < 500:
                self.x += damage * 1.25
            elif kb == 2 and self.x > -20:
                self.x -= damage * 1.25
            self.health -= damage


        if self.invul == 1:
            self.invulTime = 18

        else:

            self.health -= damage

    def animation_kill(self):

        self.idle = 0
        self.attacking = 0
        self.run = 0
        self.jumping = 0
        self.hurt = 0

    def is_alive(self):

        if self.health > 0:
            return True
        else:
            return False

    @abc.abstractmethod
    def load_sprites(self):
        pass

    @abc.abstractmethod
    def update_hitboxes(self):
        self.hurtboxRect = ((self.x, self.y), self.hurtbox)

        self.hitboxRect = ((self.x + 45, self.y + 20), self.actual_hitbox)


class Player(Character):

    def __init__(self, x, y, w = 150, h = 111):
        super(Player, self).__init__(x, y, w, h)

        self.hitbox = (45, 20, self.width - 90, self.height - 20)

        self.actual_hitbox = (self.width - 90, self.height - 20)

        self.hurtbox = (self.width - 15, self.height)

        self.load_sprites()

        self.image = self.idle_frames[0]
        self.idle = 1
        self.heading = "right"
        self.attacking = 0
        self.run = 0
        self.jumping = 0
        self.damage = 10
        self.invul = 1
        self.invulTime = 18

        self.attackDelay = 0
        self.jumpCount = 10
        self.stamina = 100
        self.staminaRegen = 2
        self.healthRegen = 0
        self.exp = 0
        self.expToUp = 100
        self.maxHP = 100
        self.maxStam = 100
        self.score = 0


    def update_hitboxes(self):
        self.hurtboxRect = ((self.x + 10, self.y), self.hurtbox)

        self.hitboxRect = ((self.x + 45, self.y + 20), self.actual_hitbox)

    def load_sprites(self):

        for i in range(4):
            self.idle_frames.append(pygame.image.load(os.path.join("d_assets/player/idle", "player_idle" + str(i) + ".png")).convert_alpha())

        for i in range(4):
            self.idleL_frames.append(pygame.transform.flip(self.idle_frames[i], 1, 0))

        for i in range(14):
            self.attacking_frames.append(pygame.image.load(os.path.join("d_assets/player/attack2", "player_attack" + str(i) + ".png")).convert_alpha())

        for i in range(14):
            self.attackingL_frames.append(pygame.transform.flip(self.attacking_frames[i], 1, 0))

        for i in range(6):
            self.run_frames.append(pygame.image.load(os.path.join("d_assets/player/run", "player_run" + str(i) + ".png")).convert_alpha())

        for i in range(6):
            self.runL_frames.append(pygame.transform.flip(self.run_frames[i], 1, 0))

        for i in range(23):
            self.jumping_frames.append(pygame.image.load(os.path.join("d_assets/player/jump", "player_jump" + str(i) + ".png")).convert_alpha())

        for i in range(23):
            self.jumpingL_frames.append(pygame.transform.flip(self.jumping_frames[i], 1, 0))

        for i in range(3):
            self.hurt_frames.append(pygame.image.load(os.path.join("d_assets/player/hurt", "player_hurt" + str(i) + ".png")).convert_alpha())

        for i in range(3):
            self.hurtL_frames.append(pygame.transform.flip(self.hurt_frames[i], 1, 0))

        for i in range(7):
            self.die_frames.append(pygame.image.load(os.path.join("d_assets/player/die", "player_die" + str(i) + ".png")).convert_alpha())

        for i in range(7):
            self.dieL_frames.append(pygame.transform.flip(self.die_frames[i], 1, 0))


class Slime(Character):

    def __init__(self, x, y, w=32, h=32):
        super().__init__(x, y, w, h)
        self.name = "slime"
        self.health = 80
        self.hitbox = (15, 40, self.width, self.height - 8)

        self.actual_hitbox = (self.width, self.height - 8)
        self.run = 0
        self.jumping = 0
        self.damage = 15
        self.speed = 3
        self.expYield = 40
        self.invul = 0
        self.invulTime = 0

        self.hurtbox = (self.width, self.height - 8)

        self.load_sprites()

        self.image = self.idle_frames[0]

    def draw_hitbox(self):
        pygame.draw.rect(self.image, (255, 0, 0), self.hitbox, 1)

    def draw_hurtbox(self):
        pygame.draw.rect(self.image, (255, 0, 0), ((15, 40), self.hurtbox), 1)


    def update_hitboxes(self):
        self.hurtboxRect = ((self.x + 15, self.y + 40), self.hurtbox)

        self.hitboxRect = ((self.x + 15, self.y + 40), self.actual_hitbox)

    def load_sprites(self):

        for i in range(10):
            self.idleL_frames.append(pygame.image.load(os.path.join("d_assets/slime_green/idle", "slime_g" + str(i) + ".png")).convert_alpha())

        for i in range(10):
            self.idle_frames.append(pygame.transform.flip(self.idleL_frames[i], 1, 0))

        for i in range(10):
            self.hurtL_frames.append(pygame.image.load(os.path.join("d_assets/slime_green/hurt", "slime_green_hurt" + str(i) + ".png")).convert_alpha())

        for i in range(10):
            self.hurt_frames.append(pygame.transform.flip(self.hurtL_frames[i], 1, 0))

        for i in range(9):
            self.dieL_frames.append(pygame.image.load(os.path.join("d_assets/slime_green/die", "die_" + str(i) + ".png")).convert_alpha())

        for i in range(9):
            self.die_frames.append(pygame.transform.flip(self.dieL_frames[i], 1, 0))


    def scale_up(self, level):

        self.health *= 1.2 ** level
        self.damage *= 1.2 ** level
        self.speed += level/10

class Slime_Red(Slime):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 32)
        self.name = "slime_red"
        self.health = 140
        self.damage = 26
        self.speed = 4
        self.expYield = 75

    def load_sprites(self):

        for i in range(10):
            self.idleL_frames.append(pygame.image.load(os.path.join("d_assets/slime_red/idle", "slime_red_idle" + str(i) + ".png")).convert_alpha())

        for i in range(10):
            self.idle_frames.append(pygame.transform.flip(self.idleL_frames[i], 1, 0))

        for i in range(10):
            self.hurtL_frames.append(pygame.image.load(os.path.join("d_assets/slime_red/hurt", "slime_red_hurt" + str(i) + ".png")).convert_alpha())

        for i in range(10):
            self.hurt_frames.append(pygame.transform.flip(self.hurtL_frames[i], 1, 0))

        for i in range(10):
            self.dieL_frames.append(pygame.image.load(os.path.join("d_assets/slime_red/die", "slime_red_die" + str(i) + ".png")).convert_alpha())

        for i in range(10):
            self.die_frames.append(pygame.transform.flip(self.dieL_frames[i], 1, 0))

class Slime_Blue(Slime):

    def __init__(self,x, y):
        super().__init__(x, y, 64, 64)
        self.name = "slime_blue"
        self.health = 250
        self.damage = 40
        self.speed = 5
        self.expYield = 100

        self.hitbox = (35, 83, self.width, self.height - 19)

        self.actual_hitbox = (self.width, self.height - 19)

        self.hurtbox = (self.width, self.height - 19)

    def load_sprites(self):

        for i in range(10):
            self.idleL_frames.append(pygame.image.load(os.path.join("d_assets/slime_blue/idle", "slime_blue_idle" + str(i) + ".png")).convert_alpha())

        for i in range(10):
            self.idle_frames.append(pygame.transform.flip(self.idleL_frames[i], 1, 0))

        for i in range(10):
            self.hurtL_frames.append(pygame.image.load(os.path.join("d_assets/slime_blue/hurt", "slime_blue_hurt" + str(i) + ".png")).convert_alpha())

        for i in range(10):
            self.hurt_frames.append(pygame.transform.flip(self.hurtL_frames[i], 1, 0))

        for i in range(10):
            self.dieL_frames.append(pygame.image.load(os.path.join("d_assets/slime_blue/die", "slime_blue_die" + str(i) + ".png")).convert_alpha())

        for i in range(10):
            self.die_frames.append(pygame.transform.flip(self.dieL_frames[i], 1, 0))

    def draw_hitbox(self):
        pygame.draw.rect(self.image, (255, 0, 0), self.hitbox, 1)

    def draw_hurtbox(self):
        pygame.draw.rect(self.image, (255, 0, 0), ((35, 83), self.hurtbox), 1)


    def update_hitboxes(self):
        self.hurtboxRect = ((self.x + 35, self.y + 83), self.hurtbox)

        self.hitboxRect = ((self.x + 35, self.y + 83), self.actual_hitbox)


class King_Slime(Slime):
    def __init__(self, x, y):
        self.roll_frames = []
        self.rollL_frames = []
        super().__init__(x, y, 256, 256)
        self.name = "king_slime"
        self.health = 1750
        self.damage = 70
        self.expYield = 450

        self.poise = 0

        self.rolling = 0
        self.smashing = 0
        self.attackTimer = 36
        self.attack_delay = 36

        self.hitbox = (150, 350, self.width - 50, self.height - 100)
        self.actual_hitbox = (self.width - 50, self.height - 100)

        self.hurtbox = (self.width - 50, self.height - 100)

        self.image = self.idle_frames[0]

    def draw_hitbox(self):
        pygame.draw.rect(self.image, (255, 0, 0), self.hitbox, 1)

    def draw_hurtbox(self):
        pygame.draw.rect(self.image, (255, 0, 0), ((150, 350), self.hurtbox), 1)

    def update_hitboxes(self):
        self.hurtboxRect = ((self.x + 150, self.y + 350), self.hurtbox)

        self.hitboxRect = ((self.x + 150, self.y + 350), self.actual_hitbox)

    def load_sprites(self):

        for i in range(10):
            self.idleL_frames.append(pygame.image.load(os.path.join("d_assets/king_slime/idle", "king_slime_idle" + str(i) + ".png")).convert_alpha())

        for i in range(10):
            self.idle_frames.append(pygame.transform.flip(self.idleL_frames[i], 1, 0))

        for i in range(10):
            self.hurtL_frames.append(pygame.image.load(os.path.join("d_assets/king_slime/hurt", "king_slime_hurt" + str(i) + ".png")).convert_alpha())

        for i in range(10):
            self.hurt_frames.append(pygame.transform.flip(self.hurtL_frames[i], 1, 0))

        for i in range(10):
            self.dieL_frames.append(pygame.image.load(os.path.join("d_assets/king_slime/die", "king_slime_die" + str(i) + ".png")).convert_alpha())

        for i in range(10):
            self.die_frames.append(pygame.transform.flip(self.dieL_frames[i], 1, 0))

        for i in range(10):
            self.rollL_frames.append(pygame.image.load(os.path.join("d_assets/king_slime/roll_attack", "king_slime_roll_attack" + str(i) + ".png")).convert_alpha())

        for i in range(10):
            self.roll_frames.append(pygame.transform.flip(self.rollL_frames[i], 1, 0))

    def choose_attack(self):

        if self.attackTimer > 0:
            self.attackTimer -= 1
        if self.attack_delay > 0 and not self.rolling and not self.smashing:
            self.attack_delay -= 1

        if self.attack_delay == 30:
            self.poise = 1

        if self.attackTimer == 0:
            self.rolling = 0
            self.smashing = 0
            self.poise = 0

        if not self.rolling and not self.smashing and not self.attackTimer and not self.attack_delay:
            self.idle = 0

            if self.x < 240:
                self.rolling = 1
            else:
                self.rolling = 2

            self.poise = 1
            self.attackTimer = 1000
            self.attack_delay = random.randrange(16, 45)


    def check_valid_anim(self):

        if self.rolling and self.hurt or self.smashing and self.hurt:
            self.hurt = 0
        if not self.idle and not self.rolling and not self.hurt and not self.smashing:
            self.currentFrames = 0
            self.idle = 1

    def update_anim(self):

        if self.is_alive():
            self.check_valid_anim()
            self.update_hitboxes()

            if self.idle == 1:
                self.currentFrames += 1
                self.heading = "right"

                if self.currentFrames == len(self.idle_frames):
                    self.currentFrames = 0

                self.image = self.idle_frames[self.currentFrames]

            elif self.idle == 2:  # IDLE LEFT
                self.currentFrames += 1
                self.heading = "left"
                if self.currentFrames == len(self.idleL_frames):
                    self.currentFrames = 0

                self.image = self.idleL_frames[self.currentFrames]

            elif self.rolling == 1:
                self.image = self.roll_frames[self.currentFrames]
                self.currentFrames += 1
                if self.currentFrames == len(self.roll_frames):
                    self.currentFrames = 0
                    #self.idle = 1

                self.image = self.roll_frames[self.currentFrames]

            elif self.rolling == 2:  # attacking Left
                self.image = self.rollL_frames[self.currentFrames]
                self.currentFrames += 1
                if self.currentFrames == len(self.rollL_frames):
                    self.currentFrames = 0
                    #self.idle = 2

                self.image = self.rollL_frames[self.currentFrames]

            elif self.hurt == 1:
                self.currentFrames += 1
                if self.currentFrames >= len(self.hurt_frames):
                    self.currentFrames = 0
                    self.idle = 1
                    self.hurt = 0

                self.image = self.hurt_frames[self.currentFrames]

            elif self.hurt == 2:
                self.currentFrames += 1
                if self.currentFrames >= len(self.hurtL_frames):
                    self.currentFrames = 0
                    self.idle = 2
                    self.hurt = 0

                self.image = self.hurtL_frames[self.currentFrames]
        else:

            self.animation_kill()
            self.health = 0
            if self.currentFrames >= len(self.die_frames):
                self.currentFrames = 0

            if self.heading == "right":
                self.die = 1
                self.currentFrames += 1
                if self.currentFrames >= len(self.die_frames):
                    self.currentFrames -= 1
                    self.die = 3

                self.image = self.die_frames[self.currentFrames]
            else:
                self.die = 2
                self.currentFrames += 1
                if self.currentFrames >= len(self.dieL_frames):
                    self.currentFrames -= 1
                    self.die = 3

                self.image = self.dieL_frames[self.currentFrames]





class Game(object):

    def __init__(self):
        self._running = 0
        self._display = None
        self.clock = pygame.time.Clock()
        self.creatures = []
        self.rectToRender = []
        self.p1 = None
        self.menu = Menu()
        self.state = self.menu.state
        if self.state == -1:
            exit(1)
        elif self.state == 2:
            self.load_game()
        else:
            self.stage = 0
            self.stageTimer = 18 * 10
        self.timer = 0      # you died screen's timer
        self.stageToBlit = 0
        self.random_stage_done = 0
        self.stageClear = 0
        self.stageBgs = []
        self.spawnDelay = 0
        self.neg = 1
        self.max_enemies = (self.stage + 1) * 3
        self.level = None
        self.levelS = None
        self.levelR = None
        self.gameOver = None
        self.gameOverS = None
        self.gameOverR = None
        self.scoreF = None
        self.scoreS = None
        self.scoreR = None
        self.nextLevelF = None
        self.nextLevelS = None
        self.nextLevelR = None
        self.remainF = None
        self.remainS = None
        self.remainR = None

        self.attackSound = None
        self.levelUpSound = None
        self.hitSound = None

    def load_game(self):

        try:

            with open(os.path.join("d_assets/save/save.txt")) as save_file:

                data = save_file.read().split("\n")
                self.stage = int(data[0][6:])
                self.stageTimer = int(data[8][6:])

        except:

            self.stage = 0
            self.stageTimer = 18 * 10

    def load_player(self):

        try:

            with open(os.path.join("d_assets/save/save.txt")) as save_file:

                data = save_file.read().split("\n")
                self.p1.level = int(data[1][6:])
                self.p1.health = float(data[2][7:])

                self.p1.exp = float(data[3][4:])
                self.p1.expToUp = float(data[4][8:])
                self.p1.maxHP = float(data[5][6:])
                self.p1.maxStam = float(data[6][8:])
                self.p1.x = float(data[7][3:])
                self.p1.score = float(data[9][6:])

        except:

            self.p1.level = 1
            self.p1.health = 100

            self.p1.exp = 0
            self.p1.expToUp = 100
            self.p1.maxHP = 100
            self.p1.maxStam = 100
            self.p1.x = 50
            self.p1.score = 0


    def launch_init(self):
        pygame.init()

        pygame.display.set_caption("Slime slayer")
        self._running = 1
        self._display = pygame.display.set_mode((640, 480))
        self.stageBgs.append(pygame.image.load(os.path.join("d_assets/bg/map0.png")).convert())
        self.stageBgs.append(pygame.image.load(os.path.join("d_assets/bg/map1.png")).convert())
        self.stageBgs.append(pygame.image.load(os.path.join("d_assets/bg/map2.png")).convert())
        self.stageBgs.append(pygame.image.load(os.path.join("d_assets/bg/map3.png")).convert())
        pygame.key.set_repeat(1, 50)
        self.p1 = Player(50, 350)
        if self.state == 2:
            self.load_player()
        # self.e1 = King_Slime(200, -50)
        # self.creatures.append(self.e1)
        self.level = pygame.font.Font(os.path.join("d_assets/font/f1.ttf"), 30)
        self.scoreF = pygame.font.Font(os.path.join("d_assets/font/f1.ttf"), 15)
        self.remainF = pygame.font.Font(os.path.join("d_assets/font/f1.ttf"), 15)
        self.nextLevelF = pygame.font.Font(os.path.join("d_assets/font/f1.ttf"), 30)
        self.gameOver = pygame.font.Font(os.path.join("d_assets/font/f1.ttf"), 100)

        self.attackSound = pygame.mixer.Sound(os.path.join("d_assets/sound/attack.ogg"))
        self.attackSound.set_volume(0.3)

        self.hitSound = pygame.mixer.Sound(os.path.join("d_assets/sound/Slash8-Bit.ogg"))
        self.hitSound.set_volume(0.1)

        self.levelUpSound = pygame.mixer.Sound(os.path.join("d_assets/sound/level_up.ogg"))
        self.levelUpSound.set_volume(0.3)

        self.on_running()

    def get_keyboard_input(self):

        button = pygame.key.get_pressed()

        if self.p1.attacking == 0 and not self.p1.die and not self.p1.hurt:

            if button[pygame.K_d] and self.p1.x < 540:
                if self.p1.jumping:
                    self.p1.jumping = 1
                    self.p1.heading = "right"
                    self.p1.x += 11
                else:
                    self.p1.idle = 0
                    self.p1.attacking = 0
                    self.p1.run = 1
                    self.p1.x += 11
            if button[pygame.K_a] and self.p1.x > -40:
                if self.p1.jumping:
                    self.p1.jumping = 2
                    self.p1.heading = "left"
                    self.p1.x -= 11
                else:
                    self.p1.idle = 0
                    self.p1.attacking = 0
                    self.p1.run = 2
                    self.p1.x -= 11
            if button[pygame.K_k] and self.p1.heading == "right" and self.p1.stamina >= 30:
                self.p1.idle = 0
                self.p1.currentFrames = 0
                self.p1.attacking = 1
                self.p1.stamina -= 30
                self.attackSound.play(1)

            if button[pygame.K_k] and self.p1.heading == "left" and self.p1.stamina >= 30:
                self.p1.idle = 0
                self.p1.currentFrames = 0
                self.p1.attacking = 2
                self.p1.stamina -= 30
                self.attackSound.play(1)

            if button[pygame.K_w] and self.p1.jumping == 0 and self.p1.stamina >= 15:
                if self.p1.heading == "right":
                    self.p1.jumping = 1
                    self.p1.run = 0
                    self.p1.idle = 0
                else:
                    self.p1.jumping = 2
                    self.p1.idle = 0
                    self.p1.run = 0
                self.p1.stamina -= 15

    def check_hit(self, attacker, target):

        if target.is_alive() and target.invulTime == 0:

            aHurtBox = pygame.Rect(attacker.hurtboxRect)
            tHitBox = pygame.Rect(target.hitboxRect)

            # print(aHurtBox)
            # print(tHitBox)
            # print("Hurtbox x:{} y:{} spanx:{} spany:{}".format(attacker.x, attacker.y, attacker.x + attacker.width, attacker.y + attacker.height))

            if aHurtBox.colliderect(tHitBox):
                #print(self.hitSound.get_num_channels(), len(self.creatures))
                self.hitSound.play()
                #print("HIT!")
                if tHitBox.x >= aHurtBox.x + aHurtBox.w / 2:
                    target.take_damage(1, attacker.damage)
                else:
                    target.take_damage(2, attacker.damage)

    def random_spawn(self):

        if self.stage % 3 != 0 or self.stage == 0:  # if not a boss stage

            spawn = random.randrange(101)

            if self.stage > 3:

                if 0 <= spawn <= 20 and self.stage > 1:
                    x = Slime_Blue(random.randrange(0, 640), -100)
                    x.scale_up(self.stage - 3)
                    self.creatures.append(x)
                elif 20 < spawn <= 50 and self.stage > 0:
                    x = Slime_Red(random.randrange(0, 640), -100)
                    x.scale_up(self.stage - 3)
                    self.creatures.append(x)
                else:
                    x = Slime(random.randrange(0, 640), -100)
                    x.scale_up(self.stage - 3)
                    self.creatures.append(x)

            else:

                if 0 <= spawn <= 20 and self.stage > 1:
                    self.creatures.append(Slime_Blue(random.randrange(0, 640), -100))
                elif 20 < spawn <= 50 and self.stage > 0:
                    self.creatures.append(Slime_Red(random.randrange(0, 640), -100))
                else:
                    self.creatures.append(Slime(random.randrange(0, 640), -100))

        else:
            self.max_enemies = 1
            x = King_Slime(250, -50)
            x.scale_up(self.stage - 3)
            self.creatures.append(x)

    def draw_player_status(self):

        pygame.draw.circle(self._display, (150, 0, 0), (24, 45), 20)
        pygame.draw.circle(self._display, (120, 0, 0), (0, 0), 100, 5)

        pygame.draw.rect(self._display, (100, 0, 0), (50, 20, self.p1.maxHP, 15))
        pygame.draw.rect(self._display, (230, 0, 0), (50, 20, self.p1.health, 15))
        pygame.draw.rect(self._display, (0, 100, 0), (50, 45, self.p1.maxStam, 15))
        pygame.draw.rect(self._display, (0, 230, 0), (50, 45, self.p1.stamina, 15))

        pygame.draw.rect(self._display, (100, 100, 100), (50, 70, 100, 7))

        if self.p1.exp <= self.p1.expToUp:
            pygame.draw.rect(self._display, (230, 230, 230), (50, 70, self.p1.exp / self.p1.expToUp * 100, 7))

    def draw_boss_status(self, boss):

        pygame.draw.rect(self._display, (200, 200, 0), (30, 460, boss.health * 0.1, 15))

    def level_up(self):

        self.p1.level += 1
        self.levelUpSound.play()
        self.p1.maxHP += 10
        self.p1.maxStam += 5
        self.p1.damage += 2
        self.p1.staminaRegen += 0.2
        self.p1.healthRegen += 0.03
        self.p1.score += int(self.p1.exp * 1.05)
        self.p1.exp = self.p1.exp - self.p1.expToUp
        self.p1.expToUp += self.p1.level * 1.25

    def change_stage(self):
        self.stage += 1
        self.stageClear = 0
        self.stageTimer = 18 * 10
        self.p1.x = -30
        self.max_enemies = (self.stage + 1) * 3
        self.random_stage_done = 0

    def random_stage(self):

        return random.randrange(4)

    def increment_timer(self):

        if self.spawnDelay > 0:
            self.spawnDelay -= 1

        if self.stageTimer > 0:
            self.stageTimer -= 1

        if self.p1.invulTime > 0:
            self.p1.invulTime -= 1

    def clear_save(self):

        file = open(os.path.join("d_assets/save/save.txt"), 'w')

        file.close()

    def save_game(self):

        with open(os.path.join("d_assets/save/save.txt"), 'w') as save_file:

            save_file.write("stage={}\nlevel={}\nhealth={}\nexp={}\nexpToUp={}\nmaxHp={}\nmaxStam={}\n".format(self.stage,
                                                                                       self.p1.level, self.p1.health,
                                                                                       self.p1.exp,
                                                                                       self.p1.expToUp,
                                                                                       self.p1.maxHP,
                                                                                       self.p1.maxStam))

            save_file.write("px={}\nsTime={}\nscore={}".format(self.p1.x, self.stageTimer, self.p1.score))

    def event(self, e):
        if e.type == pygame.QUIT:
            self._running = 0
            if self.timer == 0:
                self.save_game()

        self.get_keyboard_input()

    def on_loop(self):

        self.clock.tick(18) # Set FPS

        #print(self.p1.attacking, self.p1.hurt)

        if self.stageClear and self.p1.x >= 530:
            self.change_stage()

        if self.p1.stamina < self.p1.maxStam and not self.p1.attacking and not self.p1.jumping and not self.p1.die:
            self.p1.stamina += self.p1.staminaRegen
        if self.p1.health < self.p1.maxHP and not self.p1.die and not self.stageClear:
            self.p1.health += self.p1.healthRegen

        self.p1.update_anim()
        self.increment_timer()

        if self.p1.exp >= self.p1.expToUp:
            self.level_up()

        if self.stageTimer != 0 and len(self.creatures) < self.max_enemies and self.spawnDelay == 0:

            self.random_spawn()
            self.spawnDelay = 20

        for creature in self.creatures:

            if creature.die != 3:
                creature.update_anim()
                self.check_hit(creature, self.p1)
                if creature.name != "king_slime": # Other slime actions

                    if creature.x > self.p1.x: #LEFT
                        creature.x -= creature.speed
                        creature.idle = 2
                    elif creature.x < self.p1.x:
                        creature.x += creature.speed
                        creature.idle = 1

                    if creature.name == "slime" or creature.name == "slime_red":
                        if creature.y < 398:
                            creature.y += 10
                    if creature.name == "slime_blue":
                        if creature.y < 330:
                            creature.y += 10
                else:   # Slime King actions
                    creature.choose_attack()
                    #print(creature.x, creature.x + creature.width)

                    if creature.x < -160:
                        creature.attackTimer = 0
                        creature.x = -160

                    if creature.x > 270:
                        creature.attackTimer = 0
                        creature.x = 270

                    if creature.rolling == 1:
                        creature.x += 20
                    elif creature.rolling == 2:
                        creature.x -= 20

                    if creature.x + creature.width > self.p1.x:  # LEFT
                        creature.heading = "left"
                    elif creature.x < self.p1.x:
                        creature.heading = "right"

                    pass

            else:

                if creature.name != "king_slime":
                    self.p1.score += creature.expYield
                    self.p1.exp += creature.expYield
                    self.creatures.remove(creature)
                    del creature
                    continue
                else:
                    self.stageTimer = 0
                    self.p1.score += creature.expYield
                    self.p1.exp += creature.expYield
                    self.creatures.remove(creature)
                    del creature
                    continue

            if self.p1.attacking:
                self.check_hit(self.p1, creature)


        if self.p1.jumping:
            if self.p1.jumpCount >= -10:
                self.neg = 1
                if self.p1.jumpCount < 0:
                    self.neg -= 2
                self.p1.y -= (self.p1.jumpCount ** 2) * 0.5 * self.neg
                self.p1.jumpCount -= 1
            else:
                if self.p1.attacking:
                    self.p1.jumping = 0
                    self.p1.jumpCount = 10
                else:
                    self.p1.jumping = 0
                    self.p1.currentFrames = 0
                    self.p1.jumpCount = 10

        if self.p1.die == 3 and self.p1.y < 350:
            self.p1.y += 10


    def render(self):

        if self.p1.die != 3 or self.p1.y < 350:

            self.levelS = self.level.render("{}".format(self.p1.level), True, (255, 255, 255))
            self.levelR = self.levelS.get_rect()
            self.levelR.center = (25, 50)

           # self.p1.draw_hitbox()

            #if self.p1.attacking:
                #self.p1.draw_hurtbox()

            if self.stage >= len(self.stageBgs) and not self.random_stage_done:
                self.stageToBlit = self.random_stage()
                print(self.stage, self.stageToBlit)
                self.random_stage_done = 1
            elif self.stage < len(self.stageBgs):
                self.stageToBlit = self.stage
            self.rectToRender.append(self._display.blit(self.stageBgs[self.stageToBlit], (0, 0)))

            self.rectToRender.append(self._display.blit(self.p1.image, (self.p1.x, self.p1.y)))

            for creature in self.creatures:
                if creature.name == "king_slime":
                    self.draw_boss_status(creature)
                #creature.draw_hitbox()
                #creature.draw_hurtbox()
                self.rectToRender.append(self._display.blit(creature.image, (creature.x, creature.y)))

            self.draw_player_status()
            self.rectToRender.append(self._display.blit(self.levelS, self.levelR))

            if len(self.creatures) > 0 and self.stageTimer == 0:
                self.remainS = self.remainF.render("Eliminate all remaining enemies to continue!", True, (200, 0, 0))
                self.remainR = self.remainS.get_rect()
                self.remainR.center = (400, 60)
                self.rectToRender.append(self._display.blit(self.remainS, self.remainR))

            elif self.stageTimer == 0:
                self.nextLevelS = self.nextLevelF.render("Stage complete!", True, (200, 0, 0))
                self.nextLevelR = self.nextLevelS.get_rect()
                self.nextLevelR.center = (400, 60)
                self.rectToRender.append(self._display.blit(self.nextLevelS, self.nextLevelR))
                self.stageClear = 1

        else:
            self.timer += 1
            pygame.draw.rect(self._display, (0, 0, 0), (0, 0, 700, 600))
            self.rectToRender.clear()
            self.gameOverS = self.gameOver.render("YOU DIED", True, (230, 0, 0))
            self.gameOverR = self.gameOverS.get_rect()
            self.gameOverR.center = (330, 250)
            self.scoreS = self.scoreF.render("your score: {}".format(self.p1.score), True, (255, 255, 255))
            self.scoreR = self.gameOverS.get_rect()
            self.scoreR.center = (500, 400)
            self.rectToRender.append(self._display.blit(self.gameOverS, self.gameOverR))
            self.rectToRender.append(self._display.blit(self.scoreS, self.scoreR))

            if self.timer >= 50:
                self.clear_save()
                self._running = 0

        pygame.display.update(self.rectToRender)

    def on_running(self):

        while self._running:

            for e in pygame.event.get():
                self.event(e)
            self.on_loop()
            self.render()

        pygame.quit()


class Menu(Game):

    # todo Move menu into Game Class

    def __init__(self):
        self._running = 1
        self.state = 0
        self.mouse = None
        self._display = None
        self.mouseBtn = None
        self.mainFont = None
        self.mainMenuBg = None
        self.titleFont = None
        self.startBtnSurface = None
        self.startBtnRect = None
        self.titleS = None
        self.titleR = None
        self.contS = None
        self.contR = None
        self.start()


    def start(self):
        pygame.init()
        self._display = pygame.display.set_mode((640, 480))
        self.mainFont = pygame.font.Font(os.path.join("d_assets/font/f1.ttf"), 33)
        self.titleFont = pygame.font.Font(os.path.join("d_assets/font/f1.ttf"), 50)
        self.howToFont = pygame.font.Font(os.path.join("d_assets/font/f1.ttf"), 15)
        self.startBtnSurface = self.mainFont.render("Start", True, (0, 0, 0))
        self.startBtnRect = self.startBtnSurface.get_rect()
        self.titleS = self.titleFont.render("Slime slayer", True, (0, 0, 0))
        self.titleR = self.titleS.get_rect()
        self.contS = self.mainFont.render("Continue", True, (0, 0, 0))
        self.contR = self.contS.get_rect()
        self.howToS = self.howToFont.render("WASD to control, K to attack.", True, (255, 255 ,255))
        self.howToR = self.howToS.get_rect()

        self.mainMenuBg = pygame.image.load(os.path.join("d_assets/bg/parallax-mountain.png")).convert()
        self.titleR.center = (330, 100)
        self.startBtnRect.center = (330, 180)
        self.contR.center = (330, 330)
        self.howToR.center = (330, 400)

        pygame.display.set_caption("slime_slayer")
        self.on_running()

    def event(self, e):
        if e.type == pygame.QUIT:
            self._running = 0
            self.state = -1

    def on_loop(self):

        self.mouse = pygame.mouse.get_pos()
        self.mouseBtn = pygame.mouse.get_pressed()

        pass

    def render(self):
        self._display.blit(self.mainMenuBg, (0, 0))
        if 180 + 300 > self.mouse[0] > 180 and 150 + 50 > self.mouse[1] > 150:  # Start of New
            pygame.draw.rect(self._display, (255, 0, 0), (180, 150, 300, 50))
            pygame.draw.rect(self._display, (0, 150, 0), (180, 300, 300, 50))  # Continue Btn
            if self.mouseBtn[0] == 1:
                print("NEW GAME START!")
                self.state = 1
                self._running = 0

        elif 180 + 300 > self.mouse[0] > 180 and 300 + 50 > self.mouse[1] > 300: # Start of Cont btn.
            pygame.draw.rect(self._display, (0, 255, 0), (180, 300, 300, 50))
            pygame.draw.rect(self._display, (150, 0, 0), (180, 150, 300, 50))  # Start Button
            if self.mouseBtn[0] == 1:
                print("GAME CONTINUE!")
                self.state = 2
                self._running = 0
        else:
            pygame.draw.rect(self._display, (150, 0, 0), (180, 150, 300, 50))
            pygame.draw.rect(self._display, (0, 150, 0), (180, 300, 300, 50))

        self._display.blit(self.contS, self.contR)
        self._display.blit(self.titleS, self.titleR)
        self._display.blit(self.startBtnSurface, self.startBtnRect)
        self._display.blit(self.howToS, self.howToR)
        pygame.display.flip()


Game().launch_init()


