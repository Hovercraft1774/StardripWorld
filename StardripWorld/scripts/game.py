from scripts.settings import *
from scripts.player import *
from scripts.tilemap import *

class Game(object):

    def __init__(self):
        self.playing = True
        pg.init()
        pg.mixer.init() #if using online editor, take this out
        # creates a screen for the game
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE) #Title of the screen window
        # creates time
        self.clock = pg.time.Clock()
        pg.key.set_repeat(300,200)
        self.backgroundColor = BLACK
        self.font_name = pg.font.match_font(FONT_NAME)

        self.load_snd()
        self.load_date()
        self.new()

    def load_date(self):
        self.map = Map(MAP)
        self.bg_img = pg.image.load(GRASS_BACKGROUND).convert()
        self.bg_img = pg.transform.scale(self.bg_img, (WIDTH * 1.15, HEIGHT * 1.15))

        # self.spritesheet = Spritesheet(SPRITESHEET)


    def new(self):
        # create Sprite Groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.wall_group = pg.sprite.Group()
        self.interactables_group = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.hud_group = pg.sprite.Group()
        self.transparent_group = pg.sprite.Group()
        self.breakable_group = pg.sprite.Group()
        self.request_group = pg.sprite.Group()
        self.last_update = pg.time.get_ticks()

        #walls/map data
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'A':
                    Wall(self, col, row, wall_img, self.backgroundColor)
                elif tile == 'P':
                    self.player = Player(self, col, row, player_img, BLACK)
                #elif tile == 'W':
                    #Wall(self, col, row, wheat_img, self.backgroundColor, False)
                elif tile == 'M':
                    InteractionSpots(self, col, row, milk_img, self.backgroundColor,'Milk')
                elif tile == '.':
                     TransparentObject(self,col,row,grass_img,self.backgroundColor)
                elif tile == 'S':
                    Wall(self, col, row, stone_img, self.backgroundColor)
                elif tile == 'B':
                    RequestStations(self, col, row, book_img, self.backgroundColor,[5,1,10,7,6,10,4,2],['Apple','Cherry','Fish','Pepper','Wheat','Strawberry','Egg','Milk'],'Cake',999)
                elif tile == 'C':
                    TransparentObject(self, col, row, cake_img, self.backgroundColor)
                elif tile == 'E':
                    InteractionSpots(self, col, row, apple_img, self.backgroundColor,'Apple')
                elif tile == 'G':
                    InteractionSpots(self, col, row, egg_img, self.backgroundColor,'Egg')
                elif  tile == 'F':
                    Wall(self,col,row,fire_img,self.backgroundColor)
                elif tile == 'T':
                    Wall(self,col,row,tree_img,self.backgroundColor)
                elif tile == 'R':
                    Wall(self,col,row,water_tree_img,self.backgroundColor)
                elif tile == 'U':
                    InteractionSpots(self,col,row,fish_img,self.backgroundColor,'Fish')
                elif tile == 'H':
                    InteractionSpots(self,col,row,cherry_img,self.backgroundColor,'Cherry')
                elif tile == '0':
                    Wall(self,col,row,waterTree_img,self.backgroundColor)
                elif tile == '9':
                    Wall(self,col,row,house_img,self.backgroundColor)
                elif tile == '8':
                    Wall(self,col,row,lava_img,self.backgroundColor)
                elif tile == '6':
                    Wall(self,col,row,water_img,self.backgroundColor)
                elif tile == '3':
                    InteractionSpots(self,col,row,strawberry_img,self.backgroundColor,'Strawberry')
                elif tile == '4':
                    InteractionSpots(self,col,row,pepper_img,self.backgroundColor,'Pepper')
                elif tile == 'W':
                    InteractionSpots(self,col,row,wheat_img,WHITE,'Wheat')

        self.text = Hud(self, 0,0, cake_img,BLACK)
        self.camera = Camera(self.map.width, self.map.height)
        self.load_music(MAIN_THEME)
        #create enemy objects


    def gameLoop(self):
        pg.mixer.music.play(loops=-1)
        while self.playing:
            #tick clock
            self.dt = self.clock.tick(fps)/1000
            self.clock.tick(fps)

            #check events
            self.check_Events()

            #update all
            self.update()

            #draw
            self.draw()
        pg.mixer.music.fadeout(500)


    def check_Events(self):
        if "Cake" in self.player.inventory:
            self.playing = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_e:
                    self.player.interact()





    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)



    def draw(self):
        self.screen.fill(self.backgroundColor)
        self.screen.blit(self.bg_img, self.bg_img.get_rect())
        for i in range(5):
            for sprite in self.all_sprites:
                if sprite._layer == i+1:
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.hud_group.draw(self.screen)
        self.draw_text(self.player.last_request + " x " + str(self.player.last_amount), 38, WHITE,self.text.rect.x + 150, self.text.rect.top+30)



        # think whiteboard, must be last line
        pg.display.flip()

    def wait_for_key(self,boolien=False):
        waiting = True

        while waiting:
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                    pg.quit()
                if boolien:
                    if event.type == pg.KEYUP:
                        if event.key == pg.K_y:
                            self.confirm_snd.play()
                            return True
                        elif event.key == pg.K_n:
                            self.confirm_snd.play()
                            return False
                else:
                    if event.type == pg.KEYUP:
                        self.confirm_snd.play()
                        waiting = False

    def load_snd(self):
        # self.player_death_snd = pg.mixer.Sound(player_death_sound)
        # self.enemy_death_snd = pg.mixer.Sound(enemy_death_sound)
        # self.bullet_snd = pg.mixer.Sound(bullet_sound)
        self.confirm_snd = pg.mixer.Sound(CONFIRM_SOUND)
        self.bad_snd = pg.mixer.Sound(BAD_SOUND)
        self.collect_snd = pg.mixer.Sound(COLLECT_SOUND)
        # self.enemy_death_snd.set_volume(0.3)
        # self.player_death_snd.set_volume(0.5)
        # self.bullet_snd.set_volume(0.2)
        self.confirm_snd.set_volume(0.7)
        self.bad_snd.set_volume(1)
        self.bad_snd.set_volume(1)

    def load_music(self, music):
        self.track1 = pg.mixer.music.load(music)
        pg.mixer.music.set_volume(0.3)

    def start_Screen(self):
        # game splash/start screen
        pg.mixer.music.load(MAIN_THEME)
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.1)
        self.screen.fill(BLUE)
        self.draw_text(TITLE, 80, WHITE, WIDTH / 2, HEIGHT / 4 + 50)
        self.draw_text("Use WASD to move, E to interact, and Left Shift to sprint", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4 - 50)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("Try and make the cake!", 40, WHITE, WIDTH / 2, HEIGHT / 4 + 200)
        self.draw_text("Use the book to get hints and baket8", 40, WHITE, WIDTH / 2, HEIGHT / 4 + 250)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def end_Screen(self):
        pg.mixer.music.load(MAIN_THEME)
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.1)
        self.screen.fill(LIGHT_BLUE)
        self.draw_text("Congratulations! You made the cake", 45, YELLOW, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press Y or N to quit", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key(True)
        return False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)