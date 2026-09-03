

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "include/hslrgb.h"
#include "include/swarm.h"

#define PI 3.141592

static void update_x(float *x, const float *speed, const float *direction, int num_particles)
{
    for (int i = 0; i < num_particles; ++i)
    {
        x[i] += cosf(direction[i]) * speed[i];
    }
}

static void update_y(float *y, const float *speed, const float *direction, int num_particles)
{
    for (int i = 0; i < num_particles; ++i)
    {
        y[i] += sinf(direction[i]) * speed[i];
    }
}

static void update_position(float *x, float *y, int num_particles)
{
    for (int i = 0; i < num_particles; ++i)
    {
        if (x[i] * x[i] + y[i] * y[i] > 1)
        {
            x[i] = 0;
            y[i] = 0;
        }
    }
}

static void update_direction(float *direction, const float *angular_speed, int num_particles)
{
    for (int i = 0; i < num_particles; ++i)
    {
        direction[i] += angular_speed[i];
    }
}

swarm_t *swarm_create(int num_particles)
{
    swarm_t *s = (swarm_t *)malloc(sizeof(swarm_t) + 5 * num_particles * sizeof(float));
    s->num_particles = num_particles;
    s->x = (float *)(s->buffer);
    s->y = (float *)(s->buffer + num_particles);
    s->speed = (float *)(s->buffer + 2 * num_particles);
    s->angular_speed = (float *)(s->buffer + 3 * num_particles);
    s->direction = (float *)(s->buffer + 4 * num_particles);

    memset(s->x, 0, 2 * s->num_particles * sizeof(float));
    for (int i = 0; i < num_particles; ++i)
    {
        s->speed[i] = 0.0001 + 0.001 * rand() / RAND_MAX;
        s->angular_speed[i] = 0.006 * rand() / RAND_MAX;
        s->direction[i] = 2 * PI * rand() / RAND_MAX;
    }

    return s;
}

void swarm_update(swarm_t *s)
{
    update_x(s->x, s->speed, s->direction, s->num_particles);
    update_y(s->y, s->speed, s->direction, s->num_particles);
    update_position(s->x, s->y, s->num_particles);
    update_direction(s->direction, s->angular_speed, s->num_particles);
}

void swarm_draw(const swarm_t *s, gs_graphics *g)
{
    static double hue = 0.3;
    hue += 0.001;
    if (hue > 1)
        hue = 0;

    int width = g->surface->pitch / sizeof(uint32_t);
    for (int i = 0; i < s->num_particles; ++i)
    {
        int x = (int)(g->width * s->x[i]) + g->width / 2;
        int y = (int)(g->width * s->y[i]) + g->height / 2;

        uint32_t color = hsl_to_rgb(hue, 1, 0.7);
        if (x >= 0 && y >= 0 && x < g->width && y < g->height)
            ((uint32_t *)g->surface->pixels)[y * width + x] = color;
    }
}

void swarm_dispose(swarm_t *swarm)
{
    free(swarm);
}
