# new platformer.py

def main():
    if 0.003-frame_offset > 0:
        time.sleep(0.003-frame_offset)

    make_bg()

    player.movement_y(8,0.2)
    player.movement_x(0.07, 5.4)
    player.show_player()

    show_all_grounds()

    make_enemies()

    check_frame_times()

    show_all_checkpoints()

    gun.show_gun()

    make_health_bar()

    check_mouse_coords()

    pygame.display.update()


class Player:
    def __init__(self, true_x, true_y, length, width):
        self.true_x = true_x
        self.true_y = true_y
        self.length = length
        self.width = width

    def movement_x(self, speed, max_speed):
        global player_xvel, offset_x, old_xvel, gun_direction, gun_offset, old_offset_x

        if not check_bounds("left") and not check_bounds("right"):
            old_xvel = player_xvel*0.9

            old_offset_x = offset_x

            #left-right movement

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                gun_direction = "left"
                gun_offset = -35
                if player_xvel > 0:
                    player_xvel *= 0.92
                player_xvel -= speed+(frame_offset*30)

            elif keys[pygame.K_RIGHT]:
                gun_direction = "right"
                gun_offset = 35
                if player_xvel < 0:
                    player_xvel *= 0.92
                player_xvel += speed+(frame_offset*30)
            else:
                player_xvel *= 0.95

            if abs(player_xvel) > max_speed:

                if player_xvel > max_speed+(frame_offset*1116):
                    player_xvel = max_speed+(frame_offset*1116)
                if player_xvel < -max_speed-(frame_offset*1116):
                    player_xvel = -max_speed-(frame_offset*1116)

            self.true_x += player_xvel

        if check_bounds("left") and not check_bounds("down") and not check_bounds("up"):
            player_xvel = 0

            while check_bounds("left"):
                player.true_x += 1
        if check_bounds("right") and not check_bounds("down") and not check_bounds("up"):
            player_xvel = 0

            while check_bounds("right"):
                player.true_x -= 1


        offset_x = player_xvel * 3

    def movement_y(self, start_speed, speed):
        global player_yvel, holding_up, touching_ground, offset_y

        if self.true_y+offset_y < 250:
            #self.true_y += 3
            #offset_y += 1

            offset_y += abs(player_yvel)*0.9


        if self.true_y+offset_y > 450:
            #self.true_y -= 3
            #offset_y -= 1
            offset_y -= abs(player_yvel)*0.9


        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and check_bounds("down"):
            player_yvel = start_speed
            self.true_y -= 9
            touching_ground = False

        if check_bounds("down"):
            player_yvel = 0
        else:
            if not check_bounds("up"):
                player_yvel -= speed

        if player_yvel == 0 and not check_bounds("down"):
            while not check_bounds("down"):
                self.true_y += 0.5
        if player_yvel == 0 and check_bounds("down"):
            while check_bounds("down"):
                self.true_y -= 0.5
        if check_bounds("up"):
            player_yvel = 0
            while check_bounds("up"):
                self.true_y += 1

        if self.true_y > 3000:
            self.true_y = respawn_coords[1]
            self.true_x = respawn_coords[0]+SCWID/2
            offset_y = 100
            player_yvel = 0

        """
        if player.true_y-offset_y<300:
            offset_y -= 2
        if player.true_y-offset_y>650:
            offset_y += 2
        """

        self.true_y -= player_yvel

    def show_player(self):
        global offset_x, cam_y, animation_number, animation_tick, player_direction, prev_player_direction, wc_list, wc_1, wc_2, wc_3, wc_4,wc_5, max_animation_tick
        global wc_6

        prev_player_direction = player_direction

        if player_xvel >= 0:
            player_direction = "right"

        else:
            player_direction = "left"


        if player_direction != prev_player_direction:
            wc_1 = pygame.transform.flip(wc_1, True, False)
            wc_2 = pygame.transform.flip(wc_2, True, False)
            wc_3 = pygame.transform.flip(wc_3, True, False)
            wc_4 = pygame.transform.flip(wc_4, True, False)
            wc_5 = pygame.transform.flip(wc_5, True, False)
            wc_6 = pygame.transform.flip(wc_6, True, False)
            wc_list = [wc_1,wc_2,wc_3,wc_4, wc_5, wc_6]

        max_animation_tick = (5.41-abs(player_xvel))
        if max_animation_tick < 4.4-(frame_offset*1000):
            max_animation_tick = 4.4-(frame_offset*1000)




        if animation_number > len(wc_list)-1:
            animation_number = 0
        if abs(player_xvel)>0.7 and player_yvel < 1.2 and player_yvel > -1.2:
            animation_tick += 1
            if animation_tick > max_animation_tick:
                animation_tick = 1
                if player_yvel < 2:
                    animation_number += 1
            if animation_number > 3 and player_yvel > -3 and player_yvel < 1:
                animation_number = 0
        else:
            animation_number = 0
        
        if 5 <= player_yvel <= 8:
            animation_number = 5
        if 1.2 < player_yvel < 5:
            animation_number = 4

        #if player_yvel < -2:
            #animation_number = 5, where index 6 in wc_list is falling image
#     O
#    /|\
#     /\ should look like this for jumping up, and arms and legs should point down for falling

        win.blit(wc_list[animation_number], (SCWID/2+offset_x,self.true_y+offset_y))

def check_touching(obj1x, obj1xdist, obj1y, obj1ydist, obj2x, obj2xdist, obj2y, obj2ydist):
    if obj1x+obj1xdist > obj2x and obj2x+obj2xdist > obj1x and obj1y < obj2y+obj2ydist and obj2y < obj1y+obj1ydist:
        return True
    else:
        return False
        
class Ground:
    instancelist = []

    def __init__(self, x, y, length, width):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        Ground.instancelist.append(self)
    
    def show_ground(self):
        for i in range(0,self.width*TILESIZE,TILESIZE):
            for j in range(0,self.length*TILESIZE,TILESIZE):

                if i == 0:
                    this_brick = brick_list[1]
                else:
                    this_brick = brick_list[0]

                win.blit(this_brick,(self.x+j-player.true_x+SCWID+offset_x, self.y+i+offset_y))

class Moving_Platform(Ground):
    m_p_instancelist = []
    def __init__(self, x, y, length, width, tick, speed, max, dir):
        # if dir is left, tick is the distance and max is 0
        # if dir is right, tick is 0 and max is distance
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.tick = tick
        self.speed = speed
        self.max = max
        self.dir = dir
        Moving_Platform.m_p_instancelist.append(self)

    def change_tick(self):
        if self.dir == "left":
            self.x -= self.speed
            self.tick -= self.speed
            if self.tick < 0:
                self.dir = "right"
        if self.dir == "right":
            self.x += self.speed
            self.tick += self.speed
            if self.tick > self.max:
                self.dir = "left"
        
class Enemy:
    def __init__(self,x,y, length, width, yvel, speed):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.yvel = yvel
        self.speed = speed
    
    def move(self):
        global enemy_list, battery_color, battery_percent

        if not check_touching_sides_enemy(self):
            if self.x > player.true_x-SCWID/2 and not check_enemy_collision(self,"left"):
                self.x -= self.speed

            elif not check_enemy_collision(self,"right"):
                self.x += self.speed


        if check_touching_ground_enemy(self,only_down = True) or check_enemy_collision(self,"down"):
            self.yvel = 0

        if ((check_touching_ground_enemy(self,only_down = True) or check_enemy_collision(self,"down")) and not check_enemy_collision(self,"up")) and abs(self.yvel)<1:
            if random.randint(1,40) == 1 and not check_touching_player(self):
                self.yvel = 5.2
                self.y -= 5.2


        while check_touching_ground_enemy(self,only_down = True) or check_enemy_collision(self, "down"):
            self.y -= 1


        if not check_touching_ground_enemy(self,only_down=True) and not check_enemy_collision(self,"down"):
            self.yvel -= 0.1

        if self.y > 1500:
            enemy_list.remove(self)
            return
        
        while check_touching_ground_enemy(self, only_up = True):
            self.y += 15
            self.yvel = 0

        self.y -= self.yvel
        
        touching_player = False
        for enemy in enemy_list:

            if check_touching_player(enemy):
                touching_player = True
        
        
        if touching_player:
            battery_color = (150,150,30)
            battery_percent -= 0.02
             
        else:
            battery_color = (30,250,30)


        if battery_percent <= 1:
            battery_percent = 100

    def show_enemy(self):

        enemy_rect = pygame.Rect(self.x-player.true_x+SCWID+offset_x, self.y+offset_y,self.length,self.width)
        pygame.draw.rect(win,(255,0,255),enemy_rect)
  
class Enemy_Spawner:
    spawner_list = []

    def __init__(self,x,y,max_tick, enemy_tick):
        self.x = x
        self.y = y
        self.max_tick = max_tick
        self.enemy_tick = enemy_tick
        Enemy_Spawner.spawner_list.append(self)

    def show_enemies(self):
        global enemy_list
        self.enemy_tick = self.enemy_tick + 1
        if self.enemy_tick > self.max_tick:
            self.enemy_tick = 0
            if len(enemy_list)<MAX_ENEMIES:
                enemy_list.append(Enemy(self.x,self.y,30,30,0,random.randrange(6,17)/10))

class Jump_Pad:
    j_p_instancelist = []
    def __init__(self,x,y,length,width,power):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.power = power
        Jump_Pad.j_p_instancelist.append(self)

    def show_jump_pad(self):
        global player_yvel


        jump_rect = pygame.Rect(self.x-player.true_x+SCWID/2+offset_x, self.y+offset_y,self.length,self.width)
        pygame.draw.rect(win,(30,100,240),jump_rect)

        if check_touching(player.true_x,player.length,player.true_y,player.width,
                          self.x,self.length,self.y,self.width):
            player_yvel = self.power

class Checkpoint:
    checkpoint_list = []
    def __init__(self, x, y, length, width, active):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self. active = active
        Checkpoint.checkpoint_list.append(self)

    def show_checkpoint(self):
        if self.active:
            checkpoint_color = (30,240,255)
        else:
            checkpoint_color = (20,160,210)

        checkpoint_rect = pygame.Rect(self.x-player.true_x+SCWID+offset_x, self.y+offset_y,self.length,self.width)
        pygame.draw.rect(win,checkpoint_color,checkpoint_rect)

def make_enemies():
    global enemy_list
    for spawner in Enemy_Spawner.spawner_list:
        spawner.show_enemies()

    #for spawner in Enemy_Spawner.spawner_list:
        #spawner.show_enemies()

    for obj in enemy_list:
        obj.show_enemy()
        obj.move()
        if abs((player.true_x-SCWID/2)-obj.x)>700 or abs((player.true_y)-obj.y)>SCHEI-100:
            enemy_list.remove(obj)

def setup_objects():
    #global ground_1, ground_2, ground_3
    global sword, gun
    ground_1 = Ground(-300,700,30,3)
    ground_2 = Ground(480,610,4,3)
    ground_3 = Ground(700,500,7,3)
    ground_4 = Ground(600,350,5,1)
    ground_5 = Ground(-540,600,3,3)
    ground_6 = Ground(-670,500,3,3)
    ground_7 = Ground(-820,400,3,3)
    ground_8 = Ground(1100,650,10,4)
    ground_9 = Ground(1400,710,20,2)
    ground_10 = Ground(1500,500,15,1)
    ground_11 = Ground(1700,650,10,4)
    ground_12 = Ground(2600,750,7,3)
    ground_13 = Ground(2900,430,20,3)
    ground_14 = Ground(2500,290,7,3)
    ground_15 = Ground(2900,180,7,3)
    
    spawner_1 = Enemy_Spawner(400,100,100,0)
    spawner_2 = Enemy_Spawner(1600,300,60,0)
    spawner_3 = Enemy_Spawner(3300,570,120,0)
    spawner_4 = Enemy_Spawner(3400,300,50,0)

    gun = Gun()

    m_p_1 = Moving_Platform(0, 400, 10,2,0,1,200,"right")
    m_p_2 = Moving_Platform(1950,900,8,12,0,1.2,400,"right")
    m_p_3 = Moving_Platform(3200,120,2,3,0,0.8,300,"right")

    j_p_1 = Jump_Pad(3240,730,70,20,12)

    checkpoint_1 = Checkpoint(0,500,30,70,True)
    checkpoint_2 = Checkpoint(1900,350,30,70,False)

def make_bg():
    win.blit(bg,(((player.true_x+offset_x)*0.1)*-1-(SCWID/2),offset_y*0.2-500))

def show_all_grounds():
    global touching_list, check_side, bullet_list
    touching_list = []
    check_side = []
    for instance in Ground.instancelist:
        instance.show_ground()

    for m_p_instance in Moving_Platform.m_p_instancelist:
        m_p_instance.show_ground()
        m_p_instance.change_tick()

    for bul in bullet_list:
        bul.move_bullet()
        if abs(bul.x-player.true_x)>SCWID:
            bullet_list.remove(bul)

    for pad in Jump_Pad.j_p_instancelist:
        pad.show_jump_pad()

class Gun:
    def show_gun(self):
        global bullet_list, bullet_tick, holding_space, gun_direction, gun_offset

        gun_rect = pygame.Rect((gun_offset + SCWID/2+offset_x, player.true_y+20+offset_y,30,20))
        pygame.draw.rect(win,(180,130,255),gun_rect)

        keys = pygame.key.get_pressed()
        if not keys[pygame.K_SPACE]:
            holding_space = False
        if keys[pygame.K_SPACE]:
            if not holding_space:
                bullet_list.append(Bullet(player.true_x, player.true_y+20, gun_direction, 20, 10))
                holding_space = True

class Bullet:
    def __init__(self,x,y,direction, length, width):
        self.x = x
        self.y = y
        self.direction = direction
        self.length = length
        self.width = width

        if self.direction == "right":
            self.offset = 50
        else:
            self.offset = -30

        self.this_bullet = bullet
        if self.direction == "left":
            self.this_bullet = pygame.transform.flip(self.this_bullet, True, False)

    def move_bullet(self):
        global enemy_list

        if not check_touching_wall(self):
            if self.direction == "right":
                self.x += 12
            else:
                self.x -= 12


        win.blit(self.this_bullet,(self.offset+self.x-player.true_x+SCWID/2+offset_x, self.y+offset_y))

        for enemy in enemy_list:
            if check_touching(self.x, 10,self.y,10, (enemy.x+SCWID/2+offset_x)-self.offset, enemy.length, enemy.y, enemy.width):
                enemy_list.remove(enemy)
                bullet_list.remove(self)
                return

        if check_touching_wall(self):
            bullet_list.remove(self)

def check_bounds(direction, side_distance=0):
    for obj in Ground.instancelist:
        if direction == "up":
            if check_touching(obj.x+SCWID/2, obj.length*TILESIZE, obj.y, obj.width*TILESIZE,
                            player.true_x+3,player.length-6,player.true_y,4):
                return True
        if direction == "down":
            if check_touching(obj.x+SCWID/2, obj.length*TILESIZE, obj.y, obj.width*TILESIZE,
                            player.true_x+3,player.length-6,player.true_y+player.width,3):
                return True

        if direction == "left" or direction == "side":
            if check_touching(obj.x+SCWID/2, obj.length*TILESIZE, obj.y, obj.width*TILESIZE,
                            player.true_x-8-side_distance,4,player.true_y+3,player.width-6):
                return True
        if direction == "right" or direction == "side":
            if check_touching(obj.x+SCWID/2, obj.length*TILESIZE, obj.y, obj.width*TILESIZE,
                            player.true_x+player.length+4+side_distance,4,player.true_y+3,player.width-6):
                return True
            

    for obj in Moving_Platform.m_p_instancelist:
        if direction == "up":
            if check_touching(obj.x+SCWID/2, obj.length*TILESIZE, obj.y, obj.width*TILESIZE,
                            player.true_x+3,player.length-6,player.true_y,4):
                return True
        if direction == "down":
            if check_touching(obj.x+SCWID/2, obj.length*TILESIZE, obj.y, obj.width*TILESIZE,
                            player.true_x+3,player.length-6,player.true_y+player.width,3):
                return True

        if direction == "left" or direction == "side":
            if check_touching(obj.x+SCWID/2, obj.length*TILESIZE, obj.y, obj.width*TILESIZE,
                            player.true_x-8-side_distance,4,player.true_y+3,player.width-6):
                return True
        if direction == "right" or direction == "side":
            if check_touching(obj.x+SCWID/2, obj.length*TILESIZE, obj.y, obj.width*TILESIZE,
                            player.true_x+player.length+4+side_distance,4,player.true_y+3,player.width-6):
                return True
    return False

def check_touching_ground_enemy(enemy, only_down = False, only_up = False):
    for obj in Ground.instancelist:

        if check_touching(obj.x, obj.length*TILESIZE, obj.y, obj.width*TILESIZE,
                        enemy.x+3,enemy.length-6,enemy.y-8,4) and not only_down:
            return True

        if check_touching(obj.x, obj.length*TILESIZE, obj.y, obj.width*TILESIZE,
                        enemy.x+3,enemy.length-6,enemy.y+enemy.width,3) and not only_up:
            return True


    for obj in Moving_Platform.m_p_instancelist:

        if check_touching(obj.x, obj.length*TILESIZE, obj.y, obj.width*TILESIZE,
                        enemy.x+3,enemy.length-6,enemy.y,4) and not only_down:
            return True

        if check_touching(obj.x, obj.length*TILESIZE, obj.y, obj.width*TILESIZE,
                        enemy.x+3,enemy.length-6,enemy.y+player.width-20,3) and not only_up:
            return True

    return False

def check_touching_sides_enemy(enemy):

    for obj in Ground.instancelist:

        if check_touching(obj.x, obj.length*TILESIZE, obj.y, obj.width*TILESIZE,
                        enemy.x-8,4,enemy.y+3,enemy.width-6):      
            return True

        if check_touching(obj.x, obj.length*TILESIZE, obj.y, obj.width*TILESIZE,
                        enemy.x+enemy.length+4,4,enemy.y+3,enemy.width-6):
            return True
        


    for obj in Moving_Platform.m_p_instancelist:

        if check_touching(obj.x, obj.length*TILESIZE, obj.y, obj.width*TILESIZE,
                        enemy.x-8+obj.speed,4,enemy.y+3,enemy.width-6):
            return True

        if check_touching(obj.x, obj.length*TILESIZE, obj.y, obj.width*TILESIZE,
                        enemy.x+enemy.length+4-obj.speed,4,enemy.y+3,enemy.width-6):
            return True
        
        

    return False

def check_enemy_collision(self, direction):
    for enemy in enemy_list:
        if direction == "up":
            if check_touching(self.x+2,self.length-4,self.y-4,2,
                              enemy.x,enemy.length,enemy.y,enemy.width):
                return True
        if direction == "down":
            if check_touching(self.x+2,self.length-4,self.y+self.width+2,4,
                              enemy.x,enemy.length,enemy.y,enemy.width):
                return True
    
        if direction == "left":

            if check_touching(self.x-4,2,self.y+2,self.width-4,
                              enemy.x,enemy.length,enemy.y,enemy.width):
                return True
        if direction == "right":
            if check_touching(self.x+self.width+2,2,self.y+2,self.width-4,
                              enemy.x,enemy.length,enemy.y,enemy.width):
                return True
            
    return False

def check_touching_wall(self):
    for obj in Ground.instancelist:
        if check_touching(self.x-SCWID/2,self.length,self.y,self.width,
                        obj.x-55, obj.length*TILESIZE+90,obj.y,obj.width*TILESIZE):
            return True
    for obj in Moving_Platform.m_p_instancelist:
        if check_touching(self.x-SCWID/2,self.length,self.y,self.width,
                        obj.x-55, obj.length*TILESIZE+90,obj.y,obj.width*TILESIZE):
            return True
        
    return False
    
def check_touching_player(self):
    if check_touching(self.x+SCWID/2,self.length,self.y,self.width,
                      player.true_x,player.length,player.true_y,player.width):
        return True
    return False
    
def make_health_bar():
        battery_rect = pygame.Rect((SCWID-130,25,110,30))
        pygame.draw.rect(win,(10,30,20),battery_rect)
        bar_rect = pygame.Rect((SCWID-125,30,battery_percent,20))
        pygame.draw.rect(win,battery_color,bar_rect)

def check_frame_times():
    global frame_list, old_time, frame_offset

    frame_list.append(time.time()-old_time)
    old_time = time.time()

    frame_offset = (frame_list[-1] - min(frame_list))/6

def show_all_checkpoints():
    global respawn_coords
    for checkpoint in Checkpoint.checkpoint_list:
        checkpoint.show_checkpoint()
        if check_touching_player(checkpoint):
            checkpoint.active = True
            respawn_coords = (checkpoint.x+(checkpoint.length/2),checkpoint.y)
            for other_checkpoints in Checkpoint.checkpoint_list:
                if other_checkpoints != checkpoint:
                    other_checkpoints.active = False

def check_mouse_coords():
    if pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()
        print(round(mouse_pos[0]+player.true_x-SCWID+offset_x),"   ",round(mouse_pos[1]-offset_y))






import pygame,time, random

global player_xvel, player_yvel, player, win, offset_x, cam_y, holding_up, touching_ground
global bg, touching_list, check_side, wc_list, animation_tick, animation_number, player_direction
global enemy_list, sword, sc_list, sc_tick, sc_1,sc_2,sc_3,sc_4, bullet_list, bullet_tick
global holding_space, old_xvel, gun_direction, gun_offset, battery_percent, battery_color, brick
global brick_2, brick_list, offset_y, frame_list, old_time, frame_offset, respawn_coords
global old_offset_x, bullet

pygame.init()
SCWID = 1000
SCHEI = 800
TILESIZE = 30
MAX_ENEMIES = 14
run = True
player_xvel = 0
player_yvel = 0
win = pygame.display.set_mode((SCWID,SCHEI))
offset_x, cam_y = 0, SCHEI/2
old_offset_x = 0
player = Player(500,500,30,50)
holding_up = False
touching_ground = False
touching_list = []
check_side = []
animation_tick = 0
animation_number = 0
player_direction = "right"
enemy_list = []
sc_tick = 0
bullet_list = []
bullet_tick = 0
holding_space = False
old_xvel = player_xvel
gun_direction = "right"
gun_offset = 35
battery_percent = 100
battery_color = (30,250,30)
offset_y = 0
frame_list = []
old_time = time.time()
frame_offset = 0
respawn_coords = (500,500)

setup_objects()

#get files
bg = pygame.image.load("assets/art/bg.png")
bg = pygame.transform.scale(bg,(SCWID*2, SCHEI*2))
brick = pygame.image.load("assets/art/platforms/brick.png")
brick = pygame.transform.scale(brick,(TILESIZE, TILESIZE))
brick_2 = pygame.image.load("assets/art/platforms/brick_2.png")
brick_2 = pygame.transform.scale(brick_2,(TILESIZE, TILESIZE))
top_brick = pygame.image.load("assets/art/platforms/top_brick.png")
top_brick = pygame.transform.scale(top_brick,(TILESIZE,TILESIZE))
brick_list = [brick, top_brick]

wc_1 = pygame.image.load("assets/art/player/walk_cycle_1.png")
wc_1 = pygame.transform.scale(wc_1,(player.length,player.width))
wc_2 = pygame.image.load("assets/art/player/walk_cycle_2.png")
wc_2 = pygame.transform.scale(wc_2,(player.length,player.width))
wc_3 = pygame.image.load("assets/art/player/walk_cycle_3.png")
wc_3 = pygame.transform.scale(wc_3,(player.length-10,player.width))
wc_4 = pygame.image.load("assets/art/player/walk_cycle_4.png")
wc_4 = pygame.transform.scale(wc_4,(player.length,player.width))

wc_5 = pygame.image.load("assets/art/player/jump_1.png")
wc_5 = pygame.transform.scale(wc_5,(player.length-8,player.width))
wc_6 = pygame.image.load("assets/art/player/jump_transition.png")
wc_6 = pygame.transform.scale(wc_6,(player.length-5,player.width))
wc_list = [wc_1,wc_2,wc_3,wc_4, wc_5, wc_6]

bullet = pygame.image.load("assets/art/bullet.png")
bullet = pygame.transform.scale(bullet,(20, 10))


while run:

    main()
    #time.sleep(0.01)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()

#next steps:
# add a checkpoint system, so that when player falls, they will respawn at that point

# make bg a forest with trees and a ble sky
# animation for player,falling (animation speed based on xvel), enemy walk

# create own music? find some running sfx, using weapon sfx, enemy sfx
# upload to itch?find a way to distribute it to macOS