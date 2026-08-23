public class Particle {
    double x, y;
    double speed;
    double angularSpeed;
    double direction;

    public void init() {
        x = 0;
        y = 0;
        speed = 0.0001 + 0.001 * Math.random();
        angularSpeed = 0.006 * Math.random();
        direction = 2 * Math.PI * Math.random();
    }

    public void update() {
        x += Math.cos(direction) * speed;
        y += Math.sin(direction) * speed;

        if (x * x + y * y > 1.0) {
            x = 0;
            y = 0;
        }

        direction += angularSpeed;
    }
}