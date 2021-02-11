'''
******************************************************************
                        Instituto Tecnológico de Costa Rica
                            Ingeniería en Computadores
        Module: Star Force
        
        Python version: Python 3.8.2

        Author: Ignacio Vargas Campos
        
        Versión: 1.0

        Fecha de Última Modificación: 8/08/2020
        
*****************************************************************
'''

from random import *
import tkinter as tk
import pygame
from pygame.locals import *
import os
import platform

#mi_auto_doc()
def mi_auto_doc():
    print("load_img(file):",load_img.__doc__)
    print("load_font(file,size):",load_font.__doc__)
    print("read_file(fileName):",read_file.__doc__)
    print("save_file(fileName, writeList):",save_file.__doc__)
    print("get_spaceship_img(inclination):",get_spaceship_img.__doc__)
    print("get_pilot_img(pilot, scale=1):",get_pilot_img.__doc__)
    print("get_flag_img(flag, scale=1):",get_flag_img.__doc__)
    print("erase_area(x,y=0,width=0,height=0):",erase_area.__doc__)
    print("draw_text(text,font,color,surface,x,y):",draw_text.__doc__)
    print("main_menu(resetting=True):",main_menu.__doc__)
    print("about(resetting=True):",about.__doc__)
    print("dropdown_menu(resetting=True,click=False,scrolled=0,scrolling=False):",dropdown_menu.__doc__)
    print("score_position(orderedList,score,scoreType,i=0):",score_position.__doc__)
    print("top7_scores(scoreType,orderedList,pilotsList=[]):",top7_scores.__doc__)
    print("scores(resetting=True):",scores.__doc__)
    print("display_pilots(page,nameBox):",display_pilots.__doc__)
    print("changing_flag(page,flagBox,resetting=True):",changing_flag.__doc__)
    print("changing_pic(page,picBox,resetting=True):",changing_pic.__doc__)
    print("changing_logo(page,logoBox,resetting=True):",changing_logo.__doc__)
    print("add_new_pilot(page,newPilot=['','0','0','0','0','0'],stage=0,resetting=True):",add_new_pilot.__doc__)
    print("configurations(resetting=True,page=0,nameActive=False,nameBox=-1):",configurations.__doc__)
    print("check_keys_typing(eventList,string):",check_keys_typing.__doc__)
    print("shoot(sx,sy,inclination):",shoot.__doc__)
    print("check_shooting_collisions(shot,asteroidList):",check_shooting_collisions.__doc__)
    print("check_asteroids_collisions(asteroidList,hurtBox):",check_asteroids_collisions.__doc__)
    print("inside_circle(center,radius,point):",inside_circle.__doc__)
    print("points_inside_ring(ring,radius,hurtBox):",points_inside_ring.__doc__)
    print("check_rings_collisions(ringList,hurtBox):",check_rings_collisions.__doc__)
    print("check_fuel(canistersList,hurtBox):",check_fuel.__doc__)
    print("end_screen(condition,gameType,resetting=True):",end_screen.__doc__)
    print("game_maneuvers(resetting=True)",game_maneuvers.__doc__)
    print("game_asteroids(resetting=True):",game_asteroids.__doc__)

#misc functions
seed()

def load_img(file):
    '''
    Parameter: file name
    
    Return: pygame image object of specified image

    Restrictions: Image must be in 'imgs' folder, which must be in same folder as program, and it's name must be given as a string
    '''
    print("loaded "+file)
    path=os.path.join('imgs',file)
    image=pygame.image.load(path)
    return image

def load_font(file,size):
    '''
    Parameter: font name
    
    Return: pygame font object of specified font

    Restrictions: Font must be in 'fonts' folder, which must be in same folder as program, and it's name must be given as a string
    '''
    print("loaded "+file)
    path=os.path.join('fonts',file)
    font=pygame.font.Font(path,size)
    return font

def quit_application():
    root.destroy()
    pygame.quit()

def empty_list(emptiedList):
    if emptiedList==[]:
        return
    else:
        emptiedList.pop(0)
        empty_list(emptiedList)

def lenn(someList):
    if someList==[] or someList=="":
        return 0
    else:
        return 1+lenn(someList[1:])

#file handling
def read_file_aux(f,readList): #this function only works for crew list
    n=f.read(1)
    if n=='':
        return readList

    #[['name','pic#','flag#','brand#','asteroids score','maneuvers score']
     
    if n!='\n':
        ame=f.readline()[:-1]
        name=n+ame
    else:
        name=''
        
    
    pic=f.readline()[:-1] #[:-1] removes \n
    flag=f.readline()[:-1]
    brand=f.readline()[:-1]
    score1=f.readline()[:-1]
    score2=f.readline()[:-1]
    
    readList+=[[name,pic,flag,brand,score1,score2]] #remember everything ends with \n
    
    return read_file_aux(f,readList)
    

def read_file(fileName): #this function only works for a list of lists of strings
    '''
    Parameters: fileName
    
    Return: List with crew data 

    Restrictions: file name must be "crew"
    '''
    try:
        f=open(fileName, 'r')
        readList=read_file_aux(f,[])
        f.close()
    except:
        f=open(fileName,'w')
        readList=[]
        f.close()
        
    return readList 

def save_file_aux(f,writeList,i=0):
    if writeList==[]:
        return
    if i==lenn(writeList[0]):
        save_file_aux(f,writeList[1:])
    else:
        f.write(writeList[0][i]+'\n')
        save_file_aux(f,writeList,i+1)
    
    
def save_file(fileName, writeList): #this function only works for a list of lists of strings
    '''
    Parameters: fileName, writeList
    
    Return: None 

    Restrictions: file name must be "crew", writeList must be a list of lists, with all of their entries as strings
    '''
    try:
        f=open(fileName, 'w')
        save_file_aux(f,writeList)
        f.close()
        print(fileName[:-4]+" saved succesfully!") #[-4] para quitar el '.txt'
    except:
        print("Error while trying to save "+fileName[:-4]+" data")
    return


#global variables
screenHeight=720
screenWidth=1280 #16:9 aspect ratio
history=[]
        
#main tkinter window
root = tk.Tk()
root.title('Star Force')
root.minsize(screenWidth,screenHeight)
root.resizable(width='NO',height='NO')

icon = tk.PhotoImage(file = "imgs\icon.png")
root.iconphoto(False, icon)
#initializing pygame (embedded into tkinter)
embed = tk.Frame(root, width = screenWidth, height = screenHeight) #creates embed frame for pygame window
embed.pack() #packs window to the left

os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
if platform.system == 'Windows': #this if is for cross-platform compatibility
    os.environ['SDL_VIDEODRIVER'] = 'windib'

pygame.init() #must be initialized after frame embed
screen = pygame.display.set_mode((screenWidth,screenHeight))

#images
bgIMG           = load_img('bg.png')
starforceIMG    = load_img('starforce.png')
cardIMG         = load_img('character card.png')
addCardIMG      = load_img('add card.png')
flagsIMG        = load_img('europe flags.png')
pilotsIMG       = load_img('pilots sprites.png')
arrowfIMG       = load_img('arrowf.png')
arrowbIMG       = load_img('arrowb.png')
xIMG            = load_img('x.png')
dropdownIMG     = load_img('dropdown bar.png')
aboutIMG        = load_img('about screen.png')
screenIMG       = load_img('blank screen.png')
spaceshipsIMG   = load_img('spacecraft.png')
asteroidIMG     = load_img('asteroid.png')
crosshairIMG    = load_img('crosshairs.png')
ringIMG         = load_img('ring.png')
shotIMG         = load_img('green shot.png')
fuelIconIMG     = load_img('fuel icon.png')
fuelCanisterIMG = load_img('fuel canister.png')
heartIMG        = load_img('heart canister.png')

logos=[load_img('logo0.png'),load_img('logo1.png'),load_img('logo2.png'),load_img('logo3.png'),load_img('logo4.png'),load_img('logo5.png'),load_img('logo6.png'),load_img('logo7.png')]


#fonts
buttonFONT      = load_font('SpaceMadness.ttf',55)
difficultyFONT  = load_font('SpaceMadness.ttf',42)
nameFONT        = load_font('Silver.ttf',45)
smallNameFONT   = load_font('Silver.ttf',42)
scoreFONT       = load_font('Silver.ttf',25)
highScoresFONT  = load_font('Silver.ttf',55)
resultsFONT     = load_font('Silver.ttf',65)

#colors
GREY=GRAY=(96,95,103)
LIGHTGREY=LIGHTGRAY=(181,181,181)
WHITE=(255,255,255)
ORANGE=(200,100,20)
LIGHTORANGE=(240,160,95)
BLUE=(23,43,194)
DARKBLUE=(14,14,84)
MIDNIGHTBLUE=(10,3,41)

#misc pygame functions

def get_spaceship_img(inclination): #inclination goes from -3 to 4
    '''
    Parameters: inclination
    
    Return: surface of corresponding spaceship img

    Restrictions: inclination must be int value between -3 and 4
    '''
    row=inclination+3
    column=0

    width=213
    height=119
    x=0
    y=height*row

    surface=pygame.Surface((width,height)) #creates empty surface
    surface.fill((255,0,255))
    surface.set_colorkey((255,0,255))#makes bg transparent
    surface.blit(spaceshipsIMG,(0,0),(x,y,width,height)) #crops pilots image to surface

    return surface

def get_pilot_img(pilot, scale=1):
    '''
    Parameters: specified pilot
    
    Return: surface of corresponding pilot img

    Restrictions: pilot must be specified with int between 0 and 14
    '''
    row=pilot//5
    column=pilot%5

    width=56
    height=62
    x=width*column
    y=height*row
    
    surface=pygame.Surface((width,height)) #creates empty surface
    surface.fill((255,0,255))
    surface.set_colorkey((255,0,255))#makes bg transparent
    surface.blit(pilotsIMG,(0,0),(x,y,width,height)) #crops pilots image to surface
    

    if scale!=1:
        surface=pygame.transform.scale(surface,(round(width*scale),round(height*scale))) #optional scaling
        
    return surface

def get_flag_img(flag, scale=1):
    '''
    Parameters: specified flag
    
    Return: surface of corresponding flag img

    Restrictions: flag must be specified with int between 0 and 49
    '''
    row=flag//10
    column=flag%10

    width=32
    height=24
    x=width*column
    y=height*row
    
    surface=pygame.Surface((width,height)) #creates empty surface
    surface.fill((255,0,255))
    surface.set_colorkey((255,0,255)) #makes bg transparent
    surface.blit(flagsIMG,(0,0),(x,y,width,height)) #crops pilots image to surface

    if scale!=1:
        surface=pygame.transform.scale(surface,(round(width*scale),round(height*scale)))
        
    return surface

def erase_area(x,y=0,width=0,height=0):
    '''
    Parameters: x, y, width, geight
    
    Return: None

    Restrictions: all value must be ints, or x can be a Rect object and no other values must be specified
    '''
    if isinstance(x,int):
        pass
    else:
        rect=x
        x=rect.left
        y=rect.top
        width=rect.width
        height=rect.height
    surface=pygame.Surface((width,height)) #creates empty surface
    surface.blit(bgIMG,(0,0),(x,y,width,height)) #crops background image to surface
    screen.blit(surface,(x,y)) #blit surface to screen
    
def draw_text(text,font,color,surface,x,y):
    '''
    Parameters: text, font, color, surface, x, y
    
    Return: None

    Restrictions1: text must be string, font must be pygame font object 
    '''
    #print(text)
    if text=="":
        return
    text=font.render(text,1,color)
    surface.blit(text,(x,y))
        
    
def check_keys(eventList):
    if eventList==[]:
        return
    if eventList[0].type==KEYDOWN:
        if not eventList[0].key in history:
            history.append(eventList[0].key)     
    elif eventList[0].type==KEYUP:
        if eventList[0].key in history:
            history.remove(eventList[0].key)

    check_keys(eventList[1:])

def check_clicks(eventList,clickList):
    if eventList==[]:
        return clickList
    if eventList[0].type==MOUSEBUTTONDOWN:
        clickList.append(eventList[0].button)

    return check_clicks(eventList[1:],clickList)
    
        

################################################################------------Menu------------#################################################################################
selectedPilot=0
crew=[] #[['name','pic#','flag#','brand#','asteroids score','maneuvers score'],[another crewmember],...]
difficulty='EASY'

def main_menu(resetting=True):
    '''
    Parameters: resetting=True
    
    Return: None

    Restrictions: unless being called from within iself, resetting must not be provided 
    '''
    global easyColor,mediumColor,hardColor,difficulty,selectedPilot
    
    running=True
    events=pygame.event.get()
    check_keys(events)
    
    if resetting:
        pygame.event.clear()
        screen.blit(bgIMG, (0, 0))
        screen.blit(starforceIMG, (350, 30))
        easyColor=LIGHTORANGE
        mediumColor=ORANGE
        hardColor=ORANGE

        screen.blit(dropdownIMG,(490,228))
        draw_text(crew[selectedPilot][0],smallNameFONT,WHITE,screen,500,230)
        screen.blit(get_pilot_img(int(crew[selectedPilot][1]),0.5),(720,233))
        
    click=False
    if 1 in check_clicks(events,[]):
        click=True

    dropdownButton  = pygame.Rect(490,228,300,39)
    
    asteroidsButton = pygame.Rect(314,290,254,40)   
    maneuversButton = pygame.Rect(716,290,250,40)
    configButton    = pygame.Rect(515,470,250,40)
    scoresButton    = pygame.Rect(486,550,308,40)
    aboutButton     = pygame.Rect(574,630,132,40)

    easyButton      = pygame.Rect(384,358,92,36)
    mediumButton    = pygame.Rect(570,358,140,36)
    hardButton      = pygame.Rect(805,358,92,36)
    
    asteroidsColor=GREY
    maneuversColor=GREY
    configColor=GREY
    scoresColor=GREY
    aboutColor=GREY

    mx,my=pygame.mouse.get_pos()
    if dropdownButton.collidepoint((mx,my)) and click:
        dropdown_menu()
        running=False
    if asteroidsButton.collidepoint((mx,my)):
        asteroidsColor=WHITE
        if click:
            game_asteroids()
            running=False
    elif maneuversButton.collidepoint((mx,my)):
        maneuversColor=WHITE
        if click:
            game_maneuvers()
            running=False
    elif configButton.collidepoint((mx,my)):
        configColor=WHITE
        if click:
            configurations()
            running=False
    elif scoresButton.collidepoint((mx,my)):
        scoresColor=WHITE
        if click:
            scores()
            running=False
    elif aboutButton.collidepoint((mx,my)):
        aboutColor=WHITE
        if click: 
            about()
            running=False
    elif easyButton.collidepoint((mx,my)):
        if click:
            difficulty="EASY"
    elif mediumButton.collidepoint((mx,my)):
        if click:
            difficulty="MEDIUM"
    elif hardButton.collidepoint((mx,my)):
        if click:
            difficulty="HARD"

    if difficulty=="EASY":
        easyColor=LIGHTORANGE
        mediumColor=ORANGE
        hardColor=ORANGE
    elif difficulty=="MEDIUM":
        easyColor=ORANGE
        mediumColor=LIGHTORANGE
        hardColor=ORANGE
    elif difficulty=="HARD":
        easyColor=ORANGE
        mediumColor=ORANGE
        hardColor=LIGHTORANGE
            
    
    if running:
        erase_area(asteroidsButton)
        erase_area(maneuversButton)
        erase_area(configButton)
        erase_area(scoresButton)
        erase_area(aboutButton)
        erase_area(easyButton)
        erase_area(mediumButton)
        erase_area(hardButton)
        
        #pygame.draw.rect(screen,(0,0,255),asteroidsButton)
        #pygame.draw.rect(screen,(0,0,255),maneuversButton)
        #pygame.draw.rect(screen,(0,0,255),configButton)
        #pygame.draw.rect(screen,(0,255,0),scoresButton)
        #pygame.draw.rect(screen,(255,0,0),aboutButton)
        #pygame.draw.rect(screen,(0,0,255),easyButton)
        #pygame.draw.rect(screen,(0,255,0),mediumButton)
        #pygame.draw.rect(screen,(255,0,0),hardButton)
        draw_text("ASTEROIDS",buttonFONT,asteroidsColor,screen,314,288)
        draw_text("MANEUVERS",buttonFONT,maneuversColor,screen,716,288)
        draw_text("CONFIGURE",buttonFONT,configColor,screen,515,470)
        draw_text("HIGH SCORES",buttonFONT,scoresColor,screen,486,550)
        draw_text("ABOUT",buttonFONT,aboutColor,screen,574,630)
        draw_text("EASY",difficultyFONT,easyColor,screen,389,360)
        draw_text("MEDIUM",difficultyFONT,mediumColor,screen,576,360)
        draw_text("HARD",difficultyFONT,hardColor,screen,810,360)

        pygame.display.update()
        root.after(17,main_menu,False) #60fps

def about(resetting=True):
    '''
    Parameters: resetting=True
    
    Return: None

    Restrictions: unless being called from within iself, resetting must not be provided 
    '''
    running=True
    events=pygame.event.get()
    check_keys(events)
    
    if resetting:
        lastModified="August 8, 2020"
        version="1.0.0"
        
        screen.blit(aboutIMG,(320,120))
        draw_text(lastModified,scoreFONT,WHITE,screen,330,503)
        draw_text(version,scoreFONT,WHITE,screen,330,570)
        

    aboutBox=pygame.Rect(320,120,640,480)

    click=False
    if 1 in check_clicks(events,[]):
        click=True

    mx,my=pygame.mouse.get_pos()
    if K_ESCAPE in history or (click and not aboutBox.collidepoint((mx,my))):
        running=False
        main_menu()

    if running:
        pygame.display.update()
        root.after(17,about,False)

################################################################------------Dropdown------------##############################################################################################################################

def display_dropdown(dropdownRect,highlightI,position,i=0): #300x35 (39px on right is the arrow/scroll bar)
    if position<=selectedPilot:
        if i==lenn(crew) or i==14:                               #x=490
            return
    else:
        if i==lenn(crew) or i==13:                               #x=490
            return
    if i==0:
        pygame.draw.rect(screen,MIDNIGHTBLUE,dropdownRect)
    if i+position==selectedPilot:
        pass
    else:
        if i+position<selectedPilot or position>selectedPilot:
            y=267+35*i
        else:
            y=267+35*(i-1)

        if (position<=selectedPilot and i==highlightI-position) or (position>selectedPilot and i==highlightI-position-1):
            if lenn(crew)>14:
                pygame.draw.rect(screen,BLUE,(490,y,261,35))
            else:
                pygame.draw.rect(screen,BLUE,(490,y,300,35))
                    
        if position<=selectedPilot:
            draw_text(crew[i+position][0],smallNameFONT,WHITE,screen,500,y)  #y, x+10
            screen.blit(get_pilot_img(int(crew[i+position][1]),0.5),(720,y+3)) #y+3, x+230
        else:
            draw_text(crew[i+position+1][0],smallNameFONT,WHITE,screen,500,y)  #y, x+10
            screen.blit(get_pilot_img(int(crew[i+position+1][1]),0.5),(720,y+3)) #y+3, x+230
    display_dropdown(dropdownRect,highlightI,position,i+1)

def display_scrollbar(position):
    #starts at 268, height-268=452
    pygame.draw.rect(screen,MIDNIGHTBLUE,(751,267,39,screenHeight-267))
    pygame.draw.line(screen,GREY,(751,267),(751,screenHeight),2)
    pygame.draw.line(screen,GREY,(788,267),(788,screenHeight),2)
    
    extraCrew=lenn(crew)-14
    barHeight=452/(extraCrew+1)
    barWidth=33
    x=754
    y=round(268+position*barHeight)
    bar=pygame.Rect(x,y,barWidth,round(barHeight))
    pygame.draw.rect(screen,GREY,bar)

def check_scrolls(scrolled,clicksList):
    if clicksList==[]:
        return scrolled
    
    if clicksList[0]==4:
        scrolled-=1
        if scrolled<0:
            scrolled=0
    elif clicksList[0]==5:
        scrolled+=1
        if scrolled>lenn(crew)-14:
            scrolled=lenn(crew)-14
            
    return check_scrolls(scrolled,clicksList[1:])
    

def dropdown_menu(resetting=True,click=False,scrolled=0,scrolling=False):
    '''
    Parameters: resetting=True, click=False, scrolled=0, scrolling=False
    
    Return: None

    Restrictions: unless being called from within iself, none of the parameters must be provided 
    '''
    global selectedPilot
    running=True
    events=pygame.event.get()
    check_keys(events)

    #14 characters fills up the screen
    scrollable=False
    if lenn(crew)>14:
        scrollable=True
        
    if resetting:
        pygame.event.clear()
    
    click=False
    if 1 in check_clicks(events,[]):
        click=True

    mx,my=pygame.mouse.get_pos()
    if not scrollable:
        dropdownBox=pygame.Rect(490,267,300,(lenn(crew)-1)*35)
        
        if (K_ESCAPE in history) or (not dropdownBox.collidepoint((mx,my)) and click):
            running=False
            main_menu()

    
    elif scrollable:
        dropdownBox=pygame.Rect(490,267,261,(lenn(crew)-1)*35)
        scrollBox=pygame.Rect(751,267,39,screenHeight-267)

        scrolled=check_scrolls(scrolled,check_clicks(events,[]))

        if scrolling:
            if pygame.mouse.get_pressed()[0]:
                if my>267:
                    scrolled=int((my-267)//(452/(lenn(crew)-13)))
            else:
                scrolling==False
        else:
            if click and scrollBox.collidepoint((mx,my)) and (my-267)//(452/(lenn(crew)-13))==scrolled:
                scrolling=True
        
        if (K_ESCAPE in history) or (not dropdownBox.collidepoint((mx,my)) and not scrollBox.collidepoint((mx,my)) and click):
            running=False
            main_menu() 
    
    if dropdownBox.collidepoint((mx,my)):
        mouseOverPilot=(my-267)//35+scrolled
        if mouseOverPilot>=selectedPilot: #to account for the missing selected pilot
            mouseOverPilot+=1
        
        if click:
            selectedPilot=mouseOverPilot
            running=False
            main_menu()
    else:
        mouseOverPilot= -1
        
    if running:
        erase_area(dropdownBox)
        display_dropdown(dropdownBox,mouseOverPilot,scrolled)
        if scrollable:
            display_scrollbar(scrolled)
        pygame.display.update()
        root.after(17,dropdown_menu,False,click,scrolled,scrolling)
        
################################################################------------Scores------------##############################################################################################################################

#['name','pic#','flag#','brand#','asteroids score','maneuvers score']


def score_position(orderedList,score,scoreType,i=0): #returns score's index
    '''
    Parameters: orderedList, score, scoreType, i=0
    
    Return: position in which score should be inserted

    Restrictions: orderedList must be a list of pilots in which they're odered by score descending, score must be int, scoreType must be 'asteroids' or 'maneuvers'
    '''
    if orderedList==[]:
        return i
    if scoreType=='asteroids':
        if score>int(orderedList[0][4]):
            return i
    elif scoreType=='maneuvers':
        if score>int(orderedList[0][5]):
            return i
    else:
        print('score_position error, scoreType must be "asteroids" or "maneuvers"')
        return

    return score_position(orderedList[1:],score,scoreType,i+1)
    

def top7_scores(scoreType,orderedList,pilotsList=[]):
    '''
    Parameters: scoreType, orderedList, pilotsList=[]
    
    Return: list with top7 pilots ordered by score

    Restrictions: scoreType must be 'asteroids' or 'maneuvers', orderedList must be empty list, pilotsList must no be specified
    '''
    if orderedList==[]:
        pilotsList=crew
    if pilotsList==[]:
        return orderedList[:7]

    if scoreType=='asteroids':
        i=score_position(orderedList,int(pilotsList[0][4]),'asteroids')
    elif scoreType=='maneuvers':
        i=score_position(orderedList,int(pilotsList[0][5]),'maneuvers')
    orderedList.insert(i,pilotsList[0])

    return top7_scores(scoreType,orderedList,pilotsList[1:])


def display_positions(i=0):
    if i==7:
        return
    x1=50
    x2=754
    startY=170
    y=round(startY+i*(screenHeight-startY)/7)
    draw_text(str(i+1)+".",highScoresFONT,WHITE,screen,x1,y)
    draw_text(str(i+1)+".",highScoresFONT,WHITE,screen,x2,y)

    display_positions(i+1)

def display_scores(asteroidPilotsList,maneuverPilotsList,i=0):
    if i==7:
        return
    x1=120
    x2=824
    startY=170
    y=round(startY+i*(screenHeight-startY)/7)
    draw_text(asteroidPilotsList[0][4],highScoresFONT,WHITE,screen,x1,y)
    draw_text(maneuverPilotsList[0][5],highScoresFONT,WHITE,screen,x2,y)

    display_scores(asteroidPilotsList[1:],maneuverPilotsList[1:],i+1)

def display_names(asteroidPilotsList,maneuverPilotsList,i=0):
    if i==7:
        return
    x1=250
    x2=954
    startY=170
    y=round(startY+i*(screenHeight-startY)/7)+5
    draw_text(asteroidPilotsList[0][0],nameFONT,WHITE,screen,x1,y)
    draw_text(maneuverPilotsList[0][0],nameFONT,WHITE,screen,x2,y)

    display_names(asteroidPilotsList[1:],maneuverPilotsList[1:],i+1)

def display_pictures(asteroidPilotsList,maneuverPilotsList,i=0):
    if i==7:
        return
    x1=470
    x2=1174
    startY=170
    y=round(startY+i*(screenHeight-startY)/7)
    
    asteroidsPic=get_pilot_img(int(asteroidPilotsList[0][1]))
    maneuversPic=get_pilot_img(int(maneuverPilotsList[0][1]))

    screen.blit(asteroidsPic,(x1,y))
    screen.blit(maneuversPic,(x2,y))

    display_pictures(asteroidPilotsList[1:],maneuverPilotsList[1:],i+1)

def scores(resetting=True):
    '''
    Parameters: resetting=True
    
    Return: None

    Restrictions: unless being called from within iself, resetting must not be provided 
    '''
    running=True
    events=pygame.event.get()
    check_keys(events)
    
    if resetting:
        screen.blit(bgIMG, (0, 0))
        draw_text("ASTEROIDS",buttonFONT,WHITE,screen,120,100)
        draw_text("MANEUVERS",buttonFONT,WHITE,screen,824,100)
        
        top7Asteroids=top7_scores('asteroids',[])
        top7Maneuvers=top7_scores('maneuvers',[])

        display_positions()                   
        display_scores(top7Asteroids,top7Maneuvers)
        display_names(top7Asteroids,top7Maneuvers)
        display_pictures(top7Asteroids,top7Maneuvers)

    if K_ESCAPE in history:
        running=False
        main_menu()

    if running:
        pygame.display.update()
        root.after(17,scores,False)
        
###############################################################------------Config & Crew------------########################################################################################################
def initialize_crew(i=0):
    if i==12:
        return
    names=['Kirk','Fullerton','Wolf','Hartsfield','Hauck','Engle','McArthur','Smith','Scott','McCulley','van Hoften','Lee']
    name=names[i]
    if i==0:
        pic='0'
    else:
        pic=str(randint(1,14))
    flag=str(randint(0,49))
    brand=str(randint(0,7))
    score1=str(randint(0,3)*1000) #max has to be 30% of max score
    score2=str(randint(0,3)*1000)
    crewmember=[name,pic,flag,brand,score1,score2]

    crew.append(crewmember)

    initialize_crew(i+1)
    

def display_pilots_aux(pilotsList,nameBox,i=0):
    if i==0 or i==1:
        y=27
    elif i==2 or i==3:
        y=385
        
    if i==0 or i==2:
        x=330
    elif i==1 or i==3:
        x=690
        
    if pilotsList==[]:
        if i==4:
            return
        else:
            screen.blit(addCardIMG, (x, y))
            return
    else:
        screen.blit(cardIMG, (x, y)) #pic: x+23 y+23, flag: x+28 y+28, logo: x+146 y+34, name: x+23, y+169, score: x+24 y+231, score2: x+24 y+272

        name=pilotsList[0][0]
        pic=get_pilot_img(int(pilotsList[0][1]),1.3)
        flag=get_flag_img(int(pilotsList[0][2]),0.75)
        logo=logos[int(pilotsList[0][3])]
        score1=pilotsList[0][4]
        score2=pilotsList[0][5]

        screen.blit(pic, (x+35, y+40))
        screen.blit(flag, (x+28, y+28))
        screen.blit(logo, (x+146, y+34))

        if i==nameBox:
            draw_text(name,nameFONT,WHITE,screen,x+25,y+165)
        else:
            draw_text(name,nameFONT,LIGHTGREY,screen,x+25,y+165)
        draw_text(score1,scoreFONT,WHITE,screen,x+24,y+231)
        draw_text(score2,scoreFONT,WHITE,screen,x+24,y+272)

        if lenn(crew)>12:
            screen.blit(xIMG, (x+265, y))

        display_pilots_aux(pilotsList[1:],nameBox,i+1)
        

def display_pilots(page,nameBox):
    '''
    Parameters: page, nameBox
    
    Return: None

    Restrictions: page must be int, nameBox must be int between -1 and 3 
    '''
    pilotsList=crew[page*4:(page+1)*4]
    display_pilots_aux(pilotsList,nameBox)
    return

def display_flags(flagNumber=0):
    if flagNumber==50:
        return
    #horizontal: 20 de margen a los lados y 34 entre las banderas
    #vertical: 40 de margen y 55 entre banderas
    column=flagNumber%10
    row=flagNumber//10
    x=307+20+(32+34)*column
    y=150+40+(24+55)*row

    flag=get_flag_img(flagNumber)

    screen.blit(flag,(x,y))
    display_flags(flagNumber+1)

def check_flag_click(mx,my,i=0):
    if i==50:
        return i
    else:
        column=i%10
        row=i//10
        x=307+20+(32+34)*column
        y=150+40+(24+55)*row
        if mx>=x and mx<=(x+32):
            if my>=y and my<=(y+24):
                return i
        return check_flag_click(mx,my,i+1)
    
def changing_flag(page,flagBox,resetting=True):
    '''
    Parameters: page, flagBox, resetting=True
    
    Return: None

    Restrictions: page must be int, flagBox must be recto object, resetting must only be specified if being called recursively 
    '''
    running=True
    events=pygame.event.get()
    check_keys(events)
    
    if resetting:
        pygame.event.clear()
        pygame.draw.rect(screen,DARKBLUE,(307,150,666,420))
        display_flags()
        
    click=False
    if 1 in check_clicks(events,[]):
        click=True

    mx,my=pygame.mouse.get_pos()
    if click:
        flag=check_flag_click(mx,my)
        if flag<50:
            crew[page*4+flagBox][2]=str(flag)
            running=False
            save_file("crew.txt",crew)
            configurations(page=page)
            
    if K_ESCAPE in history:
        running=False
        history.remove(K_ESCAPE)
        configurations(page=page)

    if running:
        pygame.display.update()

        root.after(17,changing_flag,page,flagBox,False)
        
def display_pics(picNumber=0):
    if picNumber==15:
        return #son 56x62
    #horizontal: 55 de margen a los lados y 69 entre las fotos
    #vertical: 45 de margen y 48 entre fotos
    column=picNumber%5
    row=picNumber//5
    x=307+55+(56+69)*column
    y=150+68+(62+48)*row

    pic=get_pilot_img(picNumber)

    screen.blit(pic,(x,y))
    display_pics(picNumber+1)

def check_pic_click(mx,my,i=0):
    if i==15:
        return i
    else:
        column=i%5
        row=i//5
        x=307+55+(56+69)*column
        y=150+68+(62+48)*row
        if mx>=x and mx<=(x+56):
            if my>=y and my<=(y+62):
                return i
        return check_pic_click(mx,my,i+1)
    
def changing_pic(page,picBox,resetting=True):
    '''
    Parameters: page, picBox, resetting=True
    
    Return: None

    Restrictions: page must be int, picBox must be Rect object, resetting must only be specified when called recursively 
    '''
    running=True
    events=pygame.event.get()
    check_keys(events)
    
    if resetting:
        pygame.event.clear()
        pygame.draw.rect(screen,DARKBLUE,(307,150,666,420))
        display_pics()
        
    click=False
    if 1 in check_clicks(events,[]):
        click=True

    mx,my=pygame.mouse.get_pos()
    if click:
        pic=check_pic_click(mx,my)
        if pic<15:
            crew[page*4+picBox][1]=str(pic)
            running=False
            save_file("crew.txt",crew)
            configurations(page=page)
            
    if K_ESCAPE in history:
        running=False
        history.remove(K_ESCAPE)
        configurations(page=page)

    if running:
        pygame.display.update()

        root.after(17,changing_pic,page,picBox,False)

def display_logos(logoNumber=0):
    if logoNumber==8:
        return #son 80x80
    #horizontal: 92 de margen a los lados y 544 entre las fotos
    #vertical: 55 de margen y 50 entre los logos
    column=logoNumber%4
    row=logoNumber//4
    x=307+92+(80+54)*column
    y=150+100+(80+50)*row

    logo=logos[logoNumber]

    screen.blit(logo,(x,y))
    display_logos(logoNumber+1)

def check_logo_click(mx,my,i=0):
    if i==8:
        return i
    else:
        column=i%4
        row=i//4
        x=307+92+(80+54)*column
        y=150+100+(80+50)*row
        if mx>=x and mx<=(x+80):
            if my>=y and my<=(y+80):
                return i
        return check_logo_click(mx,my,i+1)
    
def changing_logo(page,logoBox,resetting=True):
    '''
    Parameters: page, picBox, resetting=True
    
    Return: None

    Restrictions: page must be int, picBox must be Rect object, resetting must only be specified when called recursively 
    '''
    running=True
    events=pygame.event.get()
    check_keys(events)
    
    if resetting:
        pygame.event.clear()
        pygame.draw.rect(screen,DARKBLUE,(307,150,666,420))
        display_logos()
         
    click=False
    if 1 in check_clicks(events,[]):
        click=True
    
    mx,my=pygame.mouse.get_pos()
    if click:
        logo=check_logo_click(mx,my)
        if logo<8:
            crew[page*4+logoBox][3]=str(logo)
            running=False
            save_file("crew.txt",crew)
            configurations(page=page)
            
    if K_ESCAPE in history:
        running=False
        history.remove(K_ESCAPE)
        configurations(page=page)

    if running:
        pygame.display.update()
  
        root.after(17,changing_logo,page,logoBox,False)

def add_new_pilot(page,newPilot=['','0','0','0','0','0'],stage=0,resetting=True):
    '''
    Parameters: page, newPilot=['','0','0','0','0'], stage=0, resetting=True
    
    Return: None

    Restrictions: page must be int, no other variables must be specified unless being called recursively 
    '''
    running=True
    events=pygame.event.get()
    check_keys(events)
    
    if resetting:
        pygame.event.clear()
        pygame.draw.rect(screen,DARKBLUE,(307,150,666,420))
        if stage==0:
            display_pics()
        if stage==1:
            display_flags()
        if stage==2:
            display_logos()

    click=False
    if 1 in check_clicks(events,[]):
        click=True
            
    mx,my=pygame.mouse.get_pos()
    if click:
        if stage==0:
            pic=check_pic_click(mx,my)
            if pic<15:
                newPilot[1]=str(pic)
                running=False
                add_new_pilot(page,newPilot,stage+1)
        if stage==1:
            flag=check_flag_click(mx,my)
            if flag<50:
                newPilot[2]=str(flag)
                running=False
                add_new_pilot(page,newPilot,stage+1)
        if stage==2:
            logo=check_logo_click(mx,my)
            if logo<8:
                newPilot[3]=str(logo)
                running=False
                crew.append(newPilot[:]) #[:] agrega una copia de la lista en vez de una referencia
                save_file("crew.txt",crew)
                configurations(page=page)

    if K_ESCAPE in history:
        running=False
        history.remove(K_ESCAPE)
        configurations(page=page)
        
    if running:
        pygame.display.update()
   
        root.after(17,add_new_pilot,page,newPilot,stage,False)

def configurations(resetting=True,page=0,nameActive=False,nameBox=-1):
    '''
    Parameters: resetting=True, page=0, nameActive=False,nameBox=-1
    
    Return: None

    Restrictions: unless being called from within the screen iself, resetting must not be provided 
    '''
    running=True
    events=pygame.event.get()
    if nameActive:
        name=crew[page*4+nameBox][0]
        newName=check_keys_typing(events,name)
        crew[page*4+nameBox][0]=newName
    else:
        check_keys(events)
    
    if resetting:
        pygame.event.clear()
        screen.blit(bgIMG, (0, 0))

    click=False
    if 1 in check_clicks(events,[]):
        click=True

    nextButton = pygame.Rect(1174,325,82,70)
    backButton = pygame.Rect(25,325,82,70)

    cardBox0= pygame.Rect(330,27,260,309)
    cardBox1= pygame.Rect(690,27,260,309)
    cardBox2= pygame.Rect(330,385,260,309)
    cardBox3= pygame.Rect(690,385,260,309)
    
    nameBox0= pygame.Rect(330+23,27+169,214,26) #x+23, y+169
    nameBox1= pygame.Rect(690+23,27+169,214,26)
    nameBox2= pygame.Rect(330+23,385+169,214,26)
    nameBox3= pygame.Rect(690+23,385+169,214,26)

    picBox0= pygame.Rect(330+23,27+23,89,99)
    picBox1= pygame.Rect(690+23,27+23,89,99)
    picBox2= pygame.Rect(330+23,385+23,89,99)
    picBox3= pygame.Rect(690+23,385+23,89,99)

    logoBox0= pygame.Rect(330+146,27+34,80,80)
    logoBox1= pygame.Rect(690+146,27+34,80,80)
    logoBox2= pygame.Rect(330+146,385+34,80,80)
    logoBox3= pygame.Rect(690+146,385+34,80,80)

    flagBox0= pygame.Rect(330+28,27+28,24,18)
    flagBox1= pygame.Rect(690+28,27+28,24,18)
    flagBox2= pygame.Rect(330+28,385+28,24,18)
    flagBox3= pygame.Rect(690+28,385+28,24,18)

    XButton0= pygame.Rect(330+265,27,16,16)
    XButton1= pygame.Rect(690+265,27,16,16)
    XButton2= pygame.Rect(330+265,385,16,16)
    XButton3= pygame.Rect(690+265,385,16,16)
    
    
    mx,my=pygame.mouse.get_pos()
    if nextButton.collidepoint((mx,my)) and click:
        if lenn(crew)>=4*(page+1):
            page+=1
    if backButton.collidepoint((mx,my)) and click:
        if page>0:
            page-=1

    if lenn(crew)>12:
        if XButton0.collidepoint((mx,my)) and click:
            if page*4<lenn(crew):
                crew.pop(page*4)
                save_file("crew.txt",crew)
        if XButton1.collidepoint((mx,my)) and click:
            if page*4+1<lenn(crew):
                crew.pop(page*4+1)
                save_file("crew.txt",crew)
        if XButton2.collidepoint((mx,my)) and click:
            if page*4+2<lenn(crew):
                crew.pop(page*4+2)
                save_file("crew.txt",crew)
        if XButton3.collidepoint((mx,my)) and click:
            if page*4+3<lenn(crew):
                crew.pop(page*4+3)
                save_file("crew.txt",crew)

    if cardBox0.collidepoint((mx,my)) and click:
        if page*4<lenn(crew):
            if picBox0.collidepoint((mx,my)):
                if flagBox0.collidepoint((mx,my)):
                    changing_flag(page,0)
                else:
                    changing_pic(page,0)
                running=False
            if logoBox0.collidepoint((mx,my)):
                changing_logo(page,0)
                running=False
            if nameBox0.collidepoint((mx,my)):
                nameBox=0
                nameActive=True
        elif page*4==lenn(crew):
            add_new_pilot(page)
            running=False

    if cardBox1.collidepoint((mx,my)) and click:
        if page*4+1<lenn(crew):
            if picBox1.collidepoint((mx,my)):
                if flagBox1.collidepoint((mx,my)):
                    changing_flag(page,1)
                else:
                    changing_pic(page,1)
                running=False
            if logoBox1.collidepoint((mx,my)):
                changing_logo(page,1)
                running=False
            if nameBox1.collidepoint((mx,my)):
                nameBox=1
                nameActive=True
        elif page*4+1==lenn(crew):
            add_new_pilot(page)
            running=False
            
    if cardBox2.collidepoint((mx,my)) and click:
        if page*4+2<lenn(crew):
            if picBox2.collidepoint((mx,my)):
                if flagBox2.collidepoint((mx,my)):
                    changing_flag(page,2)
                else:
                    changing_pic(page,2)
                running=False
            if logoBox2.collidepoint((mx,my)):
                changing_logo(page,2)
                running=False
            if nameBox2.collidepoint((mx,my)):
                nameBox=2
                nameActive=True
        elif page*4+2==lenn(crew):
            add_new_pilot(page)
            running=False
            
    if cardBox3.collidepoint((mx,my)) and click:
        if page*4+3<lenn(crew):
            if picBox3.collidepoint((mx,my)):
                if flagBox3.collidepoint((mx,my)):
                    changing_flag(page,3)
                else:
                    changing_pic(page,3)
                running=False
            if logoBox3.collidepoint((mx,my)):
                changing_logo(page,3)
                running=False
            if nameBox3.collidepoint((mx,my)):
                nameBox=3
                nameActive=True
        elif page*4+3==lenn(crew):
            add_new_pilot(page)
            running=False

    if (nameActive and ((not nameBox0.collidepoint((mx,my)) and not nameBox1.collidepoint((mx,my)) and not nameBox2.collidepoint((mx,my)) and not nameBox3.collidepoint((mx,my)) ) and click)) or K_RETURN in history or K_ESCAPE in history: 
        nameBox=-1
        nameActive=False
        save_file("crew.txt",crew)

    if K_ESCAPE in history:
        running=False
        main_menu()
    
    if running:            
        pygame.display.update()
      
        erase_area(330,27,260,309)# x:330,690 y:27,385
        erase_area(330,385,260,309)
        erase_area(690,27,260,309)
        erase_area(690,385,260,309)
        erase_area(nextButton)
        erase_area(backButton)
        erase_area(XButton0)
        erase_area(XButton1)
        erase_area(XButton2)
        erase_area(XButton3)
        
        #pygame.draw.rect(screen,(0,0,255),XBox0)
        #pygame.draw.rect(screen,(0,0,255),XBox1)
        #pygame.draw.rect(screen,(0,0,255),XBox2)
        #pygame.draw.rect(screen,(0,0,255),XBox3)
        
        if lenn(crew)>=4*(page+1):
            screen.blit(arrowfIMG,nextButton) 
        if page>0:
            screen.blit(arrowbIMG,backButton)
        display_pilots(page,nameBox)
    
        root.after(17,configurations,False,page,nameActive,nameBox)

def check_keys_typing(eventList,string):
    '''
    Parameters: eventList, string
    
    Return: new string updated to reflect changes

    Restrictions: eventList must be list of pygame events, string must be a string
    '''
    if eventList==[]:
        return string
    if eventList[0].type==KEYDOWN:
        if (eventList[0].key>=97 and eventList[0].key<=122) or eventList[0].key==32:
            if lenn(string)<15:
                if (K_LSHIFT in history) or (K_RSHIFT in history):
                    string+=chr(eventList[0].key).upper()
                else:
                    string+=chr(eventList[0].key)
        if eventList[0].key==K_BACKSPACE:
            string=string[:-1]
            
        if not eventList[0].key in history:
            history.append(eventList[0].key)     
    elif eventList[0].type==KEYUP:
        if eventList[0].key in history:
            history.remove(eventList[0].key)

    return check_keys_typing(eventList[1:],string)

###############################################################------------Game------------################################################################################################################
#depth goes from 0-50
spaceship=['x','y','inclination','inclinationX','lives','shootingCD','fuel'] #[x,y,inclination (float),lives,shooting cooldown,fuel
asteroids=[]#list of lists [centerX,centerY,depth, life]
rings=[]#list of lists [centerX,centerY,depth, life]
shots=[]#list of lists [sx,sy,depth,inclination,timer]
canisters=[]#list of lists [x,y]
timer=0
score=0


#spaceship
def init_spaceship():
    x=533
    y=300
    inclination=0
    inclinationX=0
    cooldown=0
    fuel=100

    if difficulty=="EASY":
        lives=5
        
    elif difficulty=="MEDIUM":
        lives=3
        
    elif difficulty=="HARD":
        lives=2

    spaceship[0]=x
    spaceship[1]=y
    spaceship[2]=inclination
    spaceship[3]=inclinationX
    spaceship[4]=lives
    spaceship[5]=cooldown
    spaceship[6]=fuel
    

def get_hurtbox():
    sx=spaceship[0]
    sy=spaceship[1]
    inclination=round(spaceship[2])
    extraSpace=[(24,10),(31,13),(33,18),(24,28),(20,33),(15,39),(13,42),(8,33)]
    

    extraTop=extraSpace[inclination+3][0]
    extraBottom=extraSpace[inclination+3][1]

    y=sy+extraTop
    x=sx
    height=119-(extraTop+extraBottom)
    width=214

    if inclination<=-2 or inclination>=3:# cut 1 from the sides
        x=sx+1
        width=212

    hurtBox=pygame.Rect(x,y,width,height)

    return hurtBox


def move_spaceship():
    #[x,y,inclination,inclinationX,lives,cooldown,...]

    X=spaceship[3]
    
    verticalSpeed=7
    horizontalSpeed=9
    inclinationSpeed=0.5
    e=2.7182818284
    
    if K_UP in history or K_w in history:
        spaceship[1]-=verticalSpeed
        if X>0:
            spaceship[3]-=inclinationSpeed*2
        else:
            spaceship[3]-=inclinationSpeed
        
    if K_DOWN in history or K_s in history:
        spaceship[1]+=verticalSpeed
        if X<0:
            spaceship[3]+=inclinationSpeed*2
        else:
            spaceship[3]+=inclinationSpeed

    if not K_UP in history and not K_DOWN in history and not K_w in history and not K_s in history:
        if spaceship[3]>0:
            spaceship[3]-=inclinationSpeed
        elif spaceship[3]<0:
            spaceship[3]+=inclinationSpeed

    if X>=0:
        spaceship[2]=4*(1-e**(-0.2*X))
    else:
        spaceship[2]=3*(e**(0.2*X)-1)
        
    if K_RIGHT in history or K_d in history:
        spaceship[0]+=horizontalSpeed
        
    if K_LEFT in history or K_a in history:
        spaceship[0]-=horizontalSpeed

    if spaceship[0]<0:
        spaceship[0]=0
    elif spaceship[0]>screenWidth-214:
        spaceship[0]=screenWidth-214

    if spaceship[1]<18:
        spaceship[1]=18
    elif spaceship[1]>screenHeight-91:
        spaceship[1]=screenHeight-91

    if X>15:
        spaceship[3]=15
    elif X<-15:
        spaceship[3]=-15

    if spaceship[5]>0: #handle shooting cooldown
        spaceship[5]-=1
        
def display_crosshairs():
    sx=spaceship[0]
    sy=spaceship[1]
    inclination=round(spaceship[2])

    x=sx+86
    y=sy+20*(inclination+1)

    screen.blit(crosshairIMG,(x,y))
    return
    
def display_spaceship():
    x=spaceship[0]
    y=spaceship[1]
    inclination=round(spaceship[2])

    spaceshipIMG=get_spaceship_img(inclination)
    screen.blit(spaceshipIMG,(x,y))
    return

def check_life_spaceship():
    if spaceship[4]==0 or spaceship[6]==0: #lives or fuel
        return "DEAD"
    else:
        return "ALIVE"
    
#shooting
def shoot(sx,sy,inclination):
    '''
    Parameters: sx, sy, inclination
    
    Return: None

    Restrictions: sx and sy must be ints, inclination must be int ranging from -3 to 4 
    '''
    if spaceship[5]>0:
        return
    else:
        spaceship[5]=10
        shots.append([sx,sy,1,inclination,0])

def display_shots(shotList):
    #shot=[sx,sy,depth,inclination,timer]
    
    if shotList==[]:
        return
    if shotList[0][2]==5: #if it reaches max depth

        #here we check if it kills asteroids
        erase_area(shotList[0][0]+107-30,shotList[0][1]+20*(shotList[0][3]+1)+20,60,48)
        shotList.pop(0)
        return display_shots(shotList)

    if shotList[0][4]>0:
        shotList[0][4]-=1
        return display_shots(shotList[1:])

    shotList[0][4]=1
    sx=shotList[0][0]
    sy=shotList[0][1]
    depth=shotList[0][2]
    shotList[0][2]+=1
    inclination=shotList[0][3]

    if inclination>0:
        baseHeight=48/(inclination+1)
    elif inclination<0:
        baseHeight=-48/(inclination-1)
    else:
        baseHeight=48

    if depth>1:
        erase_area(sx+107-30,sy+20*(inclination+1)+20,60,48)

    width=round(60/depth)
    height=round(baseHeight/depth)
    
    x=sx+107-width//2
    y=sy+20*(inclination+1)+20
    
    surface=pygame.Surface((60,48)) #creates empty surface
    surface.fill((255,0,255))
    surface.set_colorkey((255,0,255)) #makes bg transparent'
    surface.blit(shotIMG,(0,0)) #puts img in surface

    surface=pygame.transform.scale(surface,(width,height))

    screen.blit(surface,(x,y))

    check_shooting_collisions(shotList[0],asteroids)

    return display_shots(shotList[1:])
    
def check_shooting_collisions(shot,asteroidList):
    '''
    Parameters: shot, asteroidList
    
    Return: None

    Restrictions: shot must be list with shot variables, asteroidList must be asteroids
    '''
    if asteroidList==[]:
        return
    #asteroid= [centerX,centerY,depth, life]
    #shot=[sx,sy,depth,inclination,timer]
    asteroid=asteroidList[0]

    sx=shot[0]
    sy=shot[1]
    depth=shot[2]
    inclination=shot[3]

    if inclination>0:
        baseHeight=48/(inclination+1)
    elif inclination<0:
        baseHeight=-48/(inclination-1)
    else:
        baseHeight=48

    width=round(60/depth)
    height=round(baseHeight/depth)
    
    x=sx+107-round(60/depth)//2
    y=sy+20*(inclination+1)+20

    asteroidWidth=round(400/asteroid[2])
    asteroidHeight=round(304/asteroid[2])
    
    asteroidX=asteroid[0]-asteroidWidth//2
    asteroidY=asteroid[1]-asteroidHeight//2

    if x+width>=asteroidX and x<=asteroidX+asteroidWidth:
        if y+height>=asteroidY and y<=asteroidY+asteroidHeight: #gets hit
            asteroidList[0][3]=0
            erase_area(sx+107-30,sy+20*(inclination+1)+20,60,48)
            shots.remove(shot)
            return

    check_shooting_collisions(shot,asteroidList[1:])
    
#asteroids
def init_asteroid():
    centerX=randint(200,screenWidth-200)
    centerY=randint(192,screenHeight-152)
    depth=20
    life=1

    newAsteroid=[centerX,centerY,depth,life]
    asteroids.append(newAsteroid)

def display_asteroids(asteroidList):
    if asteroidList==[]:
        return
    
    depth=asteroidList[0][2]
    asteroidList[0][2]-=0.1
    if asteroidList[0][2]<1:
        asteroidList[0][3]=0
    else:
        width=round(400/depth)
        height=round(304/depth)
        
        x=asteroidList[0][0]-width//2
        y=asteroidList[0][1]-height//2
        
        surface=pygame.Surface((400,304)) #creates empty surface
        surface.fill((255,0,255))
        surface.set_colorkey((255,0,255)) #makes bg transparent
        surface.blit(asteroidIMG,(0,0)) #puts img in surface

        surface=pygame.transform.scale(surface,(width,height))

        screen.blit(surface,(x,y))

    display_asteroids(asteroidList[1:])

def check_life_asteroids(asteroidList):
    global score
    if asteroidList==[]:
        return

    if asteroidList[0][3]==0:
        x=asteroidList[0][0]-200
        y=asteroidList[0][1]-152
        erase_area(x,y,400,304)
        asteroids.remove(asteroidList[0])
        score+=1000
        check_life_asteroids(asteroidList[1:])
    else:
        check_life_asteroids(asteroidList[1:])

def check_asteroids_collisions(asteroidList,hurtBox):
    '''
    Parameters: asteroidList,hurtBox
    
    Return: None

    Restrictions: asteroidList must be asteroids, hurtBox must be pygame Rect object 
    '''
    global score
    if asteroidList==[]:
        return

    if asteroidList[0][2]>1:
        return check_asteroids_collisions(asteroidList[1:],hurtBox)

    asteroid=asteroidList[0]

    asteroidWidth=round(400/asteroid[2])
    asteroidHeight=round(304/asteroid[2])
    
    asteroidX=asteroid[0]-asteroidWidth//2
    asteroidY=asteroid[1]-asteroidHeight//2

    if hurtBox.right>=asteroidX and hurtBox.left<=asteroidX+asteroidWidth:
        if hurtBox.bottom>=asteroidY and hurtBox.top<=asteroidY+asteroidHeight:
            asteroidList[0][3]=0
            spaceship[4]-=1
            score-=1000
            return

    check_asteroids_collisions(asteroidList[1:],hurtBox)

#rings
def init_ring():
    centerX=randint(225,screenWidth-225)
    centerY=randint(265,screenHeight-225)
    depth=20
    life=1

    newRing=[centerX,centerY,depth,life]
    rings.append(newRing)

def display_rings(ringList):
    #[centerX,centerY,depth, life]
    if ringList==[]:
        return
    
    depth=ringList[0][2]
    if depth>4:
        ringList[0][2]-=0.1
    else:
        ringList[0][2]-=depth*(1/50)+(1/50)
    if ringList[0][2]<1:
        erase_area(ringList[0][0]-225,ringList[0][1]-225,450,450)
        ringList[0][3]=0
    else:
        width=round(450/depth)
        height=round(450/depth)
        
        x=ringList[0][0]-width//2
        y=ringList[0][1]-height//2
        
        surface=pygame.Surface((450,450)) #creates empty surface
        surface.fill((255,0,255))
        surface.set_colorkey((255,0,255)) #makes bg transparent
        surface.blit(ringIMG,(0,0)) #puts img in surface

        surface=pygame.transform.scale(surface,(width,height))
        
        erase_area(x,y,width,height)
        screen.blit(surface,(x,y))

    display_rings(ringList[1:])

def check_life_rings(ringList):
    global score
    if ringList==[]:
        return

    if ringList[0][3]==0:
        rings.remove(ringList[0])
        check_life_rings(ringList[1:])
    else:
        check_life_rings(ringList[1:])

def inside_circle(center,radius,point):
    '''
    Parameters: center, radius, point
    
    Return: boolean, whether point is inside circle or not

    Restrictions: center must be tuple (x,y), radius must be int, point must be tuple (x,y)
    '''
    distanceX= center[0]-point[0]
    distanceY= center[1]-point[1]
    distance=(distanceX**2+distanceY**2)**0.5
    #pygame.draw.line(screen,(0,255,255),(center[0],center[1]),(point[0],point[1]))

    if distance<=radius:
        return True
    else:
        return False

def points_inside_ring(ring,radius,hurtBox):
    '''
    Parameters: ring, radius, hurtBox
    
    Return: amount of points from hurtBox that are inside a ring

    Restrictions: ring must be list with ring variables, radius must be int, hurtBox must be pygame Rect object
    '''
    points=0
    center=(ring[0],ring[1])

    wingAlignment=(29,22,17,5,0,-6,-11,-20)
    inclination=round(spaceship[2])
    
    leftWing=(hurtBox.left,hurtBox.centery+wingAlignment[inclination+3])
    rightWing=(hurtBox.right,hurtBox.centery+wingAlignment[inclination+3])
    
    if inside_circle(center,radius,hurtBox.midtop):
        points+=1
    if inside_circle(center,radius,rightWing):
        points+=1
    if inside_circle(center,radius,leftWing):
        points+=1
    if inside_circle(center,radius,hurtBox.midbottom):
        points+=1

    return points

def check_rings_collisions(ringList,hurtBox):
    '''
    Parameters: ringList, hurtBox
    
    Return: None

    Restrictions: ringList must be rings, hurtBox must be pygame Rect object
    '''
    global score
    if ringList==[]:
        return

    if ringList[0][2]>1:
        return check_rings_collisions(ringList[1:],hurtBox)

    ring=ringList[0]
    radius=225
    innerRadius=206
    pointsInside=points_inside_ring(ring,radius,hurtBox)

    if pointsInside==0: #missed
        pass
    elif pointsInside>0 and pointsInside<4: #partially outside bigger ring
        spaceship[4]-=1
    elif pointsInside==4:
        if points_inside_ring(ring,innerRadius,hurtBox)==4: #goes through
            score+=1000
        else: #inside big ring but touches edge
            spaceship[4]-=1

    check_rings_collisions(ringList[1:],hurtBox)

#fuel
def check_fuel(canistersList,hurtBox):
    '''
    Parameters: canistersList, hurtBox
    
    Return: None

    Restrictions: canistersList must be canisters, hurtBox must be pygame Rect object 
    '''
    if canistersList==[]:
        if spaceship[6]>0 and timer%102==0:
            spaceship[6]-=1
        return

    canisterX=canistersList[0][0]
    canisterY=canistersList[0][1]

    if hurtBox.right>=canisterX and hurtBox.left<=canisterX+44:
        if hurtBox.bottom>=canisterY and hurtBox.top<=canisterY+60:
            spaceship[6]=101
            canisters.remove(canistersList[0])
            erase_area(canisterX,canisterY,44,60)
            
    check_fuel(canistersList[1:],hurtBox)

def init_canister():
    x=randint(0,screenWidth-44)
    y=randint(42,screenHeight-60)

    canisters.append([x,y])

def display_canisters(canistersList):
    if canistersList==[]:
        return

    x=canistersList[0][0]
    y=canistersList[0][1]
    
    screen.blit(fuelCanisterIMG,(x,y))

    display_canisters(canistersList[1:])
    

#info bar
def display_lives(i=0):
    y=12
    if difficulty=="EASY":
        pygame.draw.line(screen,GREY,(857,0),(857,40),2)
        x=868+30*i
        
    elif difficulty=="MEDIUM":
        pygame.draw.line(screen,GREY,(917,0),(917,40),2)
        x=928+30*i
        
    elif difficulty=="HARD":
        pygame.draw.line(screen,GREY,(947,0),(947,40),2)
        x=958+30*i

    if i==spaceship[4]: #spaceship[4]==lives
        return
    
    screen.blit(heartIMG,(x,y))
    display_lives(i+1)

def display_info_bar():
    #[x,y,inclination (float),lives,shooting cooldown,fuel
    pygame.draw.rect(screen,MIDNIGHTBLUE,(0,0,screenWidth,40))
    pygame.draw.line(screen,GREY,(0,40),(screenWidth,40),2)
    #pygame.draw.line(screen,GREY,(496,0),(496,40),2)

    #fuel
    screen.blit(fuelIconIMG,(5,5))
    pygame.draw.line(screen,LIGHTGREY,(40,5),(244,5))
    pygame.draw.line(screen,LIGHTGREY,(40,35),(244,35))
    pygame.draw.line(screen,LIGHTGREY,(40,5),(40,35))
    pygame.draw.line(screen,LIGHTGREY,(244,5),(244,35))
    pygame.draw.rect(screen,WHITE,(42,7,spaceship[6]*2,27))

    #player
    pygame.draw.line(screen,GREY,(1018,0),(1018,40),2)
    draw_text(crew[selectedPilot][0],smallNameFONT,WHITE,screen,1025,5)
    screen.blit(get_pilot_img(int(crew[selectedPilot][1]),0.5),(1245,5))

    #timer
    draw_text("Time:",smallNameFONT,WHITE,screen,300,5)
    if timer<30000:
        draw_text(str(timer/1000),smallNameFONT,WHITE,screen,370,5)
    else:
        draw_text("30.000",smallNameFONT,WHITE,screen,370,5)
    #score
    draw_text("Score:",smallNameFONT,WHITE,screen,570,5)
    draw_text(str(score),smallNameFONT,WHITE,screen,650,5)

    #lives
    display_lives()
    
#levels and end screen:
def asteroids_levels():
    if difficulty=="EASY":
        if timer%6494==0 and timer<6494*5:
            init_asteroid()
        if timer%3009==0 and timer!=0 and timer<28000:
            init_canister()
        
    elif difficulty=="MEDIUM":
        if timer%4335==0 and timer<4335*7:
            init_asteroid()
        if timer%4998==0 and timer!=0 and timer<28000:
            init_canister()
            
    elif difficulty=="HARD":
        if timer%3247==0 and timer<3247*9:
            init_asteroid()
        if timer%6494==0 and timer!=0 and timer<28000:
            init_canister()

def rings_levels():
    if difficulty=="EASY":
        if timer%6494==0 and timer<6494*5:
            init_ring()
        if timer%3009==0 and timer!=0 and timer<28000:
            init_canister()
        
    elif difficulty=="MEDIUM":
        if timer%4335==0 and timer<4335*7:
            init_ring()
        if timer%4998==0 and timer!=0 and timer<28000:
            init_canister()
            
    elif difficulty=="HARD":
        if timer%3247==0 and timer<3247*9:
            init_ring()
        if timer%6494==0 and timer!=0 and timer<28000:
            init_canister() 

def end_screen(condition,gameType,resetting=True): #gameType must be 'asteroids' or 'maneuvers'
    '''
    Parameters: condition, gameType, resetting=True
    
    Return: None

    Restrictions: condition must be "DEAD" or "FINISHED", gameType must be 'asteroids' or 'maneuvers', resetting must only be specified on recursive calls 
    '''
    running=True
    events=pygame.event.get()
    check_keys(events)
    
    if resetting:
        screen.blit(screenIMG,(320,120))
        
        #title
        if condition=="DEAD":
            draw_text("YOU DIED",resultsFONT,WHITE,screen,572,140)
            
        elif condition=="FINISHED":
            draw_text("FINISHED",resultsFONT,WHITE,screen,572,140)

        #score
        draw_text("Final score:",resultsFONT,WHITE,screen,340,250)
        draw_text(str(score),resultsFONT,WHITE,screen,567,250)

        #update score
        if gameType=='asteroids': #[4]
            if score>int(crew[selectedPilot][4]):
                currentTop7=top7_scores(gameType,[])
                position=score_position(currentTop7,score,gameType)+1
                if position==1:
                    draw_text("!!NEW HIGHSCORE!!",resultsFONT,ORANGE,screen,487,380)
                elif position<=7:
                    draw_text("Your score is the new #"+str(position)+"!",resultsFONT,WHITE,screen,411,380)
                    
                crew[selectedPilot][4]=str(score)
                save_file("crew.txt",crew)
            
        elif gameType=='maneuvers': #[5]
            if score>int(crew[selectedPilot][5]):
                currentTop7=top7_scores(gameType,[])
                position=score_position(currentTop7,score,gameType)+1
                if position==1:
                    draw_text("NEW HIGHSCORE",resultsFONT,ORANGE,screen,487,380)
                elif position<=7:
                    draw_text("Your score is the new #"+str(position)+"!",resultsFONT,WHITE,screen,411,380)

                crew[selectedPilot][5]=str(score)
                save_file("crew.txt",crew)
                    
        #exit
        draw_text("Press Esc or click anywhere to exit...",smallNameFONT,WHITE,screen,408,560)

    endBox=pygame.Rect(320,120,640,480)

    click=False
    if 1 in check_clicks(events,[]):
        click=True

    if K_ESCAPE in history or click:
        running=False
        main_menu()

    if running:
        pygame.display.update()
        root.after(17,end_screen,condition,gameType,False)

#game loops #####################################
def game_maneuvers(resetting=True):
    '''
    Parameters: resetting=True
    
    Return: None

    Restrictions: unless being called from within iself, resetting must not be provided 
    '''
    global timer,score, rings, canisters
    timer+=17
    running=True
    events=pygame.event.get()
    check_keys(events)

    if resetting:
        screen.blit(bgIMG, (0, 0))
        init_spaceship()
        timer=0
        score=0

        canisters=[]
        rings=[]


    sx=spaceship[0]
    sy=spaceship[1]
    inclination=round(spaceship[2])

    hurtBox=get_hurtbox()
    
    if K_ESCAPE in history:
        running=False
        main_menu()

    if check_life_spaceship()=="DEAD":
        running=False
        end_screen("DEAD",'maneuvers')

    if timer>30005:
        running=False
        end_screen("FINISHED",'maneuvers')
        
           
    if running:
        root.after(17,game_maneuvers,False)

        rings_levels()
        
        erase_area(hurtBox)

        check_rings_collisions(rings,hurtBox)
        check_life_rings(rings)
        display_rings(rings)
        
        move_spaceship()
        #pygame.draw.rect(screen,(255,0,0),get_hurtbox()) display hurtbox
        display_spaceship()
        
        display_canisters(canisters)
        check_fuel(canisters,hurtBox)
        
        display_info_bar()

        pygame.display.update()

def game_asteroids(resetting=True):
    '''
    Parameters: resetting=True
    
    Return: None

    Restrictions: unless being called from within iself, resetting must not be provided 
    '''
    global timer,score, asteroids, canisters
    timer+=17
    running=True
    events=pygame.event.get()
    check_keys(events)

    if resetting:
        screen.blit(bgIMG, (0, 0))
        init_spaceship()
        timer=0
        score=0

        canisters=[]
        asteroids=[]

    sx=spaceship[0]
    sy=spaceship[1]
    inclination=round(spaceship[2])

    hurtBox=get_hurtbox()
    
    if K_ESCAPE in history:
        running=False
        main_menu()

    if check_life_spaceship()=="DEAD":
        running=False
        end_screen("DEAD",'asteroids')

    if timer>30005:
        running=False
        end_screen("FINISHED",'asteroids')
        
           
    if running:
        root.after(17,game_asteroids,False)

        asteroids_levels()
        
        erase_area(sx+86,sy+20*(inclination+1),42,42) #crosshairs
        erase_area(sx,sy,214,119)

        check_asteroids_collisions(asteroids,hurtBox)
        check_life_asteroids(asteroids)
        display_asteroids(asteroids)

        if K_z in history or K_SPACE in history:
            shoot(sx,sy,inclination)
        
        move_spaceship()
        display_shots(shots)
        display_crosshairs()
        display_spaceship()
        
        display_canisters(canisters)
        check_fuel(canisters,hurtBox)
        
        display_info_bar()

        pygame.display.update()
    

        
##################################################################----MAIN----###########################################################################################################################################

crew=read_file("crew.txt")
if crew==[]:
    initialize_crew()
    save_file("crew.txt",crew)

main_menu()

root.protocol("WM_DELETE_WINDOW", quit_application)
root.mainloop()
