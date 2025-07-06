import pygame
import sys
import time

# ゲームの状態
GAME_PLAYING = 0
GAME_OVER = 1
GAME_CLEAR = 2

# FPSの設定
FPS = 60

# 初期化
pygame.init()

# 画面サイズ
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ブロック崩し")

# 色の定義
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# フォントの設定
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def reset_game():
    global paddle, ball, blocks, score, ball_speed_x, ball_speed_y, left_passed_time, right_passed_time
    
    # パドルの初期化
    paddle = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height - 30, paddle_width, paddle_height)
    left_passed_time = 0
    right_passed_time = 0

    # ボールの初期化
    ball = pygame.Rect(screen_width // 2, screen_height // 2, ball_radius * 2, ball_radius * 2)
    ball_speed_x = 5
    ball_speed_y = 5

    # ブロックの再生成
    blocks.clear()
    for row in range(block_rows):
        block_row = []
        for col in range(block_cols):
            block_x = col * (block_width + 10) + 20
            block_y = row * (block_height + 10) + 35
            block = pygame.Rect(block_x, block_y, block_width, block_height)
            block_row.append(block)
        blocks.append(block_row)

    # スコアのリセット
    score = 0

# パドルの設定
paddle_width = 150
paddle_height = 10
paddle_speed = 10
paddle_acceleration = 3
left_passed_time = 0
right_passed_time = 0
paddle = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height - 30, paddle_width, paddle_height)

# ボールの設定
ball_radius = 10
ball_speed_x = 3
ball_speed_y = 3
ball_speed_increment = 0.02
ball = pygame.Rect(screen_width // 2, screen_height // 2, ball_radius * 2, ball_radius * 2)

# ブロックの設定
block_width = 60
block_height = 20
block_rows = 5
block_cols = 11
blocks = []
for row in range(block_rows):
    block_row = []
    for col in range(block_cols):
        block_x = col * (block_width + 10) + 20
        block_y = row * (block_height + 10) + 35
        block = pygame.Rect(block_x, block_y, block_width, block_height)
        block_row.append(block)
    blocks.append(block_row)

# クロックオブジェクトの作成
clock = pygame.time.Clock()

# カウントダウンの表示
for i in range(3, 0, -1):
    screen.fill(black)
    countdown_text = font.render(f"Starting in {i}", True, white)
    screen.blit(countdown_text, (screen_width // 2 - countdown_text.get_width() // 2, screen_height // 2 - countdown_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(1)

# ゲーム状態の初期設定
game_state = GAME_PLAYING

running = True
score = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == GAME_OVER or game_state == GAME_CLEAR:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    game_state = GAME_PLAYING
                elif event.key == pygame.K_q:
                    running = False
    
    if game_state == GAME_PLAYING:
        # パドルの操作
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            left_passed_time += 1
            right_passed_time = 0
            paddle_speed = (10 + paddle_acceleration * left_passed_time)
            if paddle.left > 0:
                paddle.left -= paddle_speed
        elif keys[pygame.K_RIGHT]:
            right_passed_time += 1
            left_passed_time = 0
            paddle_speed = (10 + paddle_acceleration * right_passed_time)
            if paddle.right < screen_width:
                paddle.right += paddle_speed
        else:
            left_passed_time = 0
            right_passed_time = 0
            paddle_speed = 10
    
        # ボールの移動
        ball.left += ball_speed_x
        ball.top += ball_speed_y

        # ボールと壁の衝突判定
        if ball.left <= 0:
            ball.left = 0
            ball_speed_x = -ball_speed_x
        elif ball.right >= screen_width:
            ball.right = screen_width
            ball_speed_x = -ball_speed_x

        if ball.top <= 0:
            ball.top = 0
            ball_speed_y = -ball_speed_y

        elif ball.bottom >= screen_height:
            game_state = GAME_OVER
        
    # ボールとパドルの衝突判定
    if ball.colliderect(paddle):
        hit_position = (ball.left + ball.right) / 2 - (paddle.left + paddle.right) / 2
        ball_speed_x = hit_position * 0.3
        ball_speed_y = -ball_speed_y
    
    # ボールとブロックの衝突判定
    block_removed = False
    for row_index, row in enumerate(blocks):
        for block_index, block in enumerate(row):
            if ball.colliderect(block):
                ball_speed_y *= (1 + ball_speed_increment)
                ball_speed_y = -ball_speed_y
                blocks[row_index].pop(block_index)
                score += 100
                block_removed = True
                break
        if block_removed:
            break

    # 全てのブロックがなくなったかチェック
    all_blocks_cleared = True
    for row in blocks:
        if len(row) > 0:
            all_blocks_cleared = False
            break
    if all_blocks_cleared:
        game_state = GAME_CLEAR

    # 画面の描画
    screen.fill(black)

    if game_state == GAME_PLAYING:
        pygame.draw.rect(screen, blue, paddle)
        pygame.draw.ellipse(screen, white, ball)
        for row in blocks:
            for block in row:
                pygame.draw.rect(screen, green, block)

        # スコアの表示
        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (10, 10))

    elif game_state == GAME_OVER:
        draw_text("Game OVER", large_font, red, screen, screen_width // 2, screen_height // 2 - 50)
        draw_text(f"Final Scor: {score}", font, white, screen, screen_width // 2, screen_height // 2 + 10)
        draw_text("Press 'R' to Play Again or 'Q' to Quit", font, white, screen, screen_width // 2, screen_height // 2 + 60)
    elif game_state == GAME_CLEAR:
        draw_text("GAME CLEAR!", large_font, green, screen, screen_width // 2, screen_height // 2 - 50)
        draw_text(f"Final Score: {score}", font, white, screen, screen_width // 2, screen_height // 2 + 10)
        draw_text("Press 'R' to Play Again or 'Q' to Quit", font, white, screen, screen_width // 2, screen_height // 2 + 60)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()