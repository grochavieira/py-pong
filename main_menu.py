import pygame
import sys
import random
import settings
import engine
import singleplayer
import multiplayer


def start():  # menu principal do jogo
    # botão iniciar o single player
    singleplayer_button = engine.Button(
        "images/btn_sp/btn_sp", 10, settings.screen_width/2 - 300, 400)
    # botão para iniciar o multiplayer
    multiplayer_button = engine.Button("images/btn_mp/btn_mp",
                                       10, settings.screen_width/2 - 300, 550)
    button_group = pygame.sprite.Group()
    button_group.add(singleplayer_button)
    button_group.add(multiplayer_button)

    # titulo e texto de informação do jogo
    title = engine.Text("images/title/title", 12, 0.07,
                        settings.screen_width/2 - 770, 0)
    info = engine.Text("images/info/info", 2, 0.02,
                       settings.screen_width/2 - 410, 250)
    text_group = pygame.sprite.Group()
    text_group.add(title)
    text_group.add(info)

    # mouse element
    mouse = engine.Mouse()
    mouse_group = pygame.sprite.Group()
    mouse_group.add(mouse)
    while True:

        settings.screen.fill(settings.bg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollide(mouse, button_group, False):
                    collision_button = pygame.sprite.spritecollide(
                        mouse, button_group, False)[0].rect

                    if collision_button.bottom >= 550:
                        settings.button_sound.play()
                        multiplayer.start_game()
                    elif collision_button.bottom >= 350:
                        settings.button_sound.play()
                        singleplayer.start_game()

        button_group.draw(settings.screen)
        mouse_group.draw(settings.screen)
        text_group.draw(settings.screen)
        button_group.update()
        mouse_group.update()
        text_group.update()
        pygame.display.update()
        settings.clock.tick(120)
