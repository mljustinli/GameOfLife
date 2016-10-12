import sys, pygame

pygame.init()

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
        screen.fill([0, 255, 255])
        screen.blit(lines, [0, 0])
        if drawNew:
            newGen(cellGroup)
            drawNew = False
            for i in range(rows):
                for j in range(columns):
                    if cellGroup[i][j].living == True:
                        drawNew = True
        animateCells()
def animateCells():
    for i in range(rows):
        for j in range(columns):
            screen.blit(cellGroup[i][j].image, cellGroup[i][j].rect)
def newGen(cellGroup):
    holderGroup = []
    for i in range(rows):
        holderGroup.append([])
        for j in range(columns):
            holderGroup[i].append(False)
    for i in range(rows):
        for j in range(columns):
            counter = 0
            if cellGroup[(i - 1)%rows][(j - 1)%columns].living == True:
                counter += 1
            if cellGroup[(i - 1)%rows][j].living == True:
                counter += 1
            if cellGroup[(i - 1)%rows][(j + 1)%columns].living == True:
                counter += 1
            if cellGroup[i][(j + 1)%columns].living == True:
                counter += 1
            if cellGroup[(i + 1)%rows][(j + 1)%columns].living == True:
                counter += 1
            if cellGroup[(i + 1)%rows][j].living == True:
                counter += 1
            if cellGroup[(i + 1)%rows][(j - 1)%columns].living == True:
                counter += 1
            if cellGroup[i][(j - 1)%columns].living == True:
                counter += 1
            
            if counter < 2:
                holderGroup[i][j] = False
            elif counter == 3:
                holderGroup[i][j] = True
            elif counter >= 4:
                holderGroup[i][j] = False
            else:
                holderGroup[i][j] = cellGroup[i][j].living
    for i in range(rows):
        for j in range(columns):
            if holderGroup[i][j] == True:
                cellGroup[i][j].alive()
            elif holderGroup[i][j] == False:
                cellGroup[i][j].dead()
columns = 50
rows = 30
cellSize = cellWidth, cellHeight = [20, 20]
size = width, height = columns * (cellWidth + 1) + 1, rows * (cellHeight + 1) + 1
screen = pygame.display.set_mode(size)
lines = pygame.Surface(screen.get_size())
pygame.display.set_caption("Conway's Game Of Life")
screen.fill([0, 255, 255])
lines.fill([0, 255, 255])
cellGroup = []
clock = pygame.time.Clock()
drawNew = False
page = 0
font = pygame.font.Font(None, 50)
mousex = 0
mousey = 0

for i in range(0, width, cellWidth + 1):
    pygame.draw.line(lines, [0, 0, 0], [i, 0], [i, height], 1)
for j in range(0, height, cellHeight + 1):
    pygame.draw.line(lines, [0, 0, 0], [0, j], [width, j], 1)

for i in range(rows):
    cellGroup.append([])
    for j in range(columns):
        newCell = Cells([j * (cellWidth + 1) + 1, i * (cellHeight + 1) + 1], False)
        cellGroup[i].append(newCell)
        
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
                for i in range(rows):
                    for j in range(columns):
                        cellGroup[i][j].dead()
        elif event.type == pygame.MOUSEMOTION:
            mousex = event.pos[0]
            mousey = event.pos[1]
        elif event.type == pygame.MOUSEBUTTONDOWN and page == 1:
            for i in range(rows):
                for j in range(columns):
                    if cellGroup[i][j].rect.top <= mousey and cellGroup[i][j].rect.bottom >= mousey and cellGroup[i][j].rect.left <= mousex and cellGroup[i][j].rect.right >= mousex:
                        cellGroup[i][j].switchState()
    drawWhat()
    pygame.display.flip()
    clock.tick(10)