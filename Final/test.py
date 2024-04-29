import pygame

def calculate_new_xy(old_xy, speed, angle_in_degrees):
    move_vec = pygame.math.Vector2()
    move_vec.from_polar((speed, angle_in_degrees))
    return old_xy + move_vec

class Bullet:
    def __init__(self, x, y, direction, speed):
        self.image = pygame.Surface((16, 8), pygame.SRCALPHA)
        self.image.fill((255, 0, 0))
        self.image = pygame.transform.rotate(self.image, direction)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.Vector2(x, y)
        self.direction = direction
        self.speed = speed

    def update(self, screen_rect):
        self.pos = calculate_new_xy(self.pos, self.speed, -self.direction)
        self.rect.center = round(self.pos[0]), round(self.pos[1])
        if not screen_rect.colliderect(self.rect):
            return True  # Indicates bullet is out of screen
        return False

pygame.init()
screen = pygame.display.set_mode((320, 240))
clock = pygame.time.Clock()
bullets = []
play = True
frame_count = 0
while play:
    clock.tick(60)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            play = False
    
    for bullet in bullets[:]:  # Iterate over a copy to allow removal from the original list
        if bullet.update(screen.get_rect()):
            bullets.remove(bullet)

    if (frame_count % 10) == 0:
        bullets.append(Bullet(*screen.get_rect().center, frame_count, 2))

    frame_count += 1

    screen.fill((0, 0, 0))
    for bullet in bullets:
        screen.blit(bullet.image, bullet.rect)

    pygame.draw.circle(screen, (64, 128, 255), screen.get_rect().center, 10)
    pygame.display.flip()

pygame.quit()
exit()