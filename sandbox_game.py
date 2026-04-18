#sandbox
import pygame, time

pygame.init()
global screen_x, win,screen_y,list_of_grains
screen_x = 600
screen_y = 900
win = pygame.display.set_mode((screen_x,screen_y))
pygame.display.set_caption("sandbox thing")

def get_rounded(value):
    return int(20 * round(float(value)/20))

def make_square(size, color, x_pos, y_pos):
    
    rect = pygame.Rect((x_pos,y_pos,size,size))
    pygame.draw.rect(win, color, rect)
    

def make_grid(num_rows):
    
    spacing = round(screen_x / num_rows)
    for y in range(0,screen_y,spacing):
        for x in range(0,screen_x,spacing):
            make_square(spacing - 3,(230,230,230), x, y)


def make_grain(x_pos,y_pos):
    global list_of_grains
    x_pos = get_rounded(x_pos)
    y_pos = get_rounded(y_pos)
    make_square(17,(200,0,0), x_pos,y_pos)
    list_of_grains.append((x_pos,y_pos))


def update_list():
    global list_of_grains
    if reverse:
        for tup in list_of_grains: # CHANGE TO REVERSED TO MAKE IT SMOOTH
            if not (tup[0], tup[1]+20) in list_of_grains:
                if tup[1]+30 < screen_y:
                    make_square(17,(230,230,230),tup[0],tup[1])
                    list_of_grains.remove(tup)
                    list_of_grains.append((tup[0], tup[1]+20))
    else:        
        for tup in reversed(list_of_grains): # CHANGE TO REVERSED TO MAKE IT SMOOTH
            if not (tup[0], tup[1]+20) in list_of_grains:
                if tup[1]+20 < screen_y:
                    make_square(17,(230,230,230),tup[0],tup[1])
                    list_of_grains.remove(tup)
                    list_of_grains.append((tup[0], tup[1]+20))
    show_pos()

def show_pos():
    for tup in list_of_grains:
            make_square(17,(200,0,0),tup[0],tup[1])
                
    


### spacing between squares - 5
### size of square - 30
### size of smaller square - 25
list_of_grains = []
run = True
first_run = True
global reverse
reverse = False
while run:
    time.sleep(0.05)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    make_grid(30)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
        first_run = False

    if keys[pygame.K_r]:
        make_grid(30)
        list_of_grains = []
        first_run = True


    if keys[pygame.K_e]:
        reverse = True
    if keys[pygame.K_t]:
        reverse = False

        
#if first_run:
    if pygame.mouse.get_pressed()[0] and not hold:
        mouse_pos = pygame.mouse.get_pos()
        if not (get_rounded(mouse_pos[0]),get_rounded(mouse_pos[1])) in list_of_grains:
            make_grain(mouse_pos[0],mouse_pos[1])
        hold = True
    hold = False

    show_pos()
#else:
    update_list()
    pygame.display.update()
    

pygame.quit()

