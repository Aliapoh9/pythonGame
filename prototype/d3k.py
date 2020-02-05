import pygame, os


class Game(object):

    def __init__(self):
        self._running = True
        self._display = None
        self.size = self.width, self.height = 640, 480
        self.clock = pygame.time.Clock()

        self.idleFrames = []
        self.attackFrames = []

    def on_init(self):
        pygame.init()
        pygame.key.set_repeat(10, 30)
        self._display = pygame.display.set_mode(self.size)
        self._running = True

        for i in range(45):
            self.idleFrames.append(pygame.image.load(os.path.join("assets/player_idle", "idle_"+str(i)+".png")))

        for i in range(16):
            self.attackFrames.append(pygame.image.load(os.path.join("assets/player_attack", "attack_"+str(i)+".png")))


        self.idle = repeatedAnimation(self.idleFrames)
        self.attack = SimpleAnimation(self.attackFrames)
        self.idle.play()


        # creating balls for collision test.
        self.b1 = Ball((230, 0, 0), [10, 0])
        self.b2 = Ball((0, 230, 0), [10, 0])
        self.b2.relocate((100, 0))


    def on_event(self, event):

        if event.type == pygame.QUIT:
            self._running = False

        # Accepting input
        if event.type == pygame.KEYDOWN:
            """ # Movement
            if event.key == pygame.K_d:
                self.b1.xSpeed = 10
                self.b1.ySpeed = 0
            elif event.key == pygame.K_a:
                self.b1.xSpeed = -10
                self.b1.ySpeed = 0
            elif event.key == pygame.K_w:
                self.b1.ySpeed = -10
                self.b1.xSpeed = 0
            elif event.key == pygame.K_s:
                self.b1.ySpeed = 10
                self.b1.xSpeed = 0
                """
            if event.key == pygame.K_t:
                self.attack.play()

            elif event.key == pygame.K_d:
                self.idle.rect = self.idle.rect.move((5, 0))
            elif event.key == pygame.K_a:
                self.idle.rect = self.idle.rect.move((-5, 0))
            elif event.key == pygame.K_w:
                self.idle.rect = self.idle.rect.move((0, -5))
            elif event.key == pygame.K_s:
                self.idle.rect = self.idle.rect.move((0, 5))

            # self.b1.move()
        elif event.type == pygame.KEYUP:
            pass

    def on_loop(self):

        self.clock.tick(30)  # Forcing FPS to 30

        pygame.display.set_caption("FPS = {:.2f}".format(self.clock.get_fps()))

        self.idle.update()
        self.attack.update()

        #self.b2.move()
        self.b1.move()

         # hit detection
        if self.b1.rect.left <= -10 or self.b1.rect.right >= 650:
            self.b1.xSpeed = -self.b1.xSpeed

        if self.b2.rect.left <= 0 or self.b2.rect.right >= 640 or self.b2.rect.colliderect(self.b1.rect):
            self.b2.xSpeed = -self.b2.xSpeed



    def on_render(self):

        self._display.fill((0, 31, 100))

        # blit ball into screen
        self._display.blit(self.b1.surface, self.b1.rect)
        self._display.blit(self.b2.surface, self.b2.rect)

        self._display.blit(self.idle.image, self.idle.rect)

        self._display.blit(self.attack.image, self.idle.rect)

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


class Ball(object):

    def __init__(self, c, speed):
        self.color = c
        self.xSpeed = speed[0]
        self.ySpeed = speed[1]
        self.center = (25, 25)
        self.radius = 25
        self.surface = pygame.Surface((50, 50)).convert()
        self.rect = pygame.draw.circle(self.surface, self.color, self.center, self.radius)

    def move(self):
        self.rect = self.rect.move((self.xSpeed, self.ySpeed))

    def relocate(self, xAndY):
        self.rect = self.rect.move(xAndY)  # xAndY is a tuple


class SimpleAnimation(object):

    def __init__(self, frames):
        self.frames = frames
        self.current = 0
        self.image = frames[0].convert()
        self.rect = self.image.get_rect()
        self.playing = 0

    def update(self):
        if self.playing:
            self.current += 1
            if self.current == len(self.frames):
                self.current = 0
                self.playing = False # Play once, then stop and move the object away from the game screen!
                #self.rect = self.rect.move((-50, -50))

            self.image = self.frames[self.current]

    def play(self):
        self.playing = True

    def stop(self):
        self.playing = False


class repeatedAnimation(SimpleAnimation):

    def update(self):
        if self.playing:
            self.current += 1
            if self.current == len(self.frames):
                self.current = 0

            self.image = self.frames[self.current]

class Character(object):

    def __init__(self):
        self.animations = [] #List of usable animations.


class Player(Character):

    def __init__(self):
        self.idleFrames = []
        self.attackFrames = []

        for i in range(45):
            self.idleFrames.append(pygame.image.load(os.path.join("assets/player_idle", "idle_"+str(i)+".png")))

        for i in range(16):
            self.attackFrames.append(pygame.image.load(os.path.join("assets/player_attack", "attack_"+str(i)+".png")))

    def play(self, animation):
        pass


g = Game()
g.on_execute()

