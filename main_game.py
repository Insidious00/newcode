import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from map_change import *
import time
import math
import random
from itemDict import *
from pygame_functions import *



class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        screenSize(800,700)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font("arial")
        self.load_data()
        self.i = 0
        self.doorlist = []
        self.doortype = []
        self.IDList = []
        self.status = "start"
        self.newplayer = True
        self.text_true = False
        self.newpos = []
        self.health = 100
        self.magic = 100
        self.MapChange = MapChange(self, "town")
        self.firsttime = True
        self.labelText = ""
        self.labelsize = 30
        self.labelx = WIDTH/2
        self.labely =HEIGHT/2
        self.labelColour ="White"
        self.labelFont ="Arial"

    def load_data(self):
        self.maps = ['Pygame_Map.tmx']
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'img')
        self.map_folder = path.join(self.game_folder, 'maps')
        self.sound_folder = path.join(self.game_folder, 'sounds')

        self.map = TiledMap(path.join(self.map_folder, 'New_World.tmx'))
        self.map1 = TiledMap(path.join(self.map_folder, 'New_World.tmx'))
        self.map2 = TiledMap(path.join(self.map_folder, 'Inner_House1.tmx'))
        self.map3 = TiledMap(path.join(self.map_folder, 'Inner_House2.tmx'))

        self.map_img = self.map.make_map()
        self.map_img1 = self.map1.make_map()
        self.map_img2 = self.map2.make_map()
        self.map_img3 = self.map3.make_map()
        self.map_rect = self.map_img.get_rect()
        self.map1_rect = self.map_img1.get_rect()
        self.map2_rect = self.map_img2.get_rect()
        self.map3_rect = self.map_img3.get_rect()
        self.player_img = pg.image.load(path.join(self.img_folder, PLAYER_IMG4[0])).convert_alpha()
        self.npc_image = pg.image.load(path.join(self.img_folder, NPC_IMAGE1)).convert_alpha()
        self.npc_image1 = pg.image.load(path.join(self.img_folder, NPC_IMAGE2)).convert_alpha()
        self.wall_img = pg.image.load(path.join(self.img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.logo_img = pg.image.load(path.join(self.img_folder, LOGO_IMG)).convert_alpha()
        self.dialogueBackground = pg.image.load(path.join(self.img_folder, dialogueBack)).convert_alpha()

    def new(self):
        pg.mixer.music.load("ambience.mp3")
        pg.mixer.music.play(-1)
        self.newpos = []
        self.doorlist = []
        self.doortype = []
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.npc = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                if self.newplayer == True:
                    self.player = Player(self, tile_object.x, tile_object.y, self.health, self.magic)
                    self.newplayer = False
                else:
                    self.player = Player(self, self.player.pos[0], self.player.pos[1], self.player.health, self.player.magic)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'door':
                door = Door(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.name, tile_object.type)
                self.doorlist.append(door)
                self.doortype.append(tile_object.type)
            if tile_object.name == 'npc':
                NPC(self, tile_object.x, tile_object.y,tile_object.width, tile_object.height, tile_object.type)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

    def run(self):
        self.playing = True
        while self.playing:
            self.vLocation = self.check_location()
            if self.vLocation:
                self.MapChange.change(self.vLocation.type)
                self.backtrack = self.vLocation
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.player.interact(self.player, self.npc)
            self.draw()
            self.chatLabel = makeLabel(self.labelText, self.labelsize, self.labelx, self.labely, self.labelColour, self.labelFont)
            self.chatLabel.rect.center = (WIDTH/2, 18)
            showLabel(self.chatLabel)
            
    def move_player(self, player, x, y):
        player.pos = vec(x, y)

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        self.screen.fill((BLACK))
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.npc:
            self.screen.blit(sprite.image, (self.camera.apply(sprite)[0]-16, self.camera.apply(sprite)[1]-32))

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    print(self.player.pos)
                if event.key == pg.K_SPACE:
                    if self.check_npc_close():
                        self.talk(self.check_npc_close(), "Hey, How can I help you?")
                if event.key == pg.K_F1:
                    self.MapChange.brooktown()
                if event.key == pg.K_F2:
                    self.MapChange.house1()
                if event.key == pg.K_i:
                    self.openInventory()

    def check_location(self):
        for i in self.doorlist:
            if math.sqrt((i.x - self.player.pos[0])**2 + (i.y - self.player.pos[1])**2) < 30:
                return i

    def check_npc_close(self):
        for i in self.npc:
            if math.sqrt((i.x - self.player.pos[0])**2 + (i.y - self.player.pos[1])**2) < 70:
                print(i.name)
                return(i)

    def openInventory(self):
        self.inventoryimages = []
        self.screen.blit(pg.image.load(path.join(self.img_folder, "invBG.png")),(0,0))
        for i in range(0,len(self.player.inventory)):
            for r in range(1,len(itemDict)):
                if itemDict[str(1)]["id"] == self.player.inventory[i]:
                    self.inventoryimages.append(pg.image.load(path.join(self.img_folder, itemDict[str(r)]["image"])).convert_alpha())
        counter = 0
        for i in self.inventoryimages:
            self.screen.blit(i, (invPos[counter]))
            counter +=1

            #Create a sprite with the image that can check for collisions

       
               
        pygame.display.update()
        time.sleep(10)
    
            
    def talk(self, npc, reply):
        self.npc_obj = npc
        self.screen.blit(pygame.transform.scale(self.dialogueBackground, (800,800)), (0,0))
        self.screen.blit(pygame.transform.scale(self.npc_obj.image, (500, 600)),(400,200))
        self.label1text = reply
        self.label_List = []
        if self.npc_obj.name == "steven":
            self.chatLabel = makeLabel(self.label1text, 40, 100, 100, "White", "Arial", "clear")
            self.chatLabel.rect.center = (400, 25)
            showLabel(self.chatLabel)
            self.label_List.append(self.chatLabel)
            self.chatLabel1 = makeLabel("1) Who are you?", 40, 300, 150, "White", "Arial", "clear")
            showLabel(self.chatLabel1)
            self.label_List.append(self.chatLabel1)
            self.chatLabel2 = makeLabel("2) Any work?", 40, 300, 300, "White", "Arial", "clear")
            showLabel(self.chatLabel2)
            self.label_List.append(self.chatLabel2)
            self.chatLabel3 = makeLabel("3) Thanks", 40, 300, 450, "White", "Arial", "clear")
            showLabel(self.chatLabel3)
            self.label_List.append(self.chatLabel3)
            self.chatLabel4 = makeLabel("Press a Key (1, 2 or 3)...", 40, 300, 600, "White", "Arial", "clear")
            showLabel(self.chatLabel4)
            self.label_List.append(self.chatLabel4)
            self.wordbox = makeTextBox(150, 500, 300, 0, "Press a Key (1, 2 or 3)...", 20, 24)
            showLabel(self.wordbox)
            entry = textBoxInput(self.wordbox)
            if entry == "1":
                self.hide_Labels()
                hideTextBox(self.wordbox)
                pygame.display.update()
                self.talk(self.npc_obj, "My name is Steven")
            if entry == "2":
                self.hide_Labels()
                hideTextBox(self.wordbox)
                pygame.display.update()
                self.talk(self.npc_obj, "Try the blacksmith!")
            if entry == "3":
                self.hide_Labels()
                hideTextBox(self.wordbox)
                pygame.display.update()
                
            else:
                self.hide_Labels()
                hideTextBox(self.wordbox)
                pygame.display.update()

                
        if self.npc_obj.name == "blacksmith":
            self.chatLabel = makeLabel(self.label1text, 40, 100, 100, "White", "Arial", "clear")
            self.chatLabel.rect.center = (400, 25)
            showLabel(self.chatLabel)
            self.label_List.append(self.chatLabel)
            self.chatLabel1 = makeLabel("1) Who are you?", 40, 300, 150, "White", "Arial", "clear")
            showLabel(self.chatLabel1)
            self.label_List.append(self.chatLabel1)
            self.chatLabel2 = makeLabel("2) Any work?", 40, 300, 300, "White", "Arial", "clear")
            showLabel(self.chatLabel2)
            self.label_List.append(self.chatLabel2)
            self.chatLabel3 = makeLabel("3) Thanks", 40, 300, 450, "White", "Arial", "clear")
            showLabel(self.chatLabel3)
            self.label_List.append(self.chatLabel3)
            self.chatLabel4 = makeLabel("Press a Key (1, 2 or 3)...", 40, 300, 600, "White", "Arial", "clear")
            showLabel(self.chatLabel4)
            self.label_List.append(self.chatLabel4)
            self.wordbox = makeTextBox(150, 500, 300, 0, "Press a Key (1, 2 or 3)...", 20, 24)
            showLabel(self.wordbox)
            entry = textBoxInput(self.wordbox)
            if entry == "1":
                self.hide_Labels()
                hideTextBox(self.wordbox)
                pygame.display.update()
                self.talk(self.npc_obj, "Im the village Blacksmith")
            if entry == "2":
                self.hide_Labels()
                hideTextBox(self.wordbox)
                pygame.display.update()
                self.talk(self.npc_obj, "Finally!, I have added it to your quest book!.")
##                self.missions.blacksmith_quest_recieved = True
            if entry == "3":
                self.hide_Labels()
                hideTextBox(self.wordbox)
                pygame.display.update()
            else:
                self.hide_Labels()
                hideTextBox(self.wordbox)
                pygame.display.update()
                
    def hide_Labels(self):
        for i in self.label_List:
            hideLabel(i)
    
    def show_start_screen(self):
##        fade = pygame.Surface((WIDTH, HEIGHT))
##        fade.fill((255,255,255))
##        for alpha in range(0, 300):
##            fade.set_alpha(alpha)
##            #self.redrawWindow()
##            self.screen.blit(fade, (0,0))
##            pygame.display.update()
##            pygame.time.delay(2)
##        #self.screen.blit(self.logo_img, (100,100))
##        pygame.display.update()
##        x = WIDTH/2 - self.logo_img.get_width()/2
##        y = HEIGHT/2 - self.logo_img.get_width()/2
##        temp = pygame.Surface((self.logo_img.get_width(), self.logo_img.get_height())).convert()
##        for i in range(0,255):
##            temp.blit(self.screen, (-x, -y))
##            temp.blit(self.logo_img, (0, 0))
##            temp.set_alpha(i)        
##            self.screen.blit(temp, (x,y))
##            pygame.display.flip()
##            time.sleep(0.01)
##        self.screen.fill((255,255,255))
##        pygame.display.flip()
##        for i in range(0,255):
##            self.screen.fill((255,255,255))
##            temp.blit(self.screen, (-x, -y))
##            temp.blit(self.logo_img, (0, 0))
##            temp.set_alpha(255-i)        
##            self.screen.blit(temp, (x,y))
##            pygame.display.flip()
##            time.sleep(0)
##        time.sleep(2)
##        fade.fill((0,0,0))
##        for alpha in range(0, 300):
##            fade.set_alpha(alpha)
##            self.screen.blit(fade, (0,0))
##            pygame.display.update()
##            time.sleep(0.01)
##            pygame.time.delay(0)
##        self.startText("Welcome to Newcrest...")
##        
##        fade.fill((255,255,255))
##        for alpha in range(0, 300):
##            fade.set_alpha(alpha)
##            self.screen.blit(fade, (0,0))
##            pygame.display.update()
##            time.sleep(0.01)
##            pygame.time.delay(0)
        pass
        
        

    def startText(self, text):
        startLabel = makeLabel(text, 50, WIDTH/2, HEIGHT/2, "White", "Arial")
        startLabel.rect.center = (WIDTH/2, HEIGHT/2)
        showLabel(startLabel)
        time.sleep(4)
        
        hideLabel(startLabel)
        pygame.display.flip()
        
        startLabel = makeLabel("You dont remember how you got here...", 30, WIDTH/2, HEIGHT/2, "White", "Arial")
        startLabel.rect.center = (WIDTH/2, HEIGHT/2)
        showLabel(startLabel)
        time.sleep(4)

        hideLabel(startLabel)
        pygame.display.flip()

        startLabel = makeLabel("What is your name?", 30, WIDTH/2, HEIGHT/2, "White", "Arial")
        showLabel(startLabel)
        startLabel.rect.center = (WIDTH/2, HEIGHT/2)
        nameEnt = makeTextBox(WIDTH/2, HEIGHT/2 + 80, 300, 0, "Enter name here...", 0, 24)
        nameEnt.rect.center = (WIDTH/2, HEIGHT/2 + 80)
        entry = textBoxInput(nameEnt)
        hideLabel(startLabel)
        hideTextBox(nameEnt)
            

    def redrawWindow(self):
        self.screen.fill((0,0,0))
        pass

    def show_go_screen(self):
        pass


# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()








