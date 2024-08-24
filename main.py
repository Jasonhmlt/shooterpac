from pygame import *
window = display.set_mode((700, 500))
display.set_caption('My first game')
finish = False
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, h, w, x, y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(h, w))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
wall1 = GameSprite("wall.png", 80, 600, 300, 150)
wall2 = GameSprite("wall.png", 280, 30, 100, 300)
final_sprite = GameSprite("pac.png", 50, 60, 450, 450)
lose = GameSprite("fail.jpg", 700, 500, 0, 0)
win = GameSprite("win.jpg", 700, 500, 0, 0)

barrier = sprite.Group()
barrier.add(wall1)
barrier.add(wall2)

class Player(GameSprite):
    def __init__(self, player_image, h, w, x, y, speed_x, speed_y):
        GameSprite.__init__(self, player_image, h, w, x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y
    def shoot(self):
        bullet = Bullets("bullet.png", 20, 20, self.rect.right, self.rect.centery, 10)
        ammo.add(bullet)
    def update(self):
        #if self.speed_x > 0 or self.rect.x >= 0 and self.speed_x < 0:
            self.rect.x += self.speed_x
            platforms_touched = sprite.spritecollide(self, barrier, False)
            if self.speed_x > 0:
                for p in platforms_touched:
                    self.rect.right = min(self.rect.right, p.rect.left)
            elif self.speed_x < 0:
                for p in platforms_touched:
                    self.rect.left = max(self.rect.left, p.rect.right)
        #if self.speed_y > 0 or self.rect.y >= 0 and self.speed_y < 0:
            self.rect.y += self.speed_y
            platforms_touched = sprite.spritecollide(self, barrier, False)
            if self.speed_y > 0:
                for p in platforms_touched:
                    self.rect.bottom = min(self.rect.bottom, p.rect.top)
            elif self.speed_y < 0:
                for p in platforms_touched:
                    self.rect.top = max(self.rect.top, p.rect.bottom)
player = Player("1-2.png", 50, 60, 100, 400, 0, 0)

class Bullets(GameSprite):
    def __init__(self, bullets_image, h, w, x, y, speed_x):
        GameSprite.__init__(self, bullets_image, h, w, x, y)
        self.speed_x = speed_x
    def update(self):
        self.rect.x += self.speed_x
        if self.rect.x > 700:
            self.kill()

ammo = sprite.Group()

class Enemy(GameSprite):
    def __init__(self, player_image, h, w, x, y, speed_x):
        GameSprite.__init__(self, player_image, h, w, x, y)
        self.speed_x = speed_x
    side = "left"
    def update(self):
        if self.rect.x <= 460: #w1.wall_x + w1.wall_width
            self.side = "right"
        if self.rect.x >= 700 - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed_x
        else:
            self.rect.x += self.speed_x
        #self.rect.x += self.speed_x
        #if self.rect.x <= 350:
         #   self.speed_x += 20
        #if self.rect.x >= 700:
         #   self.speed_x -= 20

        
        
enemy1 = Enemy("cyborg.png", 50, 60, 550, 150, 10)
enemy2 = Enemy("cyborg.png", 50, 60, 550, 300, 10)

Enemies = sprite.Group()
Enemies.add(enemy1)
Enemies.add(enemy2)


run = True
while run:
    window.fill((0, 0, 0))
    time.delay(50)
    player.update()
    ammo.update()
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_DOWN:
                player.speed_y = 10
            elif e.key == K_UP:
                player.speed_y = -10
            elif e.key == K_LEFT:
                player.speed_x = -5
            elif e.key == K_RIGHT:
                player.speed_x = 5
            elif e.key == K_SPACE:
                player.shoot()
        elif e.type == KEYUP:
            if e.key == K_DOWN:
                player.speed_y = 0
            elif e.key == K_UP:
                player.speed_y = 0
            elif e.key == K_LEFT:
                player.speed_x = 0
            elif e.key == K_RIGHT:
                player.speed_x = 0
    if finish != True:
        player.reset()
        barrier.draw(window)
        final_sprite.reset()
      #  ammo.update()
        ammo.draw(window)
        Enemies.update()
        Enemies.draw(window)
        sprite.groupcollide(ammo, barrier, True, False)
        sprite.groupcollide(ammo, Enemies, True, True)
    if sprite.spritecollide(player, Enemies, True):
        finish = True
        lose.reset()
    elif sprite.collide_rect(player, final_sprite):
        finish = True
        win.reset()
    display.update()