from pygame import *  # Ensure all necessary pygame modules are imported
from random import randint
font.init()
mixer.init()

ancho_ven = 1800
alto_ven = 980

ventana = display.set_mode((ancho_ven, alto_ven))
display.set_caption('Space Shooter')

class Figura(sprite.Sprite):
    def __init__(self, ancho=0, alto=0, posicionx=0, posiciony=0, imagen='', velocidad=0):
        sprite.Sprite.__init__(self)
        self.ancho = ancho
        self.alto = alto
        self.posicionx = posicionx
        self.posiciony = posiciony
        self.image = transform.scale(image.load(imagen), (self.ancho, self.alto))
        self.rect = self.image.get_rect()
        self.rect.x = posicionx
        self.rect.y = posiciony
        self.velocidad = velocidad

    def dibujarFigura(self):
        ventana.blit(self.image, (self.rect.x, self.rect.y))

class PersonajePrincipal(Figura):
    def movimiento(self):
        keys = key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.rect.x -= self.velocidad
        if keys[K_RIGHT] or keys[K_d]:
            self.rect.x += self.velocidad

    def disparar(self):
        objetivox, objetivoy = mouse.get_pos()
        bala = Bala(50, 50, self.rect.centerx, self.rect.top, 'bala.png', 15, objetivox, objetivoy)
        balas.add(bala)  # Asegúrate de que las balas se añadan al grupo correctamente

    def colision(self, naves):
        for n in naves:
            if sprite.collide_rect(self, n):
                return True
        return False

class Bala(Figura):
    def __init__(self, ancho=0, alto=0, posicionx=0, posiciony=0, imagen='', velocidad=0, objetivo_x=0, objetivo_y=0):
        super().__init__(ancho, alto, posicionx, posiciony, imagen, velocidad)
        direccionx = objetivo_x - posicionx
        direcciony = objetivo_y - posiciony
        distancia = (direccionx ** 2 + direcciony ** 2) ** 0.5
        self.velocidad_x = (direccionx / distancia) * velocidad
        self.velocidad_y = (direcciony / distancia) * velocidad

    def moverarriba(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

class Enemigo(Figura):
    def movimiento(self):
        self.rect.y += self.velocidad
        if self.rect.y > alto_ven + 10:
            self.kill()

Nave = PersonajePrincipal(200, 200, ancho_ven // 2, 800, 'marc.png', 5)
fondo = transform.scale(image.load('galaxy.webp'), (ancho_ven, alto_ven))

class Fuentes():
    def __init__(self, fuente, tamano, color, color_fondo):
        self.fuente = font.SysFont(fuente, tamano)
        self.color = color
        self.color_fondo = color_fondo

    def renderizarTexto(self, texto, x, y):
        self.texto = self.fuente.render(texto, True, self.color, self.color_fondo)
        ventana.blit(self.texto, (x, y))
        return self.texto.get_rect(topleft=(x, y))

run = True
clock = time.Clock()
vida = 100
puntaje = 0
red = (235, 52, 103)
white = (255, 255, 255)
sonidodano = mixer.Sound('audi.mp3')
balas = sprite.Group()
enemigos = sprite.Group()
cantidad_de_enemigos = 7
for i in range(cantidad_de_enemigos):
    enemigo = Enemigo(200, 100, randint(60, ancho_ven - 60), 0, 'mesi.png', randint(3, 5))
    enemigos.add(enemigo)

puntaje_texto = Fuentes('SquareGame-Regular', 30, red, white)
vida_texto = Fuentes('SquareGame-Regular', 30, red, white)

titulodejuego = Fuentes('SquareGame-Regular', 80, (255, 255, 255), (0, 0, 0))
botondeiniciar = Fuentes('SquareGame-Regular', 50, (255, 255, 255), (0, 0, 0))

iniciarjuego = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == MOUSEBUTTONDOWN:  # Asegúrate de que este evento esté configurado
            if e.button == 1:  # Botón izquierdo del mouse
                Nave.disparar()  # Llama al método disparar del objeto Nave

    if not iniciarjuego:
        ventana.blit(fondo, (0, 0))
        boton_rect = botondeiniciar.renderizarTexto('Iniciar Juego', ancho_ven // 2 - 300, alto_ven // 2 + 100)
        titulodejuego.renderizarTexto('Space Shooter', ancho_ven // 2 - 300, alto_ven // 2 - 100)
        if boton_rect.collidepoint(mouse.get_pos()):
            if mouse.get_pressed()[0]:
                iniciarjuego = True
    else:
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    Nave.disparar()

        ventana.blit(fondo, (0, 0))
        puntaje_texto.renderizarTexto(f'Puntaje: {puntaje}', 10, 10)
        vida_texto.renderizarTexto(f'Vida: {vida}', ancho_ven - 200, 10)
        enemigos.draw(ventana)
        for e in enemigos:
            e.movimiento()
            if e.rect.y > alto_ven + 10:
                enemigos.remove(e)
                enemigo = Enemigo(200, 100, randint(60, ancho_ven - 60), 0, 'mesi.png', randint(3, 5))
                enemigos.add(enemigo)
        balas.draw(ventana)  # Dibuja las balas en la ventana
        for b in balas:
            b.moverarriba()  # Mueve las balas hacia arriba
            if b.rect.y < 0:  # Elimina las balas que salen de la pantalla
                balas.remove(b)
            if sprite.spritecollide(b, enemigos, True):
                sonidodano.stop()
                sonidodano.play()
                puntaje += 10
                balas.remove(b)
                enemigo = Enemigo(200, 100, randint(60, ancho_ven - 60), 0, 'mesi.png', randint(3, 5))
                enemigos.add(enemigo)
        if sprite.spritecollide(Nave, enemigos, True):
            vida -= 10
            enemigo = Enemigo(200, 100, randint(60, ancho_ven - 60), 0, 'mesi.png', randint(3, 5))
            enemigos.add(enemigo)
            if vida <= 0:
                run = False

        Nave.dibujarFigura()
        Nave.movimiento()

    clock.tick(60)
    display.update()
