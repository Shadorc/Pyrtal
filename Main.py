from tkinter import *
from math import *
import time
from rectangle import Rect

class Portal():
    def __init__(self, mouse, color):
        self.centerX = mouse.x
        self.centerY = mouse.y
        self.elements = []
        
        global salle, dude
        #Sol & Plafond : Portail horizontal
        if(mouse.y < 125 or mouse.y > 875):
            self.width = 300
            self.height = 110
        else:
            self.width = 110
            self.height = 300

        #Coordonnées de l'angle en haut à gauche
        self.topX = self.centerX-self.width/2
        self.topY = self.centerY-self.height/2

        #Coordonnées de l'angle en bas à droite
        self.botX = self.centerX+self.width/2
        self.botY = self.centerY+self.height/2
        
        #Epaisseur du portail
        thickness = 5

        #Dans l'angle supérieur gauche, il faut enlever du rayon, dans l'angle inférieur droit, il faut en rajouter
        self.elements += [salle.create_oval(self.topX,           self.topY,           self.botX,           self.botY,           fill=color)]
        self.elements += [salle.create_oval(self.topX+thickness, self.topY+thickness, self.botX-thickness, self.botY-thickness, fill='white')]
        self.elements += [salle.create_rectangle(self.topX, self.topY, self.botX, self.botY)]
 
        dude.firstPlan()
       
    def delete(self):
        #Efface tous les éléments contenus dans la liste
        for obj in self.elements:
            salle.delete(obj)

    def getHitbox(self):
        return Rect(self.topX, self.topY, self.width, self.height)

class Dude():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.photo = PhotoImage(file="PortalDude2.gif")
        self.image = salle.create_image(self.x, self.y, image=self.photo, anchor=NW)
        self.width = self.photo.width()
        self.height = self.photo.height()
        self.isGoingDown = False
        self.debug = 0

    #Mouvements
    def move(self, event):
        speed = 20

        #Haut
        if (event.char == 'z') and (800 <= self.y+self.height):
            self.y -= speed
        #Bas
        elif (event.char == 's') and (self.y+self.height <= 890):
            self.y += speed
        #Gauche
        elif (event.char == 'q') and (140 <= self.x):
            self.x -= speed
        #Droite
        elif (event.char == 'd') and (self.x+self.width <= 855):
            self.x += speed
        #The Game Easter Egg
        elif (event.char == ' '):
            text = salle.create_text(self.x+100, self.y, text="The Game")
            while self.y > -100:
                self.y -= 1
                time.sleep(0.01)
                salle.coords(self.image, self.x, self.y)
                salle.coords(text, self.x+100, self.y)
                salle.update()

        salle.delete(self.debug)
        self.debug = salle.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height)
        salle.coords(self.image, self.x, self.y)
        checkHitbox()

    def goDown(self):
        if(dude.isGoingDown == False):
            dude.isGoingDown = True
            while(self.y+self.height <= 800):
                self.y += 5
                salle.coords(self.image, self.x, self.y)
                salle.update()
                time.sleep(0.01)
            dude.isGoingDown = False
            checkHitbox()

    def firstPlan(self):
        salle.delete(self.image)
        self.image = salle.create_image(self.x, self.y, image=self.photo, anchor=NW)
        salle.update()

    def teleport(self, x, y):
        if(dude.isGoingDown == False):
            self.x = x
            self.y = y
            salle.coords(self.image, self.x, self.y)
            self.firstPlan()
            self.goDown()

    def getHitbox(self):
        return Rect(self.x, self.y, self.width, self.height)

    
#Portail Bleu
def createBluePortal(event):
    global bluePortal
    portalBisB = bluePortal
    bluePortal = Portal(event, '#6699ff')
    if(portalBisB != None):
        portalBisB.delete()
        
#Portail Orange  
def createOrangePortal(event):
    global orangePortal
    portalBisO = orangePortal
    orangePortal = Portal(event, '#ff6600')
    if(portalBisO != None):
        portalBisO.delete()

def checkHitbox():
    global dude, bluePortal, orangePortal
    if(bluePortal != None and orangePortal != None):
        if(bluePortal.getHitbox().intersects(dude.getHitbox())):
            dude.teleport(orangePortal.centerX, orangePortal.centerY)
        elif(orangePortal.getHitbox().intersects(dude.getHitbox())):
            dude.teleport(bluePortal.centerX, bluePortal.centerY)
    
frameW = 1000
frameH = 900

frame = Tk()
frame.title("Pyrtal")

salle = Canvas(frame, width=frameW, height=frameH)
dude = Dude(450, 700)

bluePortal = None
orangePortal = None

#Fond de la salle
salle.create_rectangle(125,788,875,112)

"""Effet de profondeur (lignes diagonales)"""
#Bas gauche
salle.create_line(0, frameH, 125, 788)
#Bas droit
salle.create_line(frameW, frameH, 875, 788)
#Haut droit
salle.create_line(frameW, 0, 875, 112)
#Haut gauche
salle.create_line(0, 0, 125, 112)

#Focus sur la fenêtre pour pouvoir recevoir les clics de souris et l'appuie de touches
salle.focus_set()

#Configure les touches souris / clavier
salle.bind("<Button-1>", createBluePortal)
salle.bind("<Button-3>", createOrangePortal)
salle.bind("<KeyPress>", dude.move)

chaine = Label(frame)
chaine.pack()
salle.pack()

frame.mainloop()
