import pygame
#import pygame_widgets
import random
from pygame import Vector2, Rect, draw, Color
pygame.init()
width, height = 1920,1080
screen = pygame.display.set_mode((width, height))

dt = 0
multi_shot = 1
player_damaged = False
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
                          "More Damage", "Shields", "Super Vitality", "Multishot"]
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
enemy_colors = [
    Color("#2b6e94"),
    Color("#5c5a61"),
    Color("#e3f4fc"),
    Color("#aadbf4"),
    Color("#c7e7f8")
]
bullet_colors = [
    Color("#A307A3"),
    Color("#AA08B5"),
    Color("#BF5AA4"),
    Color("#FA90A3"),
    Color("#FDACA1")
]
trail = 40
min_speed = Vector2(.1, .1)  # Applies to all characters that use scrape and run
max_speed = Vector2(100, 100)  # Applies to all characters that use scrape and run
# Both Stability mode and Gravity have been removed for being "stupid and boring"

#stability_mode = False
#stability_impact = 90 # changes how much stability affects gameplay, further from 0 = less impact
#stability_floor = -300
#gravity_factor = 1 Abandoned by its God (me)
d_color = Color("#F08080")
base_color = d_color
energy = 400.0
bullet_bounces = 1
bullet_speed = .5
shoot_cd_len = 12
energy_regen = 2
max_energy = 400
enemy_base_health = 1
pygame.mixer.music.load("Thundersnail.mp3")
lvl_threshold = 3
# Lower = Smarter, 1 = Instant Reaction
enemy_ai_level = 10
bullet_pierce = 1
upgrade_option_amount = 3