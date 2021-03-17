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
    btn_w = engine.Block("images/btns/w.png",
                         settings.screen_width/2 - settings.screen_width/4, 100)
    btn_s = engine.Block("images/btns/s.png",
                         settings.screen_width/2 - settings.screen_width/4, 160)
    text_group = pygame.sprite.Group()
    text_group.add(btn_arrow_down)
    text_group.add(btn_arrow_up)
    text_group.add(btn_w)
    text_group.add(btn_s)

    # instância as classes de player1 e player2
    player1 = engine.Player("images/Paddle.png",
                            settings.screen_width - 20, settings.screen_height/2, 5)
    player2 = engine.Player("images/Paddle.png", 20,
                            settings.screen_height/2, 5)

    # grupo para armazenar os jogadores
    multiplayer_paddle_group = pygame.sprite.Group()
    multiplayer_paddle_group.add(player1)
    multiplayer_paddle_group.add(player2)

    # cria o grupo que irá armazenar os blocos
    multiplayer_block_group = pygame.sprite.Group()

    # O mesmo que foi feito para o bloco e jogadores é feito para a bola (ball)
    ball = engine.Ball("images/Ball.png", settings.screen_width/2,
                       settings.screen_height/2, 4, 4, multiplayer_paddle_group, multiplayer_block_group)
    ball_sprite = pygame.sprite.GroupSingle()
    ball_sprite.add(ball)

    ball.reset_ball(True)

    # instancia a classe GameManager, para ser usada no loop do jogo
    multiplayer_game_manager = engine.GameManager(
        ball_sprite, multiplayer_paddle_group, multiplayer_block_group)

    # variavel utilizada para adicionar novos blocos de acordo com o tempo passado
    game_start_time = pygame.time.get_ticks()

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
                    # move o jogador1 para cima
                    player1.movement -= player1.speed
                # apertou a tecla para baixo
                if event.key == pygame.K_DOWN:
                    # move o jogador1 para baixo
                    player1.movement += player1.speed

                if event.key == pygame.K_w:
                    # move o jogador2 para cima
                    player2.movement -= player2.speed

                if event.key == pygame.K_s:
                    # move o jogador2 para baixo
                    player2.movement += player2.speed

                if event.key == pygame.K_ESCAPE:
                    running = False

            # se soltou alguma tecla
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    # reseta o movimento do jogador1 para 0
                    player1.movement += player1.speed
                if event.key == pygame.K_DOWN:
                    # reseta o movimento do jogador1 para 0
                    player1.movement -= player1.speed

                if event.key == pygame.K_w:
                    # reseta o movimento do jogador2 para 0
                    player2.movement += player2.speed

                if event.key == pygame.K_s:
                    # reseta o movimento do jogador2 para 0
                    player2.movement -= player2.speed

        current_time = pygame.time.get_ticks()
        if current_time - game_start_time >= 3500:
            game_start_time = current_time
            new_block = engine.Block("images/Block.png",
                                     random.randrange(50, settings.screen_width - 50), random.randrange(50, settings.screen_height - 50))
            multiplayer_block_group.add(new_block)

        # Desenha a tela de fundo
        settings.screen.fill(settings.bg_color)
        text_group.draw(settings.screen)
        pygame.draw.rect(settings.screen, settings.accent_color,
                         settings.middle_strip)

        # Cuida da renderização e alteração dos objetos do jogo
        multiplayer_game_manager.run_game()

        # Atualiza todo o conteúdo da tela
        pygame.display.flip()
        # define a velocidade do jogo
        settings.clock.tick(120)
