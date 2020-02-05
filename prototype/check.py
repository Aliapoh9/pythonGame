import pygame, os

class Game(object):

    def __init__(self):
        self._running = 0
        self._display = None
        self.menu = Menu()
        self.neg = 1

    def on_running(self):

        while self._running:

            for e in pygame.event.get():
                self.event(e)
            self.on_loop()
            self.render()

        pygame.quit()


class Menu(Game):
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
        self.startBtnSurface = self.mainFont.render("Start", True, (0, 0, 0))
        self.startBtnRect = self.startBtnSurface.get_rect()
        self.titleS = self.titleFont.render("Gametitle", True, (0, 0, 0))
        self.titleR = self.titleS.get_rect()
        self.contS = self.mainFont.render("Continue", True, (0, 0, 0))
        self.contR = self.contS.get_rect()

        self.mainMenuBg = pygame.image.load(os.path.join("d_assets/bg/parallax-mountain.png")).convert()
        self.titleR.center = (330, 100)
        self.startBtnRect.center = (330, 180)
        self.contR.center = (330, 330)

        pygame.display.set_caption("Gametitle")
        self.on_running()

    def event(self, e):
        if e.type == pygame.QUIT:
            self._running = 0

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
        pygame.display.flip()

Menu()