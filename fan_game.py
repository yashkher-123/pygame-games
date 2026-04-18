#somegame
import pygame,time
pygame.init()

global scwid,schei,wind_list,player_x,player_y,yvel,xvel,blue_rect_start,pause,holding,counter,fan_holding,new_level,level,end_x,end_y,blocker_list
scwid = 1200
schei = 850
win = pygame.display.set_mode((scwid,schei))


def make_player():
    player = pygame.Rect((player_x,player_y,30,30))
    pygame.draw.rect(win, (255,0,0), player)
    check_wind()
    
def check_wind():
    global player_y,yvel,xvel,player_x,prev_x,prev_y
    prev_x = player_x
    prev_y = player_y
    if not pause:
        for wind_rect in wind_list:
            if wind_rect[4] == "up":
                if check_touching(wind_rect[0],wind_rect[1],wind_rect[2],wind_rect[3],player_x,50,player_y,50):
                    
                    yvel = (player_y - wind_rect[2])
                    yvel *= 0.5

                    player_y -= yvel*0.01

            if wind_rect[4] == "right":
                if check_touching(wind_rect[0],wind_rect[1],wind_rect[2],wind_rect[3],player_x,50,player_y,50):
                    xvel = (player_x-wind_rect[1])-wind_rect[0]
                    #print(round(player_x),wind_rect[0])
                    xvel *= 0.5
                    player_x -= xvel*0.01

            if wind_rect[4] == "left":
                if check_touching(wind_rect[0],wind_rect[1],wind_rect[2],wind_rect[3],player_x,50,player_y,50):
                    xvel = wind_rect[1]-(player_x - wind_rect[0] + wind_rect[1])
                    #xvel = (50-player_x)
                    xvel *= 0.5


                    player_x += xvel*0.01

            if wind_rect[4] == "down":
                if check_touching(wind_rect[0],wind_rect[1],wind_rect[2],wind_rect[3],player_x,50,player_y,50):
                    
                    yvel = wind_rect[3] - (player_y - wind_rect[2]) - 50
                    yvel *= 0.5

                    player_y += yvel*0.01

            

def load_images():
    global left_fan,right_fan,up_fan,down_fan,blue_rect_start,rect_outline
    left_fan = pygame.image.load("fan_left_copy.png")
    left_fan = pygame.transform.scale(left_fan,(60,60))

    right_fan = pygame.image.load("fan_right_copy.png")
    right_fan = pygame.transform.scale(right_fan,(60,60))

    up_fan = pygame.image.load("fan_up_copy.png")
    up_fan = pygame.transform.scale(up_fan,(60,60))

    down_fan = pygame.image.load("fan_down_copy.png")
    down_fan = pygame.transform.scale(down_fan,(60,60))

    blue_rect_start = pygame.image.load("new_blue_rect.png").convert(24)

    rect_outline = pygame.image.load("rect_outline.png")
    rect_outline = pygame.transform.scale(rect_outline,(80,80))
    

def make_end(x,y):
    end = pygame.Rect((x,y,30,30))
    pygame.draw.rect(win, (30,200,30), end)

def make_fan(x,y,direction,length):

    make_wind(x,y,direction,length)
    if direction == "up":
        win.blit(up_fan,(x,y))

    if direction == "down":
        win.blit(down_fan,(x,y))

    if direction == "left":
        win.blit(left_fan,(x,y))

    if direction == "right":
        win.blit(right_fan,(x,y))

    

def setup_wind(opacity):
    global left_blue_rect,right_blue_rect,up_blue_rect,down_blue_rect
    
    up_blue_rect = blue_rect_start
    up_blue_rect.set_alpha(opacity)

    right_blue_rect = blue_rect_start
    right_blue_rect = pygame.transform.rotate(right_blue_rect, -90)
    right_blue_rect.set_alpha(opacity)

    left_blue_rect = blue_rect_start
    left_blue_rect = pygame.transform.rotate(left_blue_rect, 90)
    left_blue_rect.set_alpha(opacity)

    down_blue_rect = blue_rect_start
    down_blue_rect = pygame.transform.rotate(down_blue_rect, 180)
    down_blue_rect.set_alpha(opacity)

def set_wind_length(length,direction):
    global left_blue_rect,right_blue_rect,up_blue_rect,down_blue_rect
    if direction == "up":
        up_blue_rect = pygame.transform.scale(up_blue_rect,(60,length))
    if direction == "down":
        down_blue_rect = pygame.transform.scale(down_blue_rect,(60,length))

    if direction == "right":
        right_blue_rect = pygame.transform.scale(right_blue_rect,(length,60))
    if direction == "left":
        left_blue_rect = pygame.transform.scale(left_blue_rect,(length,60))

def make_wind(x,y,direction,length):
    global wind_list
    set_wind_length(length,direction)
    if direction == "up":

        win.blit(up_blue_rect,(x,y-length))
        if not (x,70,y-length,length,direction) in wind_list:
            wind_list.append((x,70,y-length,length,direction))
            
    if direction == "right":

        win.blit(right_blue_rect,(x+70,y))
        if not (x+70,length,y,70,direction) in wind_list:
            wind_list.append((x+70,length,y,70,direction))

    if direction == "left":
        
        win.blit(left_blue_rect,(x-length,y))
        if not (x-length,length,y,70,direction) in wind_list:
            wind_list.append((x-length,length,y,70,direction))

    if direction == "down":

        win.blit(down_blue_rect,(x,y+70))
        if not (x,70,y+70,length,direction) in wind_list:
            wind_list.append((x,70,y+70,length,direction))

    

def check_touching(obj1x1, obj1xdist, obj1y1, obj1ydist, obj2x1, obj2xdist, obj2y1,obj2ydist):
    if obj1x1+obj1xdist > obj2x1 and obj2x1+obj2xdist > obj1x1 and obj1y1 < obj2y1+obj2ydist and obj2y1 < obj1y1+obj1ydist:
            return True
    else:
        return False

def pause_button():
    global pause,holding
    mouse_pos = pygame.mouse.get_pos()
    
    if not pygame.mouse.get_pressed()[0] or not check_touching(mouse_pos[0],3,mouse_pos[1],3,scwid-70,40,70,40):
        holding = False
        #pausecolor = (0,0,200)

    if pause:
        pausecolor = (200,0,0)
    else:
        pausecolor = (0,0,200)


    #if check_touching(mouse_pos[0],3,mouse_pos[1],3,scwid-70,40,70,40):
        #pausecolor = (200,0,0)
    
    if pygame.mouse.get_pressed()[0] and check_touching(mouse_pos[0],3,mouse_pos[1],3,scwid-70,40,70,40) and abs(player_x-prev_x)<0.01 and abs(player_y - prev_y) < 0.01:
        if holding == False:
            if pause:
                pause = False
            else:
                pause = True
            
        holding = True

    pause_rect = pygame.Rect((scwid-60,60,30,30))
    pygame.draw.rect(win, pausecolor, pause_rect)

class Fan:
    def __init__(self,x,y,direction,length,number):
        self.x = x
        self.y = y
        self.direction = direction
        self.length = length
        self.number = number

    def show_fan(self):
        make_fan(self.x,self.y,self.direction,self.length)
        self.move_fan(8)

    def move_fan(self,total):
        global counter,fan_holding

        if pause:
            keys = pygame.key.get_pressed()
            
            if not keys[pygame.K_SPACE]:
                fan_holding = False
                
            if keys[pygame.K_SPACE]:
                if fan_holding == False:
                    counter += 1
                    
                fan_holding = True
        
            if counter == total_fans+1:
                counter = 1

            if self.number == counter:
                win.blit(rect_outline,(self.x-10,self.y-10))
                if keys[pygame.K_UP]:
                    self.remove_prev()
                    self.y -= 30
                    time.sleep(0.15)
                elif keys[pygame.K_DOWN]:
                    self.remove_prev()
                    self.y += 30
                    time.sleep(0.15)

                elif keys[pygame.K_RIGHT]:
                    self.remove_prev()
                    self.x += 30
                    time.sleep(0.15)
                elif keys[pygame.K_LEFT]:
                    self.remove_prev()
                    self.x -= 30
                    time.sleep(0.15)

                elif keys[pygame.K_w]:
                    self.remove_prev()
                    self.direction = "up"

                elif keys[pygame.K_s]:
                    self.remove_prev()
                    self.direction = "down"
                    
                elif keys[pygame.K_a]:
                    self.remove_prev()
                    self.direction = "left"

                elif keys[pygame.K_d]:
                    self.remove_prev()
                    self.direction = "right"

            
    #CHECK IF MOUSE DOWN AND TOUCHING SQUARE THEN GO TO MOUSE

    def remove_prev(self):
        global wind_list
        if self.direction == "up":
            wind_list.remove((self.x,70,self.y-self.length,self.length,self.direction))
        if self.direction == "down":
            wind_list.remove((self.x,70,self.y+70,self.length,self.direction))
        if self.direction == "right":
            wind_list.remove((self.x+70,self.length,self.y,70,self.direction))
        if self.direction == "left":
            wind_list.remove((self.x-self.length,self.length,self.y,70,self.direction))

def show_blockers(start_x,start_y):
    global pause,player_x,player_y
    for blocker in blocker_list:
        rect = pygame.Rect((blocker[0],blocker[2],blocker[1],blocker[3]))
        pygame.draw.rect(win, (40,0,0), rect)
        if check_touching(player_x,50,player_y,50,blocker[0],blocker[1],blocker[2],blocker[3]):
            pause = True
            time.sleep(1)
            player_x = start_x
            player_y = start_y
            
            

def make_level():
    global pause,new_level,level,player_x,player_y,end_x,end_y,total_fans,wind_list,blocker_list
    global fan1,fan2,fan3,fan4,fan5,fan6,fan7,fan8
    make_bg(30)
    if check_touching(player_x,50,player_y,50,end_x,50,end_y,50):
        time.sleep(1)
        new_level = True
        level += 1
        wind_list = []
        blocker_list = []
    if level == 1:
        
        if new_level:
            wind_list = []
            new_level = False
            pause = True
            end_x,end_y = 150,150
            player_x,player_y = scwid-300,schei-200
            fan1 = Fan(90,720,"up",750,1)
            fan2 = Fan(210,720,"up",750,2)
            fan3 = Fan(300,720,"up",750,3)
            total_fans = 3

        if abs(player_x-prev_x)<0.01 and abs(player_y - prev_y) < 0.01 and pause == False:
            pause = True
            player_x,player_y = scwid-300,schei-300

            
        make_end(end_x,end_y)
        #show_blockers(scwid-300,schei-200)
        fan1.show_fan()
        fan2.show_fan()
        fan3.show_fan()

    if level == 2:
        
        if new_level:
            wind_list = []
            new_level = False
            pause = True
            end_x,end_y = 150,150
            blocker_list.append((300,20,100,100))
            player_x,player_y = scwid-400,schei-400
            fan1 = Fan(100,700,"up",400,1)
            fan2 = Fan(200,700,"up",400,2)
            fan3 = Fan(300,700,"up",400,3)
            total_fans = 3

        if abs(player_x-prev_x)<0.01 and abs(player_y - prev_y) < 0.01 and pause == False:
            pause = True
            player_x,player_y = scwid-400,schei-400

            
        make_end(end_x,end_y)
        show_blockers(scwid-420,schei-420)
        fan1.show_fan()
        fan2.show_fan()
        fan3.show_fan()

    if level == 3:
        
        if new_level:
            wind_list = []
            new_level = False
            pause = True
            end_x,end_y = 550,20
            player_x,player_y = 800,700
            blocker_list.append((500,30,50,350))
            blocker_list.append((620,30,50,350))
            fan1 = Fan(100,700,"down",300,1)
            fan2 = Fan(200,700,"down",200,2)
            fan3 = Fan(300,700,"down",400,3)
            fan4 = Fan(400,700,"down",500,4)
            fan5 = Fan(500,700,"down",600,5)
            total_fans = 5

        if abs(player_x-prev_x)<0.01 and abs(player_y - prev_y) < 0.01 and pause == False:
            pause = True
            player_x,player_y = 800,700

            
        make_end(end_x,end_y)
        show_blockers(800,700)
        fan1.show_fan()
        fan2.show_fan()
        fan3.show_fan()
        fan4.show_fan()
        fan5.show_fan()

def make_bg(size):
    #spacing = round(scwid / num_rows)
    for y in range(0,schei,size):
        for x in range(0,scwid,size):
            square = pygame.Rect((x,y,size-5,size-5))
            pygame.draw.rect(win, (135,135,135), square)




"""
fan system works like (xpos,ypos,starting direction,length,fan number)
fan1 = Fan(600,600,"left",400,1)
fan2 = Fan(250,690,"up",600,2)
fan3 = Fan(180,200,"right",750,3)
fan4 = Fan(700,270,"down",500,4)
fan5 = Fan(1000,400,"left",320,5)
fan6 = Fan(850,100,"down",500,6)
fan7 = Fan(800,680,"left",400,7)
fan8 = Fan(450,760,"up",200,8) 
fan1.show_fan()
fan2.show_fan()
fan3.show_fan()
fan4.show_fan()
fan5.show_fan()
fan6.show_fan()
fan7.show_fan()
fan8.show_fan()
"""
        #NEED A SQUARE THAT OUTLINES THE SELECTED FAN

run = True
wind_list = []
player_x = 520
player_y = 600
xvel,yvel = 0,0
counter = 1
global fan1,fan2,fan3,fan4,fan5,fan6,fan7,fan8
fan1 = Fan(600,600,"left",400,1)
fan2 = Fan(250,690,"up",600,2)
fan3 = Fan(180,200,"right",750,3)
fan4 = Fan(700,270,"down",500,4)
fan5 = Fan(1000,400,"left",320,5)
fan6 = Fan(850,100,"down",500,6)
fan7 = Fan(800,680,"left",400,7)
fan8 = Fan(450,760,"up",200,8)
new_level = True
level = 1
blocker_list = []
end_x,end_y = 150,150
prev_x,prev_y = 0,0

load_images()
setup_wind(30)
pause = False
"""****MAIN***"""
while run:
    time.sleep(0.001)
    win.fill((130,130,130))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    

    make_level()

    pause_button()
    make_player()
    

    pygame.display.update()
pygame.quit()
