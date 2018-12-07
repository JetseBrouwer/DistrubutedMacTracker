import pygame
import time
import math
import random
import numpy
from numpy import genfromtxt


#slider code imported from https://www.dreamincode.net/forums/topic/401541-buttons-and-sliders-in-pygame/

#defined stuff
col_white = pygame.Color(255,255,255)
col_grey = pygame.Color(79 ,79,79)
col_blue1 = pygame.Color(116,172,199)
col_blue2 = pygame.Color(65,122,146)
col_yellow = pygame.Color(254,177,67)
col_red = pygame.Color(178,69,61)

#graphical sizes and such
MARGIN_Y = 20
MARGIN_X = 30
NODE_WIDTH = 75
NODE_HEIGHT = 300
NODE_SPACE_SIDES = 20
CORNER_DEPTH = 50
NODE_SPACE_MIDDLE = 10

#test array (AB,AC,BA,BC,CA,CB)
flow = [200,300,300,500,200,400]

class Slider():
    def __init__(self, maxi, mini):
        self.maxi = maxi  # maximum at slider position right
        self.mini = mini  # minimum at slider position left
        self.valA = self.mini  # first boundary
        self.valB = self.maxi  # first boundary
        self.hitA = False  # first boundary
        self.hitB = False  # first boundary

        self.high = self.maxi
        self.low = self.mini

        global slidescreen
        
        self.maxwidth = slidescreen.get_width()-MARGIN_X-MARGIN_X
        self.scalar = self.maxwidth/(self.maxi-self.mini)

        self.rect_sliderA = pygame.Rect((self.valA, 0), (20, 40))
        self.rect_sliderB = pygame.Rect((self.valB, 0), (20, 40))
        pygame.draw.rect(slidescreen, col_blue1, self.rect_sliderA)
        pygame.draw.rect(slidescreen, col_blue1, self.rect_sliderB)

    def draw(self):
        #update position
        self.rect_sliderA = pygame.Rect((MARGIN_X-10+(self.valA-self.mini)*self.scalar, 0), (20, 40))
        self.rect_sliderB = pygame.Rect((MARGIN_X-10+(self.valB-self.mini)*self.scalar, 0), (20, 40))

        #graph background
        slidescreen.fill(col_white)
        pygame.draw.rect(slidescreen, col_grey, pygame.Rect((MARGIN_X,15),(self.maxwidth,10)))
        pygame.draw.rect(slidescreen, col_blue2, pygame.Rect((self.low-self.mini)*self.scalar+MARGIN_X,15,(self.high-self.low)*self.scalar,10))

        #draw them
        pygame.draw.rect(slidescreen, col_blue1, self.rect_sliderA)
        pygame.draw.rect(slidescreen, col_blue1, self.rect_sliderB)
    
    def moveA(self):
        self.valA = ((pygame.mouse.get_pos()[0]-MARGIN_X)/self.scalar)+self.mini
        if self.valA < self.mini:
            self.valA = self.mini
        if self.valA > self.maxi:
            self.valA = self.maxi
        self.updatehighlow()

    def moveB(self):
        self.valB = ((pygame.mouse.get_pos()[0]-MARGIN_X)/self.scalar)+self.mini
        if self.valB < self.mini:
            self.valB = self.mini
        if self.valB > self.maxi:
            self.valB = self.maxi
        self.updatehighlow()
    
    def updatehighlow(self):
        if self.valB > self.valA:
            self.high = self.valB
            self.low  = self.valA
        else:
            self.low  = self.valB
            self.high = self.valA

def drawGUI():
    global screen
    global flow

    screen.fill(col_white)

    maxx = screen.get_width()
    maxy = screen.get_height()

    #get some rulers for drawing
    ruler_A = MARGIN_X + NODE_WIDTH          #the amount of pixels from the left side of a to start drawing
    ruler_B = maxx - MARGIN_X - NODE_WIDTH   #the amount of pixels from the right side of a to start drawing
    ruler_C = maxy - MARGIN_Y - NODE_WIDTH   #the amount of pixels from the bottom side of a to start drawing
    ruler_halfx = maxx/2

    #extra helping equations
    dist_AB = ruler_B-ruler_A
    dist_AC = ruler_C-MARGIN_Y-NODE_SPACE_SIDES

    #find the relation of crowflow to pixels
    temp_trafficsum = [0,0,0]
    temp_trafficsum[0] = flow[0]+flow[1]+flow[2]+flow[4] #sum of all traffic over A
    temp_trafficsum[1] = flow[0]+flow[2]+flow[3]+flow[5] #sum of all traffic over B
    temp_trafficsum[2] = flow[1]+flow[3]+flow[4]+flow[5] #sum of all traffic over C
    px_crowd_scalar = (NODE_HEIGHT-(2*NODE_SPACE_SIDES)-NODE_SPACE_MIDDLE)/max(temp_trafficsum)
    del temp_trafficsum

    #calculate the size of the bars - TODO makeit nice
    ab_size = flow[0]*px_crowd_scalar
    ac_size = flow[1]*px_crowd_scalar
    ba_size = flow[2]*px_crowd_scalar
    bc_size = flow[3]*px_crowd_scalar
    ca_size = flow[4]*px_crowd_scalar
    cb_size = flow[5]*px_crowd_scalar

    #basic node rectangles
    rect_A = pygame.Rect(MARGIN_X,MARGIN_Y,NODE_WIDTH,NODE_HEIGHT)
    rect_B = pygame.Rect(ruler_B,MARGIN_Y,NODE_WIDTH,NODE_HEIGHT)
    rect_C = pygame.Rect((ruler_halfx-(NODE_HEIGHT/2)),ruler_C,NODE_HEIGHT,NODE_WIDTH)
    pygame.draw.rect(screen,col_grey,rect_A)
    pygame.draw.rect(screen,col_grey,rect_B)
    pygame.draw.rect(screen,col_grey,rect_C)

    #polygons that show the relation
    polygoncanvas = pygame.Surface((dist_AB,dist_AC), pygame.SRCALPHA, 32)
    polygoncanvas = polygoncanvas.convert_alpha()

    poly_AB = pygame.draw.polygon(polygoncanvas, col_blue2, ([0, 0], [0, ab_size], [(dist_AB-(ab_size/2)), ab_size], [dist_AB, ab_size/2], [(dist_AB-(ab_size/2)), 0]))
    poly_BA = pygame.draw.polygon(polygoncanvas, col_red, ([(ba_size/2), ab_size], [0, (ba_size/2)+ab_size], [(ba_size/2), ab_size+ba_size],[dist_AB,ab_size+ba_size],[dist_AB,ab_size]))

    tmp1 = NODE_HEIGHT-NODE_SPACE_SIDES-NODE_SPACE_SIDES-ac_size-ca_size    #startin y point for the bars ac and ca
    tmp2 = (ruler_halfx-(NODE_HEIGHT/2))+NODE_SPACE_SIDES-ruler_A           #starting x point for the bars in node C
    tanx = 0.414213 #shorthand to not use the actual tngent = tan(45/2)
    tanac = tanx*ac_size
    tanca = tanx*ca_size
    tanbc = tanx*bc_size
    tancb = tanx*cb_size

    poly_AC = pygame.draw.polygon( polygoncanvas, col_blue2, (
        [0, tmp1],#topleft
        [0, tmp1+ac_size],#bottomleft
        [tmp2-CORNER_DEPTH+tanca, tmp1+ac_size],
        [tmp2+ca_size, tmp1+ac_size+ca_size+CORNER_DEPTH-tanca],
        [tmp2+ca_size, dist_AC-(ac_size/2)],#floor
        [tmp2+ca_size+(ac_size/2), dist_AC],#point
        [tmp2+ca_size+ac_size, dist_AC-(ac_size/2)],
        [tmp2+ca_size+ac_size, tmp1+ac_size+ca_size+CORNER_DEPTH-tanca-tanac],
        [tmp2-CORNER_DEPTH+tanca+tanac, tmp1]

        )) 

    poly_CA = pygame.draw.polygon( polygoncanvas, col_yellow, (
        [ca_size/2, tmp1+ac_size],
        [0, tmp1+ac_size+(ca_size/2)],
        [ca_size/2, tmp1+ac_size+ca_size], 
        [tmp2-CORNER_DEPTH, tmp1+ac_size+ca_size],
        [tmp2, tmp1+ac_size+ca_size+CORNER_DEPTH],
        [tmp2, dist_AC],
        [tmp2+ca_size, dist_AC],
        [tmp2+ca_size, tmp1+ac_size+ca_size+CORNER_DEPTH-tanca],
        [tmp2-CORNER_DEPTH+tanca, tmp1+ac_size]
        ))

    tmp3 = NODE_HEIGHT-NODE_SPACE_SIDES-NODE_SPACE_SIDES-bc_size-cb_size            #starting y point for bc and cb
    tmp4 = (ruler_halfx+(NODE_HEIGHT/2))-NODE_SPACE_SIDES-ruler_A-cb_size-bc_size   #starting x point for bc and cb in node C

    poly_BC = pygame.draw.polygon(polygoncanvas, col_red, (
        [dist_AB,tmp3], 
        [dist_AB,tmp3+bc_size],
        [tmp4+bc_size+cb_size-tancb+CORNER_DEPTH, tmp3+bc_size],
        [tmp4+bc_size, tmp3+bc_size+cb_size-tancb+CORNER_DEPTH], #outer corner
        [tmp4+bc_size,dist_AC-(bc_size/2)],
        [tmp4+(bc_size/2),dist_AC],#point
        [tmp4,dist_AC-(bc_size/2)],
        [tmp4,tmp3+bc_size+cb_size-tancb-tanbc+CORNER_DEPTH],
        [tmp4+bc_size+cb_size-tancb-tanbc+CORNER_DEPTH ,tmp3]
        ))

    poly_CB = pygame.draw.polygon(polygoncanvas, col_yellow, (
        [dist_AB-(cb_size/2), tmp3+bc_size], 
        [dist_AB, tmp3+bc_size+(cb_size/2)],
        [dist_AB-(cb_size/2), tmp3+bc_size+cb_size], 
        [tmp4+bc_size+cb_size +CORNER_DEPTH, tmp3+bc_size+cb_size], #inner corner
        [tmp4+bc_size+cb_size, tmp3+bc_size+cb_size+CORNER_DEPTH],
        [tmp4+bc_size+cb_size, dist_AC],
        [tmp4+bc_size,dist_AC],
        [tmp4+bc_size, tmp3+bc_size+cb_size-tancb+CORNER_DEPTH], #outer corner
        [tmp4+bc_size+cb_size-tancb+CORNER_DEPTH, tmp3+bc_size]
         ))
    
    #draw the geometr on the canvas
    screen.blit(polygoncanvas,(ruler_A,MARGIN_Y+NODE_SPACE_SIDES))
    del tanac,tanbc,tanca,tancb
    del tmp1,tmp2,tmp3,tmp4

    #draw the text
    #make the Tet in the appropriate size
    pygame.font.init()
    font = pygame.font.SysFont('arial',60,True) #bold arial font
    #A
    text_A = font.render('A',True,col_white)
    screen.blit(text_A,(MARGIN_X+(NODE_WIDTH/2.0)-(text_A.get_width()/2.0),MARGIN_Y+(NODE_HEIGHT/2.0)-(text_A.get_height()/2.0)))
    #B
    text_B = font.render('B',True,col_white)
    screen.blit(text_B,(ruler_B+(NODE_WIDTH/2.0)-(text_B.get_width()/2.0),MARGIN_Y+(NODE_HEIGHT/2.0)-(text_B.get_height()/2.0)))
    #C
    text_C = font.render('C',True,col_white)
    screen.blit(text_C,(ruler_halfx-(text_C.get_width()/2.0),ruler_C+(NODE_WIDTH/2.0)-(text_C.get_height()/2.0)))

    ax_offset = ruler_A + 35
    bx_offset = ruler_B - 35
    cy_offset = ruler_C - 25

    #test array (AB,AC,BA,BC,CA,CB)
    #AB
    font = pygame.font.SysFont('arial',math.floor(ab_size),True) #bold arial font
    text_AB = font.render(str(flow[0]),True,col_white)
    screen.blit(text_AB,(bx_offset-text_AB.get_width(),MARGIN_Y+NODE_SPACE_SIDES+ab_size/2-text_AB.get_height()/2))
    #AC
    font = pygame.font.SysFont('arial',math.floor(ac_size*0.6),True) #bold arial font
    text_AC = font.render(str(flow[1]),True,col_white)
    screen.blit(text_AC,(ruler_halfx-NODE_HEIGHT/2+NODE_SPACE_SIDES+ca_size+ac_size/2-text_AC.get_width()/2,cy_offset-text_AC.get_height()))
    #BA
    font = pygame.font.SysFont('arial',math.floor(ba_size),True) #bold arial font
    text_BA = font.render(str(flow[2]),True,col_white)
    screen.blit(text_BA,(ax_offset,MARGIN_Y+NODE_SPACE_SIDES+ab_size+ba_size/2-text_BA.get_height()/2))
    #BC
    font = pygame.font.SysFont('arial',math.floor(bc_size*0.6),True) #bold arial font
    text_BC = font.render(str(flow[3]),True,col_white)
    screen.blit(text_BC,(ruler_halfx+NODE_HEIGHT/2-NODE_SPACE_SIDES-cb_size-bc_size/2-text_BC.get_width()/2,cy_offset-text_BC.get_height()))
    #CA
    font = pygame.font.SysFont('arial',math.floor(ca_size),True) #bold arial font
    text_CA = font.render(str(flow[4]),True,col_white)
    screen.blit(text_CA,(ax_offset,MARGIN_Y-NODE_SPACE_SIDES+NODE_HEIGHT-ca_size/2-text_CA.get_height()/2))
    #CB
    font = pygame.font.SysFont('arial',math.floor(cb_size),True) #bold arial font
    text_CB = font.render(str(flow[5]),True,col_white)
    screen.blit(text_CB,(bx_offset-text_CB.get_width(),MARGIN_Y-NODE_SPACE_SIDES+NODE_HEIGHT-cb_size/2-text_CB.get_height()/2))

def updatevalues():
    global flow
    global data

    #filter and calculate cumulative values for set boundaries
    for i in range(len(data)):  
        tmpA = ([i[0] for i in data[i]] <= slider.high)
        tmpB = ([i[1] for i in data[i]] >= slider.low)
        tmpC = numpy.logical_and(tmpA,tmpB)
        #update flow values
        flow[i] = tmpC.sum()
        del tmpA,tmpB,tmpC

#programm starts here
#window = pygame.display.set_mode((800, 600))
window = pygame.display.set_mode((800, 600),pygame.FULLSCREEN)
window.fill(col_white)

screen = pygame.Surface((800,500), pygame.SRCALPHA, 32)
screen.fill(col_white)

slidescreen = pygame.Surface((800,100), pygame.SRCALPHA, 32)
slidescreen.fill(col_white)
pygame.display.set_caption('IoT_datavisualizer')

#test array (AB,AC,BA,BC,CA,CB)
#open csv files
data = [[],[],[],[],[],[]]
maxstuff = [0,0,0,0,0,0]
minstuff = [0,0,0,0,0,0]
Files =  ['AB.csv','AC.csv','BA.csv','BC.csv','CA.csv','CB.csv']

for i , file in enumerate(Files):
    tmpdata = genfromtxt(file, delimiter=',')
    data[i] = numpy.delete(tmpdata,[0,3,4],1)
    maxstuff[i] = numpy.amax(data[i])
    minstuff[i] = numpy.amin(data[i])
    del tmpdata

print(maxstuff , "  <>  ", minstuff)
#maxtime = numpy.amax(data)
maxtime = numpy.amax(maxstuff)
print("max time = ", maxtime)
mintime = numpy.amin(minstuff)
print("min time = ", mintime)

del maxstuff,minstuff,Files

#set maximum and minimum bounds of slider
slider = Slider(maxtime,mintime)
updatevalues()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if slider.rect_sliderA.collidepoint(pos[0],pos[1]-500):  slider.hitA = True
            elif slider.rect_sliderB.collidepoint(pos[0],pos[1]-500):  slider.hitB = True 
            print(slider.maxi, "  ",slider.mini,"  ",slider.high,"  ",slider.low)
            updatevalues()  
        elif event.type == pygame.MOUSEBUTTONUP:
            slider.hitA = False
            slider.hitB = False
            updatevalues()

    drawGUI()
    window.blit(screen,(0,0))

    if slider.hitA:slider.moveA()
    if slider.hitB:slider.moveB()
    slider.draw()
    window.blit(slidescreen,(0,520))

    pygame.display.flip()
    time.sleep(0.05)

pygame.display.quit()
pygame.quit()
exit()