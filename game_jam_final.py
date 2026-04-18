# game jam

def main():
    if menu:
        make_menu()
    if show_instructions:
        make_instructions()
    if not menu and not show_instructions:
        time.sleep(time_delay)
        make_bg()
        make_player()
        player_movement(0.15,5,0.96,player_size,0.7)
        flashlight()
        setup_lvl()
        show_lives()

def make_player():
    global player
    if fl_on:
        player.set_alpha(255)
    else:
        player.set_alpha(60)
    win.blit(player,(player_x,player_y))

def ending(x,y):
    global level, change_level, fl_on, end_square
    if fl_on:
        win.blit(end_square,(x,y))
        if end_square.get_alpha() <= 250:
            end_square.set_alpha(end_square.get_alpha() + 4)
    else:
        end_square.set_alpha(10)

    if check_touching(x,60,y,60,player_x,player_size,player_y,player_size):
        if change_level:
            level += 1
            fl_on = True
            make_bg()
            make_player()
            end_square. set_alpha(255)
            pygame.mixer.Channel(7).play(pygame.mixer.Sound('sounds/level_up_sfx.mp3'))
            win.blit(end_square,(x,y))
            pygame.display.update()
            time.sleep(1)
            reset_lvl()
            change_level = False

        change_level = True
    else:
        change_level = False

def player_movement(speed,speed_limit,friction,size,bounce):
    global player_x,player_y,player_xvel,player_yvel

    #basic movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_xvel -= speed
    elif keys[pygame.K_RIGHT]:
        player_xvel += speed
    else:
        player_xvel *= friction

    if keys[pygame.K_UP]:
        player_yvel -= speed
    elif keys[pygame.K_DOWN]:
        player_yvel += speed
    else:
        player_yvel *= friction

    #upper speed limit    
    if player_xvel>speed_limit:
        player_xvel = speed_limit
    if player_xvel<-1*speed_limit:
        player_xvel = -1*speed_limit
    if player_yvel>speed_limit:
        player_yvel = speed_limit
    if player_yvel <-1*speed_limit:
        player_yvel = -1*speed_limit

    #check bounds
    if player_x <= 0:
        player_xvel *= -bounce
        player_x = 1
    if player_x >= scwid-size:
        player_xvel *= -bounce
        player_x = scwid-size-1

    if player_y <= 0:
        player_yvel *= -bounce
        player_y = 1
    if player_y >= schei-size:
        player_yvel *= -bounce
        player_y = schei-size-1

    # check if xvel/yvel is too small
    if abs(player_xvel) <= speed-0.01:
        player_xvel = 0
    if abs(player_yvel) <= speed-0.01:
        player_yvel = 0

    # change player pos
    player_x += player_xvel
    player_y += player_yvel

class Battery:
    def __init__(self,file,x,y, length, width, collected): # collected should always be false
        self.file = file
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.collected = collected
        self.file = pygame.transform.scale(self.file,(self.length,self.width))
    
    def show_battery(self):
        global percent_tick, battery_percent, battery_empty
        if not self.collected and fl_on:
            win.blit(self.file,(self.x,self.y))
        if check_touching(self.x,self.length,self.y,self.width,player_x,player_size,player_y,player_size):
            percent_tick = 85
            pygame.mixer.Channel(6).play(pygame.mixer.Sound('sounds/battery_collect_sfx.mp3'))
            battery_empty = False
            battery_percent = pygame.Rect((scwid-124,45,85,40))
            pygame.draw.rect(win,(255,255,0),battery_percent)
            self.collected = True
            self.x = -300

class Obstacle:
    def __init__(self,file,x,y,length,width): 
        self.file = file
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.file = pygame.transform.scale(self.file,(self.length,self.width))

    def show_obs(self):
        global lives, setup_lvl_var, fl_on
        if fl_on:
            win.blit(self.file,(self.x,self.y))
            if self.file.get_alpha() <= 250:
                self.file.set_alpha(self.file.get_alpha() + 4)
        else:
            self.file.set_alpha(10)
        if check_touching(self.x,self.length,self.y,self.width,player_x,player_size,player_y,player_size):
            lives -= 1
            fl_on = True
            make_bg()
            self.file.set_alpha(255)
            win.blit(self.file,(self.x,self.y))
            make_player()
            pygame.mixer.Channel(4).play(pygame.mixer.Sound('sounds/death_sfx.mp3'))
            
            pygame.display.update()
            time.sleep(1)
            reset_lvl()

class Enemy(Obstacle):
    def __init__(self,file,x,y,length,width,tick,increment,max,start_dir,direction):
        self.file = file # start_dir should be "up", "down", "left", or "right"
        self.x = x #        diredction should be "up/down" or "left/right"
        self.y = y #        tick should be 0 or max depending on direction, increment should be around 1
        self.length = length # max should be the distance it travels
        self.width = width
        self.tick = tick
        self.increment = increment
        self.max = max
        self.start_dir = start_dir
        self.direction = direction
        self.file = pygame.transform.scale(self.file,(self.length,self.width))
    
    def change_tick(self):
        if self.direction == "up/down":
            if self.start_dir == "up":
                self.tick += self.increment
                self.y -= self.increment
                if self.tick > self.max:
                    self.start_dir = "down"
            if self.start_dir == "down":
                self.tick -= self.increment
                self.y += self.increment
                if self.tick < 0:
                    self.start_dir = "up"

        if self.direction == "left/right":
            if self.start_dir == "right":
                self.tick += self.increment
                self.x += self.increment
                if self.tick > self.max:
                    self.start_dir = "left"
            if self.start_dir == "left":
                self.tick -= self.increment
                self.x -= self.increment
                if self.tick < 0:
                    self.start_dir = "right"

def setup_lvl_once():
    global setup_lvl_var, enemy_1, obs_1, enemy_2, battery_1, enemy_3, enemy_4, percent_tick, battery_empty, obs_2, obs_3, obs_4, obs_5
    global obs_6
    # (self,file,x,y,length,width)
    # (self, file, x, y, length, width, tick, increment, max, start_dir, direction)
    # (self,file,x,y, length, width, collected)
    
    if setup_lvl_var:
        percent_tick += (85-percent_tick)*0.25
        battery_empty = False
        if level == 1:
            obs_1 = Obstacle(pygame.image.load("art/obs_square.png"),300,400,200,200)
            enemy_1 = Enemy(pygame.image.load("art/enemy.png"),500,100,150,150,0,1.4,200,"right","left/right")

            setup_lvl_var = False
            
        if level == 2:
            obs_1 = Obstacle(pygame.image.load("art/obs_square.png"),scwid/2 - 100,schei/2 - 100,250,250)
            enemy_1 = Enemy(pygame.image.load("art/enemy.png"),700,100,50,50,500,3,500,"down","up/down")
            enemy_2 = Enemy(pygame.image.load("art/enemy.png"),100,600,50,50,0,3,450,"up","up/down")
            battery_1 = Battery(pygame.image.load("art/battery_collectible.png"), 50,schei-120,30,80,False)

            setup_lvl_var = False

        if level == 3:
            obs_1 = Obstacle(pygame.image.load("art/obs_square.png"),200,100,600,600)
            enemy_1 = Enemy(pygame.image.load("art/enemy.png"),scwid/2-100,10,90,90,700,7,700,"down","up/down")
            enemy_4 = Enemy(pygame.image.load("art/enemy.png"),10,schei/2-50,90,90,0,10,900,"right","left/right")
            battery_1 = Battery(pygame.image.load("art/battery_collectible.png"), scwid/2, schei-90,30,80,False)

            setup_lvl_var = False

        if level == 4:
            enemy_4 = Enemy(pygame.image.load("art/enemy.png"),650,40,100,100,500,5,500,"left","left/right")
            enemy_1 = Enemy(pygame.image.load("art/enemy.png"),150,200,100,100,0,6,600,"right","left/right")
            enemy_2 = Enemy(pygame.image.load("art/enemy.png"),750,450,100,100,600,7,600,"left","left/right")
            enemy_3= Enemy(pygame.image.load("art/enemy.png"),150,600,100,100,0,8,600,"right","left/right")
            battery_1 = Battery(pygame.image.load("art/battery_collectible.png"), 450, 420,30,80,False)
            obs_1 = Obstacle(pygame.image.load("art/obs_square.png"),800,600,100,100)

            setup_lvl_var = False

        if level == 5:
            
            enemy_1 = Enemy(pygame.image.load("art/enemy.png"),180,180,100,100,580,5,620,"down","up/down")
            enemy_2 = Enemy(pygame.image.load("art/enemy.png"),490,620,150,150,0,5,620,"up","up/down")
            enemy_3 = Enemy(pygame.image.load("art/enemy.png"),830,180,100,100,580,5,620,"down","up/down")
            enemy_4 = Enemy(pygame.image.load("art/enemy.png"),20,350,125,125,0,8,800,"right","left/right")
            battery_1 = Battery(pygame.image.load("art/battery_collectible.png"), 600, 400,30,80,False)

            setup_lvl_var = False

        if level == 6:
            enemy_1 = Enemy(pygame.image.load("art/enemy.png"),150,50,140,140,0,9,650,"right","left/right")
            enemy_2 = Enemy(pygame.image.load("art/enemy.png"),800,640,140,140,650,9,650,"left","left/right")
            enemy_3 = Enemy(pygame.image.load("art/enemy.png"),100,650,140,140,0,7,380,"up","up/down")
            enemy_4 = Enemy(pygame.image.load("art/enemy.png"),800,200,140,140,400,7,400,"down","up/down")
            battery_1 = Battery(pygame.image.load("art/battery_collectible.png"), scwid/2-15, schei/2-40,30,80,False)
            obs_1 = Obstacle(pygame.image.load("art/obs_square.png"),20,schei/2-50,100,100)
            obs_2 = Obstacle(pygame.image.load("art/obs_square.png"),scwid-120,schei/2-50,100,100)
            obs_3 = Obstacle(pygame.image.load("art/obs_square.png"),scwid/2-50,20,100,100)
            obs_4 = Obstacle(pygame.image.load("art/obs_square.png"),scwid/2-50,schei-120,100,100)

            setup_lvl_var = False

        if level == 7:
            obs_1 = Obstacle(pygame.image.load("art/obs_square.png"),140,30,350,350)
            obs_2 = Obstacle(pygame.image.load("art/obs_square.png"),530,30,300,300)
            obs_3 = Obstacle(pygame.image.load("art/obs_square.png"),620,400,300,300)
            obs_4 = Obstacle(pygame.image.load("art/obs_square.png"),10,520,200,200)
            obs_5 = Obstacle(pygame.image.load("art/obs_square.png"),240,460,270,270)
            obs_6 = Obstacle(pygame.image.load("art/obs_square.png"),650,705,90,90)
            enemy_4 = Enemy(pygame.image.load("art/enemy.png"),350,0,100,100,700,4,700,"down","up/down")
            enemy_2 = Enemy(pygame.image.load("art/enemy.png"),900,600,100,100,900,6,900,"left","left/right")
            battery_1 = Battery(pygame.image.load("art/battery_collectible.png"), scwid-40, schei-90,30,80,False)

            setup_lvl_var = False

        if level == 8:
            obs_1 = Obstacle(pygame.image.load("art/obs_square.png"),380,20,150,150)
            obs_2 = Obstacle(pygame.image.load("art/obs_square.png"),380,190,540,540)
            enemy_2 = Enemy(pygame.image.load("art/enemy.png"),0,180,100,100,0,9,900,"right","left/right")
            enemy_3 = Enemy(pygame.image.load("art/enemy.png"),0,500,100,100,0,7,900,"right","left/right")
            enemy_1 = Enemy(pygame.image.load("art/enemy.png"),200,20,100,100,680,9,680,"down","up/down")

            setup_lvl_var = False

def setup_lvl():
    global level, obs_1, enemy_1, enemy_2, battery_1, enemy_3, enemy_4, obs_2, obs_3, obs_4, obs_5, obs_6
    if level == 1:
        setup_lvl_once()

        obs_1.show_obs()
        enemy_1.show_obs()
        enemy_1.change_tick()
        ending(scwid-120,schei-150)

    if level == 2:
        setup_lvl_once() 
        
        obs_1.show_obs()
        enemy_1.show_obs()
        enemy_1.change_tick()
        enemy_2.show_obs()
        enemy_2.change_tick()
        battery_1.show_battery()
        ending(scwid-120,schei-150)

    if level == 3:
        setup_lvl_once()

        obs_1.show_obs()
        enemy_4.show_obs()
        enemy_4.change_tick()
        enemy_1.show_obs()
        enemy_1.change_tick()
        battery_1.show_battery()
        ending(scwid-80,schei-80)

    if level == 4:
        setup_lvl_once()

        obs_1.show_obs()
        enemy_1.show_obs()
        enemy_1.change_tick()
        enemy_2.show_obs()
        enemy_2.change_tick()
        enemy_3.show_obs()
        enemy_3.change_tick()
        enemy_4.show_obs()
        enemy_4.change_tick()
        battery_1.show_battery()
        ending(scwid-100,190)

    if level == 5:
        setup_lvl_once()
        

        enemy_1.show_obs()
        enemy_1.change_tick()
        enemy_2.show_obs()
        enemy_2.change_tick()
        enemy_3.show_obs()
        enemy_3.change_tick()
        enemy_4.show_obs()
        enemy_4.change_tick()
        battery_1.show_battery()
        ending(scwid-80,schei-80)
    
    if level == 6:
        setup_lvl_once()

        obs_1.show_obs()
        obs_2.show_obs()
        obs_3.show_obs()
        obs_4.show_obs()
        enemy_1.show_obs()
        enemy_1.change_tick()
        enemy_2.show_obs()
        enemy_2.change_tick()
        enemy_3.show_obs()
        enemy_3.change_tick()
        enemy_4.show_obs()
        enemy_4.change_tick()
        battery_1.show_battery()
        ending(scwid-80,schei-80)

    if level == 7:
        setup_lvl_once()

        obs_1.show_obs()
        obs_2.show_obs()
        obs_3.show_obs()
        obs_4.show_obs()
        obs_5.show_obs()
        obs_6.show_obs()
        enemy_4.show_obs()
        enemy_4.change_tick()
        enemy_2.show_obs()
        enemy_2.change_tick()
        battery_1.show_battery()
        ending(10,schei-70)

    if level == 8:
        setup_lvl_once()

        obs_1.show_obs()
        obs_2.show_obs()
        enemy_1.show_obs()
        enemy_1.change_tick()
        enemy_2.show_obs()
        enemy_2.change_tick()
        enemy_3.show_obs()
        enemy_3.change_tick()
        ending(-200,-200)

        make_cpu(590,75)

def flashlight():
    global fl_on, bg_col, battery_percent, battery_0, flashlight_time
    flashlight_time += 1
    if flashlight_time > 100000:
        flashlight_time = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and percent_tick>3:
        if flashlight_time > 30 and not battery_empty:
            pygame.mixer.Channel(4).play(pygame.mixer.Sound('sounds/light_switch_sfx.mp3'))
            fl_on = True
    else:
        fl_on = False

    if change_level:
        fl_on = True

    if fl_on:
        flashlight_time = 0
        
        bg_col = (190,190,190)

    else:
        bg_col = (40,40,40)

    win.blit(battery_0,(scwid-130,40))

    battery_percent = pygame.Rect((scwid-111,53,return_length(),40))
    pygame.draw.rect(win,(255,255,0),battery_percent)

    if battery_empty:
        out_of_battery()

def return_length():
    global percent_tick, battery_empty
    if fl_on:
        percent_tick -= 0.15 # normally should be 0.15
        if percent_tick > 3:
            battery_empty = False
    if percent_tick <= 3:
        battery_empty = True
    return round(percent_tick)

def setup_player(size): # not used in mainloop
    global player
    player = pygame.image.load("art/player.png")
    player = pygame.transform.scale(player,(size,size))

def check_touching(obj1x, obj1xdist, obj1y, obj1ydist, obj2x, obj2xdist, obj2y, obj2ydist):
    if obj1x+obj1xdist > obj2x and obj2x+obj2xdist > obj1x and obj1y < obj2y+obj2ydist and obj2y < obj1y+obj1ydist:
        return True
    else:
        return False

def reset_lvl():
    global player_x, player_y, player_xvel, player_yvel, setup_lvl_var
    if lives != 0:
        time.sleep(1)
        player_x, player_y , player_xvel, player_yvel = 60,60,0,0
        setup_lvl_var = True

def make_menu():
    global menu, show_instructions, lives, player_x, player_y, player_xvel, player_yvel, level, percent_tick, setup_lvl_var
    win.blit(menu_bg,(-50,-50))
    win.blit(play,(50,450))
    #if lives == 0:
        #no_lives = pygame.font.SysFont("Times New Roman", 30)
        #no_lives_surface = no_lives.render("Out of lives. You lost.", False, (255, 0, 0))
        #win.blit(no_lives_surface, (300,300))

    mouse_pos = pygame.mouse.get_pos()
    if check_touching(mouse_pos[0],2,mouse_pos[1],2,50,330,450,150):
        if pygame.mouse.get_pressed()[0]:
            pygame.mixer.Channel(3).play(pygame.mixer.Sound('sounds/tick_sfx.mp3'))
            lives = 5
            level = 1
            percent_tick = 85
            player_x, player_y , player_xvel, player_yvel = 60,60,0,0
            setup_lvl_var = True
            menu = False
            setup_lvl_once()
        else:
            play.set_alpha(180)
    else:
        play.set_alpha(225)

    win.blit(instructions,(600,450))
    if check_touching(mouse_pos[0],2,mouse_pos[1],2,600,390,450,120):
        if pygame.mouse.get_pressed()[0]:
            pygame.mixer.Channel(3).play(pygame.mixer.Sound('sounds/tick_sfx.mp3'))
            show_instructions = True
            menu = False
        else:
            instructions.set_alpha(180)
    else:
        instructions.set_alpha(225)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        lives = 5
        level = 1
        percent_tick = 85
        player_x, player_y , player_xvel, player_yvel = 60,60,0,0
        menu = False
        setup_lvl_var = True
        setup_lvl_once()
        show_instructions = False
    if keys[pygame.K_m]:
        menu = True
        show_instructions = False

def make_instructions():
    global menu, show_instructions
    win.blit(instructions_page,(-50,-50))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        menu = False
        show_instructions = False
    if keys[pygame.K_m]:
        menu = True
        show_instructions = False
    
def make_bg():
    global light_bg, time_delay
    if fl_on:
        time_delay = 0.004
        light_bg.set_alpha(255)
        win.blit(light_bg,(-15,-15))
        #win.fill((190,190,190))
    else:
        time_delay = 0.004
        win.fill((40,40,40))
        light_bg.set_alpha(70)
        win.blit(light_bg,(-15,-15))

def out_of_battery():
    global percent_tick, lives, battery_empty
    my_font = pygame.font.SysFont('Times New Roman', 22)
    text_surface = my_font.render('Press [r] to reset the battery to full. This will cost a life.', False, (255, 0, 0))
    win.blit(text_surface, (scwid/2-300,30))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        percent_tick = 85
        lives -= 1
        battery_empty = False

def show_lives():
    global lives, show_instructions, menu
    my_font = pygame.font.SysFont('Times New Roman', 31)
    text_surface = my_font.render(f"Lives: {lives}", False, (0, 135, 100))
    win.blit(text_surface, (scwid-120,100))
    text_surface = my_font.render(f"Level: {level}", False, (0, 135, 100))
    win.blit(text_surface, (scwid-120,140))
    if lives == 0:
        my_font = pygame.font.SysFont('Times New Roman', 28)
        text_surface = my_font.render("Lives: 0", False, (0, 135, 100))
        win.blit(text_surface, (scwid-120,100))

        no_lives = pygame.font.SysFont("Times New Roman", 40)
        no_lives_surface = no_lives.render("Out of lives. You lose.", False, (255, 0, 0))
        win.blit(no_lives_surface, (300,300))
        pygame.display.update()

        time.sleep(3)
        menu = True
        show_instructions = False

def make_cpu(x,y):
    global cpu_image, fl_on, menu, show_instructions
    if fl_on:
        win.blit(cpu_image,(x,y))
        if cpu_image.get_alpha() <= 250:
            cpu_image.set_alpha(cpu_image.get_alpha() + 4)
    else:
        cpu_image.set_alpha(10)

    if check_touching(x,100,y,100,player_x,player_size,player_y,player_size):
        
        pygame.mixer.Channel(2).play(pygame.mixer.Sound('sounds/victory_sfx.mp3'))
        pygame.mixer.Channel(2).set_volume(1)

        fl_on = True
        make_bg()
        cpu_image.set_alpha(255)
        win.blit(cpu_image,(x,y))
        make_player()
        pygame.display.update()
        time.sleep(1)

        my_font = pygame.font.SysFont('Calibri', 31)
        text_surface = my_font.render("Shutting down CPU...", False, (0, 100, 40))
        win.blit(text_surface, (scwid/2-100,schei/2))
        pygame.display.update()

        time.sleep(3)

        fl_on = False
        make_bg()
        time.sleep(0.5)
        my_font = pygame.font.SysFont('Calibri', 31)
        text_surface = my_font.render("Shut down successfully!", False, (0, 255, 60))
        win.blit(text_surface, (scwid/2-300,schei/2))

        my_font = pygame.font.SysFont('Calibri', 31)
        text_surface = my_font.render("Returning to main menu...", False, (0, 255, 60))
        win.blit(text_surface, (scwid/2-300,schei/2+90))
        pygame.display.update()

        time.sleep(3)
        
        menu = True
        show_instructions = False
        
        time.sleep(0.3)

    


# ======================= start of program ===============================


import pygame, time
pygame.init()
pygame.mixer.init()


global scwid, schei, win, player_x, player_y, player_xvel, player_yvel, fl_on, bg_col
global battery_0, battery_percent, percent_tick, level, run, menu, menu_bg, play, instructions
global instructions_page, show_instructions, player, battery_empty, lives, time_delay, cpu_image
global setup_lvl_var, flashlight_time, change_level, player_size, battery_collectible, end_square


scwid = 1000
schei = 800
run = True
player_x = 60
player_y = 60
player_xvel = 0
player_yvel = 0
fl_on = False
bg_col = (40,40,40)
percent_tick = 85
level = 1
menu = True
show_instructions = False
setup_lvl_var = True
flashlight_time = 0
change_level = False
player_size = 50
battery_percent = pygame.Rect((scwid-124,45,85,40))
battery_empty = False
lives = 5
fl_on = False
time_delay = 0.01


# load image files
battery_0 = pygame.image.load("art/battery_0_copy.png")
battery_0 = pygame.transform.scale(battery_0,(130,65))
battery_percent = pygame.Rect((player_x,player_y,85,40))
menu_bg = pygame.image.load("art/menu_bg.png")
menu_bg = pygame.transform.scale(menu_bg,(scwid+100,schei+100))
play = pygame.image.load("art/play.png")
play = pygame.transform.scale(play,(330,150))
instructions = pygame.image.load("art/instructions.png")
instructions = pygame.transform.scale(instructions,(390,120))
instructions_page = pygame.image.load("art/intro_pg.png")
instructions_page = pygame.transform.scale(instructions_page,(scwid+100,schei+100))
battery_collectible = pygame.image.load("art/battery_collectible.png")
battery_collectible = pygame.transform.scale(battery_collectible,( 50,150))
end_square = pygame.image.load("art/ending.png")
end_square = pygame.transform.scale(end_square,(65,65))
light_bg = pygame.image.load("art/light_bg.png")
light_bg = pygame.transform.scale(light_bg,(scwid+30,schei+30))
cpu_image = pygame.image.load("art/cpu_image.png")
cpu_image = pygame.transform.scale(cpu_image,(100,100))
end_screen = pygame.image.load("art/end_screen.png")
end_screen = pygame.transform.scale(end_screen,(scwid,schei))


# load sound files
pygame.mixer.music.load("sounds/bg_music.mp3")
pygame.mixer.music.set_volume(0.2)
# pygame.mixer.Channel(4).play(pygame.mixer.Sound('filename.mp3')) # make sure to use an unused channel


pygame.display.set_caption("Switch")
win = pygame.display.set_mode((scwid,schei))
pygame.font.init()

setup_player(player_size)
pygame.mixer.music.play(20,-1,300)
while run:
    
    main()
    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            win.blit(end_screen,(0,0))
            pygame.display.update()
            time.sleep(0.15)

            run = False

pygame.quit()
