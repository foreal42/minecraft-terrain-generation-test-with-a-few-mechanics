import pygame as pg
import random

pg.init()

screenwidth = 1900
screenheight = 500

display = pg.display.set_mode((screenwidth, screenheight))
pg.display.set_caption("tsc jumping sim beta 4.5")

grass = pg.transform.scale(pg.image.load("C:/Users/yousef_al-salem/Onedrive - Nord Anglia Education/NAE - Files/Documents/Pictures/Untitled.png").convert_alpha(), (50, 50))
dirt = pg.transform.scale(pg.image.load("C:/Users/yousef_al-salem/Onedrive - Nord Anglia Education/NAE - Files/Documents/Pictures/dirt block texture.jfif").convert_alpha(), (50, 50))
no_walk = pg.transform.scale(pg.image.load("C:/Users/yousef_al-salem/OneDrive - Nord Anglia Education/NAE - Files/Documents/Pictures/ssc.png").convert_alpha(), (50, 50))
runninganim = pg.transform.scale(pg.image.load("C:/Users/yousef_al-salem/OneDrive - Nord Anglia Education/NAE - Files/Documents/Pictures/sscrun.png").convert_alpha(), (50, 50))
jumping = pg.transform.scale(pg.image.load("C:/Users/yousef_al-salem/Onedrive - Nord Anglia Education/NAE - Files/Desktop/tsc jumping.png").convert_alpha(), (50, 50))
alan_bg = pg.transform.scale(pg.image.load("C:/Users/yousef_al-salem/OneDrive - Nord Anglia Education/NAE - Files/Documents/Pictures/alan bg.jfif").convert(), (1900, 500))

clock = pg.time.Clock()
run = True
fps = 120

class Player:
    def __init__(self):
        self.rect = pg.FRect(50, 50, 50, 50)
        self.velocity = 0
        self.xvelocity = 0
        self.canjump = True
        self.dragging = False
        self.cancollide = True
        self.running = False

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
        if pg.key.get_pressed()[pg.K_a] and self.canjump == True:
            display.blit(runninganim, self.rect)
        elif pg.key.get_pressed()[pg.K_d] and self.canjump == True:
            display.blit(pg.transform.flip(runninganim, True, False), self.rect)
        elif self.canjump == False:
            display.blit(jumping, self.rect)
        elif pg.key.get_pressed()[pg.K_d] and self.canjump == False:
            display.blit(pg.transform.flip(runninganim, True, False), self.rect)
        elif pg.key.get_pressed()[pg.K_a] and self.canjump == False:
            display.blit(jumping, self.rect)
        else:
            display.blit(no_walk, self.rect)

class Block:
    def __init__(self, pos):
        self.rect = pg.FRect(pos[0], pos[1], 50, 50)
        self.velocity = 0
        self.xvelocity = 0
        self.touched = False
        self.canjump = True
        self.cancollide = False
        self.dragging = False
        if pos[1] >= 300:
            self.grassblock = False
        else:
            self.grassblock = True

    def update(self, entity):
        for entities in entity:
            if entities == self:# or self.dragging or entities.dragging:
                continue

            if self.rect.colliderect(entities) and entities.cancollide == True:
                entities.velocity = 0
                entities.rect.bottom = self.rect.top
                entities.canjump = True

            elif self.rect.colliderect(entities) and entities.cancollide == True:
                entities.velocity = 0
                entities.rect.bottom = self.rect.top
                entities.canjump = True

        if self.touched == True:
            self.rect.x += self.xvelocity * dt
            self.rect.y += self.velocity * dt
            self.velocity += 1600 * dt
            self.cancollide = True
            
        # if self.velocity > 4000:
        #     self.velocity = 3500
        # if self.velocity < -4000:
        #     self.velocity = -3500

        self.updatedmousepos = pg.mouse.get_pos()
        self.updatedmouse = pg.mouse.get_pressed()
        self.boxleft = self.rect.centerx - 25
        self.boxright = self.rect.centerx + 25
        self.boxtop = self.rect.centery - 25
        self.boxbottom = self.rect.centery + 25
        self.dragging = False

        if self.updatedmouse[0] and self.updatedmousepos[0] > self.boxleft and self.updatedmousepos[0] < self.boxright and self.updatedmousepos[1] > self.boxtop and self.updatedmousepos[1] < self.boxbottom:
            self.rect.centery = self.updatedmousepos[1]
            self.rect.centerx = self.updatedmousepos[0]
            self.xvelocity = 0
            self.velocity = 0
            self.dragging = True
            self.touched = True
            self.cancollide = True

    def render(self):
        if self.grassblock == True:
            display.blit(grass, self.rect)
        if self.grassblock == False:
            display.blit(dirt, self.rect)

listofhieghts = [-1, 0, 1]

def generate_terrain():
    global blockslist
    blockslist = []
    coords = []
    y = 6
    for x in range(int(screenwidth / 50)):
        for _ in range(int(screenheight / 50)):
            y += random.choice(listofhieghts)
            while y > (screenheight / 50): 
                y -= 1
            while y < 5:
                y += 1

            if ((x)*50, y*50) in coords:
                continue
            coords.append(((x)*50, y*50))
            blockslist.append(Block(((x)*50, y*50)))

    # for x in range(int(screenwidth / 50)):
    #     h = random.randint(2, 10)
    #     for y in range(h):
    #         blockslist.append(Block(((x)*50, screenheight - y*50)))

player = Player()
generate_terrain()

print(len(blockslist))
while run:
    dt = clock.tick(fps) * 0.001
    display.blit(alan_bg, (0, 0))

    player.update()
    player.render()

    for blocks in blockslist:
        blocks.update([player] + blockslist)
        blocks.render()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.update()
