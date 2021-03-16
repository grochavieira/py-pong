import pygame
import sys
import random


# classe base que será herdada pelas outras
# é utilizada para carregar a imagem e criar
# um retangulo ao redor dela, para que não sejá
# necessário repetir a mesma coisa nas outras por
# se tratar de elementos em comum
class Block(pygame.sprite.Sprite):
    def __init__(self, image_path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(image_path)  # carrega o sprite
        # desenha o retangulo em volta da imagem
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


class Player(Block):  # Classe que define a raquete e suas funções
    def __init__(self, image_path, x_pos, y_pos, speed):
        super().__init__(image_path, x_pos, y_pos)
        self.speed = speed  # define a velocidade do jogador
        self.movement = 0  # define a movimentação do jogador

    # função para limitar até onde a raquete pode ir
    def screen_constrain(self):
        if self.rect.top <= 0:  # se a raquete chegou até o 'teto' da tela
            self.rect.top = 0
        if self.rect.bottom >= screen_height:  # se a raquete chegou até o 'chão' da tela
            self.rect.bottom = screen_height

    # função para atualizar a raquete
    def update(self, ball_group):
        self.rect.y += self.movement  # movimenta a raquete
        self.screen_constrain()  # chama a função impor limite até onde pode ir


class Ball(Block):  # classe que define a bola e sua funções
    def __init__(self, image_path, x_pos, y_pos, speed_x, speed_y, paddles):
        super().__init__(image_path, x_pos, y_pos)
        # randomiza a direção inicial que a bola ira começar
        self.speed_x = speed_x * random.choice((-1, 1))
        self.speed_y = speed_y * random.choice((-1, 1))
        self.paddles = paddles
        self.active = False  # será usado para saber se a bola está movimentando
        self.score_time = 0

    # função para atualizar a bola
    def update(self):
        if self.active:  # se a bola está movimentando
            # atualiza sua posição
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()  # chama a função de colisões
        else:  # se não
            self.restart_counter()  # reseta o contador

    # função para definir as colisões da bola
    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            # toca o som de hit quando a bola toca na parte
            # de cima ou de baixo da tela
            pygame.mixer.Sound.play(hit_sound)
            self.speed_y *= -1  # joga a bola para outra posição

        # a função spritecollide é utilizada para fazer algo
        # quando dois objetos colidem, no caso a colisão das
        # raquetes (self.paddles) com a bola (self) e a terceiro
        # parâmetro se refere a eliminar todos os elementos que colidiram
        # com o elemento de referência se deixar como True, para False
        # apenas retorna uma lista dos elementos que colidiram
        if pygame.sprite.spritecollide(self, self.paddles, False):
            # toca o som de hit
            pygame.mixer.Sound.play(hit_sound)
            # como retorna uma lista de elementos, é pego
            # somente o primeiro elemento, que pode ser a raquete
            # do jogador ou do oponente
            collision_paddle = pygame.sprite.spritecollide(
                self, self.paddles, False)[0].rect

            # agora que sabemos qual raquete está ocorrendo
            # a colisão, basta utilizar as condições a seguir
            # para mudar a posição da bola
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1

            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1

            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1

            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y < 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1

    # função para resetar a bola sempre que algúem marca
    # um ponto
    def reset_ball(self, start_game):
        self.active = False  # a bola não esta movimentando
        # define de forma aleatória a direção que irá iniciar
        self.speed_x *= random.choice((-1, 1))
        self.speed_y *= random.choice((-1, 1))
        # pega o tempo quando a bola foi resetada
        self.score_time = pygame.time.get_ticks()
        # joga a bola para o centro da tela
        self.rect.center = (screen_width/2, screen_height/2)
        # ativa um som quando a bola sai pra fora da tela
        if(not start_game):
            pygame.mixer.Sound.play(score_sound)

    # função para resetar o contador, que é chamado sempre
    # que alguém marca algum ponto, ou no inicio do jogo
    def restart_counter(self):
        current_time = pygame.time.get_ticks()  # pega o tempo atual
        countdown_number = 3  # contador que será renderizado na tela

        # basicamente essas condições são utilizadas
        # para contar 3 segundos antes da bola começar a se
        # movimentar, além de renderizar na tela um contador
        # para os jogadores saberem quando a bola voltar a se
        # movimentar
        if current_time - self.score_time <= 700:
            countdown_number = 3
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        if current_time - self.score_time >= 2100:
            self.active = True

        # cria o texto que será renderizado
        time_counter = basic_font.render(
            str(countdown_number), True, accent_color)
        # cria um retangulo em volta do texto e define sua posição na tela
        time_counter_rect = time_counter.get_rect(
            center=(screen_width/2, screen_height/2 + 50))
        # desenha na tela o retangulo
        pygame.draw.rect(screen, bg_color, time_counter_rect)
        # coloca de fato na tela o contador
        screen.blit(time_counter, time_counter_rect)


class Opponent(Block):  # classe utilizada para o oponente e suas funções
    def __init__(self, image_path, x_pos, y_pos, speed):
        super().__init__(image_path, x_pos, y_pos)
        self.speed = speed  # velocidade do oponente

    # função para atualizar o oponente
    def update(self, ball_group):
        # é apenas um sistema de movimentação básico
        # se a bola estiver em acima da raquete
        # a raquete se move para cima
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        # se a bola estiver abaixo
        # a raquete se move para baixo
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed
        # mantendo os limites da tela pela função abaixo
        self.constrain()

    # função define o limite da raquete em relação a tela
    # igual a do jogador
    def constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height


class GameManager:  # classe para gerenciar o jogo
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self):
        # Desenha os objetos do jogo
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        # Atualiza os objetos do jogo
        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    # função utilizada para verificar e chamar a função
    # de resetar a bola quando ocorrer colisão nas laterais
    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:  # a bola saiu pela direita
            self.opponent_score += 1  # aumenta o score o oponent
            self.ball_group.sprite.reset_ball(False)  # reseta a bola
        if self.ball_group.sprite.rect.left <= 0:  # a bola saiu pela esquerda
            self.player_score += 1  # aumenta o score do jogador
            self.ball_group.sprite.reset_ball(False)  # reseta a bola

    # função para desenhar o score na tela
    def draw_score(self):
        # cria o texto para o score do jogador
        # e do oponente
        player_score = basic_font.render(
            str(self.player_score), True, accent_color)
        opponent_score = basic_font.render(
            str(self.opponent_score), True, accent_color)

        # cria um objeto ao redor do texto dos scores
        # e também define a posição do texto
        player_score_rect = player_score.get_rect(
            midleft=(screen_width / 2 + 40, screen_height/2))
        opponent_score_rect = opponent_score.get_rect(
            midright=(screen_width/2 - 40, screen_height/2))

        # coloca os scores na tela
        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([1, 1])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Button(pygame.sprite.Sprite):
    def __init__(self, base_images_path, number_of_images, pos_x, pos_y):
        super().__init__()
        self.sprites = []

        for i in range(number_of_images):
            image_path = base_images_path + str(i + 1) + ".png"
            self.sprites.append(pygame.image.load(image_path))

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self):
        self.current_sprite += 0.07

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]


# General setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Janela principal
screen_width = 1280  # largura
screen_height = 720  # altura
# cria a janela do jogo
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")  # titulo

# Variáveis globais
bg_color = pygame.Color("#040F0F")  # code de fundo
accent_color = (253, 255, 252)  # cor das letras e linha no meio
basic_font = pygame.font.Font("freesansbold.ttf", 32)  # carrega a fonte
hit_sound = pygame.mixer.Sound("sounds/pong.wav")  # carrega o som de hit
score_sound = pygame.mixer.Sound("sounds/score.wav")  # carrega o som de score
# cria uma linha que será desenhada no meio da tela
middle_strip = pygame.Rect(screen_width/2 - 2, 0, 4, screen_height)


# Objetos do jogo
# instância as classes de player e opponent
player = Player("images/Paddle.png", screen_width - 20, screen_height/2, 5)
opponent = Opponent("images/Paddle.png", 20, screen_height/2, 5)

# os objetos player e opponent são adicionados a um sprite group
# para que todos sejam renderizados ao mesmo tempo na tela ou atualizados
# assim não existe a necessidade de fazer um por um
singleplayer_paddle_group = pygame.sprite.Group()
singleplayer_paddle_group.add(player)
singleplayer_paddle_group.add(opponent)

# O mesmo que foi feito para o player e opponent é feito para a bola (ball)
ball = Ball("images/Ball.png", screen_width/2,
            screen_height/2, 4, 4, singleplayer_paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

# botão iniciar o single player
singleplayer_button = Button(
    "images/btn_sp/btn_sp", 10, screen_width/2 - 300, 300)
# botão para iniciar o multiplayer
multiplayer_button = Button("images/btn_mp/btn_mp",
                            10, screen_width/2 - 300, 500)
button_group = pygame.sprite.Group()
button_group.add(singleplayer_button)
button_group.add(multiplayer_button)

# mouse element
mouse = Mouse()
mouse_group = pygame.sprite.Group()
mouse_group.add(mouse)


def main_menu():  # menu principal do jogo
    while True:

        screen.fill(bg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollide(mouse, button_group, False):
                    collision_button = pygame.sprite.spritecollide(
                        mouse, button_group, False)[0].rect

                    if collision_button.bottom >= 500:
                        multiplayer_game()
                    elif collision_button.bottom >= 300:
                        singleplayer_game()

        button_group.draw(screen)
        mouse_group.draw(screen)
        button_group.update()
        mouse_group.update()
        pygame.display.update()
        clock.tick(120)


def singleplayer_game():
    ball.reset_ball(True)

    # instancia a classe GameManager, para ser usada no loop do jogo
    game_manager = GameManager(ball_sprite, singleplayer_paddle_group)
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

        # Desenha a tela de fundo
        screen.fill(bg_color)
        pygame.draw.rect(screen, accent_color, middle_strip)

        # Cuida da renderização e alteração dos objetos do jogo
        game_manager.run_game()

        # Atualiza todo o conteúdo da tela
        pygame.display.flip()
        # define a velocidade do jogo
        clock.tick(120)


def multiplayer_game():
    # Objetos do jogo
    # instância as classes de player1 e player2
    player1 = Player("images/Paddle.png",
                     screen_width - 20, screen_height/2, 5)
    player2 = Player("images/Paddle.png", 20, screen_height/2, 5)

    multiplayer_paddle_group = pygame.sprite.Group()
    multiplayer_paddle_group.add(player1)
    multiplayer_paddle_group.add(player2)

    # O mesmo que foi feito para o player e opponent é feito para a bola (ball)
    ball = Ball("images/Ball.png", screen_width/2,
                screen_height/2, 4, 4, multiplayer_paddle_group)
    ball_sprite = pygame.sprite.GroupSingle()
    ball_sprite.add(ball)

    ball.reset_ball(True)

    # instancia a classe GameManager, para ser usada no loop do jogo
    multiplayer_game_manager = GameManager(
        ball_sprite, multiplayer_paddle_group)
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
                    player1.movement -= player1.speed
                # apertou a tecla para baixo
                if event.key == pygame.K_DOWN:
                    # move o jogador para baixo
                    player1.movement += player1.speed

                if event.key == pygame.K_w:
                    player2.movement -= player2.speed

                if event.key == pygame.K_s:
                    player2.movement += player2.speed

                if event.key == pygame.K_ESCAPE:
                    running = False

            # se soltou alguma tecla
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    # reseta o movimento do jogador para 0
                    player1.movement += player1.speed
                if event.key == pygame.K_DOWN:
                    # reseta o movimento do jogador para 0
                    player1.movement -= player1.speed

                if event.key == pygame.K_w:
                    player2.movement += player2.speed

                if event.key == pygame.K_s:
                    player2.movement -= player2.speed

        # Desenha a tela de fundo
        screen.fill(bg_color)
        pygame.draw.rect(screen, accent_color, middle_strip)

        # Cuida da renderização e alteração dos objetos do jogo
        multiplayer_game_manager.run_game()

        # Atualiza todo o conteúdo da tela
        pygame.display.flip()
        # define a velocidade do jogo
        clock.tick(120)


main_menu()
