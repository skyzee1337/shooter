from pygame import *
from random import randint
font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 25)
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()


window = display.set_mode((700, 500))
display.set_caption('стрелашкэ')
background = transform.scale(image.load('galaxy.jpg'),(700, 500))
game = True

class GameSprite(sprite.Sprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__()
        self.image = transform.scale(image.load(filename),(w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, filename, w, h, speed, x, y, health=100):
        super().__init__(filename, w, h, speed, x, y)
        self.health = health

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 635:
            self.rect.x += self.speed
    def fire1(self):
        bullet1 = Bullet('ббшки.png', 10, 20, 10, self.rect.centerx , self.rect.top)
        bullets.add(bullet1)


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 480:
            self.rect.y = -100
            self.rect.x = randint(50, 650 - self.rect.width)
            self.speed = randint(2, 3)
            lost += 1

    def __init__(self, filename, w, h, speed, x, y):
        super().__init__(filename, w, h, speed, x, y)
        self.last_shot_time = time.get_ticks()
        self.shoot_interval = 2000

    def shoot(self):
        current_time = time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_interval:
            self.last_shot_time = current_time
            bullet2 = Bullet('fkkf[.jfif', 10, 20, -3, self.rect.centerx , self.rect.top)
            ebullets.add(bullet2)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()





class enemy_fire(GameSprite):
    def __init__(self, filename, w, h, speed, x, y, damage=25):
        super().__init__(filename, w, h, speed, x, y)
        self.damage = damage
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500: 
            self.kill()


bullets = sprite.Group()
ebullets = sprite.Group()




button = GameSprite('fire-button2.png', 65, 65, 0, 295, 250)
player = Player('воларбб.jfif', 65, 65, 5, 50, 430)
enemies = sprite.Group()
enemy1 = Enemy('бшн.jfif', 65, 35, 2, randint(0, 635), 0)
enemy2 = Enemy('бшн.jfif', 65, 35, 2, randint(0, 635), 0)
enemy3 = Enemy('бшн.jfif', 65, 35, 2, randint(0, 635), 0)
enemy4 = Enemy('бшн.jfif', 65, 35, 2, randint(0, 635), 0)
enemy5 = Enemy('бшн.jfif', 65, 35, 2, randint(0, 635), 0)
enemies.add(enemy1, enemy2, enemy3, enemy4, enemy5)














clock = time.Clock()
FPS = 60
HP = 100
killed = 0
lost = 0
finish = False
menu = True

win = font2.render('волар бб снесда ГЗ',1, (0,255,0))
lose1 = font2.render('волар бб не снесда ГЗ', 1, (255,0,0))
lose2 = font2.render('волар бб ЗАДЕФАЛИ(как так-то?)', 1, (255,0,0))


while game:
    if menu:
        window.blit(background, (0, 0))
        button.reset()
        for e in event.get():  
            if e.type == QUIT:
                game = False
            if e.type == MOUSEBUTTONDOWN:
                x, y = e.pos
                if button.rect.collidepoint(x,y):
                    menu = False
    if finish == False and menu == False:
    
        window.blit(background, (0, 0))
        for monster in enemies:
            monster.shoot()
        player.update()
        player.reset()
        enemies.update()
        bullets.draw(window)
        bullets.update()
        ebullets.draw(window)
        ebullets.update()  
        enemies.draw(window)
        text_HP = font1.render('HP:' +str(player.health), 1, (0,255,0) )
        text_kill = font1.render('убито:' +str(killed), 1, (255,0,0))
        text_lose = font1.render("Пропущено:" + str(lost), 1, (255,255,255))
        window.blit(text_HP, (50, 90))
        window.blit(text_lose, (50,50))
        window.blit(text_kill, (50, 70))
        if player.health <= 0:
            window.blit(lose2, (250,350) )
            finish = True
        if killed > 50:
            window.blit(win, (250,350))
            finish = True
        if lost > 3:
            window.blit(lose1, (250,350))
            finish = True

        sprites_list=sprite.groupcollide(enemies, bullets, True, True)
        sprites_list1=sprite.spritecollide(player, ebullets, True)
        for ebullet in sprites_list1:
            player.health -= 25
        for monster in sprites_list:
            killed += 1
            enemy1 = Enemy('бшн.jfif', 65, 35, randint(1,2), randint(0, 635), 0)
            enemies.add(enemy1)
        for e in event.get():  
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    player.fire1()
    if finish == True and menu == False:
        for e in event.get():
            if e.tipe == QUIT:
                game = False
    display.update()
    clock.tick(FPS)
