import pygame as pg
import random

pg.init()

screenwidth = 1900
screenheight = 500

display = pg.display.set_mode((screenwidth, screenheight))

clock = pg.time.Clock()
run = True
fps = 60

class Player:
    def __init__(self):
        self.rect = pg.FRect(50, 50, 50, 50)
        self.velocity = 0
        self.xvelocity = 0
        self.canjump = True

    def update(self):
        self.rect.x += self.xvelocity * dt
        self.rect.y += self.velocity * dt
        self.xvelocity /= 6 ** dt
        self.velocity += 1800 * dt

        if pg.key.get_just_pressed()[pg.K_SPACE] and self.canjump == True:
            self.velocity = -50700 * dt
            self.canjump = False
        if pg.key.get_pressed()[pg.K_d]:
            self.xvelocity += 1700 * dt
        if pg.key.get_pressed()[pg.K_a]:
            self.xvelocity -= 1700 * dt
        if pg.key.get_pressed()[pg.K_r]:
            self.rect = pg.FRect(50, 50, 50, 50)

    def render(self):
        pg.draw.rect(display, (255, 255, 255), self.rect)

class Block:
    def __init__(self, pos):
        self.rect = pg.FRect(pos[0], pos[1], 50, 50)
        self.velocity = 0
        self.xvelocity = 0
        self.touched = False

    def update(self, entity):
        for entities in entity:
            if self.rect.colliderect(entities):
                entities.velocity = 0
                entities.rect.bottom = self.rect.top
                entities.canjump = True

        if self.touched == True:
            self.rect.x += self.xvelocity * dt
            self.rect.y += self.velocity * dt
            self.velocity += 1600 * dt

        self.updatedmousepos = pg.mouse.get_pos()
        self.updatedmouse = pg.mouse.get_pressed()
        self.boxleft = self.rect.centerx - 25
        self.boxright = self.rect.centerx + 25
        self.boxtop = self.rect.centery - 25
        self.boxbottom = self.rect.centery + 25

        if self.updatedmouse[0] and self.updatedmousepos[0] > self.boxleft and self.updatedmousepos[0] < self.boxright and self.updatedmousepos[1] > self.boxtop and self.updatedmousepos[1] < self.boxbottom:
            self.rect.centery = self.updatedmousepos[1]
            self.rect.centerx = self.updatedmousepos[0]
            self.xvelocity = 0
            self.velocity = 0
            self.touched = True

    def render(self):
        pg.draw.rect(display, (0, 255, 0), self.rect)

listofhieghts = [-1, 0, 1]

def generate_terrain():
    global blockslist
    blockslist = []
    y = 6
    for x in range(int(screenwidth / 50)):
        for _ in range(int(screenheight / 50)):
            y += random.choice(listofhieghts)
            while y > (screenheight / 50):
                y -= 1
            while y < 5:
                y += 1
            blockslist.append(Block(((x)*50, y*50)))

    # for x in range(int(screenwidth / 50)):
    #     h = random.randint(2, 10)
    #     for y in range(h):
    #         blockslist.append(Block(((x)*50, screenheight - y*50)))

player = Player()
generate_terrain()

while run:
    dt = clock.tick(fps) * 0.001
    display.fill((0,0,0))

    player.update()
    player.render()

    for blocks in blockslist:
        blocks.update([player])
        blocks.render()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.update()