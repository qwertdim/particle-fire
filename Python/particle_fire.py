import math
import numpy as np
import pygame

# -------------------------------------------------
# HSL → RGB (returns R, G, B as ints 0-255)
# -------------------------------------------------
def hsl_to_rgb(hue: float, sat: float, light: float):
    hue = (hue - math.floor(hue)) * 6.0
    chroma = (1.0 - abs(2.0 * light - 1.0)) * sat
    hue_mod_2 = hue - 2.0 * math.floor(hue / 2.0)
    x = chroma * (1.0 - abs(hue_mod_2 - 1.0))

    if hue < 1.0:
        r, g, b = chroma, x, 0.0
    elif hue < 2.0:
        r, g, b = x, chroma, 0.0
    elif hue < 3.0:
        r, g, b = 0.0, chroma, x
    elif hue < 4.0:
        r, g, b = 0.0, x, chroma
    elif hue < 5.0:
        r, g, b = x, 0.0, chroma
    else:
        r, g, b = chroma, 0.0, x

    m = light - chroma / 2.0
    if m < 0.0:
        m = 0.0

    return (r + m) * 255, (g + m) * 255, (b + m) * 255


# -------------------------------------------------
# Swarm
# -------------------------------------------------
class Swarm:
    def __init__(self, n: int):
        rng = np.random.default_rng()
        self.particles_x = np.zeros(n, dtype=np.float32)
        self.particles_y = np.zeros(n, dtype=np.float32)
        self.particles_speed = rng.uniform(0.0001, 0.0011, n)
        self.particles_angular_speed = rng.uniform(0.0, 0.006, n)
        self.particles_direction = rng.uniform(0.0, np.pi * 2.0, n)
        self.hue = 0.3

    def update(self):
        self.particles_x += np.cos(self.particles_direction) * self.particles_speed
        self.particles_y += np.sin(self.particles_direction) * self.particles_speed
        mask = self.particles_x * self.particles_x + self.particles_y * self.particles_y > 1.0
        self.particles_x[mask] = 0.0
        self.particles_y[mask] = 0.0
        self.particles_direction += self.particles_angular_speed

    def draw(self, buf: np.ndarray, width: int, height: int):
        """buf shape = (height, width, 3)"""
        self.hue += 0.001
        if self.hue > 1.0:
            self.hue = 0.0

        rgb = np.array(hsl_to_rgb(self.hue, 1.0, 0.7), dtype=np.uint8)

        x = (width * self.particles_x).astype(np.int16) + width // 2
        y = (width * self.particles_y).astype(np.int16) + height // 2
        mask = (0 <= y) & (y < height) & (0 <= x) & (x < width)
        buf[x[mask], y[mask]] = rgb


# -------------------------------------------------
# Fast vectorized 3-pixel box blur (separable)
# Matches the original edge handling reasonably well
# -------------------------------------------------
def blur(buf: np.ndarray):
    """
    Separable box blur of radius 1.
    buf shape = (H, W, 3), dtype=uint8
    """
    new_buf = buf.astype(np.uint16)
    new_buf[:-1] += buf[1:]
    new_buf[1:] += buf[:-1]
    new_buf[:, :-1] += buf[:, 1:]
    new_buf[:, 1:] += buf[:, :-1]
    new_buf //= 5
    buf[:] = new_buf


# -------------------------------------------------
# Main
# -------------------------------------------------
def main():
    WIDTH, HEIGHT = 800, 600
    N_PARTICLES = 2000

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Particle Fire (fast)")
    clock = pygame.time.Clock()

    # Persistent buffer: (height, width, 3)
    buf = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)

    swarm = Swarm(N_PARTICLES)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        swarm.update()
        swarm.draw(buf, WIDTH, HEIGHT)
        blur(buf)

        # pygame.surfarray expects (width, height, 3)
        pygame.surfarray.blit_array(screen, buf)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
