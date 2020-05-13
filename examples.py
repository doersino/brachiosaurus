import brachiosaurus as bs  # heartbreakingly, python won't accept 🦕 as an alias

import math
import random

𝕣 = random.random
τ = 2 * math.pi

def spiral_mountain(c):
    """
    First shot at implementing spirals, looks a bit like an inverted mountain.
    """

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
    """Second try, looks like the Debian logo."""

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
    """Third try, looks like a rose."""

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
    """Test pattern for various primitives."""

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
    """Grid of spirals with increasing winding numbers."""

    x = 5
    y = 2
    for i in range(1, x * y + 1):
        c.spiral(((i - 1) % x) * 9, int((i - 1) / x) * 9, i, 4 / i)

def circle_heart(c):
    """
    Concentric circles, only parts of which are drawn closer to the center,
    yielding a vaguely heart-shaped negative space.
    """

    for i in range(15):
        c.arc(0, 0, i + 2, τ/2 - (τ/2 * ((i+1) / 15)), τ/2 + (τ/2 * ((i+1) / 15)))

def spiral_row(c):
    """Diagonal row of ever-more-spiraly spirals."""
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
    """Radial lines, with an interruption."""

    def xy(r, a):
        x = r * math.cos(a)
        y = r * math.sin(a)
        return [x, y]

    m = 36 * 5

    for i in range(0, m):
        a = τ * (i / m)
        r1 = 6 + 𝕣() * 2
        r2 = 4 + 𝕣()
        r4 = 3 + 𝕣()
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
    """
    Trojaborg labyrinth, take 1 (drawn in an order that was easy to generate,
    but thus with lots of unnecessary pen movements), see:
    https://i.pinimg.com/originals/db/5f/e7/db5fe768cf21d0fd00a7f6be6ca43c73.jpg
    """

    # TODO make its size parametric (this one is an 11-ring variant, other variants exist: https://en.wikipedia.org/wiki/Troy_Town)

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
    """
    Trojaborg labyrinth, take 2 (correct drawing order), can be drawn next to
    take 1 (hence xoff) to show differences due to pen up/down inaccuracies.
    """

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

def wiki_spiral(c):
    """
    Fancy spiral thingy, via
    https://commons.wikimedia.org/wiki/File:Turtle_Graphics_Spiral.svg.
    """

    def xy(r, a):
        x = r * math.cos(a)
        y = r * math.sin(a)
        return [x, y]

    #angles = [0, τ/3, 2*τ/3]
    #angles = [0, τ/4, τ/2, 3*τ/4]
    corners = 3
    #corners = 2
    #corners = 10
    angles = [a/corners * τ for a in range(corners)]
    turns = 3
    m = 40
    for i in range(m):
        for j, angle in enumerate(angles):
            r = m - i - j/3
            a = angle + turns * i/m
            [x,y] = xy(r, a)
            if (j == 0 and i == 0):
                c.move(x, y)
            else:
                c.line(x, y)

def overlaid_3dish_balls(c):
    def xy(r, a):
        x = r * math.cos(a)
        y = r * math.sin(a)
        return [x, y]

    m = 30
    for i in range(m):
        a1 = τ/2 * i/m
        a2 = -a1 - math.sin(a1)
        r = 10

        [x,y] = xy(r, a1)
        c.move(x,y)
        [x,y] = xy(r, a2)
        c.line(x,y)
        [x,y] = xy(2*r/3, a1+τ/4)
        c.move(x,y)
        [x,y] = xy(2*r/3, a2+τ/4)
        c.line(x,y)

def line_circles(c):
    """
    Circles made up of lines, via
    https://twitter.com/generativehut/status/1257576360933023744 and
    https://stackoverflow.com/a/14310071.
    """

    # TODO could do this with multiple colors, one for each circle

    nm = 5
    mm = (nm-2)*7
    ro = 10
    for n in range(nm):
        r = ro * 2*n/3
        m = int(mm * r/ro)
        for i in range(1, m):
            x = -r + 2 * r * i/m
            y = math.sqrt(r ** 2 - x ** 2)
            c.move(x+n/nm,y - r)
            c.line(x+n/nm,-y - r)

def hatched_circle(c):
    for n in range(5):
        m = 2*(2 ** n)
        r = 10
        for i in range(1, m):
            x = -r + 2 * r * i/m
            y = math.sqrt(r ** 2 - x ** 2)
            c.move(x - r, y - r)
            c.line(x - r, -y - r)
        for i in range(1, m):
            y = -r + 2 * r * i/m
            x = math.sqrt(r ** 2 - y ** 2)
            c.move(x - r, y - r)
            c.line(-x - r, y - r)

def ca(c):
    """Elementary cellular automaton."""

    random.seed(42)

    # config
    rules = [11,26,30,57,60,90,106,150]
    #rules = [60]
    width = 15
    height = 30

    # state keeping
    rule = {}
    state = []
    log = []

    # process rule
    rule_choice = random.choice(rules)
    bin_rule_choice = list("{:08b}".format(rule_choice))
    for i, ru in enumerate(bin_rule_choice):
        rule["{:03b}".format(i)] = ru

    # init ca
    for _ in range(width):
        state.append("1" if 𝕣() > 0.5 else "0")
    log.append(state)

    # run ca
    while len(log) < height:
        state2 = []
        for i, _ in enumerate(state):
            left = (i - 1) % len(state)
            middle = i
            right = (i + 1) % len(state)

            neighborhood = state[left] + state[middle] + state[right]

            state2.append(rule[neighborhood])
        state = state2
        log.append(state2)

    for y, st in enumerate(log):
        for x, ce in enumerate(st):
            if ce == "1":
                c.circle(x, y, 0.5, 0.03)

def uji(c):
    """https://en.m.wikipedia.org/wiki/Uji_(Being-Time)"""

    m = 4
    d = 12

    for i in range(m):
        i = i/d
        c.move(0+i, 0)
        c.line(0+i, 2)
        c.arc(0.75, 2, -0.75+i, 0, τ/2)
        c.line(1.5-i, 0)

    for i in range(m):
        i = i/d
        c.move(2-i, 0)
        c.line(2-i, 2)
        c.arc(0.75, 2, 1.25-i, 0, τ/4)

    for i in range(m):
        i = i/d
        c.move(2.5-i, 0)
        c.line(2.5-i, 2)

def overlapping_circles(c):
    for i in range(10):
        c.arc(1, 0, -math.sqrt(i+1)/math.sqrt(10), 0, τ)
    c.arc(2, 0, -1, 0, τ/3)
    c.arc(2, 0, -1, 2*τ/3, τ)

def moire_spirals(c):
    """An attempt to create Moiré patterns using spirals."""

    for i in range(4):
        c.spiral(0, i, 10, 1, 0.3)

c = bs.Canvas()

#uji(c)
trojaborg_labyrinth_2(c)

#plotter = bs.AutoPlotter().from_file("test-patterns/accuracy.json")
plotter = bs.AutoPlotter().from_canvas(c)
plotter.emit()
