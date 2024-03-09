import pygame
from pygame.locals import *
import random

pygame.init()

width = 600
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

gray = ('#808080')
oil = ('#3B3131')
red = ('#FF0000')

gameover = False
speed = 2
score = 0

marker_width = 10
marker_height = 50

road = (100, 0, 390, height)
left_edge_marker = (90, 0, marker_width, height)
right_edge_marker = (490, 0, marker_width, height)

left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

lane_marker_move_y = 0

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        pygame.sprite.Sprite.__init__(self)

        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (int(new_width), int(new_height)))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

class PlayerVehicle(Vehicle):
    def __init__(self, image, x, y):
        image = pygame.image.load('images/bmw.png')
        super().__init__(image, x, y, 0)

player_x = 300
player_y = 400

player_group = pygame.sprite.Group()
player = PlayerVehicle('bmw.png', player_x, player_y)
player_group.add(player)

vehicle_group = pygame.sprite.Group()

def add_vehicle():
    lane = random.choice(lanes)
    speed = 3
    image_filename = random.choice(['kawazaki.png', 'taxi.png', 'truck1.png', 'truck2.png'])
    image = pygame.image.load('images/' + image_filename)
    vehicle = Vehicle(image, lane + 45, -50, speed)
    vehicle_group.add(vehicle)

# load the crash image
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()

clock = pygame.time.Clock()
fps = 110
running = True
vehicle_add_counter = 0

while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and player.rect.center[0] > left_lane:
        player.rect.x -= 5
    elif keys[K_RIGHT] and player.rect.center[0] < right_lane + 100:
        player.rect.x += 5

    collisions = pygame.sprite.spritecollide(player, vehicle_group, False)
    if collisions:
        print("Game Over - Collision!")
        running = False

        # Iterate over vehicles for collision handling
        for vehicle in vehicle_group:
            if pygame.sprite.collide_rect(player, vehicle):
                gameover = True

                # Handle the direction of the collision
                if keys[K_LEFT]:  # Check the direction of player movement
                    player.rect.left = vehicle.rect.right
                    crash_rect.center = (player.rect.left, (player.rect.centery + vehicle.rect.centery) / 2)
                elif keys[K_RIGHT]:
                    player.rect.right = vehicle.rect.left
                    crash_rect.center = (player.rect.right, (player.rect.centery + vehicle.rect.centery) / 2)

    screen.fill(oil)
    pygame.draw.rect(screen, gray, road)
    pygame.draw.rect(screen, (0, 0, 0), left_edge_marker)
    pygame.draw.rect(screen, (0, 0, 0), right_edge_marker)

    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0

    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, (255, 255, 255), (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, (255, 255, 255), (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, (255, 255, 255), (right_lane + 45, y + lane_marker_move_y, marker_width, marker_height))

    player_group.draw(screen)
    player_group.update()

    vehicle_group.draw(screen)
    vehicle_group.update()

    vehicle_add_counter += 1
    if vehicle_add_counter >= 50:
        add_vehicle()
        vehicle_add_counter = 0

    # check if there's a head-on collision
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = (player.rect.centerx, player.rect.top)

    # display game over
    if gameover:
        screen.blit(crash, crash_rect)
        pygame.draw.rect(screen, red, (0, 50, width, 100))

        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game over. play again? ( enter Y or N)', True, (255, 255, 255))
        text_rect = text.get_rect(center=(width // 2, 100))
        screen.blit(text, text_rect)

        pygame.display.update()

        # check if player wants to play again
        while gameover:
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == QUIT:
                    gameover = False
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_y:
                        # reset the game
                        gameover = False
                        speed = 2
                        score = 0
                        vehicle_group.empty()
                        player.rect.center = (player_x, player_y)
                    elif event.key == K_n:
                        # exit the loops
                        gameover = False
                        running = False

pygame.quit()
