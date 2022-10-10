from pygame import *

screen=display.set_mode((1800,900))

blocks={}
amount=0
saveX=[]
saveY=[]
enemyX=[]
enemyY=[]
toolselect=1

print("\n\n\nLevel builder\n----------------\nLeft click on two points to create rectangle\nRight click to delete block\nRed area is out of screen\n\nTo extract rectangles, type print(blocks) then \ncopy and paste into code as a dicionary and remove\n<> and capitalize R")

running=True
while running:
    click=False
    for evnt in event.get():
        if evnt.type== QUIT:
            running=False
            for i in blocks:
                blocks[i].x-=20
                blocks[i].y-=20
        if evnt.type==MOUSEBUTTONDOWN:
            if evnt.button==1:
                click=True
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    keys=key.get_pressed()
#-----------------------
    screen.fill((255,0,0))
    draw.rect(screen,(255,255,255),(20,20,1800,900))
    for i in blocks:
        draw.rect(screen,(0,0,0),blocks[i])
        if blocks[i].collidepoint(mx,my):
            draw.rect(screen,(255,0,0),blocks[i],3)
            if mb[2]:
                blocks.pop(i)
                break
        if blocks[i].width<0:
            blocks[i].x+=blocks[i].width
            blocks[i].width=blocks[i].width*-1
        if blocks[i].height<0:
            blocks[i].y+=blocks[i].height
            blocks[i].height=blocks[i].height*-1


    for i in range(0,len(enemyX)):
        draw.rect(screen,(0,0,255),(enemyX[i],enemyY[i],30,30))
        if Rect(enemyX[i],enemyY[i],30,30).collidepoint(mx,my):
            draw.rect(screen,(255,0,0),(enemyX[i],enemyY[i],30,30),3)
            if mb[2]:
                enemyX.pop(i)
                enemyY.pop(i)
                break
            
            
    if click:
        if toolselect==1:
            saveX.append(mx)
            saveY.append(my)
        elif toolselect==2:
            enemyX.append(mx)
            enemyY.append(my)
            
    if len(saveX)==2:
        amount+=1
        blocks[str(amount)]=Rect(saveX[0],saveY[0],saveX[1]-saveX[0],saveY[1]-saveY[0])
        saveX.clear()
        saveY.clear()
    if len(saveX)==1:
        draw.rect(screen,(0,0,0),(saveX[0],saveY[0],mx-saveX[0],my-saveY[0]),1)

    if keys[K_1]:
        toolselect=1
    if keys[K_2]:
        toolselect=2

#-----------------------
    display.flip()
quit()
