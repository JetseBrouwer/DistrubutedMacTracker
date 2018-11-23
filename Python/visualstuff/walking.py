import pygame
import time
import numpy
import random
from numpy import genfromtxt

#A-line (337, 588) (400, 546)
#B-line (107, 75)  (121, 70)
##C-line (408, 97) (450, 156)
#C-linenew(468, 44)(518, 112)
#cross1 -line (224, 231) (218, 283) routes B-C and B-A
#cross2 (301, 271) (231, 258) routes B-A

#main image = 1000*850
col_white = pygame.Color(255,255,255)
col_grey = pygame.Color(79 ,79,79)
col_blue1 = pygame.Color(116,172,199)
col_blue2 = pygame.Color(65,122,146)
MARGIN_X = 30

def getstartpoint(route):
    r = (random.randint(0,100)/100)
    if (route == 0 or route == 1): return   numpy.array([int(337+(r*63)),int(588-(r*42) )])
    elif (route == 2 or route == 3): return numpy.array([int(107+(r*14)),int(75-(r*5)   )])
    elif (route == 4 or route == 5): return numpy.array([int(468+(r*50)),int(44+(r*68)  )])
    else: return  numpy.array([0,0])

def getmidpoint(route):
    r = (random.randint(0,100)/100)
    if (route == 1 or route == 4):  return numpy.array([int(301-(r*70)),int(271-(r*13))]) #AC/CA
    else:                           return numpy.array([int(224-(r*6)),int(231+(r*52))]) #BC/CB/AB/BA
        
def getendpoint(route):
    r = (random.randint(0,100)/100)
    if (route == 2 or route == 4):   return numpy.array([int(337+(r*63)),int(588-(r*42))])
    elif (route == 0 or route == 5): return numpy.array([int(107+(r*14)),int(75-(r*5))])
    elif (route == 1 or route == 3): return numpy.array([int(468+(r*50)),int(44+(r*68)  )])
    else: return numpy.array([0,0])

class Walker():
    def __init__(self, startingpoint, midpoint, endpoint,starttime, endtime):
        self.startp = startingpoint
        self.midp = midpoint
        self.endp = endpoint
        self.t_start = starttime
        self.t_end = endtime

        self.duration = self.t_end-self.t_start

        self.col = pygame.Color(random.randint(0,255),random.randint(0,255),random.randint(0,255)) #random color
        self.pos = self.startp #starting position default

        self.vect_start_mid = self.midp - self.startp
        self.vect_mid_end = self.endp - self.midp
        self.lengtha = numpy.linalg.norm(self.vect_start_mid)
        self.lengthb = numpy.linalg.norm(self.vect_mid_end) 
        self.speed = 1/self.duration
        self.midpoint = self.lengtha/(self.lengtha+self.lengthb)

    def draw(self):        
        global globaltime
        global surf_img2
        
        if (globaltime >= self.t_start and globaltime <= self.t_end): 
            self.updatepos()
            pygame.draw.circle(surf_img2, self.col, self.pos ,3)

    def updatepos(self):
        global globaltime
        d = (globaltime - self.t_start) * self.speed
        invm = 1 / self.midpoint
        invm2 = 1 / (1-self.midpoint)
        if d >= self.midpoint:
            dd = d - self.midpoint
            self.pos = (self.midp + (self.vect_mid_end * (dd*invm2))).astype(int)
        else: 
            self.pos = (self.startp + (self.vect_start_mid * (d*invm))).astype(int)

class Slider():
    def __init__(self, maxi, mini):
        global surf_slider

        self.maxi = maxi  # maximum at slider position right
        self.mini = mini  # minimum at slider position left
        self.val = self.mini  # first boundary
        self.hit = False  # first boundary
        self.high = self.maxi
        self.low = self.mini

        self.maxwidth = surf_slider.get_width()-MARGIN_X-MARGIN_X
        self.scalar = self.maxwidth/(self.maxi-self.mini)

        self.rect_slider = pygame.Rect((MARGIN_X-10, 0), (20, 40))
        pygame.draw.rect(surf_slider, col_blue1, self.rect_slider)

    def draw(self):
        #update position
        self.rect_slider = pygame.Rect((MARGIN_X-10+(self.val-self.mini)*self.scalar, 0), (20, 40))
        #graph background
        surf_slider.fill(col_white)
        pygame.draw.rect(surf_slider, col_grey, pygame.Rect((MARGIN_X,15),(self.maxwidth,10))) #draw grey bar
        pygame.draw.rect(surf_slider, col_blue1, self.rect_slider)
    
    def move(self):
        global globaltime
        if self.hit: 
            self.val = ((pygame.mouse.get_pos()[0]-MARGIN_X)/self.scalar)+self.mini    
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi
        #print (self.val)
        globaltime = self.val

    def updatepos(self):
        self.val = globaltime

#get the maximum and minimum time and store everything local
data = [[],[],[],[],[],[]]
maxtmp = [0,0,0,0,0,0]
mintmp = [0,0,0,0,0,0]
Files =  ['AB.csv','AC.csv','BA.csv','BC.csv','CA.csv','CB.csv']
#Files = ['ABx.csv','ABx.csv','ABx.csv','ABx.csv','ABx.csv','ABx.csv']
#Files = ['ABx.csv']

for i , file in enumerate(Files):
    tmpdata = genfromtxt(file, delimiter=',')
    data[i] = numpy.delete(tmpdata,[0,3,4],1)
    #make walkers
    maxtmp[i] = numpy.amax(data[i])
    mintmp[i] = numpy.amin(data[i])
    del tmpdata
maxtime = numpy.amax(maxtmp)
mintime = numpy.amin(mintmp)
del mintmp,maxtmp,Files
#print(mintime,"   <>   ",maxtime)

walkers = []
#make the walkers
for i in range(len(data)):          # route
    for j in range(len(data[i])):   # walker
        w = Walker(getstartpoint(i),getmidpoint(i),getendpoint(i),data[i][j][0],data[i][j][1])
        #print("  ",j, "--", w.startp,"  ", w.midp, "  ", w.endp, "-time: ", w.t_start, "  ", w.t_end)
        walkers.append(w)

#programm starts here
#surf_window = pygame.display.set_mode((600, 700))
surf_window = pygame.display.set_mode((600, 700),pygame.FULLSCREEN)
pygame.display.set_caption('IoT_flowvisualizer')

surf_img = pygame.image.load('map.PNG')
surf_img2 = surf_img.copy()
surf_slider = pygame.Surface((500,100), pygame.SRCALPHA, 32)

surf_window.fill(col_white)
surf_slider.fill(col_white)

#font for text
pygame.font.init()
font = pygame.font.SysFont('arial',40,True)
font_s = pygame.font.SysFont('arial',20,True)


slider = Slider(maxtime,mintime)

#buttons are 80 by 35
Button_play = pygame.Rect(510,610,80,35)
Button_play6 = pygame.Rect(510,655,80,35)
playing = False
playspeed = 1

globaltime = mintime
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if slider.rect_slider.collidepoint(pos[0],pos[1]-630):  
                playing = False
                slider.hit = True
            elif Button_play.collidepoint(pos):
                if (playing == True and speed == 1):
                    #print('pause') 
                    playing = False
                else:
                    #print('speed1')
                    speed = 1
                    playing = True
            elif Button_play6.collidepoint(pos):
                if (playing == True and speed == 6):
                    #print('pause')
                    playing = False
                else: 
                    #print('speed6')
                    speed = 6
                    playing = True


        elif event.type == pygame.MOUSEBUTTONUP:
            slider.hit = False

    if slider.hit:slider.move()
    elif playing == True: 
        globaltime = globaltime + (speed/20)
        #maxtime
        if globaltime > maxtime:
            globaltime = maxtime
            playing = False
        slider.updatepos()
    
    #draw slider
    slider.draw()
    #draw lines
    surf_img2 = surf_img.copy()
    pygame.draw.line(surf_img2,col_grey,(337, 588),(400, 546),3) # A
    pygame.draw.line(surf_img2,col_grey,(107, 75), (121, 70),3) #B
    pygame.draw.line(surf_img2,col_grey,(468, 44),(518, 112),3) #C
    #draw the clock
    surf_img2.blit(font.render(time.strftime('%H:%M', time.localtime(globaltime)),True,col_grey),(500,550))
    #draw buttons
    surf_window.fill(col_white)
    pygame.draw.rect(surf_window,col_blue2,Button_play)
    pygame.draw.rect(surf_window,col_blue2,Button_play6)
    surf_window.blit(font_s.render('play',True,col_white),(535,615))
    surf_window.blit(font_s.render('play x6 ',True,col_white),(522,660))


    for w in walkers:
        w.draw()

    surf_window.blit(surf_img2,(0,0))
    surf_window.blit(surf_slider,(0,630))
    pygame.display.flip()
    time.sleep(0.05)

pygame.display.quit()
pygame.quit()
exit()