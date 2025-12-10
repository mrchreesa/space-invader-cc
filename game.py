import pygame
import random
import sys
import os

# === STEP 1: Setup Window & Constants ===
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 255, 0)
BULLET_COLOR = (0, 0, 255)
ENEMY_COLOR = (255, 0, 0)

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, "2DSpaceShooterStarBlaster")
SOUNDS_DIR = os.path.join(SCRIPT_DIR, "sounds")

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Shooter - Coding Club")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# === Load Sound Effects ===
shoot_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "shoot.wav"))
explosion_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "explosion.wav"))
gameover_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "gameover.wav"))
shoot_sound.set_volume(0.3)
explosion_sound.set_volume(0.5)
gameover_sound.set_volume(0.7)

# === Load Sprites ===
def load_sprite(folder, filename, scale=None, rotate=0):
    """Load a sprite image and optionally scale/rotate it."""
    path = os.path.join(ASSETS_DIR, folder, filename)
    image = pygame.image.load(path).convert_alpha()
    if rotate:
        image = pygame.transform.rotate(image, rotate)
    if scale:
        image = pygame.transform.scale(image, scale)
    return image

# Load sprite images
player_img = load_sprite("Ships", "Spaceship.png", (60, 60))
bullet_img = load_sprite("Effects", "blast00010001.png", (15, 30))
enemy_img = load_sprite("Ships", "Spaceship5.png", (50, 50), rotate=180)

# Load background
try:
    bg = load_sprite("BGS", os.listdir(os.path.join(ASSETS_DIR, "BGS"))[0], (WIDTH, HEIGHT))
except:
    bg = None

def main():
    global running
    
    # === STEP 2: Add Player ===
    player = pygame.Rect(WIDTH // 2 - 30, HEIGHT - 70, 60, 60)
    player_speed = 5

    # === STEP 3: Shooting Bullets ===
    bullets = []
    shoot_cooldown = 0

    # === STEP 4: Enemies & Spawning ===
    enemies = []
    spawn_timer = 0
    score = 0

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            # === STEP 2: Player Movement ===
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.x -= player_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.x += player_speed
            player.x = max(0, min(WIDTH - player.width, player.x))

            # === STEP 3: Shooting Bullets ===
            if keys[pygame.K_SPACE] and shoot_cooldown <= 0:
                bullets.append(pygame.Rect(player.centerx - 7, player.top - 30, 15, 30))
                shoot_sound.play()
                shoot_cooldown = 10
            shoot_cooldown = max(0, shoot_cooldown - 1)

            # Update bullets
            for bullet in bullets[:]:
                bullet.y -= 12
                if bullet.top < 0:
                    bullets.remove(bullet)

            # === STEP 4: Enemies & Spawning ===
            spawn_timer += 1
            if spawn_timer > 60:
                enemies.append(pygame.Rect(random.randint(0, WIDTH - 50), -50, 50, 50))
                spawn_timer = 0

            # Update enemies
            for enemy in enemies[:]:
                enemy.y += 3
                if enemy.top > HEIGHT:
                    enemies.remove(enemy)

            # === STEP 5: Collisions & Scoring ===
            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if bullet.colliderect(enemy):
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        explosion_sound.play()
                        score += 1
                        break

            # Player-enemy collision
            for enemy in enemies[:]:
                if enemy.colliderect(player):
                    game_over = True
                    gameover_sound.play()
                    break

            # === Draw Game ===
            if bg:
                screen.blit(bg, (0, 0))
            else:
                screen.fill(BLACK)

            # Draw player (with sprite)
            screen.blit(player_img, player)

            # Draw bullets (with sprite)
            for bullet in bullets:
                screen.blit(bullet_img, bullet)

            # Draw enemies (with sprite)
            for enemy in enemies:
                screen.blit(enemy_img, enemy)

            # Draw score
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

        else:
            # === STEP 6: Game Over Screen ===
            screen.fill(BLACK)
            game_over_text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))
            restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - 200, HEIGHT // 2 + 40))

            # Handle restart/quit
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                main()  # Restart the game
                return
            if keys[pygame.K_q]:
                running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
