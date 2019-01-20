import pygame
from pygame import *
import sys
from os.path import abspath, dirname
from random import randint, choice

pygame.init()
#Paths to fonts, images, sounds
BASE_PATH = abspath(dirname(__file__))
FONT_PATH = BASE_PATH + '/fonts/'
IMAGE_PATH = BASE_PATH + '/images/'
SOUND_PATH = BASE_PATH + '/sounds/'

pygame.mouse.set_visible(1) #visiable mouse cursor
pygame.display.set_caption('AoS') #Game window name
icon = pygame.image.load("images/icon.png") #window's icon
pygame.display.set_icon(icon) #window's icon load

#Colors in R G B
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (241, 255, 0)
#window size
SCREEN = display.set_mode((800, 600))
#load font and images
FONT = FONT_PATH + 'tt0588m.ttf' 
IMG_NAMES = ['plane','Bonus', 'enemy1_1', 'enemy1_2','enemy2_1', 'enemy2_2','enemy3_1', 'enemy3_2','bullet','bullet2', 'icon', 'explosion2', 'explosion3', 'explosion1']
IMAGES = {name: image.load(IMAGE_PATH + '{}.png'.format(name)).convert_alpha()
          for name in IMG_NAMES}

#menu music
pygame.mixer.Channel(4).play(pygame.mixer.Sound('sounds/menumusic.WAV'))


#class plane- player 
class plane(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = IMAGES['plane']
        self.rect = self.image.get_rect(topleft=(375, 540))
        self.speed = 5
#adding move keys
    def update(self, keys, *args):
        if keys[K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 740:
            self.rect.x += self.speed
        game.screen.blit(self.image, self.rect)

#addnig bullet class
class Bullet(sprite.Sprite):
    def __init__(self, xpos, ypos, direction, speed, filename, side):
        sprite.Sprite.__init__(self)
        self.image = IMAGES[filename]
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        self.speed = speed
        self.direction = direction
        self.side = side
        self.filename = filename

    def update(self, keys, *args):
        game.screen.blit(self.image, self.rect)
        self.rect.y += self.speed * self.direction
        if self.rect.y < 15 or self.rect.y > 600:  #range
            self.kill()

#ennemies
class Enemy(sprite.Sprite):
    def __init__(self, row, column):
        sprite.Sprite.__init__(self)
        self.row = row
        self.column = column
        self.images = []
        self.load_images()
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.direction = 1
        self.rightMoves = 30
        self.leftMoves = 30
        self.moveNumber = 15
        self.moveTime = 600
        self.timer = time.get_ticks()

    def update(self, keys, currentTime, enemies):
        if currentTime - self.timer > self.moveTime:
            if self.direction == 1:
                maxMove = self.rightMoves + enemies.rightAddMove
            else:
                maxMove = self.leftMoves + enemies.leftAddMove

            if self.moveNumber >= maxMove:
                if self.direction == 1:
                    self.leftMoves = 30 + enemies.rightAddMove
                elif self.direction == -1:
                    self.rightMoves = 30 + enemies.leftAddMove
                self.direction *= -1
                self.moveNumber = 0
                self.rect.y += 35
            elif self.direction == 1:
                self.rect.x += 10
                self.moveNumber += 1
            elif self.direction == -1:
                self.rect.x -= 10
                self.moveNumber += 1

            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]

            self.timer += self.moveTime

        game.screen.blit(self.image, self.rect)
    #Order of enemies
    def load_images(self):
        images = {0: ['1_2', '1_1'],
                  1: ['2_2', '2_1'],
                  2: ['2_2', '2_1'],
                  3: ['3_1', '3_2'],
                  4: ['3_1', '3_2'],
                  }
        img1, img2 = (IMAGES['enemy{}'.format(img_num)] for img_num in
                      images[self.row])
        self.images.append(transform.scale(img1, (40, 35)))
        self.images.append(transform.scale(img2, (40, 35)))


class EnemiesGroup(sprite.Group):
    def __init__(self, columns, rows):
        sprite.Group.__init__(self)
        self.enemies = [[0] * columns for _ in range(rows)]
        self.columns = columns
        self.rows = rows
        self.leftAddMove = 0
        self.rightAddMove = 0
        self._aliveColumns = list(range(columns))
        self._leftAliveColumn = 0
        self._rightAliveColumn = columns - 1
        self._leftKilledColumns = 0
        self._rightKilledColumns = 0

    def add(self, *sprites):
        super(sprite.Group, self).add(*sprites)

        for s in sprites:
            self.enemies[s.row][s.column] = s

    def is_column_dead(self, column):
        for row in range(self.rows):
            if self.enemies[row][column]:
                return False
        return True

    def random_bottom(self):
        random_index = randint(0, len(self._aliveColumns) - 1)
        col = self._aliveColumns[random_index]
        for row in range(self.rows, 0, -1):
            enemy = self.enemies[row - 1][col]
            if enemy:
                return enemy
        return None
    #kill function
    def kill(self, enemy):
        if not self.enemies[enemy.row][enemy.column]:
            return  

        self.enemies[enemy.row][enemy.column] = None
        isColumnDead = self.is_column_dead(enemy.column)
        if isColumnDead:
            self._aliveColumns.remove(enemy.column)

        if enemy.column == self._rightAliveColumn:
            while self._rightAliveColumn > 0 and isColumnDead:
                self._rightAliveColumn -= 1
                self._rightKilledColumns += 1
                self.rightAddMove = self._rightKilledColumns * 5
                isColumnDead = self.is_column_dead(self._rightAliveColumn)

        elif enemy.column == self._leftAliveColumn:
            while self._leftAliveColumn < self.columns and isColumnDead:
                self._leftAliveColumn += 1
                self._leftKilledColumns += 1
                self.leftAddMove = self._leftKilledColumns * 5
                isColumnDead = self.is_column_dead(self._leftAliveColumn)
#makes bonus
class Wunderwaffe(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = IMAGES['Bonus']
        self.image = transform.scale(self.image, (75, 35))
        self.rect = self.image.get_rect(topleft=(-80, 45))
        #position
        self.row = 5
        #speed
        self.moveTime = 25000
        #direction
        self.direction = 1
        self.timer = time.get_ticks()
        #special soundtrack when bonus arrived
        self.wunderwaffeEntered = mixer.Sound(SOUND_PATH + 'wunderwaffe.wav')
        self.wunderwaffeEntered.set_volume(1)
        self.playSound = True

    def update(self, keys, currentTime, *args):
        resetTimer = False
        passed = currentTime - self.timer
        if passed > self.moveTime:
            if (self.rect.x < 0 or self.rect.x > 800) and self.playSound:
                self.wunderwaffeEntered.play()
                self.playSound = False
            if self.rect.x < 840 and self.direction == 1:
                self.wunderwaffeEntered.fadeout(38000)
                self.rect.x += 5
                game.screen.blit(self.image, self.rect)
            if self.rect.x > -100 and self.direction == -1:
                self.wunderwaffeEntered.fadeout(38000)
                self.rect.x -= 6
                game.screen.blit(self.image, self.rect)

        if self.rect.x > 830:
            self.playSound = True
            self.direction = -1
            resetTimer = True
        if self.rect.x < -90:
            self.playSound = True
            self.direction = 1
            resetTimer = True
        if passed > self.moveTime and resetTimer:
            self.timer = currentTime
#adding explosion after death
class Explosion(sprite.Sprite):
    def __init__(self, xpos, ypos, row, plane, wunderwaffe , score):
        sprite.Sprite.__init__(self)
        self.isWunderwaffe = wunderwaffe
        self.isplane = plane
        if wunderwaffe:
            self.text = Text(FONT, 20, str(score), YELLOW, xpos + 20, ypos + 6)
        elif plane:
            self.image = IMAGES['plane']
            self.rect = self.image.get_rect(topleft=(xpos, ypos))
        else:
            self.row = row
            self.load_image()
            self.image = transform.scale(self.image, (40, 35))
            self.rect = self.image.get_rect(topleft=(xpos, ypos))
            game.screen.blit(self.image, self.rect)

        self.timer = time.get_ticks()

    def update(self, keys, currentTime):
        passed = currentTime - self.timer
        if self.isWunderwaffe:
            if passed <= 200:
                self.text.draw(game.screen)
            elif 400 < passed <= 600:
                self.text.draw(game.screen)
            elif passed > 600:
                self.kill()
        elif self.isplane:
            if 300 < passed <= 600:
                game.screen.blit(self.image, self.rect)
            elif passed > 900:
                self.kill()
        else:
            if passed <= 100:
                game.screen.blit(self.image, self.rect)
            elif 100 < passed <= 200:
                self.image = transform.scale(self.image, (50, 45))
                game.screen.blit(self.image,
                                 (self.rect.x - 6, self.rect.y - 6))
            elif passed > 400:
                self.kill()

    def load_image(self):
        imgColors = ['1', '2', '2', '3', '3']
        self.image = IMAGES['explosion{}'.format(imgColors[self.row])]
                

#adding lifes
class Life(sprite.Sprite):
    def __init__(self, xpos, ypos):
        sprite.Sprite.__init__(self)
        self.image = IMAGES['plane']
        self.image = transform.scale(self.image, (23, 23))
        self.rect = self.image.get_rect(topleft=(xpos, ypos))

    def update(self, keys, *args):
        game.screen.blit(self.image, self.rect)

#game texts colours, size
class Text(object):
    def __init__(self, textFont, size, message, color, xpos, ypos):
        self.font = font.Font(textFont, size)
        self.surface = self.font.render(message, True, color)
        self.rect = self.surface.get_rect(topleft=(xpos, ypos))

    def draw(self, surface):
        surface.blit(self.surface, self.rect)
    

class AoS(object):
    def __init__(self):
        pygame.mixer.pre_init(44100,16,2,4096)
        init()
        self.caption = display.set_caption('AoS')
        self.screen = SCREEN
        self.background = image.load(IMAGE_PATH + 'background.jpg').convert()
        self.startGame = False
        self.mainScreen = True
        self.gameOver = False
        self.enemyPositionDefault = 65
        self.enemyPositionStart = self.enemyPositionDefault
        self.enemyPosition = self.enemyPositionStart
        
        
    def reset(self, score, lives, newGame=False):
        self.player = plane()
        self.playerGroup = sprite.Group(self.player)
        self.explosionsGroup = sprite.Group()
        self.bullets = sprite.Group()
        self.enemyBullets = sprite.Group()
        self.wunderwaffeplane = Wunderwaffe()
        self.wunderwaffeGroup = sprite.Group(self.wunderwaffeplane)
        self.reset_lives(lives)
        self.enemyPosition = self.enemyPositionStart
        self.make_enemies()
        self.keys = key.get_pressed()
        self.clock = time.Clock()
        self.timer = time.get_ticks()
        self.noteTimer = time.get_ticks()
        self.planeTimer = time.get_ticks()
        self.score = score
        self.lives = lives
        self.create_audio()
        self.create_text()
        self.makeNewplane = False
        self.planeAlive = True
    

    def reset_lives_sprites(self):
        self.life1 = Life(60, 5)
        self.life2 = Life(91, 5)
        self.life3 = Life(122, 5)

        if self.lives == 3:
            self.livesGroup = sprite.Group(self.life1, self.life2, self.life3)
        elif self.lives == 2:
            self.livesGroup = sprite.Group(self.life1, self.life2)
        elif self.lives == 1:
            self.livesGroup = sprite.Group(self.life1)
#life reset
    def reset_lives(self, lives):
        self.lives = lives
        self.reset_lives_sprites()
#create audio
    def create_audio(self):
        self.sounds = {}
        for sound_name in ['shoot', 'enemykill','plane_explosion', 'wunderwaffe', 'menumusic', 'Explosion']:
            self.sounds[sound_name] = mixer.Sound(
                SOUND_PATH + '{}.wav'.format(sound_name))
            self.sounds[sound_name].set_volume(0.2)

        self.musicNotes = [mixer.Sound(SOUND_PATH + '{}.wav'.format(i)) for i
                           in range(4)]
        for sound in self.musicNotes:
            sound.set_volume(0.5)

        self.noteIndex = 0

#game texts
    def create_text(self):
        self.titleText = Text(FONT, 90, 'Aces of the Sky', YELLOW, 150, 90)
        self.gameOverText = Text(FONT, 80, 'Game Over', YELLOW, 240, 200)
        self.nextStageText = Text(FONT, 80, 'Next Stage', YELLOW, 240, 200)
        self.scoreText = Text(FONT, 20, 'Score: ', YELLOW, 640, 5)
        self.livesText = Text(FONT, 20, 'Lives: ', YELLOW, 5,5)
        self.buttonText1 = Text('fonts/ALGER.TTF', 41, 'NEW GAME', YELLOW, 298, 320)
        self.buttonText2 = Text('fonts/ALGER.TTF', 45, 'EXIT', YELLOW, 350, 470)
        self.HS = Text(FONT, 20, 'HS: ', YELLOW, 640, 5)
    @staticmethod #method
    def should_exit(evt):
        return evt.type == QUIT or (evt.type == KEYUP and evt.key == K_ESCAPE)

    #adds key support
    def input(self):
        self.keys = key.get_pressed()
        for e in event.get():
            if self.should_exit(e):
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if len(self.bullets) == 0 and self.planeAlive:
                        if self.score < 1000:
                            bullet = Bullet(self.player.rect.x + 23,
                                            self.player.rect.y + 5, -1, 15, 'bullet', 'center')
                            self.bullets.add(bullet)
                            self.allSprites.add(self.bullets)
                            self.sounds['shoot'].play()
                        else:
                            leftbullet = Bullet(self.player.rect.x + 8, self.player.rect.y + 5, -1, 15, 'bullet', 'left')
                            rightbullet = Bullet(self.player.rect.x + 38, self.player.rect.y + 5, -1, 15, 'bullet', 'right')
                            self.bullets.add(leftbullet)
                            self.bullets.add(rightbullet)
                            self.allSprites.add(self.bullets)
                            self.sounds['shoot'].play()
                           
#makes enemies
    def make_enemies(self):
        enemies = EnemiesGroup(10, 5)
        for row in range(5):
            for column in range(10):
                enemy = Enemy(row, column)
                enemy.rect.x = 157 + (column * 50)
                enemy.rect.y = self.enemyPosition + (row * 45)
                enemies.add(enemy)
        self.enemies = enemies
        self.allSprites = sprite.Group(self.player, self.enemies, self.livesGroup, self.wunderwaffeplane)
#add anemy attack
    def make_enemies_shoot(self):
        if (time.get_ticks() - self.timer) > 700:
            enemy = self.enemies.random_bottom()
            if enemy:
                self.enemyBullets.add(
                    Bullet(enemy.rect.x + 14, enemy.rect.y + 20, 1, 5,'bullet2', 'center'))
                self.allSprites.add(self.enemyBullets)
                self.timer = time.get_ticks()

    def scores(self, row):
        scores = {0: 30,
                  1: 20,
                  2: 20,
                  3: 10,
                  4: 10,
                  5: choice([50, 100, 150, 300])
                  }

        score = scores[row]
        self.score += score
        return score
    
    
    #draws buttons
    def butt(self):
        pygame.draw.rect(SCREEN, RED,(290,300,220,90))
        self.buttonText1.draw(self.screen)
        pygame.draw.rect(SCREEN, RED,(290,450,220,90))
        self.buttonText2.draw(self.screen)
        
    #draws main menu
    def mainmenu(self):
        self.butt()
        self.titleText.draw(self.screen)
        mouse = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed()
        
        for e in event.get():
            if self.should_exit(e):
                sys.exit()
            if e.type == KEYUP:
                self.startGame = True
                self.mainScreen = False

        if 510 > mouse[0] > 290 and 390 > mouse[1] > 300:
            
            if press[0] == 1:
                pygame.mixer.pause()
                self.startGame = True
                self.mainScreen = False
                
                
        if 510 > mouse[0] > 290 and 540 > mouse[1] > 450:
            if press[0] == 1:
                pygame.quit()
                quit()

                
    #speed enemies
    def update_enemy_speed(self):
        if len(self.enemies) <= 10:
            for enemy in self.enemies:
                enemy.moveTime = 400
        if len(self.enemies) == 1:
            for enemy in self.enemies:
                enemy.moveTime = 200
    #collisions
    def collisions(self):
        collidedict = sprite.groupcollide(self.bullets, self.enemyBullets, True, False)
        if collidedict:
            for value in collidedict.values():
                for currentSprite in value:
                        self.enemyBullets.remove(currentSprite)
                        self.allSprites.remove(currentSprite)

        enemiesdict = sprite.groupcollide(self.bullets, self.enemies, True, False)
        if enemiesdict:
            for value in enemiesdict.values():
                for currentSprite in value:
                    self.enemies.kill(currentSprite)
                    self.sounds['enemykill'].play()
                    score = self.scores(currentSprite.row)
                    explosion = Explosion(currentSprite.rect.x, currentSprite.rect.y, currentSprite.row, False, False, score)
                    self.explosionsGroup.add(explosion)
                    self.allSprites.remove(currentSprite)
                    self.enemies.remove(currentSprite)
                    self.gameTimer = time.get_ticks()
                    break
        wunderwaffedict = sprite.groupcollide(self.bullets, self.wunderwaffeGroup, True, True)
        
        if wunderwaffedict:
            for value in wunderwaffedict.values():
                for currentSprite in value:
                    currentSprite.wunderwaffeEntered.stop()
                    self.sounds['enemykill'].play()
                    score = self.scores(currentSprite.row)
                    explosion = Explosion(currentSprite.rect.x, currentSprite.rect.y, currentSprite.row, False, True, score)
                    self.explosionsGroup.add(explosion)
                    self.allSprites.remove(currentSprite)
                    self.wunderwaffeGroup.remove(currentSprite)
                    newplane = Wunderwaffe()
                    self.allSprites.add(newplane)
                    self.wunderwaffeGroup.add(newplane)
                    break       


        bulletsdict = sprite.groupcollide(self.enemyBullets, self.playerGroup,
                                          True, False)
        if bulletsdict:
            for value in bulletsdict.values():
                for playerplane in value:
                    if self.lives == 3:
                        self.lives -= 1
                        self.livesGroup.remove(self.life3)
                        self.allSprites.remove(self.life3)
                    elif self.lives == 2:
                        self.lives -= 1
                        self.livesGroup.remove(self.life2)
                        self.allSprites.remove(self.life2)
                    elif self.lives == 1:
                        self.lives -= 1
                        self.livesGroup.remove(self.life1)
                        self.allSprites.remove(self.life1)
                    elif self.lives == 0:
                        self.gameOver = True
                        self.startGame = False
                    self.sounds['plane_explosion'].play()
                    explosion = Explosion(playerplane.rect.x, playerplane.rect.y,
                                          0, True, False, 0)
                    self.explosionsGroup.add(explosion)
                    self.allSprites.remove(playerplane)
                    self.playerGroup.remove(playerplane)
                    self.makeNewplane = True
                    self.planeTimer = time.get_ticks()
                    self.planeAlive = False

        if sprite.groupcollide(self.enemies, self.playerGroup, True, True):
            self.gameOver = True
            self.startGame = False
            
    #create player plane after death
    def create_new_plane(self, createplane, currentTime):
        if createplane and (currentTime - self.planeTimer > 900):
            self.player = plane()
            self.allSprites.add(self.player)
            self.playerGroup.add(self.player)
            self.makeNewplane = False
            self.planeAlive = True
    #add game over screen
    def create_game_over(self, currentTime):
        self.screen.blit(self.background, (0, 0))
        self.scoreText2 = Text(FONT, 20, str(self.score), YELLOW, 715, 5)
        self.scoreText.draw(self.screen)
        self.scoreText2.draw(self.screen)
        passed = currentTime - self.timer
        if passed < 750:
            self.gameOverText.draw(self.screen)
        elif 750 < passed < 1500:
            self.screen.blit(self.background, (0, 0))
        elif 1500 < passed < 2250:
            self.gameOverText.draw(self.screen)
        elif 2250 < passed < 2750:
            self.screen.blit(self.background, (0, 0))
        elif passed > 3000:
            self.mainScreen = True

        for e in event.get():
            if self.should_exit(e):
                sys.exit()

    #mainloop
    def main(self):
        while True:
            if self.mainScreen:
                self.reset(0, 3, True)
                self.screen.blit(self.background, (0, 0))
                self.mainmenu()
            elif self.startGame:
                if len(self.enemies) == 0:
                    currentTime = time.get_ticks()
                    if currentTime - self.gameTimer < 3000:
                        self.screen.blit(self.background, (0, 0))
                        self.scoreText2 = Text(FONT, 20, str(self.score), YELLOW, 715, 5)
                        self.scoreText.draw(self.screen)
                        self.scoreText2.draw(self.screen)
                        self.nextStageText.draw(self.screen)
                        self.livesText.draw(self.screen)
                        self.livesGroup.update(self.keys)
                        self.input()
                    if currentTime - self.gameTimer > 3000:
                        self.enemyPositionStart += 35
                        self.reset(self.score, self.lives)
                        self.gameTimer += 3000
                else:
                    currentTime = time.get_ticks()
                    self.screen.blit(self.background, (0, 0))
                    self.scoreText2 = Text(FONT, 20, str(self.score), YELLOW, 715, 5)
                    self.scoreText.draw(self.screen)
                    self.scoreText2.draw(self.screen)
                    self.livesText.draw(self.screen)
                    self.input()
                    self.explosionsGroup.update(self.keys, currentTime)
                    self.allSprites.update(self.keys, currentTime, self.enemies)
                    self.collisions()
                    self.create_new_plane(self.makeNewplane, currentTime)
                    self.update_enemy_speed()
                    if len(self.enemies) > 0:
                        self.make_enemies_shoot()

            elif self.gameOver:
                currentTime = time.get_ticks()
                #enemy reset starting position
                self.enemyPositionStart = self.enemyPositionDefault
                self.create_game_over(currentTime)

            display.update()
            #60 FPS
            self.clock.tick(60) 

if __name__ == '__main__':
    game = AoS()
    game.main()

