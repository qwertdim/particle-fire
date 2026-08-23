


import javax.swing.JFrame;
import javax.swing.SwingUtilities;
import javax.swing.WindowConstants;

public class Main {
    public static void main(String[] args) {
        final int WIDTH = 800;
        final int HEIGHT = 600;
        final int N_PARTICLES = 2000;

        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("Particle Fire");
            Screen screen = new Screen(WIDTH, HEIGHT);
            Swarm swarm = new Swarm(N_PARTICLES);

            frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            frame.setResizable(false);
            frame.add(screen);
            frame.pack();
            frame.setLocationRelativeTo(null);
            frame.setVisible(true);

            // Simple uncapped game loop (close to the original SDL_Delay(2) style)
            Thread loop = new Thread(() -> {
                while (true) {
                    swarm.update();
                    swarm.draw(screen);
                    screen.blur();
                    screen.repaint();

                    try {
                        Thread.sleep(2);   // ~500 theoretical FPS, same idea as SDL_Delay(2)
                    } catch (InterruptedException e) {
                        break;
                    }
                }
            });
            loop.setDaemon(true);
            loop.start();
        });
    }
}




