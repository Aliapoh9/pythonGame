import pygame
import random

balls = []

class Ball(object):

    def __init__(self, c, s):
        self.color = c
        self.speed = s
        self.pos = (25, 25)
        self.s = 25
        self.surface = pygame.Surface((50, 50)).convert()
        self.rect = pygame.draw.circle(self.surface, self.color, self.pos, self.s)
        balls.append(self)

    def move(self):
        self.rect = self.rect.move(self.speed)


def main():

    pygame.init()

    logo = pygame.image.load("ball.jpg")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Slower than sound.")

    screen = pygame.display.set_mode((600, 460)) # Initialize the main display!

    clock = pygame.time.Clock()

    # image = pygame.image.load("stick.png")
    # image = pygame.transform.scale(image, (100, 100))


    #b1 = Ball((200, 0, 3), [2, 3])
    #b2 = Ball((1, 55, 12), [3, 4])

    for i in range(400):
        b = Ball((150, 0, 0), [i+1, i+1])


    running = True

    while running:

        clock.tick_busy_loop()
        pygame.display.set_caption("FPS = {:.2f}".format(clock.get_fps()))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        for i in range(len(balls)):
            balls[i].move()
            if balls[i].rect.left < 0 or balls[i].rect.right > 600:
                balls[i].speed[0] = -balls[i].speed[0]
            if balls[i].rect.top < 0 or balls[i].rect.bottom > 480:
                balls[i].speed[1] = -balls[i].speed[1]

            screen.blit(balls[i].surface, balls[i].rect)


        pygame.display.flip()


main()