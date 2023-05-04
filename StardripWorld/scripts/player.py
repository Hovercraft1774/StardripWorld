from scripts.settings import *

# class Spritesheet:
#     # utility class for loading and parsing spritesheets
#     def __init__(self, filename):
#         self.spritesheet = pg.image.load(filename).convert()
#
#     def get_image(self, x, y, width, height):
#         # grab an image out of a larger spritesheet
#         image = pg.Surface((width, height))
#         image.blit(self.spritesheet, (0, 0), (x, y, width, height))
#         image = pg.transform.scale(image, (width // 2, height // 2))
#         return image

class Player(pg.sprite.Sprite):#must be a sprite inherited otherwise it won't fit in groups

    def __init__(self,game,x,y,img_dir,color_key):
        self._layer = 3
        super(Player,self).__init__()
        # self.player_img = pg.transform.flip(self.player_img, True, True) #this flips the image along the x,y axis
        self.game = game #adds reference to the game
        self.image = self.get_image(img_dir)
        self.image.set_colorkey(color_key)#gets rid of black color and makes it transparent
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.rect.center = (self.x,self.y)
        self.inventory = {}
        self.speed = PLAYER_SPEED
        self.coins = 0
        self.last_request = ""
        self.last_amount = ""

        self.addToGroups()

    def addToGroups(self):
        self.game.all_sprites.add(self)
        self.game.player_group.add(self)

    def get_image(self,img_dir):
        self.img = pg.image.load(img_dir).convert()
        self.img = pg.transform.scale(self.img, (TILE_SIZE, TILE_SIZE))
        return self.img

    def get_keys(self):
        # checks if a key is pressed
        self.vx,self.vy = 0,0
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] or keys[pg.K_w]:  # if key is being pressed, move up
            self.vy = -self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:  # if key is being pressed, move down
            self.vy = self.speed
        if keys[pg.K_LEFT] or keys[pg.K_a]:  # if key is being pressed, move left
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:  # if key is being pressed, move right
            self.vx = self.speed
        if keys[pg.K_LSHIFT]:
            self.speed = PLAYER_SPEED*2
        else:
            self.speed = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def collide_with_walls(self,dir):

        hits = pg.sprite.spritecollide(self, self.game.wall_group, False)
        if hits:
            if dir == 'x':
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
            if dir == 'y':
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def check_breakable(self,dir):
        hits = pg.sprite.spritecollide(self, self.game.breakable_group, False)
        if hits:
            if hits[0].needed_object != None:
                needed_object = hits[0].needed_object
                if needed_object in self.inventory and self.inventory.get(hits[0].needed_object)>0:
                    hits[0].new_object
                    hits[0].kill()
                    self.inventory[needed_object] -= 1
            if not hits[0].broken:
                if dir == 'x':
                    if self.vx > 0:
                        self.x = hits[0].rect.left - self.rect.width
                    if self.vx < 0:
                        self.x = hits[0].rect.right
                    self.vx = 0
                    self.rect.x = self.x
                if dir == 'y':
                    if self.vy > 0:
                        self.y = hits[0].rect.top - self.rect.height
                    if self.vy < 0:
                        self.y = hits[0].rect.bottom
                    self.vy = 0
                    self.rect.y = self.y

    def interact(self):
        hits = pg.sprite.spritecollide(self,self.game.interactables_group,False)
        if hits:
            item = hits[0].resource
            if item not in self.inventory:
                self.inventory[item] = 1
            else:
                self.inventory[item] += 1
            self.game.collect_snd.play()
            print(self.inventory)

        hits = pg.sprite.spritecollide(self, self.game.request_group, False)
        if hits:
            checks = 0
            for i in range(len(hits[0].items_requested)):
                item = hits[0].items_requested[i]
                if item in self.inventory and self.inventory.get(item) >= hits[0].amount_requested[i]:
                    checks += 1
                elif item not in self.inventory or self.inventory.get(item) < hits[0].amount_requested[i]:
                    self.last_request = str(item)
                    self.last_amount = str(hits[0].amount_requested[i])
                    self.game.bad_snd.play()
                print(self.inventory)
                if checks >= len(hits[0].items_requested):
                    reward = hits[0].reward
                    if reward not in self.inventory:
                        self.inventory[reward] = hits[0].reward_amount
                    else:
                        self.inventory[reward] += hits[0].reward_amount
                    self.game.confirm_snd.play()

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.check_breakable('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.check_breakable('y')


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, img_dir, color_key):
        self._layer = 1
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.get_image(img_dir)
        self.image.set_colorkey(color_key)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*TILE_SIZE
        self.rect.y = y*TILE_SIZE
        self.addToGroups()

    def addToGroups(self):
        self.game.all_sprites.add(self)
        self.game.wall_group.add(self)

    def get_image(self,img_dir):
        self.img = pg.image.load(img_dir).convert()
        self.img = pg.transform.scale(self.img, (TILE_SIZE, TILE_SIZE))
        return self.img

class TransparentObject(pg.sprite.Sprite):
    def __init__(self, game, x, y, img_dir, color_key):
        self._layer = 1
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.get_image(img_dir)
        self.image.set_colorkey(color_key)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*TILE_SIZE
        self.rect.y = y*TILE_SIZE
        self.addToGroups()

    def addToGroups(self):
        self.game.all_sprites.add(self)
        self.game.transparent_group.add(self)

    def get_image(self,img_dir):
        self.img = pg.image.load(img_dir).convert()
        self.img = pg.transform.scale(self.img, (TILE_SIZE, TILE_SIZE))
        return self.img

class InteractionSpots(pg.sprite.Sprite):
    def __init__(self, game, x, y, img_dir, color_key, resource):
        self._layer = 1
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.get_image(img_dir)
        self.image.set_colorkey(color_key)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*TILE_SIZE
        self.rect.y = y*TILE_SIZE
        self.resource = resource
        self.addToGroups()

    def addToGroups(self):
        self.game.all_sprites.add(self)
        self.game.interactables_group.add(self)

    def get_image(self,img_dir):
        self.img = pg.image.load(img_dir).convert()
        self.img = pg.transform.scale(self.img, (TILE_SIZE, TILE_SIZE))
        return self.img

class Hud(pg.sprite.Sprite):
    def __init__(self, game, x, y, img_dir, color_key):
        self._layer = 6
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.get_image(img_dir)
        self.image.set_colorkey(color_key)
        self.rect = self.image.get_rect()
        self.offsetx = x
        self.offsety = y
        self.rect.x = self.offsetx*TILE_SIZE
        self.rect.y = self.offsety*TILE_SIZE
        self.addToGroups()

    def addToGroups(self):
        self.game.hud_group.add(self)

    def get_image(self,img_dir):
        self.img = pg.image.load(img_dir).convert()
        self.img = pg.transform.scale(self.img, (TILE_SIZE, TILE_SIZE))
        return self.img
    def update(self):

        self.x = self.game.player.x + self.offsetx
        self.y = self.game.player.y + self.offsety

class BreakableObjects(pg.sprite.Sprite):
    def __init__(self, game, x, y, img_dir, color_key,transformation,needed_object=None):
        self._layer = 1
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.color_key = color_key
        self.image = self.get_image(img_dir)
        self.image.set_colorkey(self.color_key)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.needed_object = needed_object
        self.new_object = transformation
        self.broken = False
        self.addToGroups()

    def addToGroups(self):
        self.game.all_sprites.add(self)
        self.game.breakable_group.add(self)

    def get_image(self, img_dir):
        self.img = pg.image.load(img_dir).convert()
        self.img = pg.transform.scale(self.img, (TILE_SIZE, TILE_SIZE))
        return self.img

class RequestStations(pg.sprite.Sprite):
    def __init__(self, game, x, y, img_dir, color_key,amount_requested=[],items_requested=[],reward="",reward_amount=1):
        self._layer = 2
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.get_image(img_dir)
        self.image.set_colorkey(color_key)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.amount_requested = amount_requested
        self.items_requested = items_requested
        self.reward = reward
        self.reward_amount = reward_amount
        self.addToGroups()

    def addToGroups(self):
        self.game.all_sprites.add(self)
        self.game.request_group.add(self)

    def get_image(self, img_dir):
        self.img = pg.image.load(img_dir).convert()
        self.img = pg.transform.scale(self.img, (TILE_SIZE, TILE_SIZE))
        return self.img
