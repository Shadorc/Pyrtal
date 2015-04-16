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
            self.elements += [salle.create_oval(self.x-150, self.y-55, self.x+150, self.y+55, fill=color)]
            self.elements += [salle.create_oval(self.x-145, self.y-50, self.x+145, self.y+50, fill='white')]
            self.width = 300
            self.height = 110
        else:
            self.elements += [salle.create_oval(self.x-55, self.y-150, self.x+55, self.y+150, fill=color)]
            self.elements += [salle.create_oval(self.x-50, self.y-145, self.x+50, self.y+145, fill='white')]
            self.width = 110
            self.height = 300

        dude.firstPlan()
       
    def delete(self):
        #Efface tous les éléments contenus dans la liste
        for obj in self.elements:
            salle.delete(obj)

    def getHitbox(self):
        return Rect(self.x, self.y, self.width, self.height)

class Dude():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.photo = PhotoImage(file="PortalDude2.gif")
        self.image = salle.create_image(self.x, self.y, image = self.photo)
        self.width = self.photo.width()
        self.height = self.photo.height()
        self.isGoingDown = False

    #Mouvements
    def move(self, event):
        speed = 20

        #Haut
        if (event.char == 'z') and (810 <= self.y):
            self.y -= speed
        #Bas
        elif (event.char == 's') and (self.y <= 910):
            self.y += speed
        #Gauche
        elif (event.char == 'q') and (100 <= self.x):
            self.x -= speed
        #Droite
        elif (event.char == 'd') and (self.x <= 900):
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

        salle.coords(self.image, self.x, self.y)
        checkHitbox()

    def goDown(self):
        if(dude.isGoingDown == False):
            dude.isGoingDown = True
            while(self.y <= 810):
                self.y += 5
                salle.coords(self.image, self.x, self.y)
                salle.update()
                time.sleep(0.01)
            dude.isGoingDown = False
            checkHitbox()

    def firstPlan(self):
        salle.delete(self.image)
        self.image = salle.create_image(self.x, self.y, image = self.photo)
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
frameH = 1000

frame = Tk()
frame.title("Pyrtal")

salle = Canvas(frame, width=frameW, height=frameH)
dude = Dude(500, 900)

bluePortal = None
orangePortal = None

#Fond de la salle
salle.create_rectangle(125,875,875,125)

#Effet de profondeur (lignes diagonales)
salle.create_line([0, 1000, 125, 875])
salle.create_line([1000, 1000, 875, 875])                                                       
salle.create_line([1000, 0, 875, 125])
salle.create_line([0, 0, 125, 125])

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
