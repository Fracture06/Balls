import pygame
#import pygame_widgets
import random
from pygame import Vector2, Rect, draw

pygame.init()
width, height = 1920,1080
screen = pygame.display.set_mode((width, height))

# To Do

# Rounds of enemies DONE :3

# Upgrades after each round with upgrade options DONE :3

# More enemy AI types which can be specified with an augment on enemy_init DONE :3

# Make the enemies and bullets actually do things (partially done, bullets kill enemies) DONE :3

# Make it so enemies do not spawn on player Naw, good enough, we got healing in the game now with vamperism, it's not that deep DONE :3

# Perks EX: Vampire DONE :3

# make bullets despawn upon hitting enemies DONE :3

# Add Wall Classifications, on second thought, what would I even do with these? DONE :3

# Make the game look pretty

# Revamp Start Menu

# Add Tutorial Video

# Homing Bullet Perk, Health Perk

# initialization variables
dt = 0
shields = False
shield_chance = 10
vamperism_proc_chance = 0
dabloons = 0
omni_discount = 0
dash_discount = 0
health_regen = 0
damage_buff = 0
omnishot = False
vamperism = False
fired_bullets = 0
player_location = Vector2(width / 2, height / 2)
player_velocity = Vector2(0, 0)
player_added_velocity = Vector2(0, 0)
#stability = 100
move_speed = 40
base_move_speed = move_speed
playable_region = Rect(0, 0, width, height)
enemy_count = 0
enemies = {
}
bullet_count = 0
bullets = {
}
last_velocity = Vector2(1,1)
shoot_cd = 0
enemy_ai = True
pygame.mixer.init()
current_wave = 0
player = "alive"
max_hp = 400
player_hp = max_hp
player_hbox = Rect(0,0,35,35)
dashing = False
kills = 0
direction = Vector2(1,0)
overall_speed = 1
level = 0
all_mode = False
level_select = False
can_dash = False
level_option = "null"
game_state = "menu"
current_upgrades = []
total_level_up_options = ["Super Speed", "Bouncy Bullets", "Bullet Velocity",
                          "Omni Shot", "Fire Rate", "Dash", "Vamperism",
                          "Bullet Pierce", "Bonus Options!", "Energize",
                          "More Damage", "Shields", "Super Vitality"]#, "Bullet Homing"]
buttons = {
}
button_count = 0
directions = {
    "left" : Vector2(-1,0),
    "right" : Vector2(1,0),
    "up" : Vector2(0,-1),
    "down" : Vector2(0,1),
    "left_up" : Vector2(-1,-1).normalize(),
    "left_down" : Vector2(-1,1).normalize(),
    "right_up" : Vector2(1,-1).normalize(),
    "right_down" : Vector2(1,1,).normalize(),
    "all" : Vector2(0,0)
}
using_energy = False

# Quick Settings
trail = 40
min_speed = Vector2(.1, .1)  # Applies to all characters that use scrape and run
max_speed = Vector2(100, 100)  # Applies to all characters that use scrape and run

# Both Stability mode and Gravity have been removed for being "stupid and boring"

#stability_mode = False
#stability_impact = 90 # changes how much stability affects gameplay, further from 0 = less impact
#stability_floor = -300
#gravity_factor = 1 Abandoned by its God (me)

d_color = "crimson"
energy = 400.0
bullet_bounces = 1
bullet_speed = .5
shoot_cd_len = 12
energy_regen = 2
max_energy = 400
enemy_base_health = 1
pygame.mixer.music.load("Thundersnail.mp3")
lvl_threshold = 3
enemy_ai_level = 10
bullet_pierce = 1
upgrade_option_amount = 3

pygame.mixer.music.play(-1,0.0)

# functions

# Button Creater
def button_init(bx, by, wide, high, press_function, text = "Place holder", remove_on_press = False, clear_on_press = False):
    global buttons, button_count

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
    button_dim = Rect(bx, by, wide, high)

    buttons[len(buttons)] = {
        "color" : color,
        "button size" : button_dim,
        "press function" : press_function,
        "text" : text,
        "remove on press" : remove_on_press,
        "clear on press" : clear_on_press
    }

    button_count += 1

# Button Code
def button():
    global buttons, mouse, game_state
    for current_button, data in buttons.copy().items():
        button_size = data["button size"]
        color = data["color"]
        press_func = data["press function"]
        text = data["text"]
        remove = data["remove on press"]
        clear = data["clear on press"]

        if button_size.x <= mouse[0] <= button_size.width+button_size.x and button_size.y <= mouse[1] <= button_size.height+button_size.y:
            pygame.draw.rect(screen, color, button_size)
            text_surface = font.render(text, True, "white")
            screen.blit(text_surface, button_size.topleft)
            if pygame.mouse.get_pressed()[0]:
                if press_func == "spawn enemy":
                    enemy_init("basic")
                elif press_func == "start":
                    game_state = "game"
                elif press_func in total_level_up_options:
                    level_up_options(press_func)
                elif press_func == "Start Dev Mode":
                    global max_hp, player_hp, max_energy, energy, move_speed, bullet_bounces, shoot_cd_len, energy_regen, bullet_speed, omnishot, can_dash, vamperism
                    game_state = "game"
                    max_hp = 1000
                    player_hp = max_hp
                    max_energy = 1000
                    energy = max_energy
                    move_speed = 80
                    bullet_bounces = 5
                    shoot_cd_len = 1
                    energy_regen = 10
                    bullet_speed = 1.5
                    omnishot = True
                    can_dash = True
                    vamperism = True
                else:
                    print("Unknown Button Error, skipping...")
                if remove and not clear:
                    del buttons[current_button]
                elif clear:
                    buttons.clear()
        else:
            pygame.draw.rect(screen, color, button_size)
            text_surface = font.render(text, True, "white")
            screen.blit(text_surface, button_size.topleft)

# The UI
def ui():
    energy_bar = Rect(10,10,energy,40)
    draw.rect(screen, "slategray", Rect(0,0,(max_energy+20), 60))
    draw.rect(screen, "gray17", Rect(10, 10, max_energy, 40))
    draw.rect(screen, "dodgerblue", energy_bar)
    health_bar = Rect(10, 60, player_hp, 40)
    draw.rect(screen, "slategray", Rect(0, 50, (max_hp + 20), 60))
    draw.rect(screen, "gray17", Rect(10, 60, max_hp, 40))
    draw.rect(screen, "crimson", health_bar)

# Controls Movement, entity agnostic
def scrape_and_run(current_cords, current_velocity, added_velocity, subject, trail_color, bounces, shape = "circle", size = 28):
    global max_speed, min_speed, trail, last_velocity

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
        #if subject == "driver" and stability_mode:
        #    stability -= 50
    elif current_cords.y + current_velocity.y >= height or current_cords.y + current_velocity.y <= 0:
        #print("Something Hit Something")
        hit_wall = True
        current_velocity.y *= -1
        current_cords.x += current_velocity.x
        current_cords.y += current_velocity.y
        #if subject == "driver" and stability_mode:
        #    stability -= 50
    elif playable_region.collidepoint(current_cords.x + current_velocity.x, current_cords.y + current_velocity.y):
        current_cords.x += current_velocity.x
        current_cords.y += current_velocity.y
    else:
        print("Something Hit Something")

    #if not playable_region.collidepoint(current_cords.x, current_cords.y):
    #    print("Out of Bounds")

    # Draws Trail
    trail_length = Vector2(0, 0)
    if (current_cords.x - current_velocity.x * .5 + current_velocity.y - current_velocity.y * .5) >= 10:
        trail_length.x = current_velocity.x# * .25
        trail_length.y = current_velocity.y# * .25
    else:
        trail_length = current_velocity
    if abs(current_velocity.x) + abs(current_velocity.y) >= 5:
        for f in range(trail):
            if shape == "circle":
                draw.circle(screen, trail_color, ((random.randint(-3, 3) + current_cords.x - trail_length.x * f * .25),
                                                   (random.randint(-3, 3) + current_cords.y - trail_length.y * f * .25)),
                                   (size - f))
            elif shape == "rect":
                draw.rect(screen, trail_color, Rect((random.randint(-3, 3) + current_cords.x - trail_length.x * f * .25),
                                                   (random.randint(-3, 3) + current_cords.y - trail_length.y * f * .25),
                                                   (size - f), (size - f)))
    if subject == "bullet" and hit_wall == True:
        return current_cords.x, current_cords.y, bounces-1
    elif subject == "bullet":
        return current_cords.x, current_cords.y, bounces

    #if subject == "enemy":

    return current_cords.x, current_cords.y, last_velocity

# Draws player and runs scrape and run for player
def driver():
    global player_location, shields, player_velocity, player_added_velocity, trail, d_color, player_hp, player_hbox, enemy_count, dashing, player, kills, overall_speed, direction

    overall_speed = abs(player_velocity.x)+abs(player_velocity.y)+1
    # Scrape and run for player
    scrape_and_run(player_location, player_velocity, player_added_velocity, "driver", d_color, 0)

    # Player draw
    draw.circle(screen, d_color, player_location, 30)

    player_hbox.center = player_location

    if len(enemies) > 0:
        for data in enemies.values():
            if pygame.Rect.colliderect(player_hbox, data["hitbox"]) and dashing == False:
                if shields == False:
                    player_hp -= 100
                    data["health"] = 0
                    print("You were Hit!")
                else:
                    if random.randint(1, shield_chance) == 1:
                        data["health"] = 0
                        print("You were Hit, but your shield blocked it!")
                    else:
                        player_hp -= 100
                        data["health"] = 0
                        print("You were Hit!")
            elif pygame.Rect.colliderect(player_hbox, data["hitbox"]) and dashing == True:
                data["health"] = 0
                print ("Melee Kill!")
                kills += 1

    if player_hp <= 0:
        player = "dead"

# Spawns Enemies, this could just be a lamda, but those scare me
def enemy_init(enemy_type):
    global width, height, enemies, enemy_count

    # Spawnable Range
    elocation=Vector2(random.uniform(width*.8,width*.01),random.uniform(height*.99,height*.01))

    # Color randomizer
    if enemy_type == "basic":
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
        health = enemy_base_health*2
        h_box = Rect(0,0,35,35)
    elif enemy_type == "Tank":
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
        health = enemy_base_health*3
        h_box = Rect(0,0,50,50)
    elif enemy_type == "Super Speed Snorkler":
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
    else:
        print("Unknown Enemy Type, Defaulting to Basic")
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
        "hitbox" : h_box,
        "type" : enemy_type
    }
    enemy_count += 1

# Runs the enemies
def enemy():
    global enemies, enemy_count, player_location, enemy_ai, kills, enemy_ai_level, player_hp
    for this_enemy, data in list(enemies.items()):
        cord = data["cord"]
        e_velocity = data["velocity"]
        color = data["color"]
        health = data["health"]
        hitbox = data["hitbox"]
        type = data["type"]

        #enemy AI

        hitbox.center = cord

        shape = "circle"

        # Makes enemies less "effective", higher b = slower reaction time
        active = random.randint(1, int(enemy_ai_level)*2)
        hold = enemy_ai_level
        if type == "Super Speed Snorkler":
            enemy_ai_level = 1
        evelocity_add = Vector2(0, 0)
        if enemy_ai and active == 1:
            evelocity_add = Vector2(0,0)
            if cord.x <= player_location.x:
                evelocity_add.x += move_speed*.05
            else:
                evelocity_add.x -= move_speed*.05
            if cord.y <= player_location.y:
                evelocity_add.y += move_speed*.05
            else:
                evelocity_add.y -= move_speed*.05
            if type == "Super Speed Snorkler":
                evelocity_add *= 2

        if type == "tank":
            shape = "rect"
            size = 609
        elif type == "basic":
            shape = "circle"
            size = 28
        elif type == "Super Speed Snorkler":
            shape = "circle"
            size = 20
        else:
            shape = "circle"
            size = 28

        scrape_and_run(cord, e_velocity, evelocity_add, "enemy", color, 0, shape, size)

        enemy_ai_level = hold

        # Registers Hits
        if len(bullets) > 0:
            for i in bullets.values():
                if pygame.Rect.colliderect(hitbox, i["hitbox"]):
                    health -= 1 + damage_buff
                    i["pierce"] -= 1
                    data["health"] = health
                    data["color"] = "gray14"
        if health < 1:
            del enemies[this_enemy]
            enemy_count -= 1
            pygame.mixer.Sound("ouch_AKigkiF.mp3").play(0,-1,0)
            kills += 1
            if vamperism and (random.randint(1,10-vamperism_proc_chance)) == 1:
                player_hp += 1
                print ("Get Vamped")
                if player_hp > max_hp:
                    player_hp = max_hp

        # Render Enemies
        if type == "Tank":
            draw.rect(screen, color, Rect(cord.x-30, cord.y-30, 60, 60), 0, 20)
        if type == "basic":
            draw.circle(screen, color, cord, 30)
        if type == "Super Speed Snorkler":
            draw.circle(screen, color, cord, 20)

# Spawns Bullets
def shoot(b_direction):
    global bullets, bullet_count, player_location, player_velocity
    global bullet_bounces, last_velocity, bullet_speed, all_mode, bullet_pierce
    global energy, shoot_cd, shoot_cd_len, directions, using_energy, fired_bullets
    if player == "alive":
        using_energy = True
        if energy > 0 and b_direction != "all":
            if shoot_cd >= shoot_cd_len:
                blocation=player_location.copy()
                bvelocity = directions[b_direction].copy()
                if not all_mode:
                    shoot_cd = 0
                    energy -= 20

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

                bullets[fired_bullets] = {
        "cord" : blocation,
        "velocity" : bvelocity,
        "color" : color,
        "bounces" : bullet_bounces,
        "hitbox" : hitbox,
        "pierce" : bullet_pierce
    }
                bullet_count += 1
                fired_bullets += 1
                pygame.mixer.Sound("pew-pew-lame-sound-effect.mp3").play(0,-1,0)
        elif b_direction == "all" and energy > 0 :
            all_mode = True
            shoot("left")
            shoot("right")
            shoot("up")
            shoot("down")
            shoot("left_down")
            shoot("right_up")
            shoot("left_up")
            shoot("right_down")
            all_mode = False
            energy -= 40 - omni_discount
            shoot_cd = 0
        else:
            print("Out of Energy")

# Runs the Bullets
def bullet():
    global bullets, bullet_count, fired_bullets
    for this_bullet, data in list(bullets.items()):
        cord = data["cord"]
        b_velocity = data["velocity"]
        color = data["color"]
        bounces = data["bounces"]
        hitbox = data["hitbox"]

        b_add_vel = Vector2(b_velocity.x*bullet_speed,b_velocity.y*bullet_speed)

        # Shoot the Bullets
        if data["bounces"] < 1:
            del bullets[this_bullet]
            bullet_count -= 1
        elif data["pierce"] < 1:
            del bullets[this_bullet]
            bullet_count -= 1

        bdata = scrape_and_run(cord, b_velocity, b_add_vel, "bullet", color, bounces, "circle", 10)
        data["bounces"] = bdata[2]

        # Moves hitbox
        hitbox.center = cord

        # Render Enemies
        draw.circle(screen, color, cord, 10)

# Spawns Waves of Enemies
def wave():
    global current_wave, enemy_ai_level
    while current_wave > len(enemies)+1:
        for i in range(current_wave):
            type = random.randint(1,3)
            if type == 1:
                enemy_init("basic")
            elif type == 2:
                enemy_init("Tank")
            elif type == 3:
                enemy_init("Super Speed Snorkler")
    current_wave += 1
    if enemy_ai_level > 3:
        enemy_ai_level -= 1

# Levels you Up Replaced by the level card system
#def lvl_up():
#    global max_energy, bullet_bounces, player_hp, shoot_cd_len, energy_regen, max_hp, bullet_speed, level
#    max_energy += 50
#    max_hp += 1
#    player_hp += 1
#    energy_regen += 1
#    print ("LEVEL UP!")
#    level += 1

def dir_shift():
    global directions
    for a,b in list(directions.items()):
        g = b.rotate(5)
        directions[a] = g

def level_button_array():
    global buttons
    num = 0
    for _ in range(upgrade_option_amount):
        num += 1
        option = total_level_up_options[(random.randint(1,len(total_level_up_options)))-1]
        button_init(width/upgrade_option_amount + num*310-500, 300, 250, 500, option, option, True, True)

def level_up_options(selected_option):
    global level_option, game_state
    if selected_option == "Super Speed":
        global move_speed
        move_speed += 5
    elif selected_option == "Bouncy Bullets":
        global bullet_bounces
        bullet_bounces += 1
    elif selected_option == "Fire Rate":
        global shoot_cd_len
        if shoot_cd_len > 0:
            shoot_cd_len -= 1
    elif selected_option == "Bullet Velocity":
        global bullet_speed
        bullet_speed += .1
    elif selected_option == "Omni Shot":
        global omnishot, omni_discount
        if omnishot and omni_discount < 39:
            omni_discount += 1
        omnishot = True
    elif selected_option == "Dash":
        global can_dash, dash_discount
        if can_dash and dash_discount < 4:
            dash_discount += 1
        can_dash = True
    elif selected_option == "Vamperism":
        global vamperism, vamperism_proc_chance
        if vamperism and vamperism_proc_chance < 9:
            vamperism_proc_chance += 1
        vamperism = True
    elif selected_option == "Bullet Pierce":
        global bullet_pierce
        bullet_pierce += 1
    elif selected_option == "Bonus Options!":
        global upgrade_option_amount
        upgrade_option_amount += 1
    elif selected_option == "Energize":
        global energy_regen, max_energy
        energy_regen += 10
        max_energy += 50
    elif selected_option == "More Damage":
        global damage_buff
        damage_buff += 1
    elif selected_option == "Super Vitality":
        global health_regen, max_hp
        health_regen += 1
        max_hp += 10
    elif selected_option == "Shields":
        global shields, shield_chance
        if shields and shield_chance > 1:
            shield_chance -= 1
        shields = True







    else:
        print("Level Option Error, skipping...")

    print (f"You selected option: {selected_option}")

    game_state = "game"
# initialization

pygame.display.set_caption('Driver')

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
running = True

def restart():
    global max_hp, shoot_cd, dabloons, player_hp, max_energy, energy, player, current_wave, kills, level, lvl_threshold, enemy_ai_level, game_state, dt, vamperism_proc_chance, omni_discount, dash_discount, damage_buff, omnishot, vamperism, fired_bullets, player_location, move_speed, enemy_count, enemies, bullet_count, bullets, dashing, all_mode, level_select, can_dash, using_energy
    max_hp = 400
    shoot_cd = 0
    dabloons = 0
    player_hp = max_hp
    max_energy = 400
    energy = max_energy
    player = "alive"
    current_wave = 0
    kills = 0
    level = 0
    lvl_threshold = 3
    enemy_ai_level = 10
    game_state = "game"
    vamperism_proc_chance = 0
    omni_discount = 0
    dash_discount = 0
    damage_buff = 0
    omnishot = False
    vamperism = False
    fired_bullets = 0
    player_location = Vector2(width / 2, height / 2)
    # stability = 100
    move_speed = base_move_speed
    enemy_count = 0
    enemies = {
    }
    bullet_count = 0
    bullets = {
    }
    dashing = False
    all_mode = False
    level_select = False
    can_dash = False
    using_energy = False


# Intro Screen

# TBD

button_init(550,550,100,50, "start", "start", True, True)
button_init(750,550,250,50, "Start Dev Mode", "Start Dev Mode", True, True)

# The following code was found on stackoverflow

# Game Loop
while running:
    screen.fill("indianred4")

    # Gets Mouse
    mouse = pygame.mouse.get_pos()

    # poll for events

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == "menu":
        button()

    if game_state == "game":

        #if event.type == pygame.MOUSEBUTTONDOWN:
        #    shooting = True
        #if event.type == pygame.MOUSEBUTTONUP:
        #    shooting = False

    # Reset Velocity Addition
        player_added_velocity = Vector2(0, 0)
        if energy > max_energy:
            energy = max_energy
        player_hp += health_regen
        if player_hp > max_hp:
            player_hp = max_hp

    # background

        using_energy = False

    # Applies low stability movement debuff
    #if stability_mode:
    #    # Sets minimum stability
    #    if stability < stability_floor:
    #        stability = stability_floor
    #    if stability != 0:
    #
    #        # Formula makes it more likely to trigger at lower stability, and more intense, auto adjusts itself to the stability floor, so no need to re-configure it
    #        drunk_trigger = random.randint(0, int(-stability_floor - abs(stability + (stability_floor // stability_impact) - stability_floor / 3))) <= 10 and stability < 0
    #        # Formula makes it more likely to trigger at lower stability, and more intense, auto adjusts itself to the stability floor, so no need to re-configure it
    #        if drunk_trigger:
    #            player_added_velocity.y += random.uniform(abs(2 * stability / stability_impact),
    #                                                  -abs(2 * stability / stability_impact))
    #            player_added_velocity.x += random.uniform(abs(2 * stability / stability_impact),
    #                                                  -abs(2 * stability / stability_impact))

    # Button
        button()

    #prevents post death hp/energy gain error
        if player == "dead":
            player_hp = 0
            energy = 0

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
        if keys[pygame.K_LSHIFT] and energy >= 1 and can_dash:
            player_velocity.x *= 1.1
            player_velocity.y *= 1.1
            energy -= 5 - dash_discount
            dashing = True
            using_energy = True
        else:
            dashing = False

        # To be honest, this feature was kinda useless, goodbye forever you wretch
        #if keys[pygame.K_r]:
        #    dir_shift()

        # Shooting Logic
        if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            shoot("left_up")
        elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            shoot("right_up")
        elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            shoot("right_down")
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            shoot("left_down")
        elif keys[pygame.K_LEFT]:
            shoot("left")
        elif keys[pygame.K_RIGHT]:
            shoot("right")
        elif keys[pygame.K_UP]:
            shoot("up")
        elif keys[pygame.K_DOWN]:
            shoot("down")

        # Dev Keys
        if keys[pygame.K_v]:
            enemy_init("basic")
        if keys[pygame.K_SPACE] and omnishot:
            shoot("all")



    # Shooting/Energy Moved to Shoot Function
    #if player == "alive":
    #    if shooting == True and energy > 0:
    #        if shoot_cd >= shoot_cd_len:
    #            shoot(direction)
    #            energy -= 15
    #            shoot_cd = 0
    #        else:
    #            shoot_cd += 1
    #    elif shooting == False and energy < max_energy:
    #        energy += energy_regen
    #        shoot_cd += 1
    #    elif shooting:
    #        print("Out of Energy")
    #    else:
    #        shoot_cd += 1

    # The Enemy
        enemy()

    # Player is You
        if player == "alive":
            driver()
        else:
            draw.circle(screen, "black", player_location, 30)
            text_surface = font.render("You Died!", True, "white")
            screen.blit(text_surface, (width/2-100, height/2-20))
            text_surface = font.render("Press R to Restart", True, "white")
            screen.blit(text_surface, (width/2-150, height/2+20))
            if keys[pygame.K_r]:
                # Reset Game
                restart()

        # The Bullets
        bullet()

        if len(enemies) <= 0:
            wave()

        if kills >= lvl_threshold-level:
            #lvl_up()
            lvl_threshold += level + 3
            kills = 0
            player_hp = max_hp
            game_state = "level_up"

        ui()

        button()

        if energy < max_energy and using_energy == False:
            energy += energy_regen
        shoot_cd += 1

    if game_state == "level_up":
        if len(buttons) <= 0:
            level_button_array()
        button()
    # misc
    pygame.display.flip()
    dt = clock.tick(60) / 1000

print("The Game has ended")