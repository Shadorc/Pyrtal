from tkinter import *
from math import *
import time
from rectangle import Rect

class Portal():
    def __init__(self, mouse, color):
        self.x = mouse.x
        self.y = mouse.y
        self.elements = []
        self.color = color

        global salle, dude
        #Roof or floor, lying portal
        if(mouse.y < 125 or mouse.y > 875):
            self.elements += [salle.create_oval(mouse.x-150, mouse.y-55, mouse.x+150, mouse.y+55, fill=color)]
            self.elements += [salle.create_oval(mouse.x-145, mouse.y-50, mouse.x+145, mouse.y+50, fill='white')]
            self.width = 300
            self.height = 110
        else:
            self.elements += [salle.create_oval(mouse.x-55, mouse.y-150, mouse.x+55, mouse.y+150, fill=color)]
            self.elements += [salle.create_oval(mouse.x-50, mouse.y-145, mouse.x+50, mouse.y+145, fill='white')]
            self.width = 110
            self.height = 300

        self.hitbox = Rect(self.x, self.y, self.width, self.height)
        dude.firstPlan()
       
    def delete(self):
        #Undraw all objects containing by elements array
        for obj in self.elements:
            salle.delete(obj)

class Dude():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 115
        self.height = 168
        self.photo = PhotoImage(file="PortalDude2.gif")
        self.image = salle.create_image(self.x, self.y, image = self.photo)
        self.hitbox = Rect(self.x, self.y, self.width, self.height)
        self.isGoingDown = False

    #Moving fuctions
    def move(self, event):
        speed = 20

        #Move up
        if (event.char == 'z') and (810 <= self.y):
            self.y -= speed
        #Move down
        elif (event.char == 's') and (self.y <= 910):
            self.y += speed
        #Move left
        elif (event.char == 'q') and (100 <= self.x):
            self.x -= speed
        #Move right
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
        self.hitbox = Rect(self.x, self.y, self.width, self.height)
        checkHitbox()

    def goDown(self):
        if(dude.isGoingDown == False):
            dude.isGoingDown = True
            while(self.y <= 810):
                self.y += 5
                salle.coords(self.image, self.x, self.y)
                salle.update()
                time.sleep(0.01)
                self.hitbox = Rect(self.x, self.y, self.width, self.height)
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

    
#Blue portal
def createBluePortal(event):
    global bluePortal
    portalBisB = bluePortal
    bluePortal = Portal(event, '#6699ff')
    if(portalBisB != None):
        portalBisB.delete()
        
#Orange Portal   
def createOrangePortal(event):
    global orangePortal
    portalBisO = orangePortal
    orangePortal = Portal(event, '#ff6600')
    if(portalBisO != None):
        portalBisO.delete()

def checkHitbox():
    global dude, bluePortal, orangePortal
    if(bluePortal != None and orangePortal != None):
        if(bluePortal.hitbox.intersects(dude.hitbox)):
            dude.teleport(orangePortal.x, orangePortal.y)
        elif(orangePortal.hitbox.intersects(dude.hitbox)):
            dude.teleport(bluePortal.x, bluePortal.y)
        #dude.goDown()
    
frameW = 1000
frameH = 1000

frame = Tk()
frame.title("Pyrtal")

salle = Canvas(frame, width=frameW, height=frameH)
dude = Dude(500, 900)

bluePortal = None
orangePortal = None

# Back of the room #
salle.create_rectangle(125,875,875,125)

# Depth  #
salle.create_line([0, 1000, 125, 875])
salle.create_line([1000, 1000, 875, 875])                                                       
salle.create_line([1000, 0, 875, 125])
salle.create_line([0, 0, 125, 125])

#Set focus to catch mouse and keyboard input
salle.focus_set()

# Binding Mouse and Keyboard #
salle.bind("<Button-1>", createBluePortal)
salle.bind("<Button-3>", createOrangePortal)
salle.bind("<KeyPress>", dude.move)

chaine = Label(frame)
chaine.pack()
salle.pack()

frame.mainloop()
