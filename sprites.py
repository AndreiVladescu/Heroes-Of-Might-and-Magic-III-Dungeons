import random
import pygame as pg
from random import uniform
from os import path
import numpy

from game_settings import *
from tilemap import collide_hit_rect

vec = pg.math.Vector2
debug_mode = False

def collide_with_walls(sprite, group, dir):
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
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0
        self.last_shot = 0
        self.last_hit = 0
        self.health = PLAYER_HEALTH
        self.magic = PLAYER_MAGIC
        self.stamina = PLAYER_STAMINA
        self.stamina_recovery_time = pg.time.get_ticks()
        self.rage = 0
        self.rage_time = 0
        self.rage_time_activation = pg.time.get_ticks()
        self.inventory = self.game.inventory

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
            self.game.play_sound('P', 'walk')
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
            self.game.play_sound('P', 'walk')
        if keys[pg.K_q]:
            now = pg.time.get_ticks()
            if now - self.last_shot > MISSLE_RATE:
                if not self.magic <= 5:
                    self.game.play_sound('P', 'attack_magic', True)
                    self.magic -= 5
                    self.last_shot = now
                    dir = vec(1, 0).rotate(-self.rot)
                    pos = self.pos + MISSLE_OFFSET.rotate(-self.rot)
                    Missle(self.game, pos, dir)
                    self.vel = vec(-RECOIL, 0).rotate(-self.rot)
        if keys[pg.K_e]:
            now = pg.time.get_ticks()
            if now - self.last_hit > MELEE_RATE:
                if not self.stamina <= 10:
                    self.game.play_sound('P', 'attack_melee', True)
                    self.stamina -=10
                    self.last_hit = now
                    Sword(self.game, self.pos)
        if keys[pg.K_r]:
            if self.rage == 300:
                self.rage_time = 3
                self.rage = 0;
                self.rage_time_activation = pg.time.get_ticks()
            elif self.rage >= 200:
                self.rage_time = 2
                self.rage -= 200
                self.rage_time_activation = pg.time.get_ticks()
            elif self.rage >= 100:
                self.rage_time = 1
                self.rage -= 100
                self.rage_time_activation = pg.time.get_ticks()

        if pg.time.get_ticks() - self.game.inventory.last_crafting_activation > 100:
            if keys[pg.K_1]:
                    if self.inventory.display_crafting_menu == False:
                        self.inventory.display_crafting_menu = True
                    else:
                        self.inventory.display_crafting_menu = False
            if keys[pg.K_2]:
                if self.inventory.item_list[1] > 0 and self.health < PLAYER_HEALTH:
                    self.inventory.item_list[1] -= 1
                    self.health += HEALTH_POTION_POINTS
            if keys[pg.K_3]:
                if self.inventory.item_list[2] > 0 and self.magic < PLAYER_MAGIC:
                    self.inventory.item_list[2] -= 1
                    self.magic += MAGIC_POTION_POINTS

            if keys[pg.K_4] and self.inventory.display_crafting_menu:
                if self.inventory.item_list[3] >= 2 and self.inventory.item_list[4] >=4:
                    self.game.MISSLE_DAMAGE_MULTIPLIER += 20
                    self.inventory.item_list[3] -= 2
                    self.inventory.item_list[4] -= 4

            if keys[pg.K_5] and self.inventory.display_crafting_menu:
                if self.inventory.item_list[3] >= 4 and self.inventory.item_list[4] >= 2:
                    self.game.SWORD_DAMAGE_MULTIPLIER += 20
                    self.inventory.item_list[3] -= 4
                    self.inventory.item_list[4] -= 2

            if keys[pg.K_h] and self.inventory.display_crafting_menu:
                if self.inventory.item_list[3] >= 2 and self.inventory.item_list[4] >= 2:
                    self.inventory.item_list[1] += 1
                    self.inventory.item_list[3] -= 2
                    self.inventory.item_list[4] -= 2

            if keys[pg.K_m] and self.inventory.display_crafting_menu:
                if self.inventory.item_list[3] >= 1 and self.inventory.item_list[4] >= 3:
                    self.inventory.item_list[2] += 1
                    self.inventory.item_list[3] -= 1
                    self.inventory.item_list[4] -= 3

            if keys[pg.K_8] and self.inventory.display_crafting_menu:
                if self.inventory.item_list[3] >= 2 and self.inventory.item_list[4] >= 3 and not self.inventory.has_pick:
                    self.inventory.has_pick = True
                    self.inventory.item_list[3] -= 2
                    self.inventory.item_list[4] -= 3

            if keys[pg.K_9] and self.inventory.display_crafting_menu:
                if self.inventory.item_list[3] >= 2 and self.inventory.item_list[4] >= 2 and not self.inventory.has_axe:
                    self.inventory.has_axe = True
                    self.inventory.item_list[3] -= 2
                    self.inventory.item_list[4] -= 2
            self.inventory.last_crafting_activation = pg.time.get_ticks()

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if (self.stamina < PLAYER_STAMINA):
            if (pg.time.get_ticks() - self.stamina_recovery_time > 2000):
                self.stamina +=PLAYER_STAMINA_REGEN
                self.stamina_recovery_time = pg.time.get_ticks()

class Inventory (pg.sprite.Sprite):
    def __init__(self, game):
        self.display_crafting_menu = False
        self.has_pick = False
        self.has_axe = False
        self.last_crafting_activation = pg.time.get_ticks()
        self.game = game
        self.cell_dimension = 64
        self.number_of_cells = 7
        self.x = (WIDTH - self.cell_dimension * self.number_of_cells) / 2
        self.y = HEIGHT - self.cell_dimension
        self.height = self.cell_dimension
        self.width = self.cell_dimension * self.number_of_cells
        self.surf = self.game.screen
        self.item_list = [0, 0, 0, 0, 0, 0, 0]
        self.sword_image = self.game.weapon_img
        self.wand_image = self.game.missle_img
        self.pickaxe_image = self.game.pickaxe_image
        self.axe_image = self.game.axe_image

    def update(self):
        self.fill_rect = pg.Rect( self.x, self.y, self.width, self.height)
        pg.draw.rect(self.surf, BLACK, self.fill_rect)
        for index in range (0, self.number_of_cells):
            #draws inventory bg, outline, quantity and selection number
            outline_rect = pg.Rect(self.x + self.cell_dimension * index,self.y,self.cell_dimension, self.cell_dimension)
            pg.draw.rect(self.surf, WHITE, outline_rect, 3)
            if not (index == 3 or index == 4):
                self.draw_text(str(index + 1), outline_rect.centerx + 10,outline_rect.centery + 10)
            if not (index == 0 or index == 5 or index == 6) :
                self.draw_text(str(self.item_list[index]) + 'x',outline_rect.centerx - 30, outline_rect.centery - 10)
            #draws item in inventory
            self.draw_item(index,outline_rect.centerx - 10, outline_rect.centery - 10)
        #display crafting menu
        if self.display_crafting_menu:
            self.draw_crafting_menu()

    def draw_text(self, text, x, y):
        size = 15
        color = WHITE
        font = pg.font.Font(self.game.title_font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.surf.blit(text_surface, text_rect)

    def draw_item(self, index, x, y):
        if index == 0:
            self.draw_text('Craft', x, y)
        elif index == 1:
            image = self.game.item_images['health']
            self.surf.blit(image, vec(x, y))
        elif index == 2:
            image = self.game.item_images['magic']
            self.surf.blit(image, vec(x, y))
        elif index == 3:
            image = self.game.obstacle_images['wood']
            self.surf.blit(image, vec(x, y))
        elif index == 4:
            image = self.game.obstacle_images['ore']
            self.surf.blit(image, vec(x, y))
        elif index == 5 and self.has_pick:
            image = self.game.pickaxe_image
            self.surf.blit(image, vec(x - 20, y - 20))
        elif index == 6 and self.has_axe:
            image = self.game.axe_image
            self.surf.blit(image, vec(x - 20, y - 20))

    def draw_crafting_menu(self):
        x = 10
        y = HEIGHT / 4
        fill_rect = pg.Rect(x, y, 330, 600)
        pg.draw.rect(self.surf, BLACK, fill_rect)
        out_rect = pg.Rect(x, y, 330, 600)
        pg.draw.rect(self.surf, WHITE, out_rect, 3)
        self.draw_text('4.Wand Damage increase: 2 Wood ,4 Ore' , x + 5, y + 5)
        self.draw_text('5.Sword Damage increase: 4 Wood ,2 Ore', x + 5, y + 105)
        self.draw_text('8.Pickaxe: 2 Wood ,3 Ore', x + 5, y + 205)
        self.draw_text('9.Axe: 2 Wood ,2 Ore', x + 5, y + 305)
        self.draw_text('h.Health Potion: 2 Wood ,2 Ore', x + 5, y + 405)
        self.draw_text('m.Magic Potion: 1 Wood ,3 Ore', x + 5, y + 505)
        self.surf.blit(self.game.wand_image_crafting, vec(x + 25, y + 25))
        self.surf.blit(self.game.sword_image_crafting, vec(x + 25, y + 125))
        self.surf.blit(self.game.pickaxe_image_crafting, vec(x + 25, y + 225))
        self.surf.blit(self.game.axe_image_crafting, vec(x + 25, y + 325))
        self.surf.blit(self.game.item_images['health'], vec(x + 100, y + 425))
        self.surf.blit(self.game.item_images['magic'], vec(x + 100, y + 535))

class Item(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.all_sprites, game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.obstacle_images[type]
        self.type = type
        self.rect = self.image.get_rect()
        self.hit_rect = OBSTACLE_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.health = 5

    def update(self):
        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()
            ## drop item

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.dist_to_player = numpy.linalg.norm(self.game.player.pos - self.pos)

    def update(self):
        self.dist_to_player = numpy.linalg.norm(self.game.player.pos - self.pos)
        self.draw_health()
        if self.dist_to_player < 80 and not debug_mode:
            self.game.play_sound('T', 'attack')
        if self.dist_to_player < MOB_PLAYER_DETECTION_RANGE and not debug_mode:
            self.game.play_sound('T', 'walk')
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center

        if self.health <= 0:
            if self.game.player.rage <= PLAYER_RAGE - MOB_HEALTH / 2:
                self.game.player.rage += MOB_HEALTH / 2
            else:
                self.game.player.rage = PLAYER_RAGE
            self.game.play_sound('T', 'death')
            random_item_drop = random.uniform(0, 100)
            if random_item_drop > 75:
                self.game.inventory.item_list[1] += 1
            elif random_item_drop > 50:
                self.game.inventory.item_list[2] += 1
            elif random_item_drop > 25:
                self.game.inventory.item_list[3] += 1
            else:
                self.game.inventory.item_list[4] += 1
            self.kill()
            ## drop  health

    def draw_health(self):
        col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

class Boss(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.boss
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.boss_img
        self.rect = self.image.get_rect()
        self.hit_rect = BOSS_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = BOSS_HEALTH
        self.dist_to_player = numpy.linalg.norm(self.game.player.pos - self.pos)

    def update(self):
        self.dist_to_player = numpy.linalg.norm(self.game.player.pos - self.pos)
        self.draw_health()
        if self.dist_to_player < 140 and not debug_mode:
            self.game.play_sound('M', 'attack')
        if self.dist_to_player < MOB_PLAYER_DETECTION_RANGE and not debug_mode:
            self.game.play_sound('M', 'walk')
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.boss_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(BOSS_SPEED, 0).rotate(-self.rot)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.game.play_sound('M', 'death')
            self.kill()
            self.game.end_screen()

    def draw_health(self):
        col = PURPLE
        width = int(self.rect.width * self.health / BOSS_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 5)
        if self.health < BOSS_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

class Missle(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.missles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rot = game.player.rot
        self.image = pg.transform.rotate(self.game.missle_img, self.rot)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(-MISSLE_SPREAD, MISSLE_SPREAD)
        self.vel = dir.rotate(spread) * MISSLE_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.image = pg.transform.rotate(self.game.missle_img, self.rot)
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > MISSLE_LIFETIME:
            self.kill()

class Sword(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.weapon
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rot = game.player.rot
        self.image = pg.transform.rotate(self.game.weapon_img, self.rot)
        self.rect = self.image.get_rect()
        pos = pos + vec(25, -15).rotate(-self.game.player.rot)
        self.pos = vec(pos)
        self.rect.center = game.player.rect.center
        self.spawn_time = pg.time.get_ticks()

    def update (self):
        self.image = pg.transform.rotate(self.game.weapon_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > 100:
            self.spawn_time=pg.time.get_ticks()
            self.kill()

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
