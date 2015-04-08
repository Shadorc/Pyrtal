from tkinter import *
from math import *
import time
import threading 

class portal():

    def createPortal(self, mouse, color):
        #Logs are love, Logs are life. #oui
        chaine.configure(text = "Click spotted in X =" + str(mouse.x) +", Y =" + str(mouse.y))
        
        self.portal = []

        #Roof or floor, lying portal
        if(mouse.y < 125 or mouse.y > 875):
            self.portal += [salle.create_oval(mouse.x-150, mouse.y-50, mouse.x+150, mouse.y+50, fill=color)]
            self.portal += [salle.create_oval(mouse.x-145, mouse.y-45, mouse.x+145, mouse.y+45, fill='white')]
        else:
            self.portal += [salle.create_oval(mouse.x-50, mouse.y-150, mouse.x+50, mouse.y+150, fill=color)]
            self.portal += [salle.create_oval(mouse.x-45, mouse.y-145, mouse.x+45, mouse.y+145, fill='white')]
            
        return self.portal
        
    #Blue portal
    def bluePortal(self, event):
        self.bluePortalElements = []
        delete(bluePortalElements)
        self.bluePortalElements = self.createPortal(event, '#6699ff')

    #Orange Portal   
    def orangePortal(self, event):
        self.orangePortalElements = []
        delete(self.orangePortalElements)  
        self.orangePortalElements = self.createPortal(event, '#ff6600')

#Moving fuctions
def move(event):
    global x, y, dude
    speed = 20

    #Move up
    if (event.char == 'z') and (810 <= y):
        y -= speed
    #Move down
    elif (event.char == 's') and (y <= 910):
        y += speed
    #Move left
    elif (event.char == 'q') and (100 <= x):
        x -= speed
    #Move right
    elif (event.char == 'd') and (x <= 900):
        x += speed
        
    elif (event.char == ' '):
        a = threading.Thread(None, explosion, None, (), {}) 
        a.start() 

    salle.coords(dude, x, y)


def explosion():
    global y
    text = salle.create_text(x+100, y, text="The Game")
    while y > -100:
            y -= 1
            time.sleep(0.01)
            salle.coords(dude, x, y)
            salle.coords(text, x+100, y)

def gravity():
    if y < 810:
        move(0, 20)
   
def delete(elements):
    #Undraw all objects containing by elements array
    for obj in elements:
        salle.delete(obj)
    #Reset elements array
    elements = []


#portal.bluePortalElements = []
#portal.orangePortalElements = []

frameW = 1000
frameH = 1000

#Dude coordinate
x = 500
y = 900

frame = Tk()
frame.title("Pyrtal")

salle = Canvas(frame, width=frameW, height=frameH)

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
salle.bind("<Button-1>", portal.bluePortal)
salle.bind("<Button-3>", portal.orangePortal)
salle.bind("<KeyPress>", move)

photo = PhotoImage(file="PortalDude2.gif")
dude = salle.create_image(x, y, image=photo)

chaine = Label(frame)
chaine.pack()
salle.pack()

frame.mainloop()
