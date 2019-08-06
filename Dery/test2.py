import pygame

pygame.init()

gameDisplay = pygame.display.set_mode((500, 700))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

image = pygame.image.load('Logo.png')

def image(x, y):
    gameDisplay.blit(carImg, (x,y))

x = (display)

crashed = False

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        
        print(event)

    pygame.display.update()

    clock.tick(60)

pygame.quit()
quit()