'==========================================================
'  Particle Fire Explosion - Faithful + Flicker-Free QB64
'==========================================================

$RESIZE:ON

CONST ScrW = 800
CONST ScrH = 600
CONST NPART = 2000
CONST PI = 3.141592653589793

TYPE Particle
    x AS DOUBLE
    y AS DOUBLE
    speed AS DOUBLE
    angSpeed AS DOUBLE
    dir AS DOUBLE
END TYPE

DIM SHARED particles(0 TO NPART - 1) AS Particle
DIM SHARED buffer(0 TO ScrW * ScrH - 1) AS LONG
DIM SHARED backbuf(0 TO ScrW * ScrH - 1) AS LONG
DIM SHARED hue AS DOUBLE
DIM SHARED canvas AS LONG

RANDOMIZE TIMER

' Create the visible screen
SCREEN _NEWIMAGE(ScrW, ScrH, 32)
_TITLE "Particle Fire - Faithful QB64"

' Create off-screen image (this is what we draw into)
canvas = _NEWIMAGE(ScrW, ScrH, 32)

' Start with a clean black screen
CLS , _RGB32(0, 0, 0)
_DISPLAY

' Initialize all particles
FOR i = 0 TO NPART - 1
    CALL ParticleInit(i)
NEXT

hue = 0.0

'==================== MAIN LOOP ====================
DO
    CALL UpdateParticles
    CALL DrawParticles
    CALL Blur

    ' --- Fast copy of buffer → canvas using memory ---
    DIM src AS _MEM, dest AS _MEM
    src = _MEM(buffer())
    dest = _MEMIMAGE(canvas)
    _MEMCOPY src, src.OFFSET, src.SIZE TO dest, dest.OFFSET
    _MEMFREE src
    _MEMFREE dest

    ' Show the result
    _PUTIMAGE (0, 0), canvas
    _DISPLAY

    IF _KEYDOWN(27) THEN EXIT DO          ' ESC to quit
LOOP

' Clean up
_FREEIMAGE canvas
END

'==========================================================
'  Particle routines
'==========================================================
SUB ParticleInit (i AS LONG)
    particles(i).x = 0
    particles(i).y = 0
    particles(i).speed = 0.0001 + 0.001 * RND
    particles(i).angSpeed = 0.006 * RND
    particles(i).dir = 2 * PI * RND
END SUB

SUB UpdateParticles
    FOR i = 0 TO NPART - 1
        particles(i).x = particles(i).x + COS(particles(i).dir) * particles(i).speed
        particles(i).y = particles(i).y + SIN(particles(i).dir) * particles(i).speed

        IF particles(i).x * particles(i).x + particles(i).y * particles(i).y > 1 THEN
            particles(i).x = 0
            particles(i).y = 0
        END IF

        particles(i).dir = particles(i).dir + particles(i).angSpeed
    NEXT
END SUB

SUB DrawParticles
    hue = hue + 0.001
    IF hue >= 1 THEN hue = 0

    col&& = HslToRgb(hue, 1, 0.7)

    FOR i = 0 TO NPART - 1
        ' Original C code uses width for both axes
        x = INT(ScrW * particles(i).x) + ScrW \ 2
        y = INT(ScrW * particles(i).y) + ScrH \ 2

        IF x >= 0 AND y >= 0 AND x < ScrW AND y < ScrH THEN
            buffer(y * ScrW + x) = col&&
        END IF
    NEXT
END SUB

'==========================================================
'  HSL → RGB (same algorithm as the original C version)
'==========================================================
FUNCTION HslToRgb&& (h AS DOUBLE, s AS DOUBLE, l AS DOUBLE)
    h = (h - INT(h)) * 6
    chroma = (1 - ABS(2 * l - 1)) * s
    hueMod2 = h - 2 * INT(h / 2)
    x = chroma * (1 - ABS(hueMod2 - 1))

    IF h < 1 THEN
        r = chroma: g = x: b = 0
    ELSEIF h < 2 THEN
        r = x: g = chroma: b = 0
    ELSEIF h < 3 THEN
        r = 0: g = chroma: b = x
    ELSEIF h < 4 THEN
        r = 0: g = x: b = chroma
    ELSEIF h < 5 THEN
        r = x: g = 0: b = chroma
    ELSE
        r = chroma: g = 0: b = x
    END IF

    m = l - chroma / 2
    IF m < 0 THEN m = 0

    ri = INT((r + m) * 255 + 0.5)
    gi = INT((g + m) * 255 + 0.5)
    bi = INT((b + m) * 255 + 0.5)

    HslToRgb&& = _RGB32(ri, gi, bi)
END FUNCTION

'==========================================================
'  Exact 3-pixel box blur from the original C program
'==========================================================
SUB Blur
    ' Horizontal pass
    FOR y = 0 TO ScrH - 1
        sumR = 0: sumG = 0: sumB = 0

        FOR x = 0 TO ScrW - 1
            IF x > 1 THEN
                c&& = buffer(y * ScrW + (x - 2))
                sumR = sumR - _RED32(c&&)
                sumG = sumG - _GREEN32(c&&)
                sumB = sumB - _BLUE32(c&&)
            END IF

            IF x = 0 THEN
                c&& = buffer(y * ScrW)
                sumR = sumR + _RED32(c&&)
                sumG = sumG + _GREEN32(c&&)
                sumB = sumB + _BLUE32(c&&)
            END IF

            IF x < ScrW - 1 THEN
                c&& = buffer(y * ScrW + (x + 1))
                sumR = sumR + _RED32(c&&)
                sumG = sumG + _GREEN32(c&&)
                sumB = sumB + _BLUE32(c&&)
            END IF

            IF x = 0 OR x = ScrW - 1 THEN count = 2 ELSE count = 3

            backbuf(y * ScrW + x) = _RGB32(sumR \ count, sumG \ count, sumB \ count)
        NEXT
    NEXT

    ' Vertical pass
    FOR x = 0 TO ScrW - 1
        sumR = 0: sumG = 0: sumB = 0

        FOR y = 0 TO ScrH - 1
            IF y > 1 THEN
                c&& = backbuf((y - 2) * ScrW + x)
                sumR = sumR - _RED32(c&&)
                sumG = sumG - _GREEN32(c&&)
                sumB = sumB - _BLUE32(c&&)
            END IF

            IF y = 0 THEN
                c&& = backbuf(x)
                sumR = sumR + _RED32(c&&)
                sumG = sumG + _GREEN32(c&&)
                sumB = sumB + _BLUE32(c&&)
            END IF

            IF y < ScrH - 1 THEN
                c&& = backbuf((y + 1) * ScrW + x)
                sumR = sumR + _RED32(c&&)
                sumG = sumG + _GREEN32(c&&)
                sumB = sumB + _BLUE32(c&&)
            END IF

            IF y = 0 OR y = ScrH - 1 THEN count = 2 ELSE count = 3

            buffer(y * ScrW + x) = _RGB32(sumR \ count, sumG \ count, sumB \ count)
        NEXT
    NEXT
END SUB