import pygame
import sys
import random
import time

# Pygameの初期化
pygame.init()

# 画面サイズとタイトルの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("シューティングゲーム")

# 色の定義
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# ゲームのフレームレート設定
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # プレイヤーの画像や形状を設定
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 50)
        self.speed = 5
        self.bullet_group = pygame.sprite.Group()
        self.shoot_delay = 200  # 弾の発射間隔（ミリ秒）
        self.last_shot_time = 0  # 最後に弾を発射した時刻

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

        # スペースキーで弾を発射
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > self.shoot_delay:
                self.shoot()
                self.last_shot_time = current_time
                if self.shoot_delay > 75:
                    self.shoot_delay -= 0.5

        if keys[pygame.K_a]:
            time.sleep(0.05)

        # 弾の更新
        self.bullet_group.update()

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.bullet_group.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))  # 弾の画像や形状を設定
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        # 画面外に出たら削除する
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))  # 敵の画像や形状を設定
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed = random.randrange(1, 5)

    def update(self):
        self.rect.y += self.speed
        self.speed += 0.1
        if self.rect.top > screen_height + 10:
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed = random.randrange(1, 5)

# スプライトグループの作成
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
enemies = pygame.sprite.Group()

# 最初に5つの敵を生成してスプライトグループに追加
for _ in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# 衝突判定の関数
def check_collision(player, enemies):
    return pygame.sprite.spritecollide(player, enemies, True)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # 画面を黒で塗りつぶす

        # ゲームの更新
        player.update()
        enemies.update()

        # 弾の敵との衝突判定
        if pygame.sprite.groupcollide(player.bullet_group, enemies, True, True):
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            if random.random() <= 0.25:
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)

        # スプライトの描画
        all_sprites.draw(screen)
        player.bullet_group.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # FPSを60に設定
        # 衝突判定
        hits = check_collision(player, enemies)
        for hit in hits:
            new_enemy = Enemy()
            all_sprites.add(new_enemy)
            enemies.add(new_enemy)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


# player_rect = pygame.Rect(200, 300, 50, 50)
# enemy_rect = pygame.Rect(400, 300, 50, 50)

# if player_rect.colliderect(enemy_rect):
#         print("衝突しました！")

# pygame.draw.rect(screen, RED, player_rect)
# pygame.draw.rect(screen, RED, enemy_rect)