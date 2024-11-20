import pygame
import random

pygame.init()

# Definir constantes
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# Crear la pantalla del juego
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Alien Invasion")

reloj = pygame.time.Clock()

# Intentar cargar las imágenes
try:
    nave_imagen = pygame.image.load('imagenes/nave.png')  
    nave_imagen = pygame.transform.scale(nave_imagen, (50, 50))  

    alien_imagen = pygame.image.load('imagenes/alien.png')  
    alien_imagen = pygame.transform.scale(alien_imagen, (50, 50))  
    
    fondo_imagen = pygame.image.load('imagenes/fondo.jpg')  
    fondo_imagen = pygame.transform.scale(fondo_imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))  

except pygame.error as e:
    print(f"Error al cargar la imagen: {e}")
    pygame.quit()
    exit()

# 
COLOR_BALA = (255, 255, 255)

# Configuración de la nave del jugador
class Nave:
    def __init__(self):
        self.image = nave_imagen  # Asignamos la imagen de la nave
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO_PANTALLA // 2
        self.rect.bottom = ALTO_PANTALLA - 10
        self.velocidad = 5

    def mover(self, direccion):
        if direccion == "izquierda" and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if direccion == "derecha" and self.rect.right < ANCHO_PANTALLA:
            self.rect.x += self.velocidad

    def dibujar(self):
        pantalla.blit(self.image, self.rect)  # Dibujar la nave en la pantalla

# Configuración de las balas
class Bala:
    def __init__(self, x, y):
        self.image = pygame.Surface((5, 10))
        self.image.fill(COLOR_BALA)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidad = 7

    def mover(self):
        self.rect.y -= self.velocidad

    def dibujar(self):
        pantalla.blit(self.image, self.rect)

# Configuración de los alienígenas
class Alien:
    def __init__(self):
        self.image = alien_imagen  # Asignamos la imagen del alien
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO_PANTALLA - 50)
        self.rect.y = random.randint(-150, -50)
        self.velocidad = random.randint(1, 3)

    def mover(self):
        self.rect.y += self.velocidad

    def dibujar(self):
        pantalla.blit(self.image, self.rect)  # Dibujar el alien en la pantalla

# Función principal del juego
def juego():
    nave = Nave()
    aliens = [Alien() for _ in range(10)]  # Lista de aliens
    balas = []
    alienes_eliminados = 0  # Contador de alienígenas eliminados

    # Fuente para mostrar el contador en pantalla
    fuente = pygame.font.SysFont("Arial", 30)

    # Bucle principal del juego
    while True:
        # Dibujar el fondo primero, asegurándonos de que esté detrás de todo lo demás
        pantalla.blit(fondo_imagen, (0, 0))

        # Verificar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Obtener teclas presionadas
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            nave.mover("izquierda")
        if teclas[pygame.K_RIGHT]:
            nave.mover("derecha")
        if teclas[pygame.K_SPACE]:
            balas.append(Bala(nave.rect.centerx, nave.rect.top))

        # Mover y dibujar las balas
        for bala in balas[:]:
            bala.mover()
            if bala.rect.bottom < 0:
                balas.remove(bala)
            else:
                bala.dibujar()

        # Mover y dibujar los alienígenas
        for alien in aliens[:]:
            alien.mover()
            if alien.rect.top > ALTO_PANTALLA:
                aliens.remove(alien)
                aliens.append(Alien())  # Reaparece un nuevo alien
            else:
                alien.dibujar()

        # Verificar colisiones entre balas y alienígenas
        for bala in balas[:]:
            for alien in aliens[:]:
                if bala.rect.colliderect(alien.rect):
                    balas.remove(bala)
                    aliens.remove(alien)
                    aliens.append(Alien())  # Reaparece un nuevo alien
                    alienes_eliminados += 1  # Incrementar el contador
                    break

        for alien in aliens[:]:
            if nave.rect.colliderect(alien.rect):  
                game_over(alienes_eliminados)  
                return 

        # Dibujar la nave
        nave.dibujar()

        # Mostrar el contador de alienígenas eliminados
        texto_puntos = fuente.render(f"Aliens Eliminados: {alienes_eliminados}", True, (255, 255, 255))
        pantalla.blit(texto_puntos, (10, 10))

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(60)

# Función para mostrar Game Over
def game_over(alienes_eliminados):
    fuente = pygame.font.SysFont("Arial", 50)
    mensaje = fuente.render("GAME OVER", True, (255, 0, 0))
    pantalla.blit(mensaje, (ANCHO_PANTALLA // 2 - mensaje.get_width() // 2, ALTO_PANTALLA // 2 - mensaje.get_height() // 2))

    # Mostrar los alienígenas eliminados al final
    fuente_puntos = pygame.font.SysFont("Arial", 30)
    texto_puntos = fuente_puntos.render(f"Aliens eliminados: {alienes_eliminados}", True, (255, 255, 255))
    pantalla.blit(texto_puntos, (ANCHO_PANTALLA // 2 - texto_puntos.get_width() // 2, ALTO_PANTALLA // 2 + 50))

    pygame.display.flip()  # Actualizar la pantalla para mostrar el mensaje
    pygame.time.delay(2000)  # Esperar 2 segundos antes de cerrar el juego

# Ejecutar el juego
if __name__ == "__main__":
    juego()

