import pygame
import random
import wx

#initialization variables
outp= wx.App(False)
width, height= wx.GetDisplaySize()
dt = 0
trail = 20

#Place-Holder Value
forbidden_regions = pygame.Vector2 (3000,3000)

player_location = pygame.Vector2(width/2,height/2)
player_velocity = pygame.Vector2(0,0)
player_added_velocity = pygame.Vector2(0,0)

#Applies to all characters that use scrape and run
max_speed = pygame.Vector2(100,100)

#functions

#Controls Movement, entity agnostic
#FIX WITH ABS
def scrape_and_run(current_cords, current_velocity, added_velocity, forbidden_regions):
    global max_speed
    if (abs(current_velocity.x) >= 2 and player_velocity.y >= 2) and (current_velocity.x <= max_speed.x and current_velocity.y <= max_speed.y):
        current_velocity.x /= 1.1
        current_velocity.y /= 1.1
    elif current_velocity.x <= 2 and player_velocity.y <= 2:
        current_velocity.x = 0
        current_velocity.y = 0
    else:
        print ("INVALID VELOCITY ERROR")
    current_velocity.x += added_velocity.x
    current_velocity.y += added_velocity.y
    if pygame.Vector2((current_cords.x + current_velocity.x),(current_cords.y + current_velocity.y)) != forbidden_regions:
        current_cords.x += current_velocity.x
        current_cords.y += current_velocity.y
    elif pygame.Vector2((current_cords.x + current_velocity.x),(current_cords.y + current_velocity.y))== forbidden_regions:
        print("Out of Bounds")
    else:
        print("UNKNOWN MOVEMENT ERROR")
    return current_cords.x,current_cords.y

#Draws player and keeps track of stats
def driver():
    global player_location
    global player_velocity
    global player_added_velocity
    global trail
    global forbidden_regions

    pygame.draw.circle(screen, "red", player_location, 40)

    player_location = pygame.Vector2(scrape_and_run(player_location, player_velocity, player_added_velocity, forbidden_regions))

    #for i in range(trail):
    #    pygame.draw.circle(screen, "red", ((player_location.x-player_velocity.x*i),(player_location.y-player_velocity.y*i)), 20)


#initialization

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

#Main Loop

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Reset Velocity Addition

    player_added_velocity = pygame.Vector2(0, 0)

    #Controls

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_added_velocity.y -= 200 * dt
    if keys[pygame.K_s]:
        player_added_velocity.y += 200 * dt
    if keys[pygame.K_a]:
        player_added_velocity.x -= 200 * dt
    if keys[pygame.K_d]:
        player_added_velocity.x += 200 * dt
    screen.fill("blue")
    driver()

    pygame.display.flip()
    dt = clock.tick(60) / 1000