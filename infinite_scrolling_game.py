#new scrolling
import pygame,time,random
pygame.init()

global scwid,schei,player_y,cam_x,cam_y,yvel,holding,player,bg,xvel,level,jumpheight,jh_tick,game_run,player_height,platform_list,plat_dir
player = pygame.image.load("player2.png")
bg = pygame.image.load("bg.png")
portal = pygame.image.load("portal.png")
highjump = pygame.image.load("JumpHigher.png")
squarespike = pygame.image.load("squarespike.png")
start_screen = pygame.image.load("start_screen.png")
#coin = pygame.image.load("coin.png")
player = pygame.transform.scale(player,(70,50))
portal = pygame.transform.scale(portal,(50,50))
highjump = pygame.transform.scale(highjump,(50,50))
squarespike = pygame.transform.scale(squarespike,(120,120))
#coin = pygame.transform.scale(coin,(30,30))

scwid = 700
schei = 900
win = pygame.display.set_mode((scwid,schei))
start_screen = pygame.transform.scale(start_screen,(scwid,schei))
bg = pygame.transform.scale(bg,(7000*2,9000*2))

def x_change_player():
    global cam_x,cam_y,xvel
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and not return_left_bounds(3,):
        if xvel < 0:
            xvel *= 0.9
        if  xvel<1 and xvel>-1:
            xvel = 2
        xvel += 0.07
 
    elif keys[pygame.K_RIGHT] and not return_right_bounds(3,):
        if xvel > 0:
            xvel *= 0.9
        if  xvel<1 and xvel>-1:
            xvel = -2
        xvel -= 0.07
    else:
        xvel *= 0.85
    cam_x += xvel

    if return_left_bounds(3) and not return_lower_bounds(5):
        cam_x -= 7
    
    if return_right_bounds(3) and not return_lower_bounds(5):
        cam_x += 7

    if xvel > 6.5:
        xvel = 6.5
    if xvel < -6.5:
        xvel = -6.5
        

def y_change_player():
    global player_y,yvel,holding,cam_y,jumpheight,jh_tick,game_run,level

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and return_lower_bounds(yvel):
        yvel = -1*jumpheight
    if return_lower_bounds(6) and not keys[pygame.K_UP]:
        yvel = 0
        if return_lower_bounds(yvel):
                player_y -= yvel + 2.7
    else:
        if not return_upper_bounds(yvel):
            yvel += 0.7
    if not return_upper_bounds(-1*yvel):
        player_y += yvel
    if return_upper_bounds(-1*yvel):
        player_y -= yvel - 9
        yvel = 0

    if player_y < 200:
        player_y += 3
        cam_y += 3

    player_y += 2
    cam_y +=2
    
    if yvel > 70:
        time.sleep(0.5)
        game_run = False
        level = 1
        reset()

    if jh_tick <= 0:
        jumpheight = 16

    if jh_tick > 0:
        jh_tick -= 1
        jumpheight = 18

    if player_y + yvel + 70 > schei:
        reset()
        
def make_platform(x,y,leng,wid):
    
    rect = pygame.Rect((x,y,leng,wid))
    pygame.draw.rect(win, (0,200,200), rect)

def make_portal(x,y):
    win.blit(portal,(x,y))
    check_object("portal",x,50,y,50)

def make_highjump(x,y):
    win.blit(highjump,(x,y))
    check_object("jumpheight",x,50,y,50)

def make_squarespike(x,y):
    win.blit(squarespike,(x,y))
    check_object("squarespike",x,120,y,70)

def make_ms(x,y):
    win.blit(squarespike,(x,y))

#def make_coin(x,y):
    #win.blit(coin,(x,y))

def return_lower_bounds(offset):
    global player_y
    for x in range(0,75,5):
        if pygame.Surface.get_at(win,(round(scwid/2)+x, round(player_y+50+offset)))[:3] == (0,200,200):
            return True
    return False


def return_left_bounds(offset):

    for x in range(0,55,5):
        if pygame.Surface.get_at(win,(round(scwid/2)-offset, round(player_y+x)))[:3] == (0,200,200):
            return True
    return False

    
def return_right_bounds(offset):
    
    for x in range(0,55,5):
        if pygame.Surface.get_at(win,(round(scwid/2)+70+offset, round(player_y+x)))[:3] == (0,200,200):
            return True
    return False

def return_upper_bounds(offset):
    global player_y
    for x in range(0,75,5):
        if pygame.Surface.get_at(win,(round(scwid/2)+x, round(player_y-offset)))[:3] == (0,200,200):
            return True

    return False

def check_touching(obj1x1, obj1xdist, obj1y1, obj1ydist, obj2x1, obj2xdist, obj2y1,obj2ydist):
    if obj1x1+obj1xdist > obj2x1 and obj2x1+obj2xdist > obj1x1 and obj1y1 < obj2y1+obj2ydist and obj2y1 < obj1y1+obj1ydist:
            return True
    else:
        return False

def reset():
    global cam_y,cam_x,player_y,yvel_xvel,jh_tick,platform_list
    yvel = 0
    xvel = 0
    jh_tick = 0
    player_y = schei/2+100
    cam_y = schei/2+100
    cam_x = scwid/2
    platform_list = [(0,100)]

class Moving_Spike:


    def __init__(self,ms_tick_x, ms_tick_y,spike_x,spike_y,go_back,starting_tick_x,starting_tick_y):
        self.starting_tick_y = starting_tick_y
        self.starting_tick_x = starting_tick_x
        self.ms_tick_x = ms_tick_x
        self.ms_tick_y = ms_tick_y
        self.go_back = go_back
        self.spike_x = spike_x
        self.spike_y = spike_y

    def  set_spike(self):

        make_ms(cam_x+self.spike_x+self.ms_tick_x, cam_y+self.spike_y+self.ms_tick_y)
        check_object("squarespike",cam_x+self.spike_x+self.ms_tick_x,120,cam_y+self.spike_y+self.ms_tick_y,70)

    def change_x(self):
        if not self.go_back and self.ms_tick_x > 0:
            self.ms_tick_x -= 4

        if self.ms_tick_x == 0:
            self.ms_tick_x += 4
            self.go_back = True

        if self.go_back and self.ms_tick_x < self.starting_tick_x:
            self.ms_tick_x += 4

        if self.ms_tick_x == self.starting_tick_x:
            self.ms_tick_x -= 4
            self.go_back = False

    def change_y(self):
        if not self.go_back and self.ms_tick_y > 0:
            self.ms_tick_y -= 4

        if self.ms_tick_y == 0:
            self.ms_tick_y += 4
            self.go_back = True

        if self.go_back and self.ms_tick_y < self.starting_tick_y:
            self.ms_tick_y += 4

        if self.ms_tick_y == self.starting_tick_y:
            self.ms_tick_y -= 4
            self.go_back = False


    

def check_object(obj, x_pos, obj_leng, y_pos, obj_wid):
    global jh_tick,jumpheight,level,game_run
    
    if obj == "jumpheight":
            if check_touching(scwid/2,70,player_y,50, x_pos, obj_leng, y_pos, obj_wid):
                jumpheight = 15
                jh_tick = 300

    if obj == "portal":
         if check_touching(scwid/2,70,player_y,50, x_pos, obj_leng, y_pos, obj_wid):
            level += 1
            time.sleep(0.5)
            reset()

    if obj == "squarespike":
        if check_touching(scwid/2,70,player_y,50, x_pos, obj_leng, y_pos, obj_wid):
            time.sleep(0.5)
            game_run = False
            level = 1
            reset()

################
def draw_level():
    global level,jumpheight,jh_tick_player_height,platform_list


    for platform in platform_list:
        make_platform(cam_x+platform[0],cam_y+platform[1],150,30)
    if cam_y > platform_list[len(platform_list)-1][1]*-1:
        make_new_platform()


def make_new_platform():
    global platform_list,plat_dir
    last_platform = platform_list[len(platform_list)-1]
    
    if plat_dir == "left" and random.randint(1,2) == 1:
        plat_dir = "right"
    if plat_dir == "right" and random.randint(1,2) == 1:
        plat_dir = "left"

        
    if plat_dir == "left":
        platform_list.append((last_platform[0]+random.randint(-240,-180),last_platform[1]+random.randint(-160,-130)))

    if plat_dir == "right":
        platform_list.append((last_platform[0]+random.randint(180,240),last_platform[1]+random.randint(-160,-130)))
        

level = 3
yvel = 0
xvel = 0
player_y = schei/2+100
cam_y = schei/2+100
cam_x = scwid/2
jumpheight = 16
jh_tick = 0
platform_list = [(0,100)]
player_height = 0
plat_dir = "left"
new_level_run = False
run = True
game_run = False
old_time = time.time() # ADDED 7-7-25


lvl_2_spike_y = Moving_Spike(0,200,-300,-100,False,0,200)

while run:
    time.sleep(0.004)
    #win.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if not game_run:
        win.blit(start_screen,(0,0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]  or keys[pygame.K_SPACE]:
            game_run = True

    else:
        win.blit(bg, (cam_x*0.31-5000,cam_y*0.31-12000))
        win.blit(player, (scwid/2,player_y))

        draw_level()

        x_change_player()
        y_change_player()

    if time.time()-old_time < 0.02: # ADDED 7-7-25
        time.sleep(0.02-(time.time()-old_time))   # ADDED 7-7-25
    old_time = time.time()       # ADDED 7-7-25
      
    pygame.display.update()
pygame.quit()
