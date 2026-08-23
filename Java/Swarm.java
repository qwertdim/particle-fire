public class Swarm {
    private final Particle[] particles;
    private double hue = 0.3;

    public Swarm(int n) {
        particles = new Particle[n];
        for (int i = 0; i < n; i++) {
            particles[i] = new Particle();
            particles[i].init();
        }
    }

    public void update() {
        for (Particle p : particles) {
            p.update();
        }
    }

    public void draw(Screen screen) {
        hue += 0.001;
        if (hue > 1.0) hue = 0.0;

        int color = HslRgb.hslToRgb(hue, 1.0, 0.7);
        int w = screen.getWidth();
        int h = screen.getHeight();
        int[] buffer = screen.getBuffer();

        for (Particle p : particles) {
            // Note: original C code uses width for both X and Y scaling
            int x = (int) (w * p.x) + w / 2;
            int y = (int) (w * p.y) + h / 2;

            if (x >= 0 && y >= 0 && x < w && y < h) {
                buffer[y * w + x] = color;
            }
        }
    }
}