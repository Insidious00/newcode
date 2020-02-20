import pygame as pg
import time
from random import uniform
from settings import *
from tilemap import collide_hit_rect
from os import path
vec = pg.math.Vector2
from pygame_functions import *


def collide_with_obstacle(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, health, magic):
        self.name = "Tom"
        self.health = health
        self.inventory = ["1","2","3","4"]
        self.magic = magic
        alpha = (0,255,0)
        self.current_frame = 0
        self.last_update = 0
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.image.convert_alpha()
        self.image.set_colorkey(alpha)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.allow_walk = True

    def collide_with_doors(self, sprite, group, dir):
        if dir == 'x':
            self.hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
            if self.hits:
                print("!")
                sprite.vel.x = 0
                sprite.hit_rect.centerx = sprite.pos.x
                return True
                
        if dir == 'y':
            self.hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
            if self.hits:
                print("!")
                sprite.vel.y = 0
                sprite.hit_rect.centery = sprite.pos.y
                return True
            
    def collide_with_doorsin(self, sprite, group, dir):
        if dir == 'x':
            self.hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
            if self.hits:
                print("!")
                sprite.vel.x = 0
                sprite.hit_rect.centerx = sprite.pos.x
                return True
                
        if dir == 'y':
            self.hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
            if self.hits:
                print("!")
                sprite.vel.y = 0
                sprite.hit_rect.centery = sprite.pos.y
                return True

    def get_keys(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'img')
        self.map_folder = path.join(self.game_folder, 'maps')
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if self.allow_walk == True:
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                i = 1
                self.pos[0] -= 4
                self.game.player_img = pg.image.load(path.join(self.img_folder, PLAYER_IMG1[self.current_frame])).convert_alpha()
                self.animate(i)
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                i = 2
                self.pos[0] += 4
                self.game.player_img = pg.image.load(path.join(self.img_folder, PLAYER_IMG2[self.current_frame])).convert_alpha()
                self.animate(i)
            if keys[pg.K_UP] or keys[pg.K_w]:
                i = 3
                self.pos[1] -= 4
                self.game.player_img = pg.image.load(path.join(self.img_folder, PLAYER_IMG3[self.current_frame])).convert_alpha()
                self.animate(i)
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                i = 4
                self.pos[1] += 4
                self.game.player_img = pg.image.load(path.join(self.img_folder, PLAYER_IMG4[self.current_frame])).convert_alpha()
                self.animate(i)
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    self.current_frame = 1

    def animate(self, i):
        now = pg.time.get_ticks()
        if now - self.last_update > 150:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % 3

    def update(self):
        self.get_keys()
        self.image = self.game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_obstacle(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_obstacle(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        collide_with_obstacle(self, self.game.npc, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_obstacle(self, self.game.npc, 'y')
        self.rect.center = self.hit_rect.center

    def interact(self, group1, group2):
        self.hits = pg.sprite.spritecollide(group1, group2, False, collide_hit_rect)
        if self.hits:
            print("True")

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Door(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, name, ty):
        self.groups = game.doors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.name = name
        self.type = ty
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.w = w
        self.x = x
        self.y = y
        print(self.x)
        self.rect.x = x
        self.rect.y = y

class NPC(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h,name):
        alpha = (0,255,0)
        self.name = name
        self.text = self.get_dialogue(self.name)
        self.game = game
        self.image = self.get_image()
        self.image.convert_alpha()
        self.image.set_colorkey(alpha)
        self.groups = game.npc
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        print(self.x)
        self.rect.x = x
        self.rect.y = y

    def get_image(self):
        if self.name == "steven":
            return(self.game.npc_image1)
        if self.name == "blacksmith":
            return(self.game.npc_image)

    def get_dialogue(self, name):
        if self.name == "steven":
            return(Mission_Init_1)
        if self.name == "npc1":
            return(DIALOGUE1)
        if self.name == "blacksmith":
            return(Mission_Dial_1)
