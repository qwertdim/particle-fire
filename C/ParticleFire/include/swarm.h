#ifndef SWARM_H_INCLUDED_
#define SWARM_H_INCLUDED_

#include "graphics.h"

typedef struct
{
    int num_particles;
    float *x;
    float *y;
    float *speed;
    float *angular_speed;
    float *direction;
    float buffer[1];
} swarm_t;

swarm_t *swarm_create(int num_particles);
void swarm_draw(const swarm_t *s, gs_graphics *g);
void swarm_update(swarm_t *s);
void swarm_dispose(swarm_t *s);

#endif // SWARM_H_INCLUDED_