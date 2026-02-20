import pygame 
from random import randint, choice
from button import Button

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Ninja Run')

font1 = pygame.font.Font('Pixeltype.ttf', 50)
font2 = pygame.font.Font('Pixeltype.ttf', 150)

gameplay = False
start = 0

playerm = pygame.image.load('playerm.png')
playerm = pygame.transform.scale(playerm, (200,150))


def update_score():
    time_now = pygame.time.get_ticks() - start
    score = font1.render(f'{time_now//100}', False, (64,64,64))
    score_rect = score.get_rect(center=(400,50))
    screen.blit(score, score_rect)


def obst_move(obst_list, player_rect):
    if obst_list:
        for obst_rect, obst_type in obst_list:

            # Ground spike tracks player horizontally
            if obst_type == 1:
                if obst_rect.centerx > player_rect.centerx:
                    obst_rect.x -= 5
                elif obst_rect.centerx < player_rect.centerx:
                    obst_rect.x += 5
                screen.blit(obst1, obst_rect)

            # Air blade straight line
            elif obst_type == 2:
                obst_rect.x -= 8
                screen.blit(obst2, obst_rect)

            elif obst_type == 3:
                obst_rect.x -= 10
                screen.blit(obst3, obst_rect)

        obst_list = [(obst, t) for (obst, t) in obst_list if -100 < obst.x < 900]
        return obst_list
    else:
        return []


def collisions(player_rect, obst_list):
    for obst_rect, _ in obst_list:
        if player_rect.colliderect(obst_rect):
            return False
    return True


# ================= LOAD ASSETS =================

bg_sky = pygame.image.load('sky.jpg').convert()
bg_sky = pygame.transform.scale(bg_sky, (800,370))

bg_ground = pygame.image.load('ground.png').convert()

player = pygame.image.load('player.png').convert_alpha()
player = pygame.transform.scale(player, (50,70))
player_rect = player.get_rect(midbottom=(80,370))

over = font2.render('Game Over', False, (64,64,64))
over_rect = over.get_rect(center=(400,200))

global obst1, obst2, obst3

obst1 = pygame.image.load('obstacles/spikes/spikes_1.png').convert_alpha()
obst1 = pygame.transform.scale(obst1, (60,40))

obst2 = pygame.image.load('obstacles/rotating_blades/blade_3.png').convert_alpha()
obst2 = pygame.transform.scale(obst2, (50,50))

obst3 = pygame.image.load('obstacles/rotating_blades/blade_2.png').convert_alpha()
obst3 = pygame.transform.scale(obst3, (50,50))


obst_list = []
player_grav = 0

obst_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obst_timer, 1200)


# ================= MAIN LOOP =================

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # MENU CLICK
        if not gameplay:
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_mouse = pygame.mouse.get_pos()
                if playbutton.checkForInput(menu_mouse):
                    gameplay = True
                    start = pygame.time.get_ticks()
                    obst_list.clear()
                    player_rect.midbottom = (80,370)

        # GAMEPLAY EVENTS
        if gameplay:

            if event.type == pygame.KEYDOWN and player_rect.bottom >= 370:
                if event.key == pygame.K_SPACE:
                    player_grav = -18

            if event.type == obst_timer:

                # Make spikes more common
                obst_type = choice([1,1,1,2,3])

                # Difficulty scaling based on time
                time_now = (pygame.time.get_ticks() - start) // 1000

                if obst_type == 1:
                    # Spawn multiple spikes
                    spike_count = randint(1, 3 + time_now // 10)

                    for i in range(spike_count):
                        obst_rect = obst1.get_rect(
                            midbottom=(randint(100,700), 370)
                        )
                        obst_list.append((obst_rect, 1))

                elif obst_type == 2:
                    obst_rect = obst2.get_rect(
                        center=(randint(900,1100), 250)
                    )
                    obst_list.append((obst_rect, 2))

                elif obst_type == 3:
                    obst_rect = obst3.get_rect(
                        center=(randint(900,1100), 180)
                    )
                    obst_list.append((obst_rect, 3))


    # ================= MENU =================

    if not gameplay:

        screen.fill((0,0,90))
        screen.blit(playerm, (300,150))

        menu_mouse = pygame.mouse.get_pos()

        menutitle = font2.render('Ninja Run', False, (255,255,255))
        menutitle_rect = menutitle.get_rect(center=(400,80))
        screen.blit(menutitle, menutitle_rect)

        playbutton = Button(
            image=None,
            pos=(400,260),
            text_input="PLAY",
            font=font1,
            base_color="White",
            hovering_color="Yellow"
        )

        quitbutton = Button(
            image=None,
            pos=(400,320),
            text_input="QUIT",
            font=font1,
            base_color="White",
            hovering_color="Red"
        )

        for button in [playbutton, quitbutton]:
            button.changeColor(menu_mouse)
            button.update(screen)

        if pygame.mouse.get_pressed()[0]:
            if quitbutton.checkForInput(menu_mouse):
                pygame.quit()
                exit()

    # ================= GAME =================

    else:

        screen.blit(bg_sky,(0,0))
        screen.blit(bg_ground,(0,370))

        update_score()

        # Player movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_rect.x -= 5
        if keys[pygame.K_RIGHT]:
            player_rect.x += 5

        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > 800:
            player_rect.right = 800

        # Gravity
        player_grav += 1
        player_rect.y += player_grav

        if player_rect.bottom >= 370:
            player_rect.bottom = 370

        screen.blit(player, player_rect)

        obst_list = obst_move(obst_list, player_rect)

        gameplay = collisions(player_rect, obst_list)

        if not gameplay:
            screen.blit(over, over_rect)

    pygame.display.update()
    clock.tick(60)
