import pygame
#import pygame_widgets
import random
import wx

#test stuff

#initialization variables
outp= wx.App(False)
width, height= wx.GetDisplaySize()
dt = 0
player_location = pygame.Vector2(width/2,height/2)
player_velocity = pygame.Vector2(0,0)
player_added_velocity = pygame.Vector2(0,0)
stability = 100
move_speed = 55
base_move_speed = move_speed

#Quick Settings
trail = 20000
min_speed = pygame.Vector2(.1,.1) #Applies to all characters that use scrape and run
max_speed = pygame.Vector2(100,100) #Applies to all characters that use scrape and run
stability_mode = False
#changes how much stability affects gameplay, further from 0 = less impact 
stability_impact = 90 
stability_floor = -300
gravity_factor = 1

#Place-Holder Value
forbidden_regions = pygame.Vector2 (3000,3000)

playable_region = pygame.Rect(0, 0, width, height)

#functions

#Stat bar
def stat_bar():
    global stability
    global player_velocity

#Controls Movement, entity agnostic
def scrape_and_run(current_cords, current_velocity, added_velocity, subject, gravity_dir, gravity):
    global max_speed
    global min_speed
    global stability

    # Applies Velocity
    current_velocity.x += added_velocity.x
    current_velocity.y += added_velocity.y

    #exists to fix up and left directions from reversing direction when triggering maximum speed
    positive_dirx = 1
    positive_diry = 1
    if abs(current_velocity.x) != current_velocity.x:
        positive_dirx = -1
    if abs(current_velocity.y) != current_velocity.y:
        positive_diry = -1

    #Checks if target is going fast enough to be considered moving, and applies movement decay
    if  abs(current_velocity.x) >= min_speed.x:
        current_velocity.x /= 1.05
    if  abs(player_velocity.y) >= min_speed.y:
        current_velocity.y /= 1.05

    #Checks if target is moving above maximum speed, and sets them to max speed if so
    if abs(current_velocity.x) >= max_speed.x:
        current_velocity.x = max_speed.x * positive_dirx
    if abs(current_velocity.y) >= max_speed.y:
        current_velocity.y = max_speed.y * positive_diry

    #Stops Target when going below minimum speed
    if abs(current_velocity.x) <= min_speed.x:
        current_velocity.x = 0
    if abs(current_velocity.y) <= min_speed.y:
        current_velocity.y = 0
    
    #Gravity
    if gravity == True:
        if gravity_dir == "down":
            current_velocity.y+=gravity_factor

    #if not playable_region.collidepoint(current_cords.x+current_velocity.x,current_cords.y+current_velocity.y):
    if current_cords.x+current_velocity.x >= width or current_cords.x+current_velocity.x <= 0:
        print("Out of Bounds")
        current_velocity.x *= -1
        current_cords.x += current_velocity.x
        current_cords.y += current_velocity.y
        if subject == "driver" and stability_mode:
            stability -= 50
    elif current_cords.y+current_velocity.y >= height or current_cords.y+current_velocity.y <= 0:
        print("Out of Bounds")
        current_velocity.y *= -1
        current_cords.x += current_velocity.x
        current_cords.y += current_velocity.y
        if subject == "driver" and stability_mode:
            stability -= 50
    elif playable_region.collidepoint(current_cords.x+current_velocity.x,current_cords.y+current_velocity.y):
        current_cords.x += current_velocity.x
        current_cords.y += current_velocity.y
    else:
        print("UNKNOWN MOVEMENT ERROR")

    if not playable_region.collidepoint(current_cords.x, current_cords.y):
        print("Out of Bounds")
        
    return current_cords.x,current_cords.y

#Draws player and runs scrape and run for player
def driver():
    global player_location
    global player_velocity
    global player_added_velocity
    global trail

    #Scrape and run for player
    player_location = pygame.Vector2(scrape_and_run(player_location, player_velocity, player_added_velocity, "driver", "down", False))

    #Trail
    trail_length = pygame.Vector2(0,0)
    if (player_velocity.x*.5 + player_location.y-player_velocity.y*.5) >= 10:
        trail_length.x = player_velocity.x*.25
        trail_length.y = player_velocity.y*.25
    else:
        trail_length = player_velocity
    if abs(player_velocity.x)+abs(player_velocity.y) >=5:
        for i in range(trail):
            pygame.draw.circle(screen, "red", ((random.randint(-3,3)+player_location.x-trail_length.x*i*.5),(random.randint(-3,3)+player_location.y-trail_length.y*i*.5)), (28-i))

    #Player draw
    pygame.draw.circle(screen, "red", player_location, 30)

#Controls the evil squares
def enemy():
    pass

#initialization
pygame.init()
pygame.display.set_caption('Driver')
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

#Test Stuff

#Intro Screen
#TBD

#Main Loop
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Reset Velocity Addition
    player_added_velocity = pygame.Vector2(0, 0)

    #Sets minimum stability
    if stability < stability_floor:
        stability = stability_floor
    
    #Formula makes it more likely to trigger at lower stability, and more intense, auto adjusts itself to the stability floor, so no need to re-configure it
    drunk_trigger = random.randint(0,int(-stability_floor-abs(stability+(stability_floor//stability_impact)-stability_floor/3))) <= 10 and stability < 0

    #Applies low stability movement debuff
    if stability != 0:
        #Formula makes it more likely to trigger at lower stability, and more intense, auto adjusts itself to the stability floor, so no need to re-configure it
        if drunk_trigger:
            player_added_velocity.y += random.uniform(abs(2*stability/stability_impact),-abs(2*stability/stability_impact))
            player_added_velocity.x += random.uniform(abs(2*stability/stability_impact),-abs(2*stability/stability_impact))

    #Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_added_velocity.y -= move_speed * dt
    if keys[pygame.K_s]:
        player_added_velocity.y += move_speed * dt
    if keys[pygame.K_a]:
        player_added_velocity.x -= move_speed * dt
    if keys[pygame.K_d]:
        player_added_velocity.x += move_speed * dt
    if keys[pygame.K_SPACE]:
        player_velocity.x = (1.2 + random.uniform(50,-50))
        player_velocity.y = (1.2 + random.uniform(50,-50))
        stability += 1
    if keys[pygame.K_e]:
        player_velocity.x *= 1.4
        player_velocity.y *= 1.4

    #background
    screen.fill("blue")

    #Player
    driver()

    #misc
    pygame.display.flip()
    dt = clock.tick(60) / 1000


print ("The Game has ended")