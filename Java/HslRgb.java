public final class HslRgb {
    private HslRgb() {}

    public static int hslToRgb(double hue, double sat, double light) {
        // Keep hue in [0,1) then scale to [0,6)
        hue = (hue - Math.floor(hue)) * 6.0;

        double chroma = (1.0 - Math.abs(2.0 * light - 1.0)) * sat;
        double hueMod2 = hue - 2.0 * Math.floor(hue / 2.0);
        double x = chroma * (1.0 - Math.abs(hueMod2 - 1.0));

        double r = 0, g = 0, b = 0;

        if (hue < 1.0) {
            r = chroma; g = x;     b = 0;
        } else if (hue < 2.0) {
            r = x;      g = chroma; b = 0;
        } else if (hue < 3.0) {
            r = 0;      g = chroma; b = x;
        } else if (hue < 4.0) {
            r = 0;      g = x;     b = chroma;
        } else if (hue < 5.0) {
            r = x;      g = 0;     b = chroma;
        } else {
            r = chroma; g = 0;     b = x;
        }

        double m = light - chroma / 2.0;
        if (m < 0) m = 0;

        r += m;
        g += m;
        b += m;

        int ri = (int) Math.round(r * 255);
        int gi = (int) Math.round(g * 255);
        int bi = (int) Math.round(b * 255);

        return (ri << 16) | (gi << 8) | bi;
    }
}