import pygame
#import pygame_widgets
import random
import wx
from pygame import Vector2, Rect

# To Do

# Rounds of enemies
# Upgrades after each round that change stats around
# More enemy AI types which can be specified with an augment on enemy_init
# Make the enemies and bullets actually do things

#Reminder for when you get back, you were working on hitboxes for bullets around line 297

# initialization variables
outp = wx.App(False)
width, height = wx.GetDisplaySize()
dt = 0
player_location = Vector2(width / 2, height / 2)
player_velocity = Vector2(0, 0)
player_added_velocity = Vector2(0, 0)
stability = 100
move_speed = 55
base_move_speed = move_speed
playable_region = Rect(0, 0, width, height)
enemy_count = 0
enemies = {
}
bullet_count = 0
bullets = {
}
shooting = False
last_velocity = Vector2(1,1)
shoot_cd = 0
enemy_ai = True

# Quick Settings
trail = 23
min_speed = Vector2(.1, .1)  # Applies to all characters that use scrape and run
max_speed = Vector2(100, 100)  # Applies to all characters that use scrape and run
stability_mode = False
stability_impact = 90 # changes how much stability affects gameplay, further from 0 = less impact
stability_floor = -300
#gravity_factor = 1 Abandoned by its God (me)
d_color = "crimson"
energy = 400.0
bullet_bounces = 4
bullet_speed = .2
shoot_cd_len = 3
energy_regen = 2
max_energy = 400
enemy_base_health = 1

#Level Up Card Options
upgradable_stats = {
    "Max Energy" : max_energy,
    "Bullet Bounces" : bullet_bounces,
    "Cooldown" : shoot_cd_len,
    "Color" : d_color
}

# functions

# Stat bar
def stat_bar():
    global stability
    global player_velocity

# Controls Movement, entity agnostic
def scrape_and_run(current_cords, current_velocity, added_velocity, subject, trail_color, bounces):
    global max_speed, min_speed, stability, trail, last_velocity

    hit_wall = False

    # Tracks last velocity w movement
    if subject == "driver" and (abs(current_velocity.x ) > 0 or abs(current_velocity.y) > 0):
        last_velocity = current_velocity.copy()

    # Applies Velocity
    current_velocity.x += added_velocity.x
    current_velocity.y += added_velocity.y

    # exists to fix up and left directions from reversing direction when triggering maximum speed
    positive_dirx = 1
    positive_diry = 1
    if abs(current_velocity.x) != current_velocity.x:
        positive_dirx = -1
    if abs(current_velocity.y) != current_velocity.y:
        positive_diry = -1

    # Checks if target is going fast enough to be considered moving, and applies movement decay
    if abs(current_velocity.x) >= min_speed.x:
        current_velocity.x /= 1.05
    if abs(current_velocity.y) >= min_speed.y:
        current_velocity.y /= 1.05

    # Checks if target is moving above maximum speed, and sets them to max speed if so
    if subject == "bullet":
        max_speed /= 2
    if abs(current_velocity.x) >= max_speed.x:
        current_velocity.x = max_speed.x * positive_dirx
    if abs(current_velocity.y) >= max_speed.y:
        current_velocity.y = max_speed.y * positive_diry
    if subject == "bullet":
        max_speed *= 2

    # Stops Target when going below minimum speed
    if abs(current_velocity.x) <= min_speed.x and abs(current_velocity.y) <= min_speed.y:
        current_velocity.x = 0
        current_velocity.y = 0

    # Gravity: abandoned feature
    #if gravity == True:
    #    if gravity_dir == "down":
    #        current_velocity.y += gravity_factor

    # if not playable_region.collidepoint(current_cords.x+current_velocity.x,current_cords.y+current_velocity.y):
    if current_cords.x + current_velocity.x >= width or current_cords.x + current_velocity.x <= 0:
        #print("Something Hit Something")
        hit_wall = True
        current_velocity.x *= -1
        current_cords.x += current_velocity.x
        current_cords.y += current_velocity.y
        if subject == "driver" and stability_mode:
            stability -= 50
    elif current_cords.y + current_velocity.y >= height or current_cords.y + current_velocity.y <= 0:
        #print("Something Hit Something")
        hit_wall = True
        current_velocity.y *= -1
        current_cords.x += current_velocity.x
        current_cords.y += current_velocity.y
        if subject == "driver" and stability_mode:
            stability -= 50
    elif playable_region.collidepoint(current_cords.x + current_velocity.x, current_cords.y + current_velocity.y):
        current_cords.x += current_velocity.x
        current_cords.y += current_velocity.y
    else:
        print("Something Hit Something")

    #if not playable_region.collidepoint(current_cords.x, current_cords.y):
    #    print("Out of Bounds")

    # Draws Trail
    if subject == "bullet":
        size = 10
    else:
        size = 28
    trail_length = Vector2(0, 0)
    if (current_cords.x - current_velocity.x * .5 + current_velocity.y - current_velocity.y * .5) >= 10:
        trail_length.x = current_velocity.x# * .25
        trail_length.y = current_velocity.y# * .25
    else:
        trail_length = current_velocity
    if abs(current_velocity.x) + abs(current_velocity.y) >= 5:
        for f in range(trail):
            pygame.draw.circle(screen, trail_color, ((random.randint(-3, 3) + current_cords.x - trail_length.x * f * .25),
                                               (random.randint(-3, 3) + current_cords.y - trail_length.y * f * .25)),
                               (size - f))
    if subject == "bullet" and hit_wall == True:
        return current_cords.x, current_cords.y, bounces-1
    elif subject == "bullet":
        return current_cords.x, current_cords.y, bounces

    #if subject == "enemy":

    return current_cords.x, current_cords.y, last_velocity

# Draws player and runs scrape and run for player
def driver():
    global player_location
    global player_velocity
    global player_added_velocity
    global trail
    global d_color

    # Scrape and run for player
    scrape_and_run(player_location, player_velocity, player_added_velocity, "driver", d_color, 0)

    # Trail (moved to scrape_and_run so it would apply to enemies)
    #trail_length = pygame.Vector2(0, 0)
    #if (player_velocity.x * .5 + player_location.y - player_velocity.y * .5) >= 10:
    #    trail_length.x = player_velocity.x * .25
    #    trail_length.y = player_velocity.y * .25
    #else:
    #    trail_length = player_velocity
    #if abs(player_velocity.x) + abs(player_velocity.y) >= 5:
    #    for i in range(trail):
    #        pygame.draw.circle(screen, "red", ((random.randint(-3, 3) + player_location.x - trail_length.x * i * .5),
    #                                           (random.randint(-3, 3) + player_location.y - trail_length.y * i * .5)),
    #                          (28 - i))

    # Player draw
    pygame.draw.circle(screen, "red", player_location, 30)

# Spawns Enemies, this could just be a lamda, but those scare me
def enemy_init():
    global width, height, enemies, enemy_count

    # Spawnable Range
    elocation=Vector2(random.uniform(width*.99,width*.01),random.uniform(height*.99,height*.01))

    # Color randomizer
    colors = [
        "blue",
        "cadetblue",
        "aquamarine4",
        "blue4",
        "cornflowerblue",
        "cadetblue2",
        "cyan4",
        "darkslategray4",
        "darkslategrey",
        "deepskyblue4"
    ]
    color = random.choice(colors)
    health = enemy_base_health
    h_box = Rect(0,0,35,35)

    enemies[enemy_count] = {
        "cord" : elocation,
        "velocity" : Vector2(0,0),
        "color" : color,
        "health" : health,
        "hitbox" : h_box
    }
    enemy_count += 1

def enemy():
    global enemies, enemy_count, player_location, enemy_ai
    for this_enemy, data in list(enemies.items()):
        cord = data["cord"]
        e_velocity = data["velocity"]
        color = data["color"]
        health = data["health"]
        hitbox = data["hitbox"]

        #enemy AI

        hitbox.center = cord

        # Makes enemies less "effective", higher b = slower reaction time
        active = random.randint(1, 10)

        evelocity_add = Vector2(0, 0)
        if enemy_ai and active == 1:
            evelocity_add = Vector2(0,0)
            if cord.x <= player_location.x:
                evelocity_add.x += move_speed*.1
            else:
                evelocity_add.x -= move_speed*.1
            if cord.y <= player_location.y:
                evelocity_add.y += move_speed*.1
            else:
                evelocity_add.y -= move_speed*.1
        scrape_and_run(cord, e_velocity, evelocity_add, "enemy", color, 0)

        # Registers Hits
        if len(bullets) > 0:
            for i in bullets.values():
                if pygame.Rect.colliderect(hitbox, i["hitbox"]):
                    health -= 1
                    print (health)
        if health < 1:
            del enemies[this_enemy]
            enemy_count -= 1

        # Render Enemies
        pygame.draw.circle(screen, color, cord, 30)

def shoot():
    global bullets, bullet_count, player_location, player_velocity, bullet_bounces, last_velocity, bullet_speed

    # Spawnable Range
    blocation=player_location.copy()
    bvelocity=last_velocity.copy()

    # Color randomizer
    colors = [
        "blue",
        "cadetblue",
        "aquamarine4",
        "blue4",
        "cornflowerblue",
        "cadetblue2",
        "cyan4",
        "darkslategray4",
        "darkslategrey",
        "deepskyblue4"
    ]
    color = random.choice(colors)

    hitbox = Rect(0, 0, 15, 15)

    bullets[bullet_count] = {
        "cord" : blocation,
        "velocity" : bvelocity,
        "color" : color,
        "bounces" : bullet_bounces,
        "hitbox" : hitbox
    }
    bullet_count += 1


def bullet():
    global bullets, bullet_count
    for this_bullet, data in list(bullets.items()):
        cord = data["cord"]
        b_velocity = data["velocity"]
        color = data["color"]
        bounces = data["bounces"]
        hitbox = data["hitbox"]

        b_add_vel = Vector2(b_velocity.x*bullet_speed,b_velocity.y*bullet_speed)

        bdata = scrape_and_run(cord, b_velocity, b_add_vel, "bullet", color, bounces)
        data["bounces"] = bdata[2]

        # Moves hitbox
        hitbox.center = cord

        # Render Enemies
        pygame.draw.circle(screen, color, cord, 0)

        # Shoot the Bullets
        if data["bounces"] < 1:
            del bullets[this_bullet]
            bullet_count -= 1

# initialization
pygame.init()
pygame.display.set_caption('Driver')
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

# Intro Screen

# TBD

#test enemy
enemy_init()

# Game Loop
while running:
    # poll for events

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            shooting = True
        if event.type == pygame.MOUSEBUTTONUP:
            shooting = False


    # Reset Velocity Addition
    player_added_velocity = Vector2(0, 0)

    # Applies low stability movement debuff
    if stability_mode:
        # Sets minimum stability
        if stability < stability_floor:
            stability = stability_floor
        if stability != 0:

            # Formula makes it more likely to trigger at lower stability, and more intense, auto adjusts itself to the stability floor, so no need to re-configure it
            drunk_trigger = random.randint(0, int(-stability_floor - abs(stability + (stability_floor // stability_impact) - stability_floor / 3))) <= 10 and stability < 0

            # Formula makes it more likely to trigger at lower stability, and more intense, auto adjusts itself to the stability floor, so no need to re-configure it
            if drunk_trigger:
                player_added_velocity.y += random.uniform(abs(2 * stability / stability_impact),
                                                      -abs(2 * stability / stability_impact))
                player_added_velocity.x += random.uniform(abs(2 * stability / stability_impact),
                                                      -abs(2 * stability / stability_impact))

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_added_velocity.y -= move_speed * dt
    if keys[pygame.K_s]:
        player_added_velocity.y += move_speed * dt
    if keys[pygame.K_a]:
        player_added_velocity.x -= move_speed * dt
    if keys[pygame.K_d]:
        player_added_velocity.x += move_speed * dt

    # Dev Hotkeys
    if keys[pygame.K_SPACE]:
        player_velocity.x = (1.2 + random.uniform(50, -50))
        player_velocity.y = (1.2 + random.uniform(50, -50))
        stability += 1
    if keys[pygame.K_e]:
        player_velocity.x *= 1.4
        player_velocity.y *= 1.4
    if keys[pygame.K_v]:
        enemy_init()
        for i in enemies:
            print (enemies)
    # background
    screen.fill("indianred4")

    # Shooting/Energy
    if shooting == True and energy > 0:
        if shoot_cd >= shoot_cd_len:
            shoot()
            energy -= 1
            shoot_cd = 0
        else:
            shoot_cd += 1
    elif shooting == False and energy < max_energy:
        energy += energy_regen
        shoot_cd += 1
    elif shooting:
        print("Out of Energy")
    else:
        shoot_cd += 1

    # The Enemy
    enemy()

    # The Bullets
    bullet()

    # Player is You
    driver()

    # misc
    pygame.display.flip()
    dt = clock.tick(60) / 1000

print("The Game has ended")