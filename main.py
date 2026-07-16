import pygame
from player import Player
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state

def main():
    # Iniciacion de pygame
    pygame.init()

    # Variables para 60 FPS
    reloj: pygame = pygame.time.Clock()
    dt: float = 0.0

    # Groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    # Tamaño de la ventana a usar
    screen: pygame = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    Player.containers = (updatable, drawable)
    player1 = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)

    # Game loop
    while True:
        # Funcion de bootdev para comprobar el funcionamiento correcto
        log_state()

        # Event queue que revisamos en cada iteracion
        for event in pygame.event.get():
            # Evento para salir del loop al cerrar la ventana
            if event.type == pygame.QUIT:
                return

        # Actualiza la posición de los elementos dentro del grupo updatable 
        updatable.update(dt)

        # Color de la pantalla 
        screen.fill("black")
        # Dibula a los objetos del grupo drawable en la pantalla
        for obj in drawable:
            obj.draw(screen)

        # Refresca la pantalla
        pygame.display.flip()

        # DeltaTime indica el tiempo entre tick para 60FPS, en milisegundos. 
        dt = reloj.tick(60) / 1000 


if __name__ == "__main__":
    main()
