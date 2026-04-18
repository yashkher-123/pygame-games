#more pygame  copy
import pygame
import random
import time
pygame.init()
pygame.font.init()

scwid = 700
schei = 900
global win
win = pygame.display.set_mode((scwid,schei))

pygame.display.set_caption("jetpack")

#coin_collection = pygame.mixer.Sound("coin_collect.wav")
thrust_sound = pygame.mixer.Sound("thrust_sfx.wav")
thrust_sound.set_volume(0.3)
fail_sound = pygame.mixer.Sound("fail_sfx.wav")
fail_sound.set_volume(0.8)

global last_score
global x
global xvel
global y
global yvel
global circle_x
global circle_y
global new_circle_pos
global diameter
global score_level
global start_time
global actual_time
global first_time_run
global run
global spike
global thrust
global obs_y_counter
global highscore

global old_time #NEW ADDED 7-7-25

tick = 0
run = True


def x_movement(old_x,old_xvel,friction,speed):
    global keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if old_xvel > 0:
            old_xvel = old_xvel * friction
        old_xvel -= speed + (score_level*0.0002)
        old_x += old_xvel
        moving = True

    else:
        if not keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            moving = False


    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if old_xvel < 0:
            old_xvel = old_xvel * friction
        old_xvel += speed + (score_level*0.0002)
        old_x += old_xvel
        moving = True

    else:
        if not keys[pygame.K_LEFT] or keys[pygame.K_a]:
            moving = False

    if moving == False:
        old_xvel = old_xvel * friction
        old_x += old_xvel

#x boundaries
    if old_x > scwid - width:
        old_x = scwid - width
        old_xvel = old_xvel*0.9

    if old_x < 0:
        old_x = 0
        old_xvel = old_xvel*0.9
        
    global x
    x = old_x
    global xvel
    xvel = old_xvel


def y_movement(old_y,old_yvel,jumpheight):
    global keys
    keys = pygame.key.get_pressed()
    
#jumping
        
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        
        old_yvel -= jumpheight*(2.3+(score_level*0.01))
        old_y += old_yvel

             
#constant falling
    if not keys[pygame.K_UP] and not keys[pygame.K_w]:
        if not old_y >= schei - 220:
            old_yvel += jumpheight*0.8
            old_y += old_yvel

#y boundaries
    if old_y >= schei - 220:
        old_y = schei - 220
        old_yvel = 0

    if old_y <= 0:
        old_y = 0
        old_yvel = 0

    if old_yvel < 0:
        old_yvel = old_yvel * 0.96
        
    global y
    y = old_y
    global yvel
    yvel = old_yvel



def set_new_circle(diameter):
    global circle_x
    global circle_y
    global new_circle_pos
    global score_level
    global start_time
    global actual_time
    global first_time_run
    global run
    global last_score
    global score_level
    
    if first_time_run == True:
        start_time = 5
        first_time_run = False
        
    start_time -= time.time() - actual_time
    actual_time = time.time()

    if round(start_time) < 0:
        my_font = pygame.font.SysFont('Cardiff', 130)
        text_surface = my_font.render("_", False, (255, 0, 0))
        win.blit(text_surface, (10,0))
        pygame.display.update()
        last_score = score_level
        pygame.mixer.Channel(2).play(fail_sound)
        pygame.mixer.Channel(2).stop()
        you_lost_screen()

        run = False
        start_time = 6

    if x+width > circle_x and x < (circle_x+diameter) and y+height > circle_y and y < (circle_y+diameter):
        start_time = 6
        first_time_run = True
    
    if x+width > circle_x and x < (circle_x+diameter) and y+height > circle_y and y < (circle_y+diameter):
        new_circle_pos = True
        #coin_collection.set_volume(1)
        #pygame.mixer.Channel(1).play(coin_collection)
        #pygame.mixer.music.stop()
    
    if new_circle_pos == True:
        
        circle_x = random.randint(0+(diameter*2),scwid-(diameter*2))
        circle_y = random.randint(0+(diameter*2),schei-(220))
        if (((abs(circle_x - x))**2) + ((abs(circle_y - y))**2))**0.5 < 300:
            while (((abs(circle_x - x))**2) + ((abs(circle_y - y))**2))**0.5 < 300:
                circle_x = random.randint(0+(diameter*2),scwid-(diameter*2))
                circle_y = random.randint(0+(diameter*2),schei-(220))   
        new_circle_pos = False
        score_level += 1


def draw_bg(bg):
    global win
    #draw the things and the outlines
    bg = pygame.transform.scale(bg,(scwid,schei))
    win.blit(bg,(0,0))

def draw_player(player):
    global win
    #rect_outline = pygame.draw.rect(win, (255,255,255), (x-outline,y-outline,width+(outline*2),height+(outline*2)))
    #rect_outline = pygame.transform.rotate(rect_outline,xvel*-1.5)

    player = pygame.transform.scale(player,(width,height))
    player = pygame.transform.rotate(player,xvel*-5)
    win.blit(player, (x,y))

def draw_coin(circle):
    global win

    circle = pygame.transform.scale(circle,(diameter,diameter))
    win.blit(circle, (circle_x,circle_y))

def draw_thrust(thrust):
    #play_thrust_sfx = True
    global keys
    global win
    global xvel
    thrust = pygame.transform.scale(thrust,(75,50))
    thrust = pygame.transform.rotate(thrust,xvel*-5)
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        #play_thrust_sfx = True
        win.blit(thrust,((x-8+(width*xvel*-0.02)),y+height))
        pygame.mixer.unpause()
        pygame.mixer.Sound.play(thrust_sound,loops=0,fade_ms=1200)
        #play_thrust_sfx = False
    else:
    #if play_thrust_sfx == False:
        #pygame.mixer.music.stop()
       pygame.mixer.Sound.fadeout(thrust_sound,400)
               

def draw_score(score):
    global win
    global last_score
    global score_level
    
    my_font = pygame.font.SysFont('Times New Roman', 60)
    text_surface = my_font.render(str(score), False, (0, 0, 0))
    win.blit(text_surface, (scwid/2,20))
    text_surface = my_font.render(str(round(start_time)), False, (0, 0, 0))
    win.blit(text_surface, (20,20))

def obstacle_y(obs_y_x, obs_y):
    global run
    global win
    global last_score
    global score_level
    
    if run == False:
        obs_y_x = -60
        obs_y = -60
        
    if x+width-15 > obs_y_x and x < (obs_y_x+190) and y-20 > obs_y and y < (obs_y+90):
        #print("collision",obs_y)
        last_score = score_level
        win.blit(spike,(obs_y_x,obs_y))
        pygame.display.update()
        you_lost_screen()
        run = False

    if run == False:
        obs_y_x = -60
        obs_y = -60

    
    win.blit(spike,(obs_y_x,obs_y))



def obstacle_x(obs_x, obs_x_y,spike,direction):
    global run
    global win
    global last_score
    global score_level
    
    if run == False:
        obs_x = -60
        obs_x_y = -60
        
    spike = pygame.transform.rotate(spike,direction)
    if x+width > obs_x and x < (obs_x+37) and y+height-20 > obs_x_y and y < (obs_x_y+190):
        #print("collision",x,y)
        last_score = score_level
        win.blit(spike,(obs_x,obs_x_y))
        pygame.display.update
        you_lost_screen()
        run = False
        
    if run == False:
        obs_x = -60
        obs_x_y = -60

    
    win.blit(spike,(obs_x,obs_x_y))

def obstacle_x_left(obs_x, obs_x_y,spike,direction):
    global run
    global win
    global last_score
    global score_level
    
    if run == False:
        obs_x = -60
        obs_x_y = -60
        
    spike = pygame.transform.rotate(spike,direction)
    if x+width-48 > obs_x and x < (obs_x+80) and y+height-20 > obs_x_y and y < (obs_x_y+190):
        #print("collision",x,y)
        last_score = score_level
        win.blit(spike,(obs_x,obs_x_y))
        pygame.display.update()
        you_lost_screen()
        run = False

    if run == False:
        obs_x = -60
        obs_x_y = -60
    
    win.blit(spike,(obs_x,obs_x_y))

def you_lost_screen():
    global win
    pygame.mixer.pause()
    my_font = pygame.font.SysFont('Times New Roman', 60)
    text_surface = my_font.render("You Lost!", False, (0, 0, 0))
    win.blit(text_surface, (scwid/2 - 100,schei/2 - 100))

    pygame.display.update()
    time.sleep(2)


def menu_screen():
    global win
    global run
    global last_score
    global highscore
    win.fill((105,105,105))

    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos[0] > scwid/2 - 100 and mouse_pos[0] < scwid/2 + 100 and mouse_pos[1] < schei/2 + 60 and mouse_pos[1] > schei/2 - 60:
        play_color = (230,230,255)
        if pygame.mouse.get_pressed()[0] == True:
            run = True
    else:
        play_color = (200,200,230)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
        run = True

    pygame.draw.rect(win, (play_color), (scwid/2 - 100,schei/2 - 60,200,120))
    
    my_font = pygame.font.SysFont('Cardiff', 80)
    text_surface = my_font.render("PLAY", False, (0, 0, 0))
    win.blit(text_surface, (scwid/2 - 70,schei/2 - 20))

    if last_score != -1:
        my_font = pygame.font.SysFont('Arial', 40)
        text_surface = my_font.render("Previous Score:", False, (0, 0, 0))
        win.blit(text_surface, (scwid/2 - 120,schei/2 + 80))
        text_surface = my_font.render(str(last_score), False, (0, 0, 0))
        win.blit(text_surface, (scwid/2 + 120,schei/2 + 80))

    if last_score > highscore:
        highscore = last_score

    my_font = pygame.font.SysFont('Arial', 40)
    text_surface = my_font.render("Highscore:", False, (0, 0, 0))
    win.blit(text_surface, (scwid/2 - 120,schei/2 + 130))
    text_surface = my_font.render(str(highscore), False, (0, 0, 0))
    win.blit(text_surface, (scwid/2 + 40,schei/2 + 130))

            

    
#GAMELOOP________________________________________




highscore = 0          
last_score = -1
mainloop = True
run = False
pressed_x = False

while mainloop:

    old_time = time.time() #NEW ADDED 7-7-25

    start_time = 5
    diameter = 40
    x = scwid/2
    y = schei-220
    width = 60
    height = 40
    xvel = 0
    yvel = 0
    circle_x = 0
    circle_y = 0
    score_level = -1
    start_time = 10
    actual_time = int(time.time())
    first_time_run = True
    obs_y_counter = -95
    obs_x_right_counter = scwid + 40
    obs_x_left_counter = -85
    spike = pygame.image.load("obs_y.png")
    spike = pygame.transform.scale(spike,(200,90))
    thrust = pygame.image.load("thrust.png")
    bg = pygame.image.load("bg.jpg")
    circle = pygame.image.load("coin.png")
    player = pygame.image.load("player.png")
    new_circle_pos = True



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
            pressed_x = True
    



    if run == False:

        menu_screen()
        

    while run == True:

        
    #x button

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
                run = False
                pressed_x = True

        keys = pygame.key.get_pressed()
        
        x_movement(x,xvel,0.98,0.015)

        y_movement(y,yvel,0.034)
        
        set_new_circle(40)

        draw_bg(bg)
        
        draw_player(player)

        draw_coin(circle)

        draw_thrust(thrust)

        draw_score(score_level)

        obs_y_counter -= (score_level*0.035) + 0.6
        if obs_y_counter < -90:
            obs_y_counter = schei - 30
            obs_y_x_new_pos = random.randint(20,scwid-180)

        obstacle_y(obs_y_x_new_pos,obs_y_counter)


        
        obs_x_right_counter += (score_level*0.035) + 0.6
        if obs_x_right_counter > scwid + 40:
            obs_x_right_counter = -40
            obs_x_y_right_new_pos = random.randint(100,schei-330)
            
        obstacle_x(obs_x_right_counter, obs_x_y_right_new_pos,spike,-90)

        obs_x_left_counter -= (score_level*0.035) + 0.6
        if obs_x_left_counter < -80:
            obs_x_left_counter = scwid + 30
            obs_x_y_left_new_pos = random.randint(100,schei-330)
            
        obstacle_x_left(obs_x_left_counter, obs_x_y_left_new_pos,spike,90)
        if tick == 100:
            tick = 0
            #print(last_score)
            #print(score_level)

        else:
            tick += 1


        
    #use this to debug
        if tick == 70:
            tick = 0

        else:
            tick += 1

     
        pygame.display.update()

    
        if time.time() - old_time < 0.005: #NEW ADDED 7-7-25

            time.sleep(abs(0.005-(time.time()-old_time)))#in ms  #NEW ADDED 7-7-25

        old_time = time.time() #NEW ADDED 7-7-25

    pygame.display.update()


pygame.quit()
