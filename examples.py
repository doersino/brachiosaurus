import brachiosaurus as bs  # heartbreakingly, python won't accept 🦕 as an alias

import math
import random

𝕣 = random.random
τ = 2 * math.pi

def spiral_mountain(c):
    """first try at implementing spirals, looks a bit like an inverted mountain"""

    cx = 0
    cy = 0
    w = 10
    j = 1
    detail = 0.1

    increment = τ / (360 * detail)

    n = 0
    while n < w:
        r = j * n % 1
        s = n % 1
        e = (n + increment) % 1
        c.arc(cx, cy, r, s, e, detail)
        n += increment

def spiral_debian(c):
    """second try at implementing spirals, looks like the debian logo"""

    cx = 0
    cy = 0
    w = 10
    j = 1
    detail = 0.1

    increment = τ / (360 * detail)

    n = 0
    while n < w:
        r = j * n % 1
        s = (n % 1 * τ)
        e = ((n + increment) % 1) * τ
        if (s <= e):
            c.arc(cx, cy, r, s, e, detail)
        else:
            c.arc(cx, cy, r, s, τ, detail)
            c.arc(cx, cy, r, 0, e, detail)
        n += increment

def spiral_rose(c):
    """third try at implementing spirals, looks like a rose"""

    cx = 0
    cy = 0
    w = 10
    j = 1
    detail = 0.1

    def xy(r, a):
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        return [x, y]

    increment = τ / (360 * detail)

    c.move(cx, cy)

    n = 0
    while n < w:
        r = (n / w) * j
        a = (n % 1) * τ
        [x, y] = xy(r, a)
        c.line(x, y)
        n += increment
    [x, y] = xy(j, 0)
    c.line(x, y)

def lines_boxes_arcs(c):
    """test pattern for various primitives"""

    for i in range(0,10):
        c.line(𝕣()*2, 𝕣())
    for i in range(0,10):
        x = 𝕣()*2
        y = 𝕣()
        c.rect(x, y, x + 𝕣(), y + 𝕣())
    for i in range(0,10):
        c.arc(𝕣()*2, 𝕣(), 𝕣() / 2, i, i * 2)

def concentric_circles(c):
    for i in range(0, 10):
        c.circle(0, 0, i + 2)

def spiral_grid(c):
    """grid of spirals with increasing winding numbers"""

    x = 5
    y = 2
    for i in range(1, x * y + 1):
        c.spiral(((i - 1) % x) * 9, int((i - 1) / x) * 9, i, 4 / i)

def circle_heart(c):
    """concentric circles, only parts of which are drawn closer to the center,
    yielding a vaguely heart-shaped negative space"""

    for i in range(15):
        c.arc(0, 0, i + 2, τ/2 - (τ/2 * ((i+1) / 15)), τ/2 + (τ/2 * ((i+1) / 15)))

def spiral_row(c):
    """diagonal row of ever-more-spiraly spirals"""
    for i in range(4, 21):
        c.spiral(2*i, i, i/7, 0.5)

def radial_lines(c):
    def xy(r, a):
        x = r * math.cos(a)
        y = r * math.sin(a)
        return [x, y]

    m = 36 * 2
    for i in range(0, m):
        a = τ * (i / m)
        r1 = 1 + 𝕣()
        r2 = 6 + 𝕣() * 2
        [x, y] = xy(r2, a)
        c.move(x, y)
        [x, y] = xy(r1, a)
        c.line(x, y)

def raidal_lines_interrupted(c):
    """radial lines, with an interruption"""

    def xy(r, a):
        x = r * math.cos(a)
        y = r * math.sin(a)
        return [x, y]

    m = 36 * 5

    for i in range(0, m):
        a = τ * (i / m)
        r1 = 6 + 𝕣() * 2
        r2 = 4 + 𝕣()
        r4 = 3 + 𝕣()  # shoulda swapped r4 and r3 variable names at the start of this and the following line
        r3 = 1 + 𝕣()
        [x, y] = xy(r1, a)
        c.move(x, y)
        [x, y] = xy(r2, a)
        c.line(x, y)
        [x, y] = xy(r3, a)
        c.move(x, y)
        [x, y] = xy(r4, a)
        c.line(x, y)

def concentric_squares(c):
    m = 20
    for i in range(2, m):
        c.rect(m - i, m - i, m + i, m + i)

def cog(c):
    def xy(r, a):
        x = r * math.cos(a)
        y = r * math.sin(a)
        return [x, y]

    r = 40
    t = int(r * 0.35)
    l = 1/t * τ * 0.5
    prev = 0
    for j in range(t):
        c.arc(0, 0, r, prev, prev + l)
        [x, y] = xy(r - 8, prev + l)
        c.line(x, y)
        c.arc(0, 0, r - 8, prev + l, prev + 2 * l)
        [x, y] = xy(r, prev + 2 * l)
        c.line(x, y)
        prev += 1/t * τ
    c.circle(0, 0, 5)

def trojaborg_labyrinth_1(c):
    """trojaborg labyrinth, take 1 (drawn in an order that was easy to generate,
    but thus with lots of unnecessary pen movements), see
    https://i.pinimg.com/originals/db/5f/e7/db5fe768cf21d0fd00a7f6be6ca43c73.jpg
    """
    d = 5 * τ

    # top half
    for i in range(1, 13):
        c.arc(-0.5, 0, i-0.5, τ/2, τ, i/d)

    # left half of lower center
    for i in range(1, 3):
        c.arc(-3, 0, i, 0, τ/2, i/d)

    # right half of lower center
    for i in range(1, 3):
        c.arc(3, 0, i, 0, τ/2, i/d)

    # most of right lower quarter
    for i in range(3, 10):
        c.arc(-3, 0, i, τ/4, τ/2, i/d)

    # left part of right lower quarter
    for i in range(1, 3):
        c.arc(-3, 6, i, 3*τ/4, τ+τ/4, i/d)

    # most of left lower quarter
    for i in range(3, 9):
        c.arc(3, 0, i, 0, τ/4, i/d)

    # right part of left lower quarter
    for i in range(1, 3):
        c.arc(3, 6, i, τ/4, 3*τ/4, i/d)

    # vertical line from center to bottom
    c.move(0, 0)
    c.line(0, 6)

    # horizontal line from below center left to below center right
    c.move(-3, 3)
    c.line(3, 3)

    # arc connecting left half to center
    c.arc(-3, 6, 3, 0, τ/4, i/d)

def trojaborg_labyrinth_2(c):
    """trojaborg labyrinth, take 2 (correct drawing order), can be drawn next to
    take 1 to show differences due to pen up/down inaccuracies"""

    xoff = 24

    c.arc(xoff-0.5, 0, 3-0.5, τ/2, τ)
    c.arc(xoff+3, 0, -1, 0, τ/2)
    c.arc(xoff-0.5, 0, -(5-0.5), τ/2, τ)
    c.arc(xoff-3, 0, -2, 0, τ/2)
    c.arc(xoff-0.5, 0, 1-0.5, τ/2, τ)
    c.line(xoff+0, 6)
    c.arc(xoff-3, 6, 3, 0, τ/4)
    c.arc(xoff-3, 0, 9, τ/4, τ/2)
    c.arc(xoff-0.5, 0, 12-0.5, τ/2, τ)
    c.arc(xoff+3, 0, 8, 0, τ/4)
    c.arc(xoff+3, 6, 2, τ/4, 3*τ/4)
    c.arc(xoff+3, 0, -4, 0, τ/4)
    c.arc(xoff-0.5, 0, -(8-0.5), τ/2, τ)
    c.arc(xoff-3, 0, -5, τ/4, τ/2)
    c.arc(xoff-3, 6, 1, 3*τ/4, τ+τ/4)
    c.arc(xoff-3, 0, 7, τ/4, τ/2)
    c.arc(xoff-0.5, 0, 10-0.5, τ/2, τ)
    c.arc(xoff+3, 0, 6, 0, τ/4)

    c.arc(xoff-0.5, 0, -(4-0.5), τ/2, τ)
    c.arc(xoff-3, 0, -1, 0, τ/2)
    c.arc(xoff-0.5, 0, 2-0.5, τ/2, τ)
    c.arc(xoff+3, 0, -2, 0, τ/2)
    c.arc(xoff-0.5, 0, -(6-0.5), τ/2, τ)
    c.arc(xoff-3, 0, -3, τ/4, τ/2)
    c.line(xoff+3, 3)
    c.arc(xoff+3, 0, -3, 0, τ/4)
    c.arc(xoff-0.5, 0, -(7-0.5), τ/2, τ)
    c.arc(xoff-3, 0, -4, τ/4, τ/2)
    c.arc(xoff-3, 6, 2, 3*τ/4, τ+τ/4)
    c.arc(xoff-3, 0, 8, τ/4, τ/2)
    c.arc(xoff-0.5, 0, 11-0.5, τ/2, τ)
    c.arc(xoff+3, 0, 7, 0, τ/4)
    c.arc(xoff+3, 6, 1, τ/4, 3*τ/4)
    c.arc(xoff+3, 0, -5, 0, τ/4)
    c.arc(xoff-0.5, 0, -(9-0.5), τ/2, τ)
    c.arc(xoff-3, 0, -6, τ/4, τ/2)




c = bs.Canvas()

trojaborg_labyrinth_2(c)

plotter = bs.AutoPlotter().from_canvas(c)
#plotter = AutoPlotter().from_file("test-patterns/accuracy.json")
plotter.emit()


# TODO labyrinth: make heuristic that turns generated one into hand-coded one, make its size parametric. also why does move not seem to terminate lines?

# TODO from noahdoersing.com: raindrops, labyrinth, asteroids?
# TODO some ca or gol
# TODO anything from https://read.leakyabstraction.dev/index.php?state=unread&s=inconvergent.net
# TODO plotter self portrait: pic from top down, plotted using brachiograph's built-in vectorization routine
# TODO something with multiple colors/pens, maybe https://twitter.com/generativehut/status/1257576360933023744
# TODO https://www.instagram.com/p/B-E3yNNnxOv/?igshid=s95k17q53crp
# TODO https://twitter.com/KevinsPlots/status/1257389550382571520
# TODO https://twitter.com/KevinsPlots/status/1257424415375138816
# TODO boids