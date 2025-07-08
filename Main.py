import pygame
import random
import time
import math
import os


pygame.init()
pygame.mixer.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
width,hieght = info.current_w,info.current_h
wn = pygame.display.set_mode((width-20,hieght-20))

class background:
    def __init__(self,pos) -> None:
        self.pos = pos
        self.im = pygame.transform.scale(pygame.image.load('total con background.png'),(width-20,hieght-20))

class map_hidder:
    def __init__(self,pos) -> None:
        self.pos = pos
        self.im = pygame.transform.scale(pygame.image.load('total con dark cloud hidemap.png'),((width-20)/40,(width-20)/40))

class flamethrower_soldier:
    def __init__(self,pos,side,speed,color) -> None:
        self.range = 150
        self.hp = 120
        self.firstturn = 'never'
        self.direction = 'L'
        self.move = True
        self.originalhp = 120
        self.hpbar = 50
        self.side = side
        self.color = color
        self.unittype='fs'
        self.im = pygame.transform.scale(pygame.image.load('total con flamethrower soldier.png'),((width-20)/50,(width-20)/50))
        self.originalpos = pos
        self.speed = speed
        self.pos = pos
        self.target = pos

class pistol_soldier:
    def __init__(self,pos,side,speed,color) -> None:
        self.range = 400
        self.hp = 70
        self.firstturn = 'never'
        self.direction = 'R'
        self.move = True
        self.originalhp = 70
        self.hpbar = 50
        self.side = side
        self.color = color
        self.unittype='ps'
        self.im = pygame.transform.scale(pygame.image.load('total con pistol soldier2.png'),((width-20)/50,(width-20)/50))
        self.originalpos = pos
        self.speed = speed
        self.pos = pos
        self.target = pos

class tank:
    def __init__(self,pos,side,speed,color) -> None:
        self.range = 750
        self.hp = 700
        self.firstturn = False
        self.move = True
        self.originalhp = 700
        self.hpbar = 50
        self.side = side
        self.color = color
        self.unittype='t'
        self.im = pygame.transform.scale(pygame.image.load('total con tank.png'),((width-20)/35,(width-20)/25))
        self.originalpos = pos
        self.speed = speed
        self.pos = pos
        self.target = pos

class buildingsoldiergen:
    def __init__(self,pos,side,color) -> None:
        self.unittype=['fs','ps','t']
        self.side = side
        self.color = color
        self.hpbar = 150
        self.spawnfs = False
        self.spawnps = False
        self.spawnt = False
        self.hp = 150
        self.fspsgen = pygame.transform.scale(pygame.image.load('total con soldier generator.png'),((width-20)/20,(width-20)/20))
        self.pos = pos

class picbuildingfspsgen:
    def __init__(self,pos,side) -> None:
        self.unittype='pic'
        self.side = side
        self.fspsgen = pygame.transform.scale(pygame.image.load('total con soldier generator.png'),((width-20)/20,(width-20)/20))
        self.pos = pos    

class bullet:
    def __init__(self,pos,damage,target,side) -> None:
        self.pos = pos
        self.side = side
        self.damage = damage
        self.target = target

class crate:
    def __init__(self,pos,level) -> None:
        pass

class steel_wall:
    def __init__(self,pos):
        self.pos = pos
        self.hp = 100

class picsteel_wall:
    def __init__(self,pos):
        self.pos = pos
        self.hp = None

class team:
    def __init__(self) -> None:
        self.build = True

backgrounds = [background([0,0]),background([-width+20,-hieght+20]),background([width-20,-hieght+20]),background([-width+20,hieght-20]),background([width-20,hieght-20]),background([0,-hieght+20]),background([width-20,0]),background([-width+20,0]),background([0,hieght-20])]
map_hidders = []  
map_hidders_destroyed = []  
# for i in range(22):
#     for j in range(12):
#         map_hidders.append(map_hidder([i*120-30,j*120-30]))
bullets = []
destroyed_bullets = []
walls = []
men = []
dead = []
buildings = [picbuildingfspsgen([10,10],'m'),picbuildingfspsgen([width-20-(width)/20,10],'e'),buildingsoldiergen([200,200],'e1',(255,255,0)),buildingsoldiergen([300,300],'e2',(255,0,255))]
count = 0
clicked_on_fs_ps_gen = False
# die_sound = pygame.mixer.Sound()
# flame_sound = pygame.mixer.Sound()
shot_sound = pygame.mixer.Sound('gunshot.mp3')
# n = 1
def scrolling_screen(n1,n2):
    for i in men:
        i.pos[0]+=n1
        i.pos[1]+=n2
        if i.target != 'find' and i.pos != i.target:
            i.target[0]+=n1
            i.target[1]+=n2
    for i in buildings:
        if i.unittype != 'pic':
            i.pos[0]+=n1
            i.pos[1]+=n2
    for i in backgrounds:
        i.pos[0]+=n1
        i.pos[1]+=n2
    placeofrightclick[0]+=n1
    placeofrightclick[1]+=n2

money1 = 1000
money2 = 1000
money3 = 1000
money4 = 1000
build1 = True
build2 = True
build3 = True

home_screen_showing = True
font = pygame.font.Font('freesansbold.ttf',round(hieght-hieght*7/8))
text1 = font.render('START', True,(0,255,0))
text2 = font.render('INSTRUCTIONS', True,(0,255,0))
being_held = 0
rightclicked = False
placeofrightclick = None

while home_screen_showing:
    mouse = pygame.mouse.get_pos()
    pygame.draw.rect(wn,(255,0,0),(width*3/7,hieght*2/11,width-width*4/5,hieght-hieght*7/8),5)
    pygame.draw.rect(wn,(255,0,0),(width*2/7,hieght*4/11,width-width*4/8,hieght-hieght*7/8),5)
    wn.blit(text1,(width*3/7+10,hieght*2/11+10))
    wn.blit(text2,(width*2/7+20,hieght*4/11+10))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(width*2/7,hieght*4/11,width-width*4/8,hieght-hieght*7/8)
            print(mouse)
            if mouse[0] < width*3/7 and mouse[0] > width-width*4/5 and mouse[1] > hieght*2/11 and mouse[1] < hieght-hieght*7/8:
                home_screen_showing = False
            if mouse[0] > width*2/7 and mouse[0] < width-width*4/8 and mouse[1] < hieght*4/11 and mouse[1] > hieght-hieght*7/8:
                home_screen_showing = False

while True:
    for i in backgrounds:
        wn.blit(i.im,i.pos)
    mouse = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[1] or pygame.mouse.get_pressed()[2]:
        being_held+=1
        if rightclicked == True and being_held > 1:
            pygame.draw.rect(wn,(0,0,0),(placeofrightclick[0],placeofrightclick[1],mouse[0]-placeofrightclick[0],mouse[1]-placeofrightclick[1]),3)
            for i in men:
                if i.pos[0] > placeofrightclick[0] and i.pos[0] < mouse[0] and i.pos[1] > placeofrightclick[1] and i.pos[1] < mouse[1] and i.side == 'm':
                    pygame.draw.rect(wn,(0,0,0),(i.pos[0],i.pos[1],50,50),2)
        else:
            
            rightclicked = True
            placeofrightclick = list(mouse)
    else:
        if rightclicked == True:
                for i in men:
                    if i.pos[0] > placeofrightclick[0] and i.pos[0] < mouse[0] and i.pos[1] > placeofrightclick[1] and i.pos[1] < mouse[1] and i.side == 'm':
                        i.target='find'
        being_held = 0
    scroll = True
    for i in backgrounds:
        if i.pos[0] < -3*width-(i.pos[0]+width)+1:
            scrolling_screen(1,0)
            scroll = False
        if i.pos[0] > 3*width-(i.pos[0]-width)-1:
            scrolling_screen(-1,0)
            scroll = False
        if i.pos[1] < -3*hieght-(i.pos[1]+hieght)+1:
            scrolling_screen(0,1)
            scroll = False
        if i.pos[1] > 3*hieght-(i.pos[1]-hieght)-1:
            scrolling_screen(0,-1)
            scroll = False

    if scroll == True:
        if mouse[0] < width/26:
            scrolling_screen(40,0)
        if mouse[0] > -width/26+width:
            scrolling_screen(-40,0)
        if mouse[1] < hieght/14:
            scrolling_screen(0,40)
        if mouse[1] > -hieght/14+hieght:
            scrolling_screen(0,-40)

    shot_sound_first = True
    check_building=None
    count+=1
    time.sleep(0.01)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            mouse = pygame.mouse.get_pos()
            for i in buildings:
                if i.pos[0] - mouse[0] > -175 and i.pos[0] - mouse[0] < 0 and i.pos[1] - mouse[1] > -175 and i.pos[1] - mouse[1] < 0 and money1 >= 50 and i.unittype==['fs','ps','t'] and i.side == 'm':
                    if event.key == pygame.K_f:
                        i.spawnfs = True
                        done = True
                        money1 -= 50
                        check_building = i
                    if event.key == pygame.K_p:
                        i.spawnps = True
                        done = True
                        money1 -= 50
                        check_building = i
                    if event.key == pygame.K_t:
                        i.spawnt = True
                        done = True
                        money1 -= 50
                        check_building = i
            if event.key == pygame.K_k:
                men = []
        if event.type == pygame.MOUSEBUTTONDOWN: 
            
            clicked = pygame.mouse.get_pos()
            if clicked[0] > width-((width-20)/20+40) and clicked[0] < width and clicked[1] > 0 and clicked[1] < (width-20)/20+20 and money1 >= 300:
                done = False
                money1-=300
                while done == False:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            buildings.append(buildingsoldiergen(list(pygame.mouse.get_pos()),'m',(0,0,255)))
                            done = True
            
            if clicked[0] > 0 and clicked[0] < (width-20)/20 and clicked[1] > 0 and clicked[1] < (width-20)/20 and money2 >= 300:
                done = False
                money2-=300
                while done == False:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            buildings.append(buildingsoldiergen(list(pygame.mouse.get_pos()),'e',(255,0,0)))
                            done = True
            
            for i in men:
                if i.target == 'find':
                    i.target = [clicked[0],clicked[1]]
                    if i.unittype == 't':
                        i.firstturn=True
                if i.pos[0] - clicked[0] > -75 and i.pos[0] - clicked[0] < 0 and i.pos[1] - clicked[1] > -75 and i.pos[1] - clicked[1] < 0  and i.side == 'm':
                    i.target = 'find'
                    
    for i in buildings:
        # if i.unittype == 'pic' and i.side == 'm':
        #     i.pos[0]-=width
        if count%25==0 and money2 > 200 and i.side!='m':
            i.spawnfs = True
            check_building = i
            money2 -= 50
            if count%50==0 and money2 > 100 and i.side!='m':
                i.spawnps = True
                check_building = i
                money2 -= 50
        
        if money2 > 1000 and count%200==0 and i.side != 'm' and i.unittype != 'pic':
            money2-=300
            if i.side == 'e' and build1 == True:
                build1 = False
                n1 = random.randint(-1,1)
                n2 = random.randint(-1,1)
                buildings.append(buildingsoldiergen([i.pos[0]+200*n1,i.pos[1]+200*n2],i.side,i.color))
            if i.side == 'e1' and build2 == True:
                build2 = False
                n1 = random.randint(-1,1)
                n2 = random.randint(-1,1)
                buildings.append(buildingsoldiergen([i.pos[0]+200*n1,i.pos[1]+200*n2],i.side,i.color))
            if i.side == 'e2' and build3 == True:
                build3 = False
                n1 = random.randint(-1,1)
                n2 = random.randint(-1,1)
                buildings.append(buildingsoldiergen([i.pos[0]+200*n1,i.pos[1]+200*n2],i.side,i.color))
            

    for i in buildings:
        for j in men:
            if i.pos[0] - j.pos[0] > -175 and i.pos[0] - j.pos[0] < 0 and i.pos[1] - j.pos[1] > -175 and i.pos[1] - j.pos[1] < 0 and i.side != j.side and i.unittype!='pic':
                i.hp -= 1
                if i.hp <= 0:
                    i.side = j.side
                    i.hp = 150
                    i.color = j.color
                i.spawnfs = False
                i.spawnps = False
                i.spawnt = False
            # elif i.unittype != 'pic':
            #     if i.hp < 100:
            #         i.hp += 1

        wn.blit(i.fspsgen,i.pos)
        if i.unittype != 'pic':
            pygame.draw.rect(wn,i.color,(i.pos[0],i.pos[1]-20,i.hp,10))
            pygame.draw.rect(wn,(0,0,0),(i.pos[0],i.pos[1]-20,150,10),width=1)
        if i.unittype==['fs','ps','t'] and i.spawnfs == True:
            men.append(flamethrower_soldier([i.pos[0]+100,i.pos[1]+150],i.side,12,i.color))
        if i.unittype==['fs','ps','t'] and i.spawnps == True:
            men.append(pistol_soldier([i.pos[0]+100,i.pos[1]+150],i.side,12,i.color))
        if i.unittype==['fs','ps','t'] and i.spawnt == True:
            men.append(tank([i.pos[0]+100,i.pos[1]+150],i.side,8,i.color))
            
        i.spawnfs = False
        i.spawnps = False
        i.spawnt = False

    count_for_men_place = 0
    cantattack = []
    for i in men:
        canshoot=True
        # if i.unittype=='ps' and count%7==0:
        #     i.move = True
        if i.target != 'find':
            dx = i.target[0] - i.pos[0]
            dy = i.target[1] - i.pos[1]
            distance = (dx**2 + dy**2)**0.5
            if distance <= 100:
                i.target = i.pos

            else:
                if i.speed * dx / distance < 0 and i.unittype != 't':
                    if i.direction == "L":
                        i.direction = "R"
                        i.im = pygame.transform.flip(i.im,1,0)
                if i.speed * dx / distance > 0 and i.unittype != 't':
                    if i.direction == "R":
                        i.direction = "L"
                        i.im = pygame.transform.flip(i.im,1,0)
                # if i.unittype == 't' and i.firstturn == True:
                #     pos = i.target
                #     xd = pos[0]-i.pos[0]
                #     yd = -(pos[1]-i.pos[1])
                #     angle = math.degrees(math.atan2(yd,xd))
                #     i.im = pygame.transform.rotate(i.im,angle - 90)
                i.pos[0] += i.speed * dx / distance
                i.pos[1] += i.speed * dy / distance
        target_picked = False
        count_for_men_place2 = 0
        for j in men:
            pn1 = random.choice([-1,1])
            pn2 = random.choice([-1,1])
            if i.pos[0] - j.pos[0] > -30 and i.pos[0] - j.pos[0] < 30 and i.pos[1] - j.pos[1] > -30 and i.pos[1] - j.pos[1] < 30 and i != j and i.side == j.side:
                i.pos[0]=i.pos[0]+31*pn1
                i.pos[1]=i.pos[1]+31*pn2
                # i.originalpos[0]=i.originalpos[0]+31*pn1
                # i.originalpos[1]=i.originalpos[1]+31*pn1

            if i.pos[0] - j.pos[0] > -i.range and i.pos[0] - j.pos[0] < i.range and i.pos[1] - j.pos[1] > -i.range and i.pos[1] - j.pos[1] < i.range and i.side != j.side and target_picked == False and i.move == True:
                if i.unittype == 'fs':
                    j.hp-=10
                    if j.hp > 0:
                        j.hpbar-=(50/j.originalhp)*10
                if j.hp <= 0:
                    dead.append(men.pop(count_for_men_place2))


                if i.unittype == 'ps' and count%2 == 0:
                    if shot_sound_first == True:
                        shot_sound.play()
                    shot_sound_first = False
                    bullets.append(bullet([i.pos[0]+3,i.pos[1]+10],20,[j.pos[0]+40,j.pos[1]+20],i.side))
                    i.move = False
                    canshoot = False
                    cantattack=None
                    target_picked = True


                if i.unittype == 't' and count%16 == 0:
                    if shot_sound_first == True:
                        shot_sound.play()
                    shot_sound_first = False
                    bullets.append(bullet([i.pos[0]+3,i.pos[1]+10],90,[j.pos[0]+40,j.pos[1]+20],i.side))
                    canshoot = False
                    cantattack=None
                    target_picked = True
                    
            if i.side != 'm' and i.pos[0] - j.pos[0] > -700 and i.pos[0] - j.pos[0] < 700 and i.pos[1] - j.pos[1] > -700 and i.pos[1] - j.pos[1] < 700 and i.side != j.side and target_picked == False and i.move == True:
                target_picked = True
                dx = j.pos[0]-50 - i.pos[0]
                dy = j.pos[1]-50 - i.pos[1]
                distance = (dx**2 + dy**2)**0.5

                if distance <= i.speed:
                    pass
                    # i.originalpos[0] = j.pos[0]
                    # i.originalpos[1] = j.pos[1]
                else:
                    if i.speed * dx / distance < 0 and i.unittype != 't':
                        if i.direction == "R":
                            i.direction = "L"
                            i.im = pygame.transform.flip(i.im,1,0)
                    if i.speed * dx / distance >= 0 and i.unittype != 't':
                        if i.direction == "L":
                            i.direction = "R"
                            i.im = pygame.transform.flip(i.im,1,0)
                    i.pos[0] += i.speed * dx / distance
                    i.pos[1] += i.speed * dy / distance
                    # i.originalpos[0] += 15 * dx / distance
                    # i.originalpos[0] += 15 * dx / distance

            if i.pos[0] - j.pos[0] > -100 and i.pos[0] - j.pos[0] < 100 and i.pos[1] - j.pos[1] > -100 and i.pos[1] - j.pos[1] < 100 and i.side != j.side and i.side == 'm' and target_picked == False and i.move == True:
                target_picked = True
                dx = j.pos[0] - i.pos[0]
                dy = j.pos[1] - i.pos[1]
                distance = (dx**2 + dy**2)**0.5
                if distance <= i.speed:
                    pass
                    # i.originalpos[0] = j.pos[0]
                    # i.originalpos[1] = j.pos[1]
                else:
                    i.pos[0] += i.speed * dx / distance
                    i.pos[1] += i.speed * dy / distance
            count_for_men_place2+=1
        # if count%10 == 0:
        #     n*=-1
        # i.pos[0]+=n
        # i.pos[1]+=n
        pygame.draw.rect(wn,i.color,(i.pos[0],i.pos[1]-20,i.hpbar,10))
        pygame.draw.rect(wn,(0,0,0),(i.pos[0],i.pos[1]-20,50,10),width=1)
        
        wn.blit(i.im,i.pos)
        if i.hp <= 0:
            dead.append(men.pop(count_for_men_place))
        count_for_men_place+=1
    
    count_for_bullet_place=0
    if len(bullets)!=0:    
        for x in bullets:
            pygame.draw.circle(wn,(255,255,0),x.pos,4)
            if (x.pos[0], x.pos[1]) != (x.target[0], x.target[1]):
                dx = x.target[0] - x.pos[0]
                dy = x.target[1] - x.pos[1]
                distance = (dx**2 + dy**2)**0.5
                if distance <= 30:
                    bullets.pop(count_for_bullet_place)
                else:
                    x.pos[0] += 30 * dx / distance
                    x.pos[1] += 30 * dy / distance
            for y in men:
                if x.pos[0] - y.pos[0] > 0 and x.pos[0] - y.pos[0] < 50 and x.pos[1] - y.pos[1] > 0 and x.pos[1] - y.pos[1] < 50 and x.side != y.side:
                    y.hp-=x.damage
                    if y.hp > 0:
                        y.hpbar-=(50/y.originalhp)*x.damage
        count_for_bullet_place+=1
    # which_to_disapear = []
    # for i in range(len(map_hidders)):
    #     for j in men:
    #         if j.pos[0] - map_hidders[i].pos[0] < 400 and j.pos[0] - map_hidders[i].pos[0] > -400 and j.pos[1] - map_hidders[i].pos[1] < 400 and j.pos[1] - map_hidders[i].pos[1] > -400 and j.side == 'm':
    #             which_to_disapear.append(i)
    #     wn.blit(map_hidders[i].im,map_hidders[i].pos)
    pygame.display.flip()