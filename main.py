import sys
#from os import path
#import os
from sprites import *
from tilemap import *
from user_settings import *
from random_map_generator import *

# HUD functions
def draw_player_stats(surf, health, stamina, magic, rage):
    x = 10
    if health < 0:
        health = 0
    if stamina < 0:
        stamina = 0
    if magic < 0:
        magic = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    y = 10
    #HEALTH
    fill = health * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)
    #STAMINA
    y +=30
    BAR_LENGTH -=10
    fill = stamina * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    col = GREEN
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)
    #MAGIC
    y +=30
    BAR_LENGTH -=10
    fill = magic * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    col = BLUE
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)
    #RAGE
    BAR_LENGTH = 300
    x= (WIDTH - 300)/ 2
    y= HEIGHT - 100
    fill = rage * BAR_LENGTH
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    col = YELLOW
    pg.draw.rect(surf, col, fill_rect)
    for index in range (3):
        outline_rect = pg.Rect(x + index * 100, y,100 , BAR_HEIGHT)

        pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        pg.init()
        if FULLSCREEN_MODE:
            self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def play_sound(self, entity_type, entity_action, priority = False): # play sound with priority or not
        pg.mixer.pre_init(44100, -16, 2, 2048)
        if pg.time.get_ticks() - self.time_at_sound_init > SOUND_THRESHOLD:
            self.time_at_sound_init = pg.time.get_ticks()
            if entity_type == 'T':
                for action in TROGLODYTE_SOUNDS:
                    if action == entity_action:
                        sound = pg.mixer.Sound(path.join(self.sound_folder,TROGLODYTE_SOUNDS[action]))
                        sound.play()
            elif entity_type == 'P':
                for action in PLAYER_SOUNDS:
                    if action == entity_action:
                        if priority:
                            for priority_action in TROGLODYTE_SOUNDS:
                                sound = pg.mixer.Sound(path.join(self.sound_folder, TROGLODYTE_SOUNDS[priority_action]))
                                sound.stop()
                        sound = pg.mixer.Sound(path.join(self.sound_folder,PLAYER_SOUNDS[action]))
                        sound.play()
            elif entity_type == 'p':
                sound = pg.mixer.Sound(path.join(self.sound_folder, POTION_SOUND))
                sound.play()
            elif entity_type == 'M':
                for action in MINOTAUR_SOUNDS:
                    if action == entity_action:
                        sound = pg.mixer.Sound(path.join(self.sound_folder,MINOTAUR_SOUNDS[action]))
                        sound.play()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.game_folder = game_folder
        img_folder = path.join(game_folder, 'img')
        self.sound_folder = path.join(game_folder, 'sounds')
        self.music_folder = path.join(game_folder, 'music')
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.missle_img = pg.image.load(path.join(img_folder, MISSLE_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.boss_img = pg.image.load(path.join(img_folder, BOSS_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.weapon_img = pg.image.load(path.join(img_folder, WEAPON_IMG)).convert_alpha()
        self.sword_image_crafting = pg.image.load(path.join(img_folder, WEAPON_IMG_CRAFTING)).convert_alpha()
        self.wand_image_crafting = pg.image.load(path.join(img_folder, WAND_IMAGE_CRAFTING)).convert_alpha()
        self.pickaxe_image=pg.image.load(path.join(img_folder, PICKAXE_IMAGE)).convert_alpha()
        self.axe_image=pg.image.load(path.join(img_folder, AXE_IMAGE)).convert_alpha()
        self.pickaxe_image_crafting = pg.image.load(path.join(img_folder, PICKAXE_IMAGE_CRAFTING)).convert_alpha()
        self.axe_image_crafting = pg.image.load(path.join(img_folder, AXE_IMAGE_CRAFTING)).convert_alpha()
        self.title_font = path.join(img_folder, 'gameFont.otf')
        self.item_images = {}
        self.obstacle_images ={}
        self.MISSLE_DAMAGE_MULTIPLIER = 100
        self.SWORD_DAMAGE_MULTIPLIER = 100
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        for obstacle in OBSTACLE_IMAGES:
            self.obstacle_images[obstacle] = pg.image.load(path.join(img_folder, OBSTACLE_IMAGES[obstacle])).convert_alpha()


    def new(self):
        # initialize all variables and do all the setup for a new game
        pg.mixer.music.stop()
        pg.mixer.music.load(path.join(self.music_folder, BG_MUSIC_BATTLE))
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.1)
        self.time_at_sound_init = pg.time.get_ticks()
        self.time_at_init = pg.time.get_ticks()
        self.fighting = False
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.boss = pg.sprite.Group()
        self.missles = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.weapon = pg.sprite.Group()
        self.paused = False
        self.inventory = Inventory(self)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'H':
                    Item(self, col, row, 'health')
                if tile == 'm':
                    Item(self, col, row, 'magic')
                if tile == 'w':
                    Obstacle(self, col, row, 'wood')
                if tile == 'o':
                    Obstacle(self, col, row, 'ore')
                if tile == 'B':
                    Boss(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):

        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # mobs hit player
        now = pg.time.get_ticks()
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if now - self.player.rage_time_activation > 3000 * self.player.rage_time:
                self.player.rage_time = 0
                self.player.health -= MOB_DAMAGE
                if self.player.health <= 0:
                    self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        hits = pg.sprite.spritecollide(self.player, self.boss, False, collide_hit_rect)
        for hit in hits:
            if now - self.player.rage_time_activation > 3000 * self.player.rage_time:
                self.player.rage_time = 0
                self.player.health -= BOSS_DAMAGE
                if self.player.health <= 0:
                    self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        # missles hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.missles, False, True)
        for hit in hits:
            hit.health -= MISSLE_DAMAGE * self.MISSLE_DAMAGE_MULTIPLIER / 100
            self.player.rage += hit.health / 80
            hit.vel = vec(0, 0)
        if hits:
            hit.pos -= vec(MISSLE_KNOCKBACK, 0).rotate(-hit.rot)

        hits = pg.sprite.groupcollide(self.boss, self.missles, False, True)
        for hit in hits:
            hit.health -= MISSLE_DAMAGE * self.MISSLE_DAMAGE_MULTIPLIER / 100
            hit.vel = vec(0, 0)

        # sword hits mobs
        hits = pg.sprite.groupcollide(self.mobs, self.weapon, False, False)
        for hit in hits:
            hit.health -= WEAPON_DAMAGE * self.SWORD_DAMAGE_MULTIPLIER / 100
        if hits:
            hit.pos -= vec(SWORD_KNOCKBACK, 0).rotate(-hit.rot)
            hit.vel = vec(-1, 0).rotate(-hit.rot)

        hits = pg.sprite.groupcollide(self.boss, self.weapon, False, False)
        for hit in hits:
            hit.health -= WEAPON_DAMAGE * self.SWORD_DAMAGE_MULTIPLIER / 100

        # player collides with items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' :
                hit.kill()
                self.inventory.item_list[1] += 1
            elif hit.type == 'magic':
                hit.kill()
                self.inventory.item_list[2] += 1

        # player harvest
        keys = pg.key.get_pressed()
        hits = pg.sprite.spritecollide(self.player, self.obstacles, False)
        for hit in hits:
            if hit.type == 'wood' and self.inventory.has_axe:
                if keys[pg.K_e]:
                    hit.health -=10
                    hit.kill()
                    self.inventory.item_list [3] += 1
            #elif hit.type == 'wood' and not self.inventory.has_axe:
            #    if keys[pg.K_e]:
            #        hit.health -= 1
            #        if hit.health < 0:
            #            hit.kill()
            #            self.inventory.item_list [3] += 1
            elif hit.type == 'ore' and self.inventory.has_pick:
                if keys[pg.K_e]:
                    self.inventory.item_list [4] += 1
                    hit.health -= 10
                    hit.kill()
            #elif hit.type == 'ore' and  not self.inventory.has_pick:
            #    if keys[pg.K_e]:
            #        if hit.health < 0:
            #            self.inventory.item_list [4] += 1
            #            hit.kill()
            #        hit.health -= 1


    def draw(self):
        pg.display.set_caption("Heroes of Might and Magic Dungeons")
        self.screen.fill(BGCOLOR)
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            if isinstance(sprite, Boss):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # HUD functions
        draw_player_stats(self.screen, self.player.health / PLAYER_HEALTH, self.player.stamina / PLAYER_STAMINA, self.player.magic / PLAYER_MAGIC, self.player.rage / PLAYER_RAGE)
        if self.paused:
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2 -200, HEIGHT / 2 - 50)
        self.inventory.update()
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_p:
                    self.paused = not self.paused

    def wait_for_key(self):
        key = pg.key.get_pressed()
        finish = False
        while(not finish):
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    event_temp = event.type
                    finish = True
        return event_temp
    def start_screen(self):#start screen
        pg.mixer.music.load(path.join(self.music_folder, BG_MUSIC_AMBIANCE))
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.4)
        img_folder = path.join(self.game_folder, 'img')
        homm = pg.image.load(path.join(img_folder, 'homm.png')).convert_alpha()
        homm = pg.transform.scale(homm, (WIDTH, HEIGHT))
        self.screen.blit(homm, (0, 0))
        pg.display.flip()
        self.wait_for_key()

    def select_map(self):
        pg.display.flip()
        self.screen.fill(BLACK)
        self.draw_text("Select Map", self.title_font, 40, WHITE, WIDTH / 2 - 100, 100)
        self.draw_text("1) Pre-Made Custom Map", self.title_font, 30, WHITE, 100, 200)
        self.draw_text("2) Random Map (May contain bugs)",self.title_font, 30, WHITE, 100, 300)
        map_selection = 'map.txt'
       # keys = pg.key.get_pressed()
       # if keys[pg.K_1]:
       #     map_selection = 'map.txt'
       # elif keys[pg.K_2]:
       #     map_gen()
       #     map_selection = 'random_map.txt'

        map_type = self.wait_for_key()
        if map_type == pg.K_1:
            map_selection = 'map.txt'
        elif map_type == pg.K_2:
        #else:
            map_gen()
            map_selection = 'random_map.txt'
        map_folder = path.join(self.game_folder, 'map')
        self.map = Map(path.join(map_folder, map_selection ))

    def end_screen(self): #end screen
        self.screen.fill(BLACK)
        self.draw_text("Game Over",self.title_font ,40 ,WHITE ,WIDTH / 2 - 60 ,100)
        self.draw_text("Thanks for playing", self.title_font, 40, WHITE, WIDTH / 2 -120, 150)
        self.draw_text("Press any key to restart", self.title_font, 25, WHITE, WIDTH / 2 -90, 200)
        img_folder  = path.join(self.game_folder,'img')
        thanks_image = pg.image.load(path.join(img_folder,'thanks.jpg')).convert_alpha()
        self.screen.blit(thanks_image,(WIDTH/2 - 450, 250))
        pg.display.flip()
        self.wait_for_key()

# Create the game object
g = Game()
g.start_screen()
g.select_map()
g.select_map()
while True:
    g.new()
    g.run()
    g.end_screen()
