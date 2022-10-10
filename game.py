from pygame import *
from random import *
from math import *
from glob import glob
from tkinter import *
import pickle, sys
init()
font.init()
mixer.init()

# need to know
print('''

CONTROLS
------------------------------------------
A - move left
D - move right
H - use medkit
SPACE - jump
MOUSE1 - shoot
1 - switch to assault rifle
2 - switch to pistol
3 - switch to RPG
ESC - pause game





CAMPAIGN
------------------------------------------
You are a super-solider
for humanity, fighting off machine aliens
that want to conquer the galaxy.

There are 3 stages where you fight off
hoards of enemies. Get to the yellow
square to proceed, while killing as
many aliens as one needs to.

P.S. level 2 may cause some lag



FRENZIE
------------------------------------------
Uh-oh! All ship escape exists have been
blocked by enemies. While you can, kill
as many as you can until your life ends.

Every 2 seconds, a machine-goomba spawns
Every 5 seconds, a helicopter spawns
''')

# LOAD SAVE DATA
pickle_in = open("savedata.pickle","rb")
savedata = pickle.load(pickle_in)
root = Tk()





width = root.winfo_screenwidth()
height = root.winfo_screenheight()-50
screen=display.set_mode((width,height))

root.withdraw()
player=Rect(900,600,30,43)


# basic enemy
basicenemyVX=[]
basicenemyVY=[]
basicenemyGRAV=[]
basicenemyRECT=[]
basicenemyDICT=-1
basicenemyfallcheck=[]
basicenemysaveblock=[]
basicenemystarttofallcheck=[]
basicenemyflutterfix=[]
basicenemyfluttercheck=[]
basicenemycheckflut=[]
basicenemysavex=[]
basicenemyjumpcheck=[]
basicenemysaveright=[]
basicenemyHP=[]
basicenemyjumptrigger=[]
basicenemyshotsRATE=[]
basicenemyshotsWAIT=[]

# flying enemy
flyenemyVX=[]
flyenemyVY=[]
flyenemyRECT=[]
flyenemyHP=[]
flyenemyshotsWAIT=[]
flyenemyshotsRATE=[]



# general variables
a=1
vx=0
vy=0
movex=0
grav=6
jumpcheck=0
fallcheck=1
level=0
starttofallcheck=1
saveblock=Rect(400,620,300,100)
collidefloor=Rect(player.x,player.y,player.right-player.left,player.bottom-player.top+1)
definecheck=1
flutterfix=1
savex=player.x
saveright=player.right
actualfluttercheck=0
checkflut=0
breakcheck=0
spritedirection="R"
hitmarker=0
hitmarkerwait=0
firerate=10
animationcheck=0
animationdelay=200
hp=savedata["maxhp"]
weapons_select=1
explosionstrigger=0
ded=0
dedCOL=255
buywait=0

shop=0
settings=0
deletescreen=0
pause=0
pause_shop=0

gun_animation=0
rpg_firerate=0
goomba_spawn_rate=240
heli_spawn_rate=600

resetsavedata=0

# shot variables
shotsX=[]
shotsY=[]
shotsVX=[]
shotsVY=[]
shotsTYPE=[]
shotsaveX=0
shotsaveY=0

enemyshotsX=[]
enemyshotsY=[]
enemyshotsVX=[]
enemyshotsVY=[]
enemyshotsTYPE=[]

exp_X=[]
exp_Y=[]
exp_SIZE=[]

# TYPES OF SHOTS: 1 - Pistol, 

# sprites
standright=image.load("sprites/standing/standing.PNG")
standleft=transform.flip(standright,1,0)

jumpright=image.load("sprites/jumping/jumpright.PNG")
jumpleft=transform.flip(jumpright,1,0)

goomba=image.load("sprites/enemy/basicenemy/goomba.png")
goomba=transform.scale(goomba,(30,30))

flyenemyBLIT=image.load("sprites/enemy/helicopter.png")

animationright={
    "step1" : image.load("sprites/walking/step1.PNG"),
    "step1H" : image.load("sprites/walking/step1half.PNG"),
    "step2" : image.load("sprites/walking/step2.PNG"),
    "step3" : image.load("sprites/walking/step3.PNG"),
    "step4" : image.load("sprites/walking/step4.PNG"),
    "step5" : image.load("sprites/walking/step5.PNG"),
    "step6" : image.load("sprites/walking/step6.PNG")  
    }
animationleft={
    "step1" : transform.flip(animationright["step1"],1,0),
    "step1H" : transform.flip(animationright["step1H"],1,0),
    "step2" : transform.flip(animationright["step2"],1,0),
    "step3" : transform.flip(animationright["step3"],1,0),
    "step4" : transform.flip(animationright["step4"],1,0),
    "step5" : transform.flip(animationright["step5"],1,0),
    "step6" : transform.flip(animationright["step6"],1,0),
    }
med_kit=image.load("images/medkit.png")
med_kitSHOP=transform.scale(med_kit,(86,86))

# menu
menubackground=image.load("images/menu/facility.jpg")
menubackground=transform.scale(menubackground,(1800,900))
menurects={
    "campaign" : Rect(495,305,500,30),
    "frenzie" : Rect(495,405,500,30),
    "shop" : Rect(495,505,500,30),
    "settings" : Rect(495,605,500,30)
    }
space=image.load("images/space.jpg")
space=transform.scale(space,(1800,900))

# guns
assaultrifle=image.load("images/guns/assault rifle.PNG")
rifleshop=transform.scale(assaultrifle,(150,90))
assaultrifle=transform.scale(assaultrifle,(40,27))
assaultrifleleft=transform.flip(assaultrifle,0,1)

pistolleft=image.load("images/guns/pistol.png")
pistolIMG=transform.flip(pistolleft,1,0)
pistolleft=transform.scale(pistolleft,(27,16))
pistolright=transform.flip(pistolleft,1,0)
pistolleft=transform.flip(pistolleft,1,1)

hitmarker_logo=image.load("images/hitmarker.png")
hitmarker_logo=transform.scale(hitmarker_logo,(40,40))
hitmarker2=image.load("images/hitmarker2.png")
hitmarker2=transform.scale(hitmarker2,(40,40))

rpg_left=image.load("images/guns/rpg_left.png")
rpg_right=image.load("images/guns/rpg_right.png")
rpg_left=transform.flip(rpg_left,0,1)
rpg_left=transform.scale(rpg_left,(56,34))
rpg_right=transform.scale(rpg_right,(56,34))
rpgIMG=transform.scale(rpg_right,(149,91))
rocket=image.load("images/guns/rocket.png")
# fonts & texts
pixelfont=font.Font("fonts/LcdSolid-VPzB.ttf",20)
pixelfont2=font.Font("fonts/LcdSolid-VPzB.ttf",40)
squarefont=font.Font("fonts/square_sans_serif_7.ttf",100)
smallsquarefont=font.Font("fonts/square_sans_serif_7.ttf",40)

# sounds
mixer.music.load("sounds/mw2.mp3")
hitmarkerSOUND=mixer.Sound("sounds/hitmarker.mp3")
killSOUND=mixer.Sound("sounds/kill.mp3")
explosionSOUND=mixer.Sound("sounds/explosion.mp3")
rifleSOUND=mixer.Sound("sounds/rifle.mp3")
pistolSOUND=mixer.Sound("sounds/pistol.mp3")
wastedSOUND=mixer.Sound("sounds/gta.mp3")
mixer.music.play(-1)
mixer.music.set_volume(0.1*savedata["volume"])
hitmarkerSOUND.set_volume(0.1*savedata["volume"])
killSOUND.set_volume(0.1*savedata["volume"])
explosionSOUND.set_volume(0.1*savedata["volume"])
rifleSOUND.set_volume(0.6*savedata["volume"])
pistolSOUND.set_volume(0.3*savedata["volume"])
wastedSOUND.set_volume(0.3*savedata["volume"])


# TEST LEVEL
level_TEST={
    "TESTground" : Rect(0,800,1200,100),
    "TESTthinground" : Rect(1200,800,1200,50),
    "TESTthinplatform" : Rect(1200,750,1200,1),
    "TESTobject" : Rect(400,620,300,100),
    "TESTobject2" : Rect(900,690,100,100),
    "TESTobject3" : Rect(100,720,300,300),
    "TESTwall" : Rect(100,0,100,900),
    "TESTborder" : Rect(1790,0,50,900),
    "TESTroof" : Rect(0,-50,1800,60)
}

# frenzie arena
level_1={'9': Rect(668, 737, 397, 174), '19': Rect(-18, 177, 448, 52), '20': Rect(600, 756, 82, 157), '21': Rect(543, 792, 74, 123), '22': Rect(485, 829, 67, 81), '23': Rect(434, 864, 62, 48), '24': Rect(-15, 874, 464, 40), '25': Rect(-13, -9, 38, 80), '26': Rect(-16, 207, 49, 537), '27': Rect(1054, 763, 109, 149), '28': Rect(1153, 805, 88, 110), '29': Rect(1225, 835, 84, 83), '30': Rect(1302, 871, 59, 47), '31': Rect(1354, 878, 462, 39), '32': Rect(670, -19, 39, 134), '33': Rect(976, -18, 37, 127), '34': Rect(-2, -18, 675, 32), '35': Rect(1007, -13, 806, 34), '37': Rect(1767, 1, 51, 61), '39': Rect(1762, 196, 53, 573), '40': Rect(1254, 176, 561, 47), '41': Rect(707, 538, 310, 31), '42': Rect(707, 565, 34, 88), '43': Rect(981, 559, 36, 99), '44': Rect(592, 448, 34, 40), '45': Rect(460, 357, 34, 28), '46': Rect(565, 232, 37, 30), '47': Rect(1041, 454, 41, 37), '48': Rect(1120, 348, 42, 38), '49': Rect(1035, 214, 44, 31), '50': Rect(119, 588, 234, 23), '51': Rect(1278, 578, 316, 23), '52': Rect(1268, 332, 306, 23), '53': Rect(1673, 447, 30, 26), '54': Rect(123, 323, 231, 19), '55': Rect(46, 439, 40, 37)}
frenzie_goomba_spawnX=[14, 14, 1806, 1809]
frenzie_heli_spawnX=[748, 945]
frenzie_goomba_spawnY=[147, 841, 846, 133]
frenzie_heli_spawnY=[110, 130]
goomba_wait=0
heli_wait=0

# level 1
campaign_1={
    '2': Rect(-15, 870, 1827, 46),
    '5': Rect(-14, 699, 1649, 28),
    '6': Rect(246, 819, 280, 68),
    '7': Rect(669, 789, 241, 107),
    '8': Rect(1067, 721, 32, 81),
    '9': Rect(1172, 803, 38, 73),
    '10': Rect(1738, 806, 55, 12),
    '11': Rect(1632, 750, 62, 10),
    '14': Rect(1053, 556, 116, 14),
    '15': Rect(869, 509, 117, 13),
    '17': Rect(509, 451, 135, 9),
    '18': Rect(342, 422, 140, 10),
    '20': Rect(467, 77, 1348, 1),
    '23': Rect(604, 17, 61, 60),
    '24': Rect(970, 16, 38, 61),
    '25': Rect(780, -17, 53, 26),
    '27': Rect(48, 340, 91, 4),
    '29': Rect(154, 231, 109, 7),
    '30': Rect(286, 154, 84, 12),
    '31': Rect(389, 103, 70, 15),
    '37': Rect(1515, 253, 27, 178),
    '38': Rect(1515, 429, 275, 25),
    '39': Rect(1750, 257, 39, 196),
    '40': Rect(233, 399, 55, 0),
    '41': Rect(219, 399, 55, 3),
    '43': Rect(625, 453, 18, 131),
    '44': Rect(869, 510, 14, 114),
    '45': Rect(869, 622, 366, 14),
    '47': Rect(1541, 350, 217, 1),
    '48': Rect(-18, -9, 16, 918),
    '50': Rect(1806, -15, 13, 907)}

campaign_2={'5': Rect(-18, -11, 28, 928), '6': Rect(-20, 870, 1831, 46), '7': Rect(1779, -16, 38, 931), '8': Rect(-15, -17, 1833, 35), '10': Rect(491, -2, 49, 277), '11': Rect(943, -4, 72, 286), '12': Rect(1355, -14, 64, 290), '13': Rect(471, 554, 74, 333), '17': Rect(-19, 551, 222, 29), '18': Rect(314, 552, 377, 36), '19': Rect(832, 554, 339, 41), '20': Rect(1313, 564, 269, 35), '21': Rect(1200, 239, 461, 50), '23': Rect(306, 241, 369, 46), '24': Rect(-20, 236, 225, 50), '25': Rect(944, 573, 109, 345), '26': Rect(1404, 588, 97, 330), '28': Rect(227, 738, 114, 0), '29': Rect(207, 718, 122, 0), '30': Rect(218, 721, 130, 0), '31': Rect(333, 812, 91, 3), '32': Rect(215, 741, 95, 5), '33': Rect(160, 622, 90, 9), '34': Rect(641, 626, 100, 6), '35': Rect(737, 696, 118, 7), '36': Rect(856, 787, 82, 15), '37': Rect(1127, 802, 100, 8), '38': Rect(1248, 699, 124, 6), '39': Rect(1172, 583, 61, 10), '40': Rect(1524, 825, 103, 10), '41': Rect(1643, 732, 115, 18), '43': Rect(1718, 665, 45, 19), '44': Rect(1594, 561, 47, 15), '45': Rect(1538, 464, 90, 5), '46': Rect(1620, 398, 94, 5), '48': Rect(1747, 292, 13, 0), '49': Rect(1747, 293, 12, 6), '50': Rect(802, 241, 262, 45), '52': Rect(537, 93, 405, 1), '53': Rect(1013, 89, 351, 1), '54': Rect(1409, 91, 380, 1), '55': Rect(-2, 93, 500, 1), '56': Rect(535, 784, 126, 1), '57': Rect(661, 785, 1, 89), '58': Rect(0, 786, 116, 1), '59': Rect(116, 787, 1, 89), '60': Rect(1277, 796, 144, 1), '61': Rect(1277, 797, 1, 89), '62': Rect(1701, 808, 91, 1), '63': Rect(1701, 809, 1, 78), '64': Rect(174, 153, 11, 105), '65': Rect(117, 154, 64, 6), '66': Rect(317, 157, 12, 90), '67': Rect(317, 154, 60, 7), '68': Rect(663, 174, 8, 70), '69': Rect(589, 171, 79, 9), '70': Rect(806, 171, 9, 79), '71': Rect(807, 171, 55, 10), '72': Rect(1642, 167, 12, 77), '73': Rect(1520, 163, 132, 10), '75': Rect(1210, 171, 16, 72), '76': Rect(1211, 169, 69, 8), '78': Rect(699, 447, 98, 1), '79': Rect(712, 350, 56, 0), '80': Rect(721, 349, 40, 0), '81': Rect(712, 351, 54, 3), '82': Rect(719, 260, 34, 0), '84': Rect(683, 258, 36, 0), '85': Rect(682, 255, 38, 6), '87': Rect(190, 446, 108, 1), '88': Rect(161, 351, 78, 1), '89': Rect(258, 247, 54, 0), '90': Rect(268, 244, 45, 7), '91': Rect(1094, 472, 92, 3), '92': Rect(1037, 374, 97, 12), '93': Rect(1138, 267, 69, 27), '94': Rect(485, 490, 54, 74), '95': Rect(492, 251, 17, 12), '97': Rect(494, 275, 47, 86), '98': Rect(957, 276, 51, 96), '99': Rect(969, 476, 38, 126), '100': Rect(1434, 495, 46, 95), '101': Rect(1377, 253, 1, 19), '102': Rect(1429, 275, 39, 75), '103': Rect(71, 5, 4, 92), '104': Rect(218, -3, 6, 104), '105': Rect(341, 4, 6, 98), '106': Rect(629, 6, 7, 92), '107': Rect(721, 8, 13, 89), '108': Rect(830, 9, 11, 88), '109': Rect(1161, 5, 12, 89), '110': Rect(1242, 13, 12, 76), '111': Rect(1087, 6, 7, 89), '112': Rect(1510, -3, 7, 98), '113': Rect(1570, 10, 11, 86), '114': Rect(1645, 11, 19, 80), '118': Rect(5, 381, 21, 8), '120': Rect(118, 352, 66, 200), '122': Rect(104, 471, 19, 8)}

campaign_3={'8': Rect(-17, 837, 674, 76), '9': Rect(995, 835, 818, 79), '10': Rect(-16, 573, 662, 72), '11': Rect(990, 574, 392, 69), '12': Rect(1528, 782, 246, 13), '13': Rect(1402, 627, 240, 16), '14': Rect(152, 197, 482, 90), '15': Rect(960, 221, 856, 76), '17': Rect(147, -12, 227, 101), '21': Rect(-18, -19, 1833, 14), '22': Rect(1805, -18, 12, 933), '23': Rect(-17, -12, 12, 927), '25': Rect(1011, 76, 188, 159), '26': Rect(454, 182, 180, 30), '27': Rect(199, 557, 18, 16), '29': Rect(161, 524, 21, 18), '32': Rect(132, 495, 16, 15), '34': Rect(100, 469, 15, 11), '42': Rect(620, 284, 13, 117), '43': Rect(962, 295, 11, 88), '44': Rect(634, 641, 12, 76), '45': Rect(990, 637, 12, 68), '47': Rect(60, 434, 23, 21), '49': Rect(24, 403, 18, 17), '52': Rect(439, 753, 47, 101), '54': Rect(113, 740, 52, 100), '55': Rect(243, 632, 125, 140), '56': Rect(96, 297, 21, 22)}


enemyX=[53, 99, 303, 388, 610, 1124, 1072, 1465, 1617, 1699, 44, 105, 91, 580, 611, 630, 1314, 1352, 1391, 1734, 1767, 1747, 1590, 1761, 1704, 1631, 1587, 1684, 1403, 1065, 925, 605, 768, 1552, 647, 586, 575, 866, 923, 1264, 1315, 1522, 1570, 1628, 425, 366, 61, 126, 1203, 1314, 912, 810, 418, 272, 265, 1207, 1294, 173, 452, 1093, 901, 787, 684]
enemyY=[71, 74, 78, 82, 81, 77, 72, 79, 78, 74, 834, 858, 828, 817, 841, 843, 839, 841, 842, 851, 840, 840, 812, 640, 697, 547, 438, 376, 552, 542, 542, 534, 431, 60, 219, 229, 195, 221, 232, 214, 219, 197, 223, 217, 208, 202, 210, 206, 781, 669, 776, 670, 803, 720, 411, 59, 64, 68, 521, 360, 65, 61, 58]

lvl3_enemies_X=[699, 893, 727, 917, 743, 932, 742, 888, 1449, 1314, 1492, 175, 1270, 476]
lvl3_enemies_Y=[70, 79, 394, 405, 628, 633, 792, 802, 70, 390, 402, 368, 734, 387]



# FUNCTIONS

def button(x,y,w,h):
    global mx,my,click
    draw.rect(screen,(200,200,200),(x,y,w,h))
    draw.rect(screen,(0,0,0),(x,y,w,h),1)
    if Rect(x,y,w,h).collidepoint(mx,my):
        draw.rect(screen,(255,255,255),(x,y,w,h))
        draw.rect(screen,(0,0,0),(x,y,w,h),3)
        if click:
            return True
        else:
            return False
        
        





    
def basicenemy(level):
    global ded,basicenemyVX,basicenemyVY,basicenemyGRAV,basicenemyRECT,basicenemyDICT,basicenemyfallcheck,basicenemysaveblock,basicenemystarttofallcheck,basicenemyflutterfix,basicenemyfluttercheck,basicenemycheckflut,basicenemysavex,basicenemyjumpcheck,basicenemysaveright,basicenemyHP,basicenemyjumptrigger,basicenemyshotsRATE,basicenemyshotsWAIT,a,vx,vy,movex,grav,jumpcheck,fallcheck,starttofallcheck,saveblock,collidefloor,definecheck,flutterfixsavex,saveright,actualfluttercheck,checkflut,breakcheck,spritedirection,hitmarker,hitmarkerwait,firerate,animationcheck,animationdelay,hp,weapons_select,explosionstrigger,gun_animation,flyenemyVX,flyenemyVY,flyenemyRECT,flyenemyHP,flyenemyshotsWAIT,shotsX,shotsY,shotsVX,shotsVY,shotsTYPE,shotsaveX,shotsaveY,enemyshotsX,enemyshotsY,enemyshotsVX,enemyshotsVY,enemyshotsTYPE,exp_X,exp_Y,exp_SIZE,goomba,hitmarker_logo,hitmarker2

    if True:
        # basicenemy collision & behavior
        for i in range(0,len(basicenemyVX)):
            # enemy movement AI
            if basicenemyRECT[i].x - player.right >200:
                
                basicenemyVX[i]=-3
            elif player.left - basicenemyRECT[i].right >200:
                basicenemyVX[i]=3
            else:
                basicenemyVX[i]=0
            # shooting AI
            basicenemyshotsRATE[i]+=1
            if basicenemyshotsRATE[i]==basicenemyshotsWAIT[i]:
                basicenemyshotsRATE[i]=0
                middleX=basicenemyRECT[i].x+(basicenemyRECT[i].width/2)
                middleY=basicenemyRECT[i].y+(basicenemyRECT[i].height/2)
                dX=(player.x+player.width/2)-middleX
                dY=(player.y+player.height/2)-middleY
                d=dist(middleX,middleY,(player.x+player.width/2),(player.y+player.height/2))
                enemyshotsX.append(middleX)
                enemyshotsY.append(middleY)
                enemyshotsVX.append(dX/d*10)
                enemyshotsVY.append(dY/d*10)
                enemyshotsTYPE.append(1)

            for m in range(0,len(enemyshotsX)):
                enemyshotsX[m]+=enemyshotsVX[m]
                enemyshotsY[m]+=enemyshotsVY[m]
                draw.circle(screen,(255,255,255),(enemyshotsX[m],enemyshotsY[m]),2)
                if player.collidepoint(enemyshotsX[m],enemyshotsY[m]) or player.collidepoint(enemyshotsX[m]-(enemyshotsVX[m]/2),enemyshotsY[m]-(enemyshotsVY[m]/2)):
                    hp-=3
                    enemyshotsX.pop(m)
                    enemyshotsY.pop(m)
                    enemyshotsVX.pop(m)
                    enemyshotsVY.pop(m)
                    enemyshotsTYPE.pop(m)
                    break
                for a in level:
                    if level[a].collidepoint(enemyshotsX[m],enemyshotsY[m]) or level[a].collidepoint(enemyshotsX[m]-(enemyshotsVX[m]/2),enemyshotsY[m]-(enemyshotsVY[m]/2)):
                        enemyshotsX.pop(m)
                        enemyshotsY.pop(m)
                        enemyshotsVX.pop(m)
                        enemyshotsVY.pop(m)
                        enemyshotsTYPE.pop(m)
                        breakcheck=1
                        break
                if breakcheck==1:
                    breakcheck=0
                    break
                


                # enemy jump ai
            if basicenemyjumptrigger[i]==1 and basicenemyjumpcheck[i]==1:
                basicenemyVY[i]=-10
                basicenemyjumpcheck[i]=0
                basicenemyfallcheck[i]=1
                basicenemyflutterfix[i]=1
                basicenemycheckflut[i]=1
                basicenemyjumptrigger[i]=0
            
            basicenemyRECT[i].x+=basicenemyVX[i]
            basicenemyRECT[i].y+=basicenemyVY[i]
            basicenemyRECT[i].y+=basicenemyGRAV[i]
            basicenemyVX[i]=0
            # enemy gravity
            if basicenemyVY[i]<0:
                basicenemyVY[i]+=0.05
                if basicenemyVY[i]>0:
                    basicenemyVY[i]=0
            if basicenemyfallcheck[i]==1:
                basicenemyGRAV[i]=6
            # enemy collison calling + drawing
            for a in level:
                basicenemyRECT[i],basicenemyVX[i],basicenemyVY[i],basicenemyGRAV[i],basicenemyfallcheck[i],basicenemysaveblock[i],basicenemystarttofallcheck[i],basicenemyflutterfix[i],basicenemyfluttercheck[i],basicenemysavex[i],basicenemycheckflut[i],basicenemyjumpcheck[i],basicenemyjumptrigger[i]=collideenemy(level[a],basicenemyRECT[i],basicenemyVX[i],basicenemyVY[i],basicenemyGRAV[i],basicenemyfallcheck[i],basicenemysaveblock[i],basicenemystarttofallcheck[i],basicenemyflutterfix[i],basicenemyfluttercheck[i],basicenemysavex[i],basicenemycheckflut[i],basicenemyjumpcheck[i],basicenemyjumptrigger[i])
            #draw.rect(screen,(0,0,255),basicenemyRECT[i])
            screen.blit(goomba,(basicenemyRECT[i].x,basicenemyRECT[i].y))
                
            # enemy falling off platofrm
            basicenemycollidefloor=Rect(basicenemyRECT[i].x,basicenemyRECT[i].y,basicenemyRECT[i].right-basicenemyRECT[i].left,basicenemyRECT[i].bottom-basicenemyRECT[i].top+1)
            if definecheck==1:
                if basicenemysaveblock[i].colliderect(basicenemycollidefloor):
                    basicenemysavex[i]=basicenemyRECT[i].x
                    basicenemysaveright[i]=basicenemyRECT[i].right
                    basicenemyflutterfix[i]=1
                elif (basicenemysaveright[i] - basicenemyRECT[i].right)>0 or (basicenemyRECT[i].x  - basicenemysavex[i])>0:
                    basicenemyfallcheck[i]=1
                    basicenemyjumpcheck[i]=0
                    if basicenemyVY[i]==0 and basicenemyflutterfix[i]==1 and basicenemyfluttercheck[i]==1:
                        basicenemyVY[i]=-4
                        basicenemyflutterfix[i]=0
            if basicenemycheckflut[i]==1:
                basicenemyfluttercheck[i]=0
                basicenemycheckflut[i]=0
            # enemy projectile collision
            for p in range(0,len(shotsX)):
                if basicenemyRECT[i].collidepoint(shotsX[p],shotsY[p]) or basicenemyRECT[i].collidepoint(shotsX[p]-(shotsVX[p]/2),shotsY[p]-(shotsVY[p]/2)):
                    if True:
                        if shotsTYPE[p]==1:
                            basicenemyHP[i]-=savedata["rifle_damage"]
                        if shotsTYPE[p]==2:
                            basicenemyHP[i]-=savedata["pistol_damage"]
                        if shotsTYPE[p]==3:
                            basicenemyHP[i]-=savedata["rpg_damage"]
                            explode(shotsX[p],shotsY[p],1)
                        shotsX.pop(p)
                        shotsY.pop(p)
                        shotsVX.pop(p)
                        shotsVY.pop(p)
                        shotsTYPE.pop(p)
                        hitmarker=1
                        breakcheck=1
                        break
            if breakcheck==1:
                breakcheck=0
                break

            
        for i in range(0,(len(basicenemyHP))):
            if len(basicenemyHP)>0:
                if basicenemyHP[i]<=0:
                    # enemy death
                    savedata["money"]+=4
                    savedata["score"]+=1
                    hitmarker=2
                    basicenemyVX.pop(i)
                    basicenemyVY.pop(i)
                    basicenemyGRAV.pop(i)
                    basicenemyDICT-=1
                    basicenemyRECT.pop(i)
                    basicenemyfallcheck.pop(i)
                    basicenemysaveblock.pop(i)
                    basicenemystarttofallcheck.pop(i)
                    basicenemyflutterfix.pop(i)
                    basicenemyfluttercheck.pop(i)
                    basicenemysavex.pop(i)
                    basicenemycheckflut.pop(i)
                    basicenemyjumpcheck.pop(i)
                    basicenemysaveright.pop(i)
                    basicenemyHP.pop(i)
                    breakcheck=1
            if breakcheck==1:
                breakcheck=0
                break


def projectile(level):
    global shotsX,shotsY,shotsVX,shotsVY,shotsTYPE,breakcheck,rocket
    
    if True:
        # PROJECTILES
        for i in range(0,len(shotsX)):
            shotsX[i]+=shotsVX[i]
            shotsY[i]+=shotsVY[i]
            for a in level:
                if level[a].collidepoint(shotsX[i],shotsY[i]) or level[a].collidepoint(shotsX[i]-(shotsVX[i]/2),shotsY[i]-(shotsVY[i]/2)):
                    if shotsTYPE[i]==3:
                        explode(shotsX[i],shotsY[i],1)
                    shotsX.pop(i)
                    shotsY.pop(i)
                    shotsVX.pop(i)
                    shotsVY.pop(i)
                    shotsTYPE.pop(i)
                    breakcheck=1
                    break
            if breakcheck==1:
                breakcheck=0
                break
            if shotsTYPE[i]==1:
                draw.circle(screen,(200,200,200),(shotsX[i],shotsY[i]),2)
            if shotsTYPE[i]==2:
                draw.circle(screen,(255,255,255),(shotsX[i],shotsY[i]),3)
            if shotsTYPE[i]==3:
                screen.blit(rocket,(shotsX[i]-16,shotsY[i]-16))

    
    


def flyenemy(level):
    global flyenemyBLIT,flyenemyshotsRATE,ded,flyenemyVX,flyenemyVY,flyenemyRECT,flyenemyHP,flyenemyshotsRATE,flyenemyshotsWAIT,a,vx,vy,movex,grav,jumpcheck,fallcheck,starttofallcheck,saveblock,collidefloor,definecheck,flutterfixsavex,saveright,actualfluttercheck,checkflut,breakcheck,spritedirection,hitmarker,hitmarkerwait,firerate,animationcheck,animationdelay,hp,weapons_select,explosionstrigger,gun_animation,flyenemyVX,flyenemyVY,flyenemyRECT,flyenemyHP,flyenemyshotsWAIT,shotsX,shotsY,shotsVX,shotsVY,shotsTYPE,shotsaveX,shotsaveY,enemyshotsX,enemyshotsY,enemyshotsVX,enemyshotsVY,enemyshotsTYPE,exp_X,exp_Y,exp_SIZE,goomba,hitmarker_logo,hitmarker2

    for i in range(0,len(flyenemyRECT)):
        # movement AI
        if player.x - flyenemyRECT[i].right>0:
            flyenemyVX[i]=2
        elif flyenemyRECT[i].left - player.right > 0:
            flyenemyVX[i]=-2

        

        flyenemyRECT[i].x+=flyenemyVX[i]
        flyenemyRECT[i].y+=flyenemyVY[i]

        for a in level:
            flyenemyRECT[i]=flyingenemycollide(level[a],flyenemyRECT[i])

        if True:
            # shooting AI
            flyenemyshotsRATE[i]+=1
            if flyenemyshotsRATE[i]==flyenemyshotsWAIT[i]:
                flyenemyshotsRATE[i]=0
                middleX=flyenemyRECT[i].x+(flyenemyRECT[i].width/2)
                middleY=flyenemyRECT[i].y+(flyenemyRECT[i].height/2)
                dX=(player.x+player.width/2)-middleX
                dY=(player.y+player.height/2)-middleY
                d=dist(middleX,middleY,(player.x+player.width/2),(player.y+player.height/2))
                enemyshotsX.append(middleX)
                enemyshotsY.append(middleY)
                enemyshotsVX.append(dX/d*10)
                enemyshotsVY.append(dY/d*10)
                enemyshotsTYPE.append(1)

            for m in range(0,len(enemyshotsX)):
                enemyshotsX[m]+=enemyshotsVX[m]
                enemyshotsY[m]+=enemyshotsVY[m]
                draw.circle(screen,(255,255,255),(enemyshotsX[m],enemyshotsY[m]),2)
                if player.collidepoint(enemyshotsX[m],enemyshotsY[m]) or player.collidepoint(enemyshotsX[m]-(enemyshotsVX[m]/2),enemyshotsY[m]-(enemyshotsVY[m]/2)):
                    hp-=8
                    enemyshotsX.pop(m)
                    enemyshotsY.pop(m)
                    enemyshotsVX.pop(m)
                    enemyshotsVY.pop(m)
                    enemyshotsTYPE.pop(m)
                    break
                for a in level:
                    if level[a].collidepoint(enemyshotsX[m],enemyshotsY[m]) or level[a].collidepoint(enemyshotsX[m]-(enemyshotsVX[m]/2),enemyshotsY[m]-(enemyshotsVY[m]/2)):
                        enemyshotsX.pop(m)
                        enemyshotsY.pop(m)
                        enemyshotsVX.pop(m)
                        enemyshotsVY.pop(m)
                        enemyshotsTYPE.pop(m)
                        breakcheck=1
                        break
                if breakcheck==1:
                    breakcheck=0
                    break
                
       

            # enemy projectile collision
            for p in range(0,len(shotsX)):
                if flyenemyRECT[i].collidepoint(shotsX[p],shotsY[p]) or flyenemyRECT[i].collidepoint(shotsX[p]-(shotsVX[p]/2),shotsY[p]-(shotsVY[p]/2)):
                    if True:
                        if shotsTYPE[p]==1:
                            flyenemyHP[i]-=savedata["rifle_damage"]
                        if shotsTYPE[p]==2:
                            flyenemyHP[i]-=savedata["pistol_damage"]
                        if shotsTYPE[p]==3:
                            flyenemyHP[i]-=savedata["rpg_damage"]
                            explode(shotsX[p],shotsY[p],1)
                        shotsX.pop(p)
                        shotsY.pop(p)
                        shotsVX.pop(p)
                        shotsVY.pop(p)
                        shotsTYPE.pop(p)
                        hitmarker=1
                        breakcheck=1
                        break
            if breakcheck==1:
                breakcheck=0
                break

            
    for i in range(0,(len(flyenemyHP))):
        if len(flyenemyHP)>0:
            if flyenemyHP[i]<=0:
                # enemy death
                savedata["money"]+=15
                savedata["score"]+=3
                hitmarker=2
                flyenemyVX.pop(i)
                flyenemyVY.pop(i)
                flyenemyRECT.pop(i)
                flyenemyHP.pop(i)
                breakcheck=1
                break
        if breakcheck==1:
            breakcheck=0
            break



    # draw heli
    for b in flyenemyRECT:
        screen.blit(flyenemyBLIT,(b.x,b.y))
    

    
def collide(block):
    # NOTE: collision code taken from: https://www.youtube.com/watch?v=1_H7InPMjaY&t=9s
    global grav,jumpcheck,movex,vy,fallcheck,savex,savey,starttofallcheck,player,saveblock,flutterfix,savewallblock,actualfluttercheck

    if player.colliderect(block):
        # floor collisions
        if (block.top - player.bottom)>=-10 and (block.top - player.bottom)<0 and (vy+grav)>=0:
            grav=0
            fallcheck=0
            jumpcheck=1
            vy=0
            player.bottom=block.top
            saveblock=block
            definecheck=1
            flutterfix=1
            actualfluttercheck=1
        # ceiling collisions
        if (block.bottom - player.top)<10 and (block.bottom - player.top)>0:
            if (vy+grav)<0:
                player.top=block.bottom
                vy=-5.75
        # left wall collisions
        if (block.right - player.left)<=4 and (block.right - player.left)>0:
            player.x=block.right
        # right wall collisions
        if (player.right - block.left)<=4 and (player.right - block.left)>0:
            player.x=block.left + (player.x - player.right)

def collideenemy(block,enemyRECT,enemyVX,enemyVY,enemyGRAV,enemyfallcheck,enemysaveblock,enemystarttofallcheck,enemyflutterfix,enemyfluttercheck,enemysavex,enemycheckflut,enemyjumpcheck,enemyjumptrigger):
    if enemyRECT.colliderect(block):
        # floor collisions
        if (block.top - enemyRECT.bottom)>=-10 and (block.top - enemyRECT.bottom)<0 and (enemyVY+enemyGRAV)>=0:
            enemyGRAV=0
            enemyfallcheck=0
            enemyjumpcheck=1
            enemyVY=0
            enemyRECT.bottom=block.top
            enemycollideL=1
            enemycollideR=1
            enemysaveblock=block
            definecheck=1
            enemyflutterfix=1
            enemyfluttercheck=1
            enemyjumptrigger=0
        # ceiling collisions
        if (block.bottom - enemyRECT.top)<10 and (block.bottom - enemyRECT.top)>0:
            if (enemyVY+enemyGRAV)<0:
                enemyRECT.top=block.bottom
                enemyVY=-5.75
        # left wall collisions
        if (block.right - enemyRECT.left)<=4 and (block.right - enemyRECT.left)>0:
            enemycollideL=0
            enemyRECT.x=block.right
            enemysavewallblock=block
            enemyjumptrigger=1
        # right wall collisions
        if (enemyRECT.right - block.left)<=4 and (enemyRECT.right - block.left)>0:
            enemycollideR=0
            enemyRECT.x=block.left + (enemyRECT.x - enemyRECT.right)
            enemysavewallblock=block
            enemyjumptrigger=1

            
    return enemyRECT,enemyVX,enemyVY,enemyGRAV,enemyfallcheck,enemysaveblock,enemystarttofallcheck,enemyflutterfix,enemyfluttercheck,enemysavex,enemycheckflut,enemyjumpcheck,enemyjumptrigger
    


def flyingenemycollide(block,enemyRECT):
    # floor collisions
    if block.colliderect(enemyRECT):
        if (block.top - enemyRECT.bottom)>=-10 and (block.top - enemyRECT.bottom)<0:
            enemyRECT.bottom=block.top
        # ceiling collisions
        if (block.bottom - enemyRECT.top)<10 and (block.bottom - enemyRECT.top)>0:
            enemyRECT.top=block.bottom

        # left wall collisions
        if (block.right - enemyRECT.left)<=4 and (block.right - enemyRECT.left)>0:
            enemyRECT.x=block.right
        # right wall collisions
        if (enemyRECT.right - block.left)<=4 and (enemyRECT.right - block.left)>0:
            enemyRECT.x=block.left + (enemyRECT.x - enemyRECT.right)
            
    return enemyRECT
    




def falloff():
    global collidefloor,definecheck,savex,player,saveblock,saveright,flutterfix,fallcheck,jumpcheck,vy,actualfluttercheck,checkflut
    # falling off a platform
    collidefloor=Rect(player.x,player.y,player.right-player.left,player.bottom-player.top+1)
    if definecheck==1:
        if saveblock.colliderect(collidefloor):
            savex=player.x
            saveright=player.right
            flutterfix=1
        elif (saveright - player.right)>0 or (player.x-savex)>0:
            fallcheck=1
            jumpcheck=0
            if vy==0 and flutterfix==1 and actualfluttercheck==1:
                vy=-4
                flutterfix=0
    if checkflut==1:
        actualfluttercheck=0
        checkflut=0
        


def explode(ex,ey,typee):
    global basicenemyRECT,basicenemyHP,exp_X,exp_Y,exp_SIZE,explosionSOUND,flyenemyRECT,flyenemyHP
    mixer.Sound.play(explosionSOUND)
    # has explosion place and calcs radius from it to every enemy
    for i in range(0,len(basicenemyHP)):  
        t=dist(ex,ey,basicenemyRECT[i].x,basicenemyRECT[i].y)
        if t<=100:
            if len(basicenemyRECT)>0:
                basicenemyHP[i]-=100
    for i in range(0,len(flyenemyHP)):  
        t=dist(ex,ey,flyenemyRECT[i].x,flyenemyRECT[i].y)
        if t<=100:
            if len(flyenemyRECT)>0:
                flyenemyHP[i]-=100

                
    exp_X.append(ex)
    exp_Y.append(ey)
    if typee==1:
        exp_SIZE.append(100)









def dist(x1,y1,x2,y2):
    answer=((x2-x1)**2 + (y2-y1)**2)**0.5
    return answer

        
running=True
while running:
    click=False
    for evnt in event.get():
        if evnt.type== QUIT:
            running=False
            # save game
            pickle_out=open("savedata.pickle","wb")
            pickle.dump(savedata,pickle_out)
            pickle_out.close()
        if evnt.type==MOUSEBUTTONDOWN:
            if evnt.button==1:
                click=True
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    keys=key.get_pressed()
    myClock=time.Clock()
#-----------------------


    # main menu
    if level==0 and shop==0 and settings==0 and deletescreen==0  and pause==0:
        screen.blit(menubackground,(0,0))
        draw.rect(screen,(255,255,255),(490,95,820,105))
        draw.rect(screen,(0,0,0),(490,95,820,105),5)
        screen.blit(squarefont.render("JUGGERNAUT",True,(0,0,0)),(505,100))
        draw.rect(screen,(255,255,255),menurects["frenzie"])
        draw.rect(screen,(255,255,255),menurects["shop"])
        draw.rect(screen,(255,255,255),menurects["campaign"])
        draw.rect(screen,(255,255,255),menurects["settings"])
        # ----
        screen.blit(smallsquarefont.render("Campaign",True,(0,0,0)),(505,300))
        screen.blit(smallsquarefont.render("Frenzie",True,(0,0,0)),(505,400))
        screen.blit(smallsquarefont.render("Shop",True,(0,0,0)),(505,500))
        screen.blit(smallsquarefont.render("settings",True,(0,0,0)),(505,600))
        # buttons
        if menurects["frenzie"].collidepoint(mx,my):
            if click:
                level=-1
                mixer.music.load("sounds/doom.mp3")
                mixer.music.set_volume(0.05*savedata["volume"])
                mixer.music.play(-1)
        if menurects["shop"].collidepoint(mx,my):
            if click:
                shop=1
                buywait=10
        if menurects["settings"].collidepoint(mx,my):
            if click:
                settings=1
                buywait=10
                shop=0

        if menurects["campaign"].collidepoint(mx,my):
            if click:
                hp=savedata["maxhp"]
                level=savedata["level"]
                mixer.music.load("sounds/doom.mp3")
                mixer.music.set_volume(0.05*savedata["volume"])
                mixer.music.play(-1)
                # loads level and creates enemies
                if level==1:
                   player=Rect(20,700,30,43)
                   for i in range(0,50):
                        basicenemyVX.append(0)
                        basicenemyVY.append(0)
                        basicenemyGRAV.append(6)
                        basicenemyDICT+=1
                        basicenemyRECT.append(Rect(randint(100,1700),randint(100,1700),30,30))
                        basicenemyfallcheck.append(1)
                        basicenemysaveblock.append(Rect(400,620,300,100))
                        basicenemystarttofallcheck.append(1)
                        basicenemyflutterfix.append(1)
                        basicenemyfluttercheck.append(0)
                        basicenemysavex.append(basicenemyRECT[basicenemyDICT].x)
                        basicenemycheckflut.append(0)
                        basicenemyjumpcheck.append(0)
                        basicenemysaveright.append(basicenemyRECT[basicenemyDICT].right)
                        basicenemyHP.append(100)
                        basicenemyjumptrigger.append(0)
                        basicenemyshotsRATE.append(0)
                        basicenemyshotsWAIT.append(randint(360,480))
                   for i in range(0,50):
                        basicenemyVX.append(0)
                        basicenemyVY.append(0)
                        basicenemyGRAV.append(6)
                        basicenemyDICT+=1
                        basicenemyRECT.append(Rect(randint(100,1700),0,30,30))
                        basicenemyfallcheck.append(1)
                        basicenemysaveblock.append(Rect(400,620,300,100))
                        basicenemystarttofallcheck.append(1)
                        basicenemyflutterfix.append(1)
                        basicenemyfluttercheck.append(0)
                        basicenemysavex.append(basicenemyRECT[basicenemyDICT].x)
                        basicenemycheckflut.append(0)
                        basicenemyjumpcheck.append(0)
                        basicenemysaveright.append(basicenemyRECT[basicenemyDICT].right)
                        basicenemyHP.append(100)
                        basicenemyjumptrigger.append(0)
                        basicenemyshotsRATE.append(0)
                        basicenemyshotsWAIT.append(randint(360,480))
                if level==2:
                    player=Rect(20,500,30,43)
                    for i in range(0,len(enemyX)):
                        basicenemyVX.append(0)
                        basicenemyVY.append(0)
                        basicenemyGRAV.append(6)
                        basicenemyDICT+=1
                        basicenemyRECT.append(Rect(enemyX[i],enemyY[i],30,30))
                        basicenemyfallcheck.append(1)
                        basicenemysaveblock.append(Rect(400,620,300,100))
                        basicenemystarttofallcheck.append(1)
                        basicenemyflutterfix.append(1)
                        basicenemyfluttercheck.append(0)
                        basicenemysavex.append(basicenemyRECT[basicenemyDICT].x)
                        basicenemycheckflut.append(0)
                        basicenemyjumpcheck.append(0)
                        basicenemysaveright.append(basicenemyRECT[basicenemyDICT].right)
                        basicenemyHP.append(100)
                        basicenemyjumptrigger.append(0)
                        basicenemyshotsRATE.append(0)
                        basicenemyshotsWAIT.append(randint(360,480))
                if level==3:
                    player=Rect(30,750,30,43)
                    for a in range(0,2):
                        for i in range(0,len(lvl3_enemies_X)):
                            flyenemyVX.append(0)
                            flyenemyVY.append(0)
                            flyenemyRECT.append(Rect(randint(lvl3_enemies_X[i]-10,lvl3_enemies_X[i]+10),randint(lvl3_enemies_Y[i]-10,lvl3_enemies_Y[i]+10),50,50))
                            flyenemyHP.append(200)
                            flyenemyshotsWAIT.append(randint(200,300))
                            flyenemyshotsRATE.append(0)
                # end screen
                if level==-4:
                    mixer.music.stop()
                    mixer.music.load("sounds/the_end.mp3")
                    mixer.music.play(-1)
                        

                
    buywait-=1

    #settings
    if settings==1 and level==0 and buywait<=0 and pause==0:
        #
        
        mixer.music.set_volume(0.1*savedata["volume"])
        hitmarkerSOUND.set_volume(0.1*savedata["volume"])
        killSOUND.set_volume(0.1*savedata["volume"])
        explosionSOUND.set_volume(0.1*savedata["volume"])
        rifleSOUND.set_volume(0.6*savedata["volume"])
        pistolSOUND.set_volume(0.3*savedata["volume"])
        wastedSOUND.set_volume(0.3*savedata["volume"])
        
        draw.rect(screen,(255,255,255),(250,75,1300,750))
        draw.rect(screen,(0,0,0),(250,75,1300,750),5)
        draw.line(screen,(0,0,0),(275,190),(1525,190),3)
        screen.blit(squarefont.render("settings",True,(0,0,0)),(275,100))
        screen.blit(smallsquarefont.render("volume",True,(0,0,0)),(275,250))
        volumerect=Rect(400,350,1000,20)
        draw.rect(screen,(255,0,0),volumerect)
        draw.rect(screen,(0,255,0),(400,350,500*savedata["volume"],20))
        
        back=button(1400,100,100,50)
        screen.blit(pixelfont.render("Back",True,(0,0,0)),(1410,110))
        if back:
            settings=0
            buywait=0
            
        if Rect(320,340,1120,40).collidepoint(mx,my):
            if mb[0]:
                savedata["volume"]=(mx-400)/500
                if mx>1400:
                    savedata["volume"]=2
                if mx<400:
#@@
                    savedata["volume"]=0
        draw.rect(screen,(0,0,0),(400+500*savedata["volume"]-10,340,20,40))
        screen.blit(pixelfont.render(str(round(savedata["volume"]*100,1))+"%",True,(0,0,0)),(300,350))

        # SAVE DATA RESET
        screen.blit(smallsquarefont.render("save data",True,(0,0,0)),(275,450))
        draw.rect(screen,(255,0,0),(275,510,300,50))
        draw.rect(screen,(0,0,0),(275,510,300,50),1)
        if Rect(275,510,300,50).collidepoint(mx,my):
            draw.rect(screen,(255,255,255),(275,510,300,50))
            draw.rect(screen,(0,0,0),(275,510,300,50),3)
            if click:
                settings=0
                deletescreen=1

                
        screen.blit(pixelfont.render("RESET SAVE DATA",True,(0,0,0)),(280,520))

    # delete save data
    if deletescreen==1:  
        draw.rect(screen,(0,0,0),(250,75,1300,750))
        mixer.music.pause()
        screen.blit(pixelfont.render("ARE YOU SURE?",True,(255,0,0)),(800,300))
        screen.blit(pixelfont.render("YES",True,(255,0,0)),(800,330))
        screen.blit(pixelfont.render("NO",True,(255,0,0)),(930,330))
        if Rect(930,330,30,20).collidepoint(mx,my):
            if click and resetsavedata==0:
                deletescreen=0
                settings=1
                buywait=10
                mixer.music.unpause()
        if Rect(800,330,40,20).collidepoint(mx,my):
            if click:
                resetsavedata=1
                running=False


            


    # shop          
    if shop==1 and level==0 and buywait<=0 and pause==0:
        draw.rect(screen,(255,255,255),(250,75,1300,750))
        draw.rect(screen,(0,0,0),(250,75,1300,750),5)
        draw.line(screen,(0,0,0),(275,190),(1525,190),3)
        screen.blit(squarefont.render("shop",True,(0,0,0)),(275,100))
        screen.blit(pixelfont2.render("Cash: $"+str(savedata["money"]),True,(0,0,0)),(700,150))
        screen.blit(pixelfont2.render("Ammo",True,(0,0,0)),(525,220))
        screen.blit(pixelfont2.render("Upgrades",True,(0,0,0)),(800,220))
        #screen.blit(pixelfont2.render("Other",True,(0,0,0)),(1320,220))
        back=button(1400,100,100,50)
        screen.blit(pixelfont.render("Back",True,(0,0,0)),(1410,110))
        if back:
            shop=0
            buywait=0

        # AR ammo
        screen.blit(pixelfont.render("Assault Rifle",True,(0,0,0)),(275,290))
        screen.blit(rifleshop,(275,310))
        draw.rect(screen,(200,200,200),(475,300,250,80))
        draw.rect(screen,(0,0,0),(475,300,250,80),1)
        screen.blit(pixelfont.render("Buy 10 ---- $5",True,(0,0,0)),(500,310))
        screen.blit(pixelfont.render("Rounds: "+str(savedata["rifle_ammo"]),True,(0,0,0)),(500,340))
        if Rect(475,300,250,80).collidepoint(mx,my):
            draw.rect(screen,(255,255,255),(475,300,250,80))
            draw.rect(screen,(0,0,0),(475,300,250,80),3)
            screen.blit(pixelfont.render("Buy 10 ---- $5",True,(0,0,0)),(500,310))
            screen.blit(pixelfont.render("Rounds: "+str(savedata["rifle_ammo"]),True,(0,0,0)),(500,340))
            if click and savedata["money"]>=5 and (savedata["rifle_ammo"]+10)<9999:
                savedata["rifle_ammo"]+=10
                savedata["money"]-=5

        # Pistol ammo
        screen.blit(pixelfont.render("Pistol",True,(0,0,0)),(275,400))
        screen.blit(pistolIMG,(275,420))
        draw.rect(screen,(200,200,200),(475,420,250,80))
        draw.rect(screen,(0,0,0),(475,420,250,80),1)
        screen.blit(pixelfont.render("Buy 5 ---- $5",True,(0,0,0)),(500,430))
        screen.blit(pixelfont.render("Rounds: "+str(savedata["pistol_ammo"]),True,(0,0,0)),(500,460))
        if Rect(475,420,250,80).collidepoint(mx,my):
            draw.rect(screen,(255,255,255),(475,420,250,80))
            draw.rect(screen,(0,0,0),(475,420,250,80),3)
            screen.blit(pixelfont.render("Buy 5 ---- $5",True,(0,0,0)),(500,430))
            screen.blit(pixelfont.render("Rounds: "+str(savedata["pistol_ammo"]),True,(0,0,0)),(500,460))
            if click and savedata["money"]>=5 and (savedata["pistol_ammo"]+5)<9999:
                savedata["pistol_ammo"]+=5
                savedata["money"]-=5
        # RPG ammo
        screen.blit(pixelfont.render("RPG",True,(0,0,0)),(275,500))
        screen.blit(rpgIMG,(275,520))
        draw.rect(screen,(200,200,200),(475,520,250,80))
        draw.rect(screen,(0,0,0),(475,520,250,80),1)
        screen.blit(pixelfont.render("Buy 1 ---- $5",True,(0,0,0)),(500,530))
        screen.blit(pixelfont.render("Rounds: "+str(savedata["rpg_ammo"]),True,(0,0,0)),(500,560))
        if Rect(475,520,250,80).collidepoint(mx,my):
            draw.rect(screen,(255,255,255),(475,520,250,80))
            draw.rect(screen,(0,0,0),(475,520,250,80),3)
            screen.blit(pixelfont.render("Buy 1 ---- $5",True,(0,0,0)),(500,530))
            screen.blit(pixelfont.render("Rounds: "+str(savedata["rpg_ammo"]),True,(0,0,0)),(500,560))
            if click and savedata["money"]>=5 and (savedata["rpg_ammo"]+1)<9999:
                savedata["rpg_ammo"]+=1
                savedata["money"]-=5
        # medkit
        screen.blit(pixelfont.render("Health",True,(0,0,0)),(275,710))
        screen.blit(med_kitSHOP,(275,620))
        draw.rect(screen,(200,200,200),(475,620,250,80))
        draw.rect(screen,(0,0,0),(475,620,250,80),1)
        screen.blit(pixelfont.render("Buy 1 ---- $10",True,(0,0,0)),(500,630))
        screen.blit(pixelfont.render("Packs: "+str(savedata["medkit"]),True,(0,0,0)),(500,660))
        if Rect(475,620,250,80).collidepoint(mx,my):
            draw.rect(screen,(255,255,255),(475,620,250,80))
            draw.rect(screen,(0,0,0),(475,620,250,80),3)
            screen.blit(pixelfont.render("Buy 1 ---- $10",True,(0,0,0)),(500,630))
            screen.blit(pixelfont.render("Packs: "+str(savedata["medkit"]),True,(0,0,0)),(500,660))
            if click and savedata["money"]>=10 and (savedata["medkit"]+1)<9999:
                savedata["medkit"]+=1
                savedata["money"]-=10
        # UPGRADES
        # rifle
        upgrade=button(800,300,250,80)
        screen.blit(pixelfont.render("AR +5DMG --- $100",True,(0,0,0)),(810,310))
        screen.blit(pixelfont.render("Damage: "+str(savedata["rifle_damage"]),True,(0,0,0)),(810,340))
        if upgrade and savedata["money"]>=100:
            savedata["rifle_damage"]+=5
            savedata["money"]-=100

        # pistol
        upgrade=button(800,420,250,80)
        screen.blit(pixelfont.render("Pistol +5DMG-$100",True,(0,0,0)),(810,430))
        screen.blit(pixelfont.render("Damage: "+str(savedata["pistol_damage"]),True,(0,0,0)),(810,460))
        if upgrade and savedata["money"]>=100:
            savedata["pistol_damage"]+=5
            savedata["money"]-=100
        # rpg
        upgrade=button(800,520,250,80)
        screen.blit(pixelfont.render("RPG +5DMG -- $100",True,(0,0,0)),(810,530))
        screen.blit(pixelfont.render("Damage: "+str(savedata["rpg_damage"]),True,(0,0,0)),(810,560))
        if upgrade and savedata["money"]>=100:
            savedata["rpg_damage"]+=5
            savedata["money"]-=100
        # rpg
        upgrade=button(800,520,250,80)
        screen.blit(pixelfont.render("RPG +5DMG -- $100",True,(0,0,0)),(810,530))
        screen.blit(pixelfont.render("Damage: "+str(savedata["rpg_damage"]),True,(0,0,0)),(810,560))
        if upgrade and savedata["money"]>=100:
            savedata["rpg_damage"]+=5
            savedata["money"]-=100
        # maxhp
        upgrade=button(800,620,250,80)
        screen.blit(pixelfont.render("MAXHP +5HP - $100",True,(0,0,0)),(810,630))
        screen.blit(pixelfont.render("MAXHP: "+str(savedata["maxhp"]),True,(0,0,0)),(810,660))
        if upgrade and savedata["money"]>=100:
            savedata["maxhp"]+=10
            savedata["money"]-=100


    # pause menu        
    if pause==1 and level==0 and buywait<=0 and settings==0:
        if pause_shop==0:
            screen.fill((255,255,255))
            screen.blit(squarefont.render("pause menu",True,(0,0,0)),(50,0))
            back=button(700,500,400,50)
            screen.blit(pixelfont.render("Resume Game",True,(0,0,0)),(830,515))
            if back:
                level=savelevel
            Pshop=button(700,300,400,50)
            screen.blit(pixelfont.render("Shop",True,(0,0,0)),(865,315))
            if Pshop:
                pause_shop=1
        else:
            # AR ammo
            screen.fill((255,255,255))
            back=button(700,100,400,50)
            screen.blit(pixelfont.render("Back to Pause Menu",True,(0,0,0)),(790,115))
            if back:
                pause_shop=0
            screen.blit(pixelfont.render("Money: $"+str(savedata["money"]),True,(0,0,0)),(30,10))
            screen.blit(pixelfont.render("Assault Rifle",True,(0,0,0)),(275,290))
            screen.blit(rifleshop,(275,310))
            draw.rect(screen,(200,200,200),(475,300,250,80))
            draw.rect(screen,(0,0,0),(475,300,250,80),1)
            screen.blit(pixelfont.render("Buy 10 --- $5",True,(0,0,0)),(500,310))
            screen.blit(pixelfont.render("Rounds: "+str(savedata["rifle_ammo"]),True,(0,0,0)),(500,340))
            if Rect(475,300,250,80).collidepoint(mx,my):
                draw.rect(screen,(255,255,255),(475,300,250,80))
                draw.rect(screen,(0,0,0),(475,300,250,80),3)
                screen.blit(pixelfont.render("Buy 10 ---- $5",True,(0,0,0)),(500,310))
                screen.blit(pixelfont.render("Rounds: "+str(savedata["rifle_ammo"]),True,(0,0,0)),(500,340))
                if click and savedata["money"]>=5 and (savedata["rifle_ammo"]+10)<9999:
                    savedata["rifle_ammo"]+=10
                    savedata["money"]-=5

            # Pistol ammo
            screen.blit(pixelfont.render("Pistol",True,(0,0,0)),(275,400))
            screen.blit(pistolIMG,(275,420))
            draw.rect(screen,(200,200,200),(475,420,250,80))
            draw.rect(screen,(0,0,0),(475,420,250,80),1)
            screen.blit(pixelfont.render("Buy 5 ---- $5",True,(0,0,0)),(500,430))
            screen.blit(pixelfont.render("Rounds: "+str(savedata["pistol_ammo"]),True,(0,0,0)),(500,460))
            if Rect(475,420,250,80).collidepoint(mx,my):
                draw.rect(screen,(255,255,255),(475,420,250,80))
                draw.rect(screen,(0,0,0),(475,420,250,80),3)
                screen.blit(pixelfont.render("Buy 5 ---- $5",True,(0,0,0)),(500,430))
                screen.blit(pixelfont.render("Rounds: "+str(savedata["pistol_ammo"]),True,(0,0,0)),(500,460))
                if click and savedata["money"]>=5 and (savedata["pistol_ammo"]+5)<9999:
                    savedata["pistol_ammo"]+=5
                    savedata["money"]-=5
            # RPG ammo
            screen.blit(pixelfont.render("RPG",True,(0,0,0)),(275,500))
            screen.blit(rpgIMG,(275,520))
            draw.rect(screen,(200,200,200),(475,520,250,80))
            draw.rect(screen,(0,0,0),(475,520,250,80),1)
            screen.blit(pixelfont.render("Buy 1 ---- $5",True,(0,0,0)),(500,530))
            screen.blit(pixelfont.render("Rounds: "+str(savedata["rpg_ammo"]),True,(0,0,0)),(500,560))
            if Rect(475,520,250,80).collidepoint(mx,my):
                draw.rect(screen,(255,255,255),(475,520,250,80))
                draw.rect(screen,(0,0,0),(475,520,250,80),3)
                screen.blit(pixelfont.render("Buy 1 ---- $5",True,(0,0,0)),(500,530))
                screen.blit(pixelfont.render("Rounds: "+str(savedata["rpg_ammo"]),True,(0,0,0)),(500,560))
                if click and savedata["money"]>=5 and (savedata["rpg_ammo"]+1)<9999:
                    savedata["rpg_ammo"]+=1
                    savedata["money"]-=5
            # medkit
            screen.blit(pixelfont.render("Health",True,(0,0,0)),(275,710))
            screen.blit(med_kitSHOP,(275,620))
            draw.rect(screen,(200,200,200),(475,620,250,80))
            draw.rect(screen,(0,0,0),(475,620,250,80),1)
            screen.blit(pixelfont.render("Buy 1 ---- $10",True,(0,0,0)),(500,630))
            screen.blit(pixelfont.render("Packs: "+str(savedata["medkit"]),True,(0,0,0)),(500,660))
            if Rect(475,620,250,80).collidepoint(mx,my):
                draw.rect(screen,(255,255,255),(475,620,250,80))
                draw.rect(screen,(0,0,0),(475,620,250,80),3)
                screen.blit(pixelfont.render("Buy 1 ---- $10",True,(0,0,0)),(500,630))
                screen.blit(pixelfont.render("Packs: "+str(savedata["medkit"]),True,(0,0,0)),(500,660))
                if click and savedata["money"]>=10 and (savedata["medkit"]+1)<9999:
                    savedata["medkit"]+=1
                    savedata["money"]-=10
            
        
        
            
                
            
    
                

    
    if level!=0 and level>=-1:
        # player movement variables
        screen.blit(space,(0,0))
        player.x+=vx
        player.x+=movex
        player.y+=vy
        player.y+=grav
        movex=0
        # INPUTS PRESSES
        if keys[K_1]:
            weapons_select=1
            gun_animation=0
        if keys[K_2]:
            weapons_select=2
            gun_animation=0
        if keys[K_3]:
            weapons_select=3
            gun_animation=0
        if keys[K_a]:
            movex=-3
            spritedirection="L"
            animationcheck=1
        if keys[K_d]:
            movex=+3
            spritedirection="R"
            animationcheck=1
        if keys[K_SPACE] and jumpcheck==1:
            vy=-10
            jumpcheck=0
            fallcheck=1
            flutterfix=1
            checkflut=1
        # TEST: spawn goomba
        if keys[K_q] and a==0:
            basicenemyVX.append(0)
            basicenemyVY.append(0)
            basicenemyGRAV.append(6)
            basicenemyDICT+=1
            basicenemyRECT.append(Rect(randint(250,1300),450,30,30))
            basicenemyfallcheck.append(1)
            basicenemysaveblock.append(Rect(400,620,300,100))
            basicenemystarttofallcheck.append(1)
            basicenemyflutterfix.append(1)
            basicenemyfluttercheck.append(0)
            basicenemysavex.append(basicenemyRECT[basicenemyDICT].x)
            basicenemycheckflut.append(0)
            basicenemyjumpcheck.append(0)
            basicenemysaveright.append(basicenemyRECT[basicenemyDICT].right)
            basicenemyHP.append(100)
            basicenemyjumptrigger.append(0)
            basicenemyshotsRATE.append(0)
            basicenemyshotsWAIT.append(randint(360,480))
        # TEST: spawn goomba
        if keys[K_p] and a==0:
            flyenemyVX.append(0)
            flyenemyVY.append(0)
            flyenemyRECT.append(Rect(400,randint(300,500),50,50))
            flyenemyHP.append(200)
            flyenemyshotsWAIT.append(randint(200,300))
            flyenemyshotsRATE.append(0)
        firerate+=1
        rpg_firerate+=1
        if mb[0]:
            if mx<(player.x+(player.width/2)):
                spritedirection="L"
            else:
                spritedirection="R"
            # fire assault rifle
            if weapons_select==1 and firerate>=10 and savedata["rifle_ammo"]>0:
                savedata["rifle_ammo"]-=1
                mixer.Sound.play(rifleSOUND)
                firerate=0
                middleX=player.x+(player.width/2)
                middleY=player.y+(player.height/2)
                dX=mx-middleX
                dY=my-middleY
                d=dist(middleX,middleY,mx,my)
                shotsX.append(middleX)
                shotsY.append(middleY)
                shotsVX.append(dX/d*30)
                shotsVY.append(dY/d*30)
                shotsTYPE.append(1)
            # fire rpg
            if weapons_select==3 and rpg_firerate>=240 and savedata["rpg_ammo"]>0:
                savedata["rpg_ammo"]-=1
                rpg_firerate=0
                middleX=player.x+(player.width/2)
                middleY=player.y+(player.height/2)
                dX=mx-middleX
                dY=my-middleY
                d=dist(middleX,middleY,mx,my)
                shotsX.append(middleX)
                shotsY.append(middleY)
                shotsVX.append(dX/d*5)
                shotsVY.append(dY/d*5)
                shotsTYPE.append(3)
        if click:
            # fire pistol
            if weapons_select==2 and savedata["pistol_ammo"]>0:
                savedata["pistol_ammo"]-=1
                mixer.Sound.play(pistolSOUND)
                middleX=player.x+(player.width/2)
                middleY=player.y+(player.height/2)
                dX=mx-middleX
                dY=my-middleY
                d=dist(middleX,middleY,mx,my)
                shotsX.append(middleX)
                shotsY.append(middleY)
                shotsVX.append(dX/d*30)
                shotsVY.append(dY/d*30)
                shotsTYPE.append(2)

        if keys[K_a] or keys[K_d]:
            a=1
        else:
            animationcheck=0

        # heal
        if keys[K_h] and savedata["medkit"]>0 and hp<savedata["maxhp"]:
            savedata["medkit"]-=1
            hp=savedata["maxhp"]

        if keys[K_ESCAPE]:
            savelevel=level
            level=0
            pause=1
            
        # GRAVITY
        if vy<0:
            vy+=0.05
            if vy>0:
                vy=0
        if fallcheck==1:
            grav=6


# -- LEVELS ------------------------------------------------------------------------------------------------------------------------------------------------------------------ 

    if level==-1:
        # ground
        for i in level_1:
            collide(level_1[i])
            draw.rect(screen,(150,150,150),level_1[i])
            for a in range(0,level_1[i].height,10):
                draw.line(screen,(255,255,255),(level_1[i].x,level_1[i].y + a),(level_1[i].right,level_1[i].y + a),1)
            for b in range(0,level_1[i].width,10):
                draw.line(screen,(0,0,0),(level_1[i].x + b,level_1[i].y),(level_1[i].x + b,level_1[i].bottom))

        # functions
        falloff()
        projectile(level_1)
        basicenemy(level_1)
        flyenemy(level_1)

        goomba_wait+=1
        heli_wait+=1
        # frenzie goomba spawn rate
        if goomba_wait==goomba_spawn_rate:
            if goomba_spawn_rate>120:
                goomba_spawn_rate-=1
            goomba_wait=0
            basicenemyVX.append(0)
            basicenemyVY.append(0)
            basicenemyGRAV.append(6)
            basicenemyDICT+=1
            basicenemyRECT.append(Rect(choice(frenzie_goomba_spawnX),choice(frenzie_goomba_spawnY),30,30))
            basicenemyfallcheck.append(1)
            basicenemysaveblock.append(Rect(0,0,0,0))
            basicenemystarttofallcheck.append(1)
            basicenemyflutterfix.append(1)
            basicenemyfluttercheck.append(0)
            basicenemysavex.append(0)
            basicenemycheckflut.append(0)
            basicenemyjumpcheck.append(0)
            basicenemysaveright.append(0)
            basicenemyHP.append(100)
            basicenemyjumptrigger.append(0)
            basicenemyshotsRATE.append(0)
            basicenemyshotsWAIT.append(randint(360,480))



        # frenzie heli spawn rate
        if heli_wait==heli_spawn_rate:
            if heli_spawn_rate>300:
                heli_spawn_rate-=1
            heli_wait=0
            flyenemyVX.append(0)
            flyenemyVY.append(0)
            flyenemyRECT.append(Rect(choice(frenzie_heli_spawnX),choice(frenzie_heli_spawnY),50,50))
            flyenemyHP.append(200)
            flyenemyshotsWAIT.append(randint(200,300))
            flyenemyshotsRATE.append(0)

        # player dies
        if hp<=0:
            level=-3
            mixer.music.stop()
            mixer.Sound.play(wastedSOUND)




    if level==1:
    # ground
        for i in campaign_1:
            collide(campaign_1[i])
            draw.rect(screen,(150,150,150),campaign_1[i])
            for a in range(0,campaign_1[i].height,10):
                draw.line(screen,(255,255,255),(campaign_1[i].x,campaign_1[i].y + a),(campaign_1[i].right,campaign_1[i].y + a),1)
            for b in range(0,campaign_1[i].width,10):
                draw.line(screen,(0,0,0),(campaign_1[i].x + b,campaign_1[i].y),(campaign_1[i].x + b,campaign_1[i].bottom))

        # functions
        falloff()
        projectile(campaign_1)
        basicenemy(campaign_1)
        flyenemy(campaign_1)
        
        if hp<=0:
            level=-3
            mixer.music.stop()
            mixer.Sound.play(wastedSOUND)
        nextlevelrect=Rect(1720,0,50,50)
        draw.rect(screen,(255,255,0),nextlevelrect)
        if player.colliderect(nextlevelrect):
            # proceeds to next level (clears and creates new enemies)
            level=2
            savedata["level"]=2
            hp=savedata["maxhp"]
            player=Rect(20,500,30,43)
            basicenemyVX.clear()
            basicenemyVY.clear()
            basicenemyGRAV.clear()
            if True:
                if True:
                    if True:
                        basicenemyDICT+=1
                        basicenemyRECT.clear()
                        basicenemyfallcheck.clear()
                        basicenemysaveblock.clear()
                        basicenemystarttofallcheck.clear()
                        basicenemyflutterfix.clear()
                        basicenemyfluttercheck.clear()
                        basicenemysavex.clear()
                        basicenemycheckflut.clear()
                        basicenemyjumpcheck.clear()
                        basicenemysaveright.clear()
                        basicenemyHP.clear()
                        basicenemyjumptrigger.clear()
                        basicenemyshotsRATE.clear()
                        basicenemyshotsWAIT.clear()
            if True:
                if True:
                    for i in range(0,len(enemyX)):
                        basicenemyVX.append(0)
                        basicenemyVY.append(0)
                        basicenemyGRAV.append(6)
                        basicenemyDICT+=1
                        basicenemyRECT.append(Rect(enemyX[i],enemyY[i],30,30))
                        basicenemyfallcheck.append(1)
                        basicenemysaveblock.append(Rect(400,620,300,100))
                        basicenemystarttofallcheck.append(1)
                        basicenemyflutterfix.append(1)
                        basicenemyfluttercheck.append(0)
                        basicenemysavex.append(0)
                        basicenemycheckflut.append(0)
                        basicenemyjumpcheck.append(0)
                        basicenemysaveright.append(0)
                        basicenemyHP.append(100)
                        basicenemyjumptrigger.append(0)
                        basicenemyshotsRATE.append(0)
                        basicenemyshotsWAIT.append(randint(360,480))

            
    if level==2:
        for i in campaign_2:
            collide(campaign_2[i])
            draw.rect(screen,(150,150,150),campaign_2[i])
            for a in range(0,campaign_2[i].height,10):
                draw.line(screen,(255,255,255),(campaign_2[i].x,campaign_2[i].y + a),(campaign_2[i].right,campaign_2[i].y + a),1)
            for b in range(0,campaign_2[i].width,10):
                draw.line(screen,(0,0,0),(campaign_2[i].x + b,campaign_2[i].y),(campaign_2[i].x + b,campaign_2[i].bottom))

        # functions
        falloff()
        projectile(campaign_2)
        basicenemy(campaign_2)
        flyenemy(campaign_2)

        # proceeds to next level (clears and creates new enemies)
        nextlevelrect=Rect(1600,200,20,20)
        draw.rect(screen,(255,255,0),nextlevelrect)
        if player.colliderect(nextlevelrect):
            level=3
            savedata["level"]=3
            hp=savedata["maxhp"]
            player=Rect(30,750,30,43)
            if True:
                if True:
                    for a in range(0,2):
                        for i in range(0,len(lvl3_enemies_X)):
                            flyenemyVX.append(0)
                            flyenemyVY.append(0)
                            flyenemyRECT.append(Rect(randint(lvl3_enemies_X[i]-10,lvl3_enemies_X[i]+10),randint(lvl3_enemies_Y[i]-10,lvl3_enemies_Y[i]+10),50,50))
                            flyenemyHP.append(200)
                            flyenemyshotsWAIT.append(randint(200,300))
                            flyenemyshotsRATE.append(0)
        
        if hp<=0:
            level=-3
            mixer.music.stop()
            mixer.Sound.play(wastedSOUND)
    if level==3:
        for i in campaign_3:
            collide(campaign_3[i])
            draw.rect(screen,(150,150,150),campaign_3[i])
            for a in range(0,campaign_3[i].height,10):
                draw.line(screen,(255,255,255),(campaign_3[i].x,campaign_3[i].y + a),(campaign_3[i].right,campaign_3[i].y + a),1)
            for b in range(0,campaign_3[i].width,10):
                draw.line(screen,(0,0,0),(campaign_3[i].x + b,campaign_3[i].y),(campaign_3[i].x + b,campaign_3[i].bottom))

        # functions
        falloff()
        projectile(campaign_3)
        flyenemy(campaign_3)


        endrect=Rect(1780,0,20,20)
        draw.rect(screen,(255,255,0),endrect)
        # beat the game trigger
        if player.colliderect(endrect):
            level=-4
            savedata["level"]=1
            mixer.music.stop()
            mixer.music.load("sounds/the_end.mp3")
            mixer.music.play(-1)

        # player dies
        if hp<=0 or player.y>900:
            level=-3
            mixer.music.stop()
            mixer.Sound.play(wastedSOUND)
        

            

    # DEATH SCREEN AND END SCREEN----------------

    # death screen
    if level==-3:
        ded+=1
        if dedCOL>0:
            dedCOL-=1
        screen.fill((dedCOL,dedCOL,dedCOL))
        if ded>=240:
            screen.blit(squarefont.render("You Died!",True,(255,255,255)),(600,350))
            screen.blit(pixelfont.render("Restart the game to play again.",True,(255,255,255)),(700,550))
    # end screen
    if level==-4:
        screen.fill((0,0,0))
        screen.blit(squarefont.render("You Won!",True,(255,255,255)),(600,350))
        screen.blit(pixelfont.render("Restart the game to play again.",True,(255,255,255)),(700,550))


        
        


# ------ draw stuff ---------------------------------------------------------------------------------------------------------------------------------------------------

    # player animations
    if True:
      if True:
        #draw.rect(screen,(0,255,0),player,1)
        if level!=0 and level>=-1:
            if vy==0 and animationcheck==0:
                if spritedirection=="L":
                    screen.blit(standleft,(player.x,player.y))
                else:
                    screen.blit(standright,(player.x,player.y))
            else:
                if animationcheck==0 or vy!=0:
                    if spritedirection=="L":
                        screen.blit(jumpleft,(player.x,player.y))
                    else:
                        screen.blit(jumpright,(player.x,player.y))
            # hit marker
            if hitmarker>=1:
                if hitmarkerwait==0:
                    if hitmarker==1:
                        mixer.Sound.play(hitmarkerSOUND)
                    elif hitmarker==2:
                        mixer.Sound.play(killSOUND)
                    hitmarkerwait=10
                hitmarkerwait-=1
                if hitmarker==1:
                    screen.blit(hitmarker_logo,(mx-20,my-20))
                elif hitmarker==2:
                    screen.blit(hitmarker2,(mx-20,my-20))
                if hitmarkerwait==0:
                    hitmarker=0

                    
            # running animation
            if animationcheck==1 and vy==0:
                if animationdelay<=28/4:
                    if spritedirection=="L":
                        screen.blit(animationleft["step1"],(player.x,player.y))
                    else:
                        screen.blit(animationright["step1"],(player.x,player.y))
                elif animationdelay<=56/4:
                    if spritedirection=="L":
                        screen.blit(animationleft["step1H"],(player.x,player.y))
                    else:
                        screen.blit(animationright["step1H"],(player.x,player.y))
                elif animationdelay<=112/4:
                    if spritedirection=="L":
                        screen.blit(animationleft["step2"],(player.x,player.y))
                    else:
                        screen.blit(animationright["step2"],(player.x,player.y))
                elif animationdelay<=140/4:
                    if spritedirection=="L":
                        screen.blit(animationleft["step3"],(player.x,player.y))
                    else:
                        screen.blit(animationright["step3"],(player.x,player.y))
                elif animationdelay<=168/4:
                    if spritedirection=="L":
                        screen.blit(animationleft["step4"],(player.x,player.y))
                    else:
                        screen.blit(animationright["step4"],(player.x,player.y))
                elif animationdelay<=196/4:
                    if spritedirection=="L":
                        screen.blit(animationleft["step5"],(player.x,player.y))
                    else:
                        screen.blit(animationright["step5"],(player.x,player.y))
                elif animationdelay<=224/4:
                    if spritedirection=="L":
                        screen.blit(animationleft["step6"],(player.x,player.y))
                    else:
                        screen.blit(animationright["step6"],(player.x,player.y))
                animationdelay+=1
                if animationdelay>=224/4:
                    animationdelay=0
            else:
                animationdelay=0

                
            # gun animations
            
            if mb[0] or gun_animation<120:
                if mb[0]:
                    gun_animation=0
                gun_animation+=1
                angleofshot=angle = degrees(atan2(mx-(player.x),my-(player.y + player.height/2.3))-89.5)
                if weapons_select==1:
                    if mx>player.x+player.width/2: 
                        rotPic=transform.rotate(assaultrifle,angleofshot)
                        screen.blit(rotPic,(player.x,player.y + player.height/2.3))
                    else:
                        rotPic=transform.rotate(assaultrifleleft,angleofshot)
                        screen.blit(rotPic,(player.x,player.y + player.height/2.3))
                if weapons_select==2:
                    if mx>player.x+player.width/2: 
                        rotPic=transform.rotate(pistolright,angleofshot)
                        screen.blit(rotPic,(player.x,player.y + player.height/2.3))
                    else:
                        rotPic=transform.rotate(pistolleft,angleofshot)
                        screen.blit(rotPic,(player.x,player.y + player.height/2.3))
                if weapons_select==3:
                    angleofshot=angle = degrees(atan2(mx-(player.x),my-(player.y))-89.6)
                    if mx>player.x+player.width/2: 
                        rotPic=transform.rotate(rpg_right,angleofshot)
                        screen.blit(rotPic,(player.x,player.y))
                    else:
                        rotPic=transform.rotate(rpg_left,angleofshot)
                        screen.blit(rotPic,(player.x,player.y))

            # explosions
            for i in range(0,len(exp_X)):
                draw.circle(screen,(255,100,0),(exp_X[i],exp_Y[i]),exp_SIZE[i])
                exp_SIZE[i]-=1
                if exp_SIZE[i]<0:
                    exp_X.pop(i)
                    exp_Y.pop(i)
                    exp_SIZE.pop(i)
                    break
                
# --------- HUD ELEMENTS -----------------------------------------------
            # health bar
            draw.rect(screen,(255,0,0),(20,860,200,20))
            draw.rect(screen,(0,255,0),(20,860,200*(hp/savedata["maxhp"]),20))
            screen.blit(pixelfont.render(str(hp)+"/"+str(savedata["maxhp"])+" HP",True,(255,255,255)),(30,860))
            # ammo bar
            draw.rect(screen,(255,255,255),(0,0,950,20))
            draw.rect(screen,(0,0,0),(0,0,750,20),1)
            screen.blit(pixelfont.render("Rifle Ammo:"+str(savedata["rifle_ammo"]),True,(0,0,0)),(5,0))
            draw.line(screen,(0,0,0),(190,0),(190,20),5)
            screen.blit(pixelfont.render("Pistol Ammo:"+str(savedata["pistol_ammo"]),True,(0,0,0)),(200,0))
            draw.line(screen,(0,0,0),(400,0),(400,20),5)
            screen.blit(pixelfont.render("Rocket Ammo:"+str(savedata["rpg_ammo"]),True,(0,0,0)),(410,0))
            draw.line(screen,(0,0,0),(590,0),(590,20),5)
            screen.blit(pixelfont.render("Medkits:"+str(savedata["medkit"]),True,(0,0,0)),(610,0))
            # score
            draw.rect(screen,(255,255,255),(1600,870,200,30))
            draw.rect(screen,(0,0,0),(1600,870,200,30),1)
            screen.blit(pixelfont.render("Score:"+str(savedata["score"]),True,(0,0,0)),(1610,875))
#-----------------------
        myClock.tick(120)
        #print(myClock.get_fps())
    display.flip()
if resetsavedata==1:    
    savedata={
        "money" : 100,
        "rifle_ammo" : 480,
        "pistol_ammo" : 240,
        "rpg_ammo" : 10,
        "rifle_damage" : 25,
        "pistol_damage" : 50,
        "rpg_damage" : 100,
        "medkit" : 10,
        "maxhp" : 100,
        "volume" : 1,
        "level" : 1,
        "score" : 0
        }
    pickle_out=open("savedata.pickle","wb")
    pickle.dump(savedata,pickle_out)
    pickle_out.close()
quit()
sys.exit()

