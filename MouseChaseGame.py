import pygame,random,math

def nextChaserPos(myPos,targetPos):
    # ~ return (random.randint(-1,1),random.randint(-1,1))
	# Find direction vector (dx, dy) between enemy and player.
	dx, dy = targetPos[0] - myPos[0], targetPos[1] - myPos[1]
	dist = math.hypot(dx, dy)
	if dist == 0.0:
		setGameOver()
		
	try:
		dx, dy = dx / dist, dy / dist
	except ZeroDivisionError:
		next_x = next_y = 0
	
	try:
		next_x = (dx/abs(dx))
	except ZeroDivisionError:
		next_x = 0
		
	try:
		next_y = (dy/abs(dy))
	except ZeroDivisionError:
		next_y = 0
		
	return [next_x, next_y]
   

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(pygame.Color('red1'))
        self.rect = self.image.get_rect()
        self.rect.center = (Engine.screenSize[0] / 2, Engine.screenSize[1] / 2)

    def update(self,pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        if self.rect.left > Engine.screenSize[0]-10:
            self.rect.right = Engine.screenSize[0]-10
        if self.rect.right < 10:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.bottom = 10
        if self.rect.bottom > Engine.screenSize[1]:
            self.rect.top = Engine.screenSize[1]-10

class Chaser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(pygame.Color('cyan'))
        self.rect = self.image.get_rect()
        self.rect.center = ((random.randint(0,Engine.screenSize[0])), (random.randint(0,Engine.screenSize[1])))

    def update(self,mousePos):
        if Engine.isGameOver == True:
            return
        chaserPos = nextChaserPos((self.rect.x,self.rect.y),mousePos)
        print(chaserPos,self.rect.x,self.rect.y)
        self.rect.x += chaserPos[0]
        self.rect.y += chaserPos[1]
        if self.rect.left > Engine.screenSize[0]-10:
            self.rect.right = Engine.screenSize[0]-10
        if self.rect.right < 10:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.bottom = 10
        if self.rect.bottom > Engine.screenSize[1]:
            self.rect.top = Engine.screenSize[1]-10


class Engine:
    pass

def main():
    pygame.init()
    pygame.display.set_caption('The Mouse Chase')
    Engine.screenSize = (600,400)
    Engine.surface = pygame.display.set_mode(Engine.screenSize)
    pygame.mouse.set_visible(False)
    Engine.clock = pygame.time.Clock()
    Engine.delta = 0
    Engine.fps = 30
    Engine.player = Player()
    Engine.chaserCount = 4
    Engine.isGameOver = False

    Engine.on_event = eventloop
    Engine.on_draw = drawloop

    Engine.all_sprites = pygame.sprite.Group()
    Engine.all_sprites.add(Engine.player)
    
    for x in range(0,Engine.chaserCount):
	    Engine.all_sprites.add(Chaser())
	
    mainloop()

def mainloop():
    Engine.running = True
    while Engine.running:
        Engine.on_event()

        Engine.on_draw(Engine.surface)
        Engine.delta = Engine.clock.tick(Engine.fps)

def eventloop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Engine.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Engine.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            main()
        elif event.type == pygame.KEYDOWN and  event.key == pygame.K_SPACE:
            Engine.on_draw = drawloop2
            Engine.on_event = eventloop2
        elif event.type == pygame.MOUSEMOTION:
            Engine.mousePos = event.pos

def drawGame(surface):
    # Update
    Engine.all_sprites.update(Engine.mousePos)
    
    # Draw / render
    surface.fill(pygame.Color('gray40'))
    Engine.all_sprites.draw(surface)
    return surface

def drawloop(surface):
	if Engine.isGameOver:
		showOver(surface)
	else:
	    surface.fill(pygame.Color('gray40'))
	    surface = drawGame(surface)
	pygame.display.flip()

def eventloop2():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Engine.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
	            Engine.running = False
            if event.key == pygame.K_SPACE:
                Engine.on_draw = drawloop
                Engine.on_event = eventloop

def drawloop2(surface):
    surface.fill(pygame.Color('dodgerblue'))
    surface = showPause(surface)
    pygame.display.flip()
    
def showPause(surface):
	font = pygame.font.Font('Calibri.ttf', 32)
	text = font.render("Paused", True, pygame.Color('black'), pygame.Color('dodgerblue'))
	textRect = text.get_rect() 
	textRect.center = (300,200)
	surface.blit(text, textRect)
	return surface

def setGameOver():
	Engine.isGameOver = True
    
def showOver(surface):
	font = pygame.font.Font('Calibri.ttf', 32)
	text = font.render("Game Over", True, pygame.Color('black'), pygame.Color('red1'))
	textRect = text.get_rect() 
	textRect.center = (300,200)
	surface.blit(text, textRect)
	return surface	

main()
