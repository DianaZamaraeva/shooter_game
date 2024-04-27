#Создай собственный Шутер!

from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def player_show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def left_right(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.centery, 20,20, -30)
        bullets.add(bullet)
lost = 0
score = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(50, 650)
            self.rect.y = 0
            lost = lost+1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_ogg = mixer.Sound('fire.ogg')

window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700,500))
player = Player('rocket.png', 50, 400, 100,100, 50)
font.init()
font2 = font.SysFont('Arial', 36)
bullets = sprite.Group()

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(50,650),0, 100,100, randint(2,10))
    monsters.add(monster)

game = True
finish = False
font1 = font.SysFont('Arial', 90)
win = font1.render('Ты победил!', True, (13, 231, 175))
loze = font1.render('Ты проиграл!', True, (255, 132, 85))
while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                player.fire()
                fire_ogg.play()

    if not finish:
        window.blit(background, (0,0))
        player.player_show()
        player.left_right()
        monsters.update()
        monsters.draw(window)
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10,10))
        text_win = font2.render("Поймано: " + str(score), 1, (255, 255, 255))
        window.blit(text_win, (10,40))
        bullets.update()
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(50,650),0, 100,100, randint(2,10))
            monsters.add(monster)
        #проверка победы
        if score >= 11:
            finish = True
            window.blit(win, (120,200))
        if sprite.spritecollide(player, monsters, False) or lost >= 5:
            finish = True
            window.blit(loze, (120,200))
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        for a in bullets:
            a.kill()
        for b in monsters:
            b.kill()
        time.delay(3000)
        for i in range(5):
            monster = Enemy('ufo.png', randint(50,650),0, 100,100, randint(2,10))
            monsters.add(monster)
            



        
        
        
    time.delay(50)