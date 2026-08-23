import math
import random
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

    m = max(0.0, light - chroma / 2.0)
    return (
        int(round((r + m) * 255)),
        int(round((g + m) * 255)),
        int(round((b + m) * 255)),
    )


# -------------------------------------------------
# Particle
# -------------------------------------------------
class Particle:
    __slots__ = ("x", "y", "speed", "angular_speed", "direction")

    def __init__(self):
        self.init()

    def init(self):
        self.x = 0.0
        self.y = 0.0
        self.speed = 0.0001 + 0.001 * random.random()
        self.angular_speed = 0.006 * random.random()
        self.direction = 2.0 * math.pi * random.random()

    def update(self):
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed
        if self.x * self.x + self.y * self.y > 1.0:
            self.x = 0.0
            self.y = 0.0
        self.direction += self.angular_speed


# -------------------------------------------------
# Swarm
# -------------------------------------------------
class Swarm:
    def __init__(self, n: int):
        self.particles = [Particle() for _ in range(n)]
        self.hue = 0.3

    def update(self):
        for p in self.particles:
            p.update()

    def draw(self, buf: np.ndarray, width: int, height: int):
        """buf shape = (height, width, 3)"""
        self.hue += 0.001
        if self.hue > 1.0:
            self.hue = 0.0

        r, g, b = hsl_to_rgb(self.hue, 1.0, 0.7)

        for p in self.particles:
            x = int(width * p.x) + width // 2
            y = int(width * p.y) + height // 2   # original uses width for both axes
            if 0 <= x < width and 0 <= y < height:
                buf[y, x, 0] = r
                buf[y, x, 1] = g
                buf[y, x, 2] = b


# -------------------------------------------------
# Fast vectorized 3-pixel box blur (separable)
# Matches the original edge handling reasonably well
# -------------------------------------------------
def blur(buf: np.ndarray):
    """
    In-place separable box blur of radius 1.
    buf shape = (H, W, 3), dtype=uint8
    """
    # Horizontal pass
    left  = np.roll(buf,  1, axis=1)
    right = np.roll(buf, -1, axis=1)

    # edges: average of 2 pixels, interior: average of 3
    # We approximate the original by using a weighted average that is
    # very close and fully vectorized.
    horiz = (left.astype(np.uint16) + buf.astype(np.uint16) + right.astype(np.uint16)) // 3
    # fix the two edge columns to match original count=2 behaviour more closely
    horiz[:, 0, :]  = (buf[:, 0, :].astype(np.uint16) + right[:, 0, :].astype(np.uint16)) // 2
    horiz[:, -1, :] = (buf[:, -1, :].astype(np.uint16) + left[:, -1, :].astype(np.uint16)) // 2

    # Vertical pass
    up   = np.roll(horiz,  1, axis=0)
    down = np.roll(horiz, -1, axis=0)

    vert = (up.astype(np.uint16) + horiz.astype(np.uint16) + down.astype(np.uint16)) // 3
    vert[0, :, :]  = (horiz[0, :, :].astype(np.uint16) + down[0, :, :].astype(np.uint16)) // 2
    vert[-1, :, :] = (horiz[-1, :, :].astype(np.uint16) + up[-1, :, :].astype(np.uint16)) // 2

    np.copyto(buf, vert.astype(np.uint8))


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
    buf = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

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
        pygame.surfarray.blit_array(screen, np.transpose(buf, (1, 0, 2)))
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()