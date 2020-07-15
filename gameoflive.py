import sys, pygame
import numpy as np
import time

pygame.init()

# Ancho y alto de la pantalla.
size = width, height = 600,600
# Creacion de la pantalla.
screen = pygame.display.set_mode((height,width))

# Color casi negro, casi oscuro.
bg = 25,25,25
# Pintamos el fondo del color elegido.
screen.fill(bg)

nCx, nCy = 25, 25

dimCW = width / nCx
dimCH = height / nCy

# Estado de las celdas. Vivas = 1; Muertas = 0
gameState = np.zeros((nCx, nCy))

# Autómata palo
gameState[5, 3] = 0
gameState[5, 4] = 0
gameState[5, 5] = 0
# Autómata movil
gameState[21, 21] = 0
gameState[22, 22] = 0
gameState[22, 23] = 0
gameState[21, 23] = 0
gameState[20, 23] = 0

# Control de la ejecucion del juego.
pauseExect = False
# Bucle de ejecución.
while True:

    newGameState = np.copy(gameState)

    screen.fill(bg)
    time.sleep(0.1)

    # Registramos eventos de teclado y ratón.
    ev = pygame.event.get()

    for event in ev:
        # Declaramos si se presiona una tecla.
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect
        # declaramos si se preciona el ratón.
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]
        # finalizar juego
        if event.type == pygame.QUIT:
            pygame.quit()

    for y in range(0, nCx):
        for x in range(0, nCy):

            if not pauseExect:
                # Calculamos el numero de vecinos cercanos.
                n_neigh = gameState[(x-1) % nCx, (y-1) % nCy] + \
                          gameState[(x)   % nCx, (y-1) % nCy] + \
                          gameState[(x+1) % nCx, (y-1) % nCy] + \
                          gameState[(x-1) % nCx, (y)   % nCy] + \
                          gameState[(x+1) % nCx, (y)   % nCy] + \
                          gameState[(x-1) % nCx, (y+1) % nCy] + \
                          gameState[(x)   % nCx, (y+1) % nCy] + \
                          gameState[(x+1) % nCx, (y+1) % nCy]

                # Rule #1: Una célula muerta con exactamente 3 vecinas vivas, "revive".
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Rule #2: Una célula viva con menos de 2 o más de 3 vecinas vivas, "muere".
                elif gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            # Creando el poligon de cada celda a dibujar.
            poly = [((x) * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x) * dimCW, (y+1) * dimCH)]

            # Dibujamos la celda para cada par de x e y.
            if newGameState[x, y] ==0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Actualizamos el estado del juego.
    gameState = np.copy(newGameState)
    #poly = pygame.draw.polygon(screen, ())
    #pygame.draw.rect(screen,  (255, 255, 255), rect, 1)
    pygame.display.flip()
# finaliza Pygame
pygame.quit()