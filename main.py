import pygame
import sys
from player import Player
from shot import Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event


def main():
    # Iniciacion de pygame
    pygame.init()

    # Tamaño de la ventana a usar
    screen: pygame = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Variables para 60 FPS
    reloj: pygame = pygame.time.Clock()
    dt: float = 0.0

    # Groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    player = Player(x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2)
    astrofield = AsteroidField()

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

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over")
                sys.exit()

            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    asteroid.kill()
                    shot.kill()

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
