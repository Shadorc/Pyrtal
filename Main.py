# Portal Main #

from tkinter import *
from math import *

def createPortal(event, color):
    #Logs are love, Logs are life. #oui
    chaine.configure(text = "Click spotted in X =" + str(event.x) +", Y =" + str(event.y))
    
    elements = []
    elements += [salle.create_oval(event.x-50, event.y-150, event.x+50, event.y+150, fill=color)]
    elements += [salle.create_oval(event.x-45, event.y-145, event.x+45, event.y+145, fill='white')]
    
    salle.update()
    
    return elements
    
#Blue portal
def bluePortal(event):
    global bluePortalElements
    delete(bluePortalElements)   
    bluePortalElements = createPortal(event, '#6699ff')

#Orange Portal   
def orangePortal(event):
    global orangePortalElements
    delete(orangePortalElements)  
    orangePortalElements = createPortal(event, '#ff6600')
    
def delete(elements):
    #Undraw all objects containing by elements array
    for obj in elements:
        salle.delete(obj)
    #Reset elements array
    elements = []

bluePortalElements = []
orangePortalElements = []

xmax=1000
ymax=1000

frame = Tk()
frame.title("PORTAAAAAAAAAAAAAAAAAAAAAAAAAL")

salle = Canvas(frame, width=xmax, height=ymax)

# Fond de salle #
salle.create_rectangle(125,875,875,125)

# Profondeur  #
salle.create_line([0, 1000, 125, 875])
salle.create_line([1000, 1000, 875, 875])                                                       
salle.create_line([1000, 0, 875, 125])
salle.create_line([0, 0, 125, 125])

salle.bind("<Button-1>", bluePortal)
salle.bind("<Button-2>", delete)
salle.bind("<Button-3>", orangePortal)

photo=PhotoImage(file="Portal_Dude2.gif")
salle.create_image(500, 900, image=photo)                          #Portal Dude early *access* version#

salle.update()

chaine = Label(frame)
chaine.pack()
salle.pack()

frame.mainloop()