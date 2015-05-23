from tkinter import *
from math import *
from rectangle import *
import time
import threading

"""
#--------------------------------------------------------------------------------------#
#---------------------------------CLASSE PORTAL----------------------------------------#
#--------------------------------------------------------------------------------------#
"""

class Portal():
    def __init__(self, positions, color, visible):
        self.centerX = positions[0]
        self.centerY = positions[1]
        self.elements = []
        
        #Sol & Plafond : Portail horizontal
        if(self.centerY > floor.y or self.centerY < ceiling.y+ceiling.height):
            self.width = 300
            self.height = 110
        else:
            self.width = 110
            self.height = 300

        #Coordonnées de l'angle en haut à gauche
        self.x = self.centerX-self.width/2
        self.y = self.centerY-self.height/2

        #Coordonnées de l'angle en bas à droite
        self.botX = self.x+self.width
        self.botY = self.y+self.height
        
        #Epaisseur du portail
        thickness = 5
        
        if(visible == True):
            #Dans l'angle supérieur gauche, il faut enlever du rayon, dans l'angle inférieur droit, il faut en rajouter
            self.elements += [salle.create_oval(self.x,           self.y,           self.botX,           self.botY,           fill=color)]
            self.elements += [salle.create_oval(self.x+thickness, self.y+thickness, self.botX-thickness, self.botY-thickness, fill='white')]

            #Hitbox Portail
            self.elements += [salle.create_rectangle(self.x, self.y, self.botX, self.botY)]
       
    def delete(self):
        #Efface tous les éléments contenus dans la liste
        for obj in self.elements:
            salle.delete(obj)

"""
#--------------------------------------------------------------------------------------#
#----------------------------------CLASSE DUDE-----------------------------------------#
#--------------------------------------------------------------------------------------#
"""

class Dude():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.setImage("dude_gris.gif")
        self.debug = 0
        self.moveSpeed = 20
        self.speedY = 0
        self.speedX = 0
        self.isFalling = False
        self.stop = True
        self.lastMove = ''
        self.lastShoot = 0 #Dernière fois que le dude a placé un portail

    def setImage(self, name):
        self.photo = PhotoImage(file=name)
        self.image = salle.create_image(self.x, self.y, image=self.photo, anchor=NW)
        self.width = self.photo.width() - self.photo.width()/4
        self.height = self.photo.height()

    #Mouvements
    def move(self, event):
        #Haut
        if (event.char == 'z') and (floor.y < self.y+self.height-20):
            self.y -= self.moveSpeed
            self.lastMove = 'up'
        #Bas
        elif (event.char == 's') and (self.y+self.height < floor.y+floor.height):
            self.y += self.moveSpeed
            self.lastMove = 'down'
        #Gauche
        elif (event.char == 'q') and (floor.x+40 < self.x-self.width):
            self.x -= self.moveSpeed
            self.lastMove = 'left'
        #Droite
        elif (event.char == 'd') and (self.x+self.width < floor.width-rightWall.width):
            self.x += self.moveSpeed
            self.lastMove = 'right'
        #The Game Easter Egg
        elif (event.char == ' '):
            text = salle.create_text(self.x+100, self.y, text="The Game")
            self.isFalling = True
            start = time.time()
            while(self.y > -self.height):
                t = time.time() - start
                g = 0.25
                a = -g
                self.speedY = a * t
                self.y = self.speedY * t + self.y
                salle.coords(self.image, self.x, self.y)
                salle.coords(text, self.x+100, self.y)
                salle.update()

        #Hitbox Dude
        salle.delete(self.debug)
        self.debug = salle.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height)

        salle.coords(self.image, self.x, self.y)
        checkHitbox()

"""
#--------------------------------------------------------------------------------------#
#----------------------------------CLASSE CUBE-----------------------------------------#
#--------------------------------------------------------------------------------------#
"""      

class Cube():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.photo = PhotoImage(file="cube.gif")
        self.image = salle.create_image(self.x, self.y, image=self.photo, anchor=NW)
        self.width = self.photo.width()
        self.height = self.photo.height()
        self.speedY = 0
        self.speedX = 0
        self.isFalling = False
        self.stop = True

    def move(self, x, y):
        if(x > floor.x and x+self.width < floor.x+floor.width and y+self.height > floor.y and y+self.height < floor.y+floor.height):
            self.x = x
            self.y = y
            salle.coords(self.image, self.x, self.y)

"""
#--------------------------------------------------------------------------------------#
#----------------------------------------MAIN------------------------------------------#
#--------------------------------------------------------------------------------------#
"""

def createBluePortal(event):
    createPortal(event.x, event.y, 'blue')

def createOrangePortal(event):
    createPortal(event.x, event.y, 'orange')

def portalPlacement(coordinate, size, bound1, bound2):
    if(coordinate+size > bound1):
        return (coordinate - (coordinate+size - bound1))
    elif(coordinate-size < bound2):
        return (coordinate - (coordinate-size - bound2))
    else:
        return coordinate

#Créer un Portail
def createPortal(x, y, color):
    global bluePortal, orangePortal, dude

    #Le dude ne peut tirer qu'un portail toutes les 100ms
    if((time.time() - dude.lastShoot) >= 0.1):
        dude.lastShoot = time.time()

        if(color == 'blue'):
            portal = bluePortal
            otherPortal = orangePortal
        elif(color == 'orange'):
            portal = orangePortal
            otherPortal = bluePortal

        #Si le portail est posé sur le fond de la salle
        if((leftWall.width < x < rightWall.x) and (ceiling.height < y < floor.y)):
            y = portalPlacement(y, 150, floor.y, ceiling.height)
            x = portalPlacement(x, 55, rightWall.x, leftWall.width)
        #Si le portail est sur le plafond
        elif(0 < y < ceiling.height):
            y = portalPlacement(y, 55, ceiling.height, ceiling.y)
        #Si le portail est sur le sol
        elif(floor.y < y < floor.y+floor.height):
            y = portalPlacement(y, 55, floor.y+floor.height, floor.y)
        #Si le portail est sur le mur droit
        elif(rightWall.x < x < rightWall.x+rightWall.width):
            x = portalPlacement(x, 55, rightWall.x+rightWall.width, rightWall.x)
        #Si le portail est sur le mur gauche
        elif(leftWall.x < x < leftWall.x+leftWall.width):
            x = portalPlacement(x, 55, leftWall.x+leftWall.width, leftWall.x)

        #Créé un faux portail pour voir s'il peut être posé 
        simulPortal = Portal([x, y], color, False)

        #Si le portail est placé dans un angle, ne pas le poser
        if((getHitbox(simulPortal).intersects(floor) or getHitbox(simulPortal).intersects(ceiling)) and (getHitbox(simulPortal).intersects(leftWall) or getHitbox(simulPortal).intersects(rightWall))):
            return

        #Vérifie si le portail qui va être créé n'est pas posé par dessus le deuxième
        if(otherPortal != None):
            
            #Distance entre le centreX des deux portails
            differenceX = simulPortal.centerX - otherPortal.centerX
            #Distance entre le centreY des deux portails
            differenceY = simulPortal.centerY - otherPortal.centerY

            #Si les deux portails se superposent, on décale le nouveau portail de sorte à ce qu'il se colle à l'autre
            if(getHitbox(simulPortal).intersects(getHitbox(otherPortal))):
                
                if(sqrt((differenceX)**2 + (differenceY)**2) < otherPortal.height-50):
                    #Si le portail vient de la droite, ajouter la différence pour le coller contre le bord droite
                    if(differenceX >= 0):
                        x += simulPortal.width - abs(differenceX)
                    #Si le portail vient de la gauche, soustraire la différence pour le coller sur le bord gauche
                    else:
                        x -= simulPortal.width - abs(differenceX)

                else:
                    #Si le portail vient de la droite, ajouter la différence pour le coller contre le bord droite
                    if(differenceY >= 0):
                        y += simulPortal.height - abs(differenceY)
                    #Si le portail vient de la gauche, soustraire la différence pour le coller sur le bord gauche
                    else:
                        y -= simulPortal.height - abs(differenceY)

        if(color == 'blue'):
            #Si le portail avait déjà été posé, l'effacer
            if(bluePortal != None):
                bluePortal.delete()
            bluePortal = Portal([x, y], '#6699ff', True)
            name = "dude_bleu.gif"

        elif(color == 'orange'):
            if(orangePortal != None):
                orangePortal.delete() 
            orangePortal = Portal([x, y], '#ff6600', True)
            name = "dude_orange.gif"

        dude.setImage(name)
        salle.tag_raise(dude.image)
        salle.tag_raise(cube.image)
        checkHitbox()

"""
#--------------------------------------------------------------------------------------#
#----------------------------------METHODS ENTITIES------------------------------------#
#--------------------------------------------------------------------------------------#
"""

def getHitbox(entity):
        return Rect(entity.x, entity.y, entity.width, entity.height)

def teleport(entity, x, y):
        entity.stop = False
        entity.x = x
        entity.y = y
        salle.coords(entity.image, entity.x, entity.y)
        salle.tag_raise(entity.image)
        if(entity.isFalling == False):
            t = threading.Thread(target=momentum, args=(entity,))
            t.start()

def momentum(entity):
        entity.isFalling = True
        start = time.time()
        
        while(entity.stop == False):
            #Temps écoulé en seconde depuis la dernière boucle
            t = (time.time() - start)*10
            start = time.time()
            
            a = 9.81

            #On limite la vitesse maximale à 200
            if(abs(entity.speedY < 200)):
                entity.speedY = a * t + entity.speedY
                
            entity.y = entity.speedY * t + entity.y
            entity.x = entity.speedX * t + entity.x

            secondCeiling = Rect(ceiling.x, ceiling.y, ceiling.width, ceiling.height/2)
            secondLeftWall = Rect(leftWall.x, leftWall.y, leftWall.width/2, leftWall.height)
            secondRightWall = Rect(rightWall.x+rightWall.width/2, rightWall.y, rightWall.width/2, rightWall.height) 

            if(getHitbox(entity).intersects(secondCeiling)):
                entity.speedY = 0
                #Au cas où l'entité est dans le plafond, la descendre
                entity.y = secondCeiling.height+1
            #Si l'entité touche un mur et qu'il ne vient pas de sortir d'un portail, on annule sa vitesse en X
            elif((getHitbox(entity).intersects(secondLeftWall) or getHitbox(entity).intersects(secondRightWall)) and (getHitbox(entity).intersects(bluePortal) or getHitbox(entity).intersects(orangePortal)) == False):
                entity.speedX = 0

            salle.coords(entity.image, entity.x, entity.y)
            salle.update()
            checkHitbox()

        entity.isFalling = False
        entity.speedX = 0
        entity.speedY = 0

"""
#--------------------------------------------------------------------------------------#
#-----------------------------------------HITBOX---------------------------------------#
#--------------------------------------------------------------------------------------#
"""

def checkHitbox():
    global dude, cube, bluePortal, orangePortal
    
    #Si les deux portails sont posés
    if(bluePortal != None and orangePortal != None):
        checkPortalCollision(dude)
        checkPortalCollision(cube)

    #Collisions entre le cube et le dude
    if(getHitbox(cube).perspective(getHitbox(dude))):
        if(dude.lastMove == 'up'):
            cube.move(cube.x, cube.y-dude.moveSpeed)
        elif(dude.lastMove == 'down'):
            cube.move(cube.x, cube.y+dude.moveSpeed)
        elif(dude.lastMove == 'right'):
            cube.move(cube.x+dude.moveSpeed, cube.y)
        elif(dude.lastMove == 'left'):
            cube.move(cube.x-dude.moveSpeed, cube.y)

    #Met le Cube ou le Dude en premier plan en fonction de qui est devant l'autre
    if(dude.y+dude.height > cube.y+cube.height):
        salle.tag_raise(dude.image)
    elif(dude.y+dude.height < cube.y+cube.height):
        salle.tag_raise(cube.image)
    
def checkPortalCollision(entity):
    #Si l'entité a atteint le sol alors on check les portails
    if(getHitbox(entity).intersects(floor)):

        if(getHitbox(bluePortal).intersects(getHitbox(entity)) or getHitbox(orangePortal).intersects(getHitbox(entity))):
            #Si l'entité passe par le portail bleu
            if(getHitbox(bluePortal).intersects(getHitbox(entity))):
                portal = orangePortal
            #Si l'entité passe par le portail orange
            else:
                portal = bluePortal

            #On cherche où positionner l'entité par rapport au portail
            if(getHitbox(portal).intersects(floor)):
                y = portal.centerY-(entity.height+portal.height/2)-5
                x = portal.centerX - entity.width/2
            elif(getHitbox(portal).intersects(ceiling)):
                y = portal.centerY+(portal.height/2)+5
                x = portal.centerX - entity.width/2
            elif(getHitbox(portal).intersects(leftWall)):
                y = portal.centerY-entity.height/2
                x = portal.centerX + portal.width/2
            elif(getHitbox(portal).intersects(rightWall)):
                y = portal.centerY-entity.height/2
                x = portal.centerX - portal.width/2
            else:
                y = portal.centerY-entity.height/2
                x = portal.centerX-entity.width/2
                
            teleport(entity, x, y)

            #On modifie les vitesses en fonction de là où il sort
            if(getHitbox(portal).intersects(floor)):
                entity.speedY = -entity.speedY
            elif getHitbox(portal).intersects(leftWall):
                entity.speedX = entity.speedY
            elif getHitbox(portal).intersects(rightWall):
                entity.speedX = -entity.speedY
                
        else:
            #L'entité n'est pas téléporté et a atteint le sol, on arrête de la faire tomber
            entity.stop = True

"""
#--------------------------------------------------------------------------------------#
#-------------------------------------FENETRE------------------------------------------#
#--------------------------------------------------------------------------------------#
"""
    
frameW = 1000
frameH = 900

frame = Tk()
frame.title("Pyrtal")

salle = Canvas(frame, width=frameW, height=frameH)

bluePortal = None
orangePortal = None

#Fond de la salle
salle.create_rectangle(125,788,875,112)

floor = Rect(0, 788, frameW, 125)
ceiling = Rect(0, 0, frameW, 112)
leftWall = Rect(0, 0, 125, frameH)
rightWall = Rect(875, 0, 125, frameH)

"""Effet de profondeur (lignes diagonales)"""
#Bas gauche
salle.create_line(0, frameH, leftWall.width, floor.y)
#Bas droit
salle.create_line(frameW, frameH, rightWall.x, floor.y)
#Haut droit
salle.create_line(frameW, 0, rightWall.x, ceiling.height)
#Haut gauche
salle.create_line(0, 0, leftWall.width, ceiling.height)

#Focus sur la fenêtre pour pouvoir recevoir les clics de souris et l'appuie de touches
salle.focus_set()

dude = Dude(450, 700)
cube = Cube(600, 800)

#Configure les touches souris / clavier
salle.bind("<Button-1>", createBluePortal)
salle.bind("<Button-3>", createOrangePortal)
salle.bind("<KeyPress>", dude.move)

salle.pack()

frame.mainloop()
