import pygame
from constants import PLAYER_RADIUS, LINE_WIDTH, \
                      PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOT_SPEED, \
                      PLAYER_SHOOT_COOLDOWN_SECONDS
from circleshape import CircleShape
from shot import Shot


class Player(CircleShape):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        # CoolDown para el disparo
        self.cd: float = 0.0
        # Usamos esta rotación para dibujar el triangulo
        self.rotation = 0

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(
            self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    # Toma la superficie de la pantalla dibujada para dibujarla dentro
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "White", self.triangle(),
                            LINE_WIDTH)

    # Rota al jugador en funcion de la velocidad de giro y su delta time
    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        self.cd -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt: float) -> None:
        # Iniciamos un vector recto
        unit_vector = pygame.Vector2(0, 1)
        # Giramos el vector para que apunte a la misma dirección del jugador
        vector_rotado = unit_vector.rotate(self.rotation)
        # Añadimos la velocidad para aumentar la longitud el vector la
        # distancia que tendría que moverse el jugador en ese tiempo
        # determinado.
        vector_rotado_movido = vector_rotado * PLAYER_SPEED * dt
        # La nueva posicion del jugador es la suma de la posicion anterior
        # con el nuevo vector
        self.position += vector_rotado_movido

    def shoot(self) -> None:
        if self.cd > 0:
            return
        self.cd = self.cd = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(
                                            self.rotation) * PLAYER_SHOT_SPEED
