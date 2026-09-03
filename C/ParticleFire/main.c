#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "include/graphics.h"
#include "include/swarm.h"

int main(int argc, char **argv)
{
    const int width = 800;
    const int height = 600;
    const int nparticles = 2000;
    bool uncapped = false;

    for (int i = 1; i < argc; i++)
    {
        if (strcmp(argv[i], "--uncapped") == 0)
        {
            uncapped = true;
        }
        else
        {
            fprintf(stderr, "Usage: %s [--uncapped]\n", argv[0]);
            return 1;
        }
    }

    gs_graphics *g = gs_init_graphics("Particle Fire", width, height);
    swarm_t *swarm = swarm_create(nparticles);

    uint64_t fps_start = SDL_GetTicksNS();
    uint64_t fps_frames = 0;
    bool fps_reported = false;

    while (gs_poll_events(g))
    {
        const int64_t now = SDL_GetTicksNS();
        swarm_update(swarm);
        swarm_draw(swarm, g);
        graphics_blur(g);
        gs_draw(g);

        if (!uncapped)
        {
            const int64_t delay = now - (int64_t)SDL_GetTicksNS() + 16600000;
            if (delay > 0)
                SDL_DelayNS(delay);
        }
        fps_frames++;
        const uint64_t fps_now = SDL_GetTicksNS();
        const uint64_t fps_elapsed = fps_now - fps_start;
        if (fps_elapsed >= SDL_NS_PER_SECOND)
        {
            double fps = (double)fps_frames * (double)SDL_NS_PER_SECOND /
                         (double)fps_elapsed;
            printf("\rFPS: %6.1f", fps);
            fflush(stdout);
            fps_start = fps_now;
            fps_frames = 0;
            fps_reported = true;
        }
    }

    if (fps_reported)
    {
        putchar('\n');
    }

    gs_dispose_graphics(g);
    swarm_dispose(swarm);
    return 0;
}
