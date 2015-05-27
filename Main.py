from rectangle import *
from tkinter import *
from math import *
import threading
import time

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
        #Sinon : Portail vertical
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
        self.moveSpeed = 20
        self.speedY = 0
        self.speedX = 0
        self.isFalling = False
        self.lastMove = ''
        self.lastShoot = 0 #Dernière fois que le dude a placé un portail

    def setImage(self, name):
        self.photo = PhotoImage(file=name)
        self.image = salle.create_image(self.x, self.y, image=self.photo, anchor=NW)
        self.width = self.photo.width() - self.photo.width()/4
        self.height = self.photo.height()

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

    def move(self, x, y):
        #On vérifie si le cube peut bouger c'est à dire qu'il ne sort pas du sol
        if(x > floor.x and x+self.width < floor.x+floor.width and y+self.height > floor.y and y+self.height < floor.y+floor.height):
            self.x = x
            self.y = y
            salle.coords(self.image, self.x, self.y)

"""
#--------------------------------------------------------------------------------------#
#----------------------------------METHODES PORTAILS-----------------------------------#
#--------------------------------------------------------------------------------------#
"""

def createBluePortal(event):
    createPortal(event.x, event.y, 'blue')

def createOrangePortal(event):
    createPortal(event.x, event.y, 'orange')

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

        #Créé un faux portail avec des coordonnées, une hauteur, une largeur, une hitbox, etc. pour pouvoir vérifier s'il peut être placé 
        simulPortal = Portal([x, y], color, False)

        #Si le portail est placé dans un angle, ne pas le poser
        if((getHitbox(simulPortal).intersects(floor) or getHitbox(simulPortal).intersects(ceiling)) and (getHitbox(simulPortal).intersects(leftWall) or getHitbox(simulPortal).intersects(rightWall))):
            return

        #Si un autre portail est placé, on vérifie si le portail qui va être créé n'est pas posé par dessus
        if(otherPortal != None):
            
            #Distance entre le centreX des deux portails
            differenceX = simulPortal.centerX - otherPortal.centerX
            #Distance entre le centreY des deux portails
            differenceY = simulPortal.centerY - otherPortal.centerY

            #Si les deux portails se superposent, on décale le nouveau portail de sorte à ce qu'il se colle à l'autre
            if(getHitbox(simulPortal).intersects(getHitbox(otherPortal))):

                #Si les portails se touchent par un côté
                if(sqrt((differenceX)**2 + (differenceY)**2) < otherPortal.height-50):
                    #Si le portail vient de la droite, ajouter la différence pour le coller contre le bord droite
                    if(differenceX >= 0):
                        x += simulPortal.width - abs(differenceX)
                    #Si le portail vient de la gauche, soustraire la différence pour le coller sur le bord gauche
                    else:
                        x -= simulPortal.width - abs(differenceX)
                        
                #Sinon, c'est qu'ils se touchent par le dessus ou le dessous
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
            #Si le portail avait déjà été posé, l'effacer
            if(orangePortal != None):
                orangePortal.delete() 
            orangePortal = Portal([x, y], '#ff6600', True)
            name = "dude_orange.gif"

        dude.setImage(name)
        #On met le dude et le cube au premier plan
        salle.tag_raise(dude.image)
        salle.tag_raise(cube.image)
        checkHitbox()

def portalPlacement(coordinate, size, bound1, bound2):
    #Si le portail dépasse sur la droite ou vers le bas, on le remonte/le décale sur la gauche
    if(coordinate+size > bound1):
        return (coordinate - (coordinate+size - bound1))
    #Si le portail dépasse sur la gauche ou vers le haut, on le descend/le décale sur la droite
    elif(coordinate-size < bound2):
        return (coordinate - (coordinate-size - bound2))
    #Sinon, la coordonnée n'a pas besoin d'être changée
    else:
        return coordinate

"""
#--------------------------------------------------------------------------------------#
#----------------------------------METHODES ENTITES------------------------------------#
#--------------------------------------------------------------------------------------#
"""

#Retourne un rectangle représentant la zone de collision de l'entité
def getHitbox(entity):
        return Rect(entity.x, entity.y, entity.width, entity.height)

#Téléporte l'entité aux coordonnées x et y
def teleport(entity, x, y):
        entity.x = x
        entity.y = y
        salle.coords(entity.image, entity.x, entity.y)
        salle.tag_raise(entity.image)
        #Si elle n'est pas déjà en train de chuter, on la fait tomber
        if(entity.isFalling == False):
            t = threading.Thread(target=momentum, args=(entity,))
            t.start()

def momentum(entity):
        entity.isFalling = True
        start = time.time()

        #Tant que l'entité n'a pas touché le sol
        while(entity.isFalling == True):
            #Temps écoulé en seconde depuis la dernière boucle
            t = (time.time() - start)*10
            start = time.time()
            
            a = 9.81

            #On limite la vitesse maximale à 500
            if(abs(entity.speedY < 500)):
                entity.speedY = a * t + entity.speedY
                
            entity.y = entity.speedY * t + entity.y
            entity.x = entity.speedX * t + entity.x

            #On veut que l'entité ne tape que la moitié du plafond ou des murs pour donner une impression de perspective
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
    #Si l'entité a atteint le sol alors on vérifie la collision avec les portails
    if(getHitbox(entity).intersects(floor)):

        if(getHitbox(bluePortal).intersects(getHitbox(entity)) or getHitbox(orangePortal).intersects(getHitbox(entity))):
            #Si l'entité passe par le portail bleu
            if(getHitbox(bluePortal).intersects(getHitbox(entity))):
                portal = orangePortal
            #Si l'entité passe par le portail orange
            else:
                portal = bluePortal

            #On cherche où positionner l'entité par rapport au portail
            #L'entité sort par le sol, on la place au dessus du portail et au centre
            if(getHitbox(portal).intersects(floor)):
                y = portal.centerY-(entity.height+portal.height/2)-5
                x = portal.centerX - entity.width/2
            #L'entité sort par le plafond, on la place en dessous du portail et au centre
            elif(getHitbox(portal).intersects(ceiling)):
                y = portal.centerY+(portal.height/2)+5
                x = portal.centerX - entity.width/2
            #L'entité sort par la gauche, on la place à droite du portail et au centre
            elif(getHitbox(portal).intersects(leftWall)):
                y = portal.centerY-entity.height/2
                x = portal.centerX + portal.width/2
            #L'entité sort par la droite, on la place à gauche du portail et au centre
            elif(getHitbox(portal).intersects(rightWall)):
                y = portal.centerY-entity.height/2
                x = portal.centerX - portal.width/2
            #Sinon l'entité sort par le fond de la salle, on la centre juste par rapport au portail
            else:
                y = portal.centerY-entity.height/2
                x = portal.centerX-entity.width/2
                
            teleport(entity, x, y)

            #On modifie les vitesses en fonction de là où elle sort
            if(getHitbox(portal).intersects(floor)):
                entity.speedY = -entity.speedY
            elif getHitbox(portal).intersects(leftWall):
                entity.speedX = entity.speedY
            elif getHitbox(portal).intersects(rightWall):
                entity.speedX = -entity.speedY
                
        else:
            #L'entité n'est pas téléporté et a atteint le sol, on arrête de la faire tomber
            entity.isFalling = False

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
