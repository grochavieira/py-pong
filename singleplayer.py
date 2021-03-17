import pygame
import sys
import random
import settings
import engine


def start_game():

    btn_arrow_up = engine.Block("images/btns/arrow_up.png",
                                settings.screen_width/2 + settings.screen_width/4, 100)
    btn_arrow_down = engine.Block("images/btns/arrow_down.png",
                                  settings.screen_width/2 + settings.screen_width/4, 160)
    text_group = pygame.sprite.Group()
    text_group.add(btn_arrow_down)
    text_group.add(btn_arrow_up)

    # instância as classes de player e opponent
    player = engine.Player("images/Paddle.png", settings.screen_width -
                           20, settings.screen_height/2, 5)
    opponent = engine.Opponent("images/Paddle.png", 20,
                               settings.screen_height/2, 5)

    # os objetos player e opponent são adicionados a um sprite group
    # para que todos sejam renderizados ao mesmo tempo na tela ou atualizados
    # assim não existe a necessidade de fazer um por um
    singleplayer_paddle_group = pygame.sprite.Group()
    singleplayer_paddle_group.add(player)
    singleplayer_paddle_group.add(opponent)

    singleplayer_block_group = pygame.sprite.Group()

    # O mesmo que foi feito para o player e opponent é feito para a bola (ball)
    ball = engine.Ball("images/Ball.png", settings.screen_width/2,
                       settings.screen_height/2, 4, 4, singleplayer_paddle_group, singleplayer_block_group)
    ball_group = pygame.sprite.GroupSingle()
    ball_group.add(ball)

    ball.reset_ball(True)
    # instancia a classe GameManager, para ser usada no loop do jogo
    singleplayer_game_manager = engine.GameManager(
        ball_group, singleplayer_paddle_group, singleplayer_block_group)

    game_start_time = pygame.time.get_ticks()
    previous_player_score = 0

    running = True
    while running:
        # checa os eventos do teclado e mouse
        for event in pygame.event.get():
            # se clicou no X da tela
            if event.type == pygame.QUIT:
                # sai do jogo
                pygame.quit()
                sys.exit()
            # se apertou alguma tecla
            if event.type == pygame.KEYDOWN:
                # apertou a tecla para cima
                if event.key == pygame.K_UP:
                    # move o jogador para cima
                    player.movement -= player.speed
                # apertou a tecla para baixo
                if event.key == pygame.K_DOWN:
                    # move o jogador para baixo
                    player.movement += player.speed
                if event.key == pygame.K_ESCAPE:
                    running = False

            # se soltou alguma tecla
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    # reseta o movimento do jogador para 0
                    player.movement += player.speed
                if event.key == pygame.K_DOWN:
                    # reseta o movimento do jogador para 0
                    player.movement -= player.speed

        current_time = pygame.time.get_ticks()
        if current_time - game_start_time >= 3500:
            game_start_time = current_time
            new_block = engine.Block("images/Block.png",
                                     random.randrange(50, settings.screen_width - 50), random.randrange(50, settings.screen_height - 50))
            singleplayer_block_group.add(new_block)

        if previous_player_score < singleplayer_game_manager.player_score:
            opponent.speed += 0.5
            previous_player_score = singleplayer_game_manager.player_score

        # Desenha a tela de fundo
        settings.screen.fill(settings.bg_color)
        text_group.draw(settings.screen)
        pygame.draw.rect(settings.screen, settings.accent_color,
                         settings.middle_strip)

        # Cuida da renderização e alteração dos objetos do jogo
        singleplayer_game_manager.run_game()

        # Atualiza todo o conteúdo da tela
        pygame.display.flip()
        # define a velocidade do jogo
        settings.clock.tick(120)
