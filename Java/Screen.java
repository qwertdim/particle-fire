import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.image.BufferedImage;
import java.awt.image.DataBufferInt;
import javax.swing.JPanel;

public class Screen extends JPanel {
    private final int width;
    private final int height;
    private final BufferedImage image;
    private final int[] buffer;      // main pixel buffer (persistent)
    private final int[] backBuffer;  // temporary for blur

    public Screen(int width, int height) {
        this.width = width;
        this.height = height;
        image = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        buffer = ((DataBufferInt) image.getRaster().getDataBuffer()).getData();
        backBuffer = new int[width * height];
        setPreferredSize(new Dimension(width, height));
    }

    public int getWidth()  { return width; }
    public int getHeight() { return height; }
    public int[] getBuffer() { return buffer; }

    /** Same 3-pixel box blur used in the C version (horizontal then vertical). */
    public void blur() {
        horizontalBlur(buffer, backBuffer);
        verticalBlur(backBuffer, buffer);
    }

    private void horizontalBlur(int[] input, int[] output) {
        for (int y = 0; y < height; y++) {
            int sumR = 0, sumG = 0, sumB = 0;

            for (int x = 0; x < width; x++) {
                if (x > 1) {
                    int c = input[y * width + (x - 2)];
                    sumR -= (c >> 16) & 0xFF;
                    sumG -= (c >>  8) & 0xFF;
                    sumB -=  c        & 0xFF;
                }
                if (x == 0) {
                    int c = input[y * width];
                    sumR += (c >> 16) & 0xFF;
                    sumG += (c >>  8) & 0xFF;
                    sumB +=  c        & 0xFF;
                }
                if (x < width - 1) {
                    int c = input[y * width + (x + 1)];
                    sumR += (c >> 16) & 0xFF;
                    sumG += (c >>  8) & 0xFF;
                    sumB +=  c        & 0xFF;
                }

                int count = (x == 0 || x == width - 1) ? 2 : 3;
                output[y * width + x] =
                        ((sumR / count) << 16) |
                        ((sumG / count) <<  8) |
                         (sumB / count);
            }
        }
    }

    private void verticalBlur(int[] input, int[] output) {
        for (int x = 0; x < width; x++) {
            int sumR = 0, sumG = 0, sumB = 0;

            for (int y = 0; y < height; y++) {
                if (y > 1) {
                    int c = input[(y - 2) * width + x];
                    sumR -= (c >> 16) & 0xFF;
                    sumG -= (c >>  8) & 0xFF;
                    sumB -=  c        & 0xFF;
                }
                if (y == 0) {
                    int c = input[x];
                    sumR += (c >> 16) & 0xFF;
                    sumG += (c >>  8) & 0xFF;
                    sumB +=  c        & 0xFF;
                }
                if (y < height - 1) {
                    int c = input[(y + 1) * width + x];
                    sumR += (c >> 16) & 0xFF;
                    sumG += (c >>  8) & 0xFF;
                    sumB +=  c        & 0xFF;
                }

                int count = (y == 0 || y == height - 1) ? 2 : 3;
                output[y * width + x] =
                        ((sumR / count) << 16) |
                        ((sumG / count) <<  8) |
                         (sumB / count);
            }
        }
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        g.drawImage(image, 0, 0, null);
    }

    
}


