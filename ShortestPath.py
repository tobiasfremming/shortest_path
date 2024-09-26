
import pygame as pg
import math
import colorsys



LIMIT = 0.6                       
IMAGENAME = 'maze1.jpg'      
RED = (255,0,0)                   
BLUE = (0,0,255)                  
next = [-1,0,1]       
NEXT =[()]
pixelmeter=0.1

 
class Point:
    def __init__(self,x,y):            
        self.x = x
        self.y = y
    def __str__(self):
        return str("(" + str(self.x) + " " + str(self.y)  + ")") 


def getTwinStairs(posisjon, pixels1, pixels2): 
            for i in range(len(pixels1)):
                if posisjon == pixels1[i]:
                    return pixels2[i]
                
            for j in range(len(pixels2)):
                if posisjon == pixels2[j]:
                    return pixels1[j]
                
            return (-1,-1)
            
    
    
def SetDistances(start, end, costs, distances, max, screen, drawscan, pixels1, pixels2):
    sqr2 = math.sqrt(2) 
    for x in range(width): 
        for y in range(height): 
            distances[x][y] = -1 
            
    currentGeneration = [] 
    point = Point(start.x, start.y) 
    distances[start.x][start.y] = 0 
    currentGeneration.append(point) 
    
    while (len(currentGeneration) > 0): 
        nextGeneration = [] 
        for point in currentGeneration:
            if point.x == end.x and point.y == end.y:
                return True
        
            distance = distances[point.x][point.y] 
            for i in next:
                for j in next:
                    x = point. x+ i 
                    y = point.y + j
                    if x < 0 or y < 0 or x > max.x or y > max.y:
                        continue 
        
                    if i == 0 and j == 0: 
                       pos = getTwinStairs((x,y), pixels1, pixels2) 
                       
                       if pos == (-1,-1): 
                           continue 
                       
                       
                       x = pos[0]
                       y = pos[1]
                    cost = costs[x][y]; 
                    if cost == 0: 
                       continue
                   
                    if i == 0 or j == 0: 
                        d = 1               
                    else:
                        d = sqr2 
            
                    newDistance = d / (0.001 + cost) + distance 
                    oldDistance = distances[x][y] 
              
                    if x == end.x and y == end.y:      
                        distances[x][y] = newDistance 
                        return True  
                    elif oldDistance < 0: 
                        distances[x][y] = newDistance 
                    elif newDistance < oldDistance:
                        distances[x][y] = newDistance
                    else:
                        continue                    
                    nextGeneration.append(Point(x,y)) 
              
        currentGeneration = nextGeneration 
        if drawscan:
            for point in currentGeneration:
                fraksjon = distances[point.y][point.y]/max.y 
                fraksjon = fraksjon % 1 
                               
                # Farger er her 0-1, denne gir regnbue farge. Annen type fargekoder enn rgb
                color = colorsys.hsv_to_rgb(fraksjon, 1, 1)
                r = color[0] * 255 
                g = color[1] * 255
                b = color[2] * 255
                screen.set_at((point.x , point.y) , (r,g,b)) 
            pg.display.flip()
    return False

def backtrack(start, end, distances, max, screen):    
    point = end 
    distance = distances[point.x][point.y]
    minDistance = 1000*1000 
    
    while True:
        
        nextPoint = Point(-1,-1) 
      
        for i in next:
            for j in next:          
                x = point.x + i
                y = point.y + j 
                
                if x < 0 or y < 0 or x > max.x or y > max.y: 
                    continue
                if i == 0 and j == 0:
                    pos = getTwinStairs((x,y), pixels1, pixels2) 
                       
                    if pos == (-1,-1):
                        continue
                    
                    x = pos[0]
                    y = pos[1] 

                distance = distances[x][y]
                
                if (distance < 0): 
                    continue 
            
                if (distance > minDistance): 
                    continue
            
                minDistance = distance 
                nextPoint = Point(x,y) 
          
        point = nextPoint 
        distance = minDistance 
        pg.draw.circle(screen, RED, (point.x, point.y), 2) 
        if point.x == start.x and point.y == start.y: 
            return True
    
    return False

def iscolored(color):
    if color.r == color.g and color.g == color.b: 
        return False
    else:
        return True

def GetImageCost(point, image): 
    color = image.get_at(point) 
    if iscolored(color): 
      return 1 
    value = color.b / 255 
    if value < LIMIT:
      return 0 
    return value 

def SetCostsFromImage(costs, image, width, height): 
    for x in range(width): 
        for y in range(height):
            costs[x][y] = GetImageCost((x,y), image) 
def ExpandBlackArea(costs, image, width, height): 
    """_summary_  function to expand the black area

    Args:
        costs (_type_): _description_
        image (_type_): _description_
        width (_type_): _description_
        height (_type_): _description_
    """
    for x in range(width):
        for y in range(height):
            if costs[x][y] == 0: 
                continue 
                
            foundBlackNeigbour = False 
            for i in next:
                for j in next:
                    if i == 0 and j == 0:
                        continue  
                    x_next = x + i 
                    y_next = y + j
                    if x_next < 0 or y_next < 0 or x_next > max.x or y_next > max.y: 
                        continue 
                    
                    cost = GetImageCost((x_next,y_next), image) 
                    if cost == 0:
                        foundBlackNeigbour = True 
                        break
                if foundBlackNeigbour:
                      break
                  
            if foundBlackNeigbour:    
              costs[x][y] = 0 
              
              
def getPixels(pixels1, pixels2):
    """_summary_  function to find the pixels of the stairs

    Args:
        pixels1 (Point): _description_
        pixels2 (Point): _description_
    """
    for x in range(width): 
        for y in range(height):
            if x < width/2: 
                array = pixels1
            else:
                array = pixels2 
            color = image.get_at((x, y)) 
            if color.r == 255 and color.g == 0 and color.b == 0:
                array.append((x,y))
            elif color.r == 255 and color.g == 255 and color.b == 0:
                array.append((x,y))
            elif color.r == 255 and color.g == 0 and color.b == 255:
                array.append((x,y))
            elif color.r == 0 and color.g == 255 and color.b == 0:
                array.append((x,y))
            elif color.r == 0 and color.g == 0 and color.b == 255:
                array.append((x,y))
            elif color.r == 0 and color.g == 255 and color.b == 255:
                array.append((x,y))
            elif color.r == 200 and color.g == 200 and color.b == 0:
                array.append((x,y))
            elif color.r == 200 and color.g == 0 and color.b == 200:
                array.append((x,y))
            else:
                continue
 
image = pg.image.load(IMAGENAME) 
imagerect = image.get_rect() 
# width = image.get_width() 
# height = image.get_height() 
width = 1000
height = 600   

max = Point(width-1, height-1) 

# stairs (must have been added as a colored pixel in the image)
array=1 
pixels1=[] # one array for each floor
pixels2=[]

getPixels(pixels1,pixels2) 



            
            
#==========================================================================
# Dynamisk 2 dimensionale array som er lik antall pixeler
#==========================================================================

distances = [ [ 0 for x in range(height) ] for y in range(width) ] #setter alle avstander
costs = [ [ 0 for x in range(height) ] for y in range(width) ] #setter alle kostnasder
SetCostsFromImage(costs, image, width, height) #kaller på funksjon
ExpandBlackArea(costs, image, width, height) #klaller på funksjon

#==========================================================================
# Initierer grafikken
#==========================================================================

pg.init() #initierer programmet i pygame
screen = pg.display.set_mode((width, height)) #setteer vindu (screen)
pg.font.init() #fontkomando så man kan formidle en instruks
font = pg.font.SysFont('Comic Sans MS', 60) #bestemmer font og størrelse
notFoundText = font.render("Ikke funnet!", True, RED) #bestemmer en tekst som kommer hvis den ikke finner sluttpunkt
clickText = font.render("Klikk på to punkter!", True, BLUE) #instruks

#==========================================================================
# Tegner start bildet
#==========================================================================

screen.fill((0, 0, 0)) #fyller bildet med fargene(tupple)
screen.blit(image, imagerect) #bildeet lages
screen.blit(clickText, (20, 20)) #tekst
pg.display.flip() #stopper

  
running = True #den runner
clickedPositions = [] #definerer liste over punkter som skal bestemmes

while running: #hovedloopen
    
    print("HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
   
    pg.time.wait(10) #delay
  
    for event in pg.event.get(): #hvis noe skjer, kort sagt
        if event.type == pg.MOUSEBUTTONUP: #hvis museknappen trykkes
          clickedPositions.append(pg.mouse.get_pos()) #setter punktet som trykkes på til listen over start og stopppunkt
          
        if event.type == pg.QUIT: #stopper
            running = False
            pg.quit()

        if len(clickedPositions) == 2: #finner valgte posisjoner
            start = Point(clickedPositions[0][0], clickedPositions[0][1])
            end = Point(clickedPositions[1][0], clickedPositions[1][1])
            clickedPositions.clear()

            # Tegner opp bildet og start/ende punkter
            screen.fill((0, 0, 0)) 
            screen.blit(image, imagerect)
            pg.draw.circle(screen, BLUE, (start.x, start.y), 5)
            pg.draw.circle(screen, RED, (end.x, end.y), 5)
            pg.display.flip()

            # Finner alle distansene
            found = SetDistances(start, end, costs, distances, max, screen, True, pixels1, pixels2)
             
            if not found:
                screen.blit(notFoundText, (20, 20)) #not found tekst komme rpå skjermen
            else:
                # Tegner opp veien
                screen.fill((0, 0, 0)) 
                screen.blit(image, imagerect) #tegner opp
                if not backtrack(start, end, distances, max, screen): #kaller på backtrack funksjon
                   screen.blit(notFoundText, (20, 20)) #tegner opp not found tekst
            
            time = (distances[end.x][end.y]/5.81)*1.2 #setter tiden det tar å gå. jeg regnet med at man bruker 1,2 sekunder pr meter og forholdet piksel pr meter er på 5.81
            minutes = time//60 #antall minutter som ikke er en del av en hel time
            seconds = time%60 #antall hele timer
            print ("Du bruker ", minutes, " minutter og ", seconds," sekunder på å gå denne strekningen")
            pg.display.flip() 
          





