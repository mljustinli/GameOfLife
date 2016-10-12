import sys, pygame

pygame.init()
size = width, height = 988, 589
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Conway's Game of Life")
background = pygame.Surface(screen.get_size())
background.fill([0, 255, 255])
cellGroup = []
mousex = 0
mousey = 0
clock = pygame.time.Clock()
drawNew = False

for i in range(0, width, 21):
    pygame.draw.line(background, [0, 0, 0], [i, 0], [i, height], 1)
for j in range(0, height, 21):
    pygame.draw.line(background, [0, 0, 0], [0, j], [width, j], 1)

font = pygame.font.Font(None, 50)

page = 0
cellSize = [20, 20]

class Cells(pygame.sprite.Sprite):
    def __init__(self, location, living):
        pygame.sprite.Sprite.__init__(self)
        image_surface = pygame.surface.Surface(cellSize)
        image_surface.fill([0, 255, 255])
        self.image = image_surface.convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.living = living
    def alive(self):
        image_surf = pygame.surface.Surface(cellSize)
        image_surf.fill([115, 117, 117])
        self.image = image_surf.convert()
        self.living = True
    def dead(self):
        image_surf = pygame.surface.Surface(cellSize)
        image_surf.fill([0, 255, 255])
        self.image = image_surf.convert()
        self.living = False
    def switchState(self):
        if self.living == False:
            self.living = True
            self.alive()
        else:
            self.living = False
            self.dead()
        
def drawCells():
    for cell in cellGroup:
        screen.blit(cell.image, cell.rect)

def newGen(cellGroup):
    holderGroup = []
    for index, cell in enumerate(cellGroup):
        counter = 0
        if cellGroup[index - 48].living == True:
            counter += 1
        if cellGroup[index - 47].living == True:
            counter += 1
        if cellGroup[index - 46].living == True:
            counter += 1
        if cellGroup[index + 1].living == True:
            counter += 1
        if cellGroup[index + 48].living == True:
            counter += 1
        if cellGroup[index + 47].living == True:
            counter += 1
        if cellGroup[index + 46].living == True:
            counter += 1
        if cellGroup[index - 1].living == True:
            counter += 1
        
        if counter < 2:
            holderGroup.append(False)
        elif counter == 3:
            holderGroup.append(True)
        elif counter >= 4:
            holderGroup.append(False)
        else:
            holderGroup.append(cell.living)
            
    for index, word in enumerate(holderGroup):
        if word == True:
            cellGroup[index].alive()
        elif word == False:
            cellGroup[index].dead()

def drawWhat():
    global page, drawNew
    if page == 0:
        screen.fill([255, 255, 255])
        text1 = "Click the cells and press space to run!"
        t1 = font.render(text1, 1, (0, 0, 0))
        screen.blit(t1, [screen.get_width()/2 - t1.get_width()/2, 100])
        text2 = "Press space to begin!"
        t2 = font.render(text2, 1, (0, 0, 0))
        screen.blit(t2, [screen.get_width()/2 - t2.get_width()/2, 200])
    if page == 1:
        screen.blit(background, (0, 0))
        if drawNew:
            newGen(cellGroup)
            drawNew = False
            for cell in cellGroup:
                if cell.living == True:
                    drawNew = True
        drawCells()

for i in range(0, 28):
    for j in range(0, 47):
        newCell = Cells([j * 21 + 1, i * 21 + 1], False)
        cellGroup.append(newCell)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_SPACE and page == 0:
                page = 1
            elif event.key == pygame.K_SPACE and page == 1:
                if drawNew == True:
                    drawNew = False
                else:
                    drawNew = True
            elif event.key == pygame.K_c:
                for cell in cellGroup:
                    cell.dead()
                drawNew = False
            elif event.key == pygame.K_RIGHT:
                newGen(cellGroup)
        elif event.type == pygame.MOUSEMOTION:
            mousex = event.pos[0]
            mousey = event.pos[1]
        elif event.type == pygame.MOUSEBUTTONDOWN and page == 1:
            for cell in cellGroup:
                if cell.rect.top <= mousey and cell.rect.bottom >= mousey and cell.rect.left <= mousex and cell.rect.right >= mousex:
                    cell.switchState()
    drawWhat()
    pygame.display.flip()
    clock.tick(10)