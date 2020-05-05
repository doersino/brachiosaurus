import math
import json
import socket

PI_HOSTNAME = "raspberrypi"
BG_CONFIG = dict(
    inner_arm=8,
    outer_arm=8.5,
    bounds=[-10, 5, 6, 13],
    arm_1_centre=-90,
    arm_2_centre=90,
    servo_1_centre=1582,
    servo_2_centre=1457,
    wait=0.2,
    pw_up=1550,
    pw_down=1200
    )

TAU = 2 * math.pi

class Plotter:
    def __init__(self, lines):
        self.lines = lines

    @classmethod
    def from_canvas(cls, canvas):
        return cls(canvas.emit())

    @classmethod
    def from_file(cls, filename):
        with open(filename, "r") as f:
            return cls(json.load(f))

    def optimize(self):
        # TODO path optimization? eh
        # TODO ideally: reorder list of lines such that sum of distances between end and start points is minimal. equivalent to tsp => np-complete
        pass

    def emit(self):
        print(self.lines)

class RealPlotter(Plotter):
    def __init__(self, lines):
        super().__init__(lines)

        # import inelegantly wedged inside this class's constructor because this
        # enables use of the FakePlotter class on systems without any
        # brachiograph machinery installed
        from brachiograph import BrachioGraph

        # these settings work for my brachiograph
        self.bg = BrachioGraph(**BG_CONFIG)

    def emit(self):
        self.bg.plot_lines(self.lines)
        #self.bg.grid_lines(interpolate=400, both=True)

class FakePlotter(Plotter):
    def __init__(self, lines):
        super().__init__(lines)

    def emit(self):
        """
        TODO yellow: pen movements when up, blue: line number, purple: line segement number, green: line starting point, red: line segment point
        """
        detailed = True

        x, y, w, h = self.__viewbox()
        stroke = min(w, h) / 500

        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" style="fill: none; stroke: black; stroke-width: {stroke}px;">\n'
        if detailed:
            svg += f'<path d="M0,0'
        for n, l in enumerate(self.lines):
            x, y = l[0]
            if detailed:
                svg += f' L{x},{y}" style="stroke: rgba(255,255,0,0.5); stroke-width: {stroke/2}px;" />\n'
                svg += f'<text x="{x}" y="{y}" style="font-size: {5*stroke}px; stroke: none; fill: rgba(0,0,255,0.5);">{n}</text>\n'
                svg += f'<circle cx="{x}" cy="{y}" r="{2*stroke}" style="stroke: none; fill: rgba(0,255,0,0.5);" />\n'
                svg += f'<path d="M{x},{y}'
                for m, p in enumerate(l[1:]):
                    x, y = p
                    svg += f' L{x},{y}" />\n'
                    svg += f'<text x="{x}" y="{y}" style="font-size: {5*stroke}px; stroke: none; fill: rgba(128,128,255,0.5);">{n}~{m}</text>\n'
                    svg += f'<circle cx="{x}" cy="{y}" r="{2*stroke}" style="stroke: none; fill: rgba(255,0,0,0.5);" />\n'
                    svg += f'<path d="M{x},{y}'
                svg += f'" />\n'
                svg += f'<path d="M{x},{y}'
            else:
                svg += f'<path d="M{x},{y}'
                for p in l[1:]:
                    x, y = p
                    svg += f' L{x},{y}'
                svg += f'" />\n'
        if detailed:
            svg += f' L{0},{0}" style="stroke: rgba(255,255,0,0.5); stroke-width: {stroke/2}px;" />\n'
        svg += "</svg>\n"
        print(svg)

    def __viewbox(self):
        xmin = self.lines[0][0][0]
        xmax = self.lines[0][0][0]
        ymin = self.lines[0][0][1]
        ymax = self.lines[0][0][1]
        for l in self.lines:
            for p in l:
                if p[0] < xmin:
                    xmin = p[0]
                if p[0] > xmax:
                    xmax = p[0]
                if p[1] < ymin:
                    ymin = p[1]
                if p[1] > ymax:
                    ymax = p[1]
        return (xmin, ymin, xmax - xmin, ymax - ymin)

# TODO this would be neater as a class AutoPlotter, but I haven't found a way to make that work elegantly
def AutoPlotter():
    if socket.gethostname() == PI_HOSTNAME:
        return RealPlotter
    else:
        return FakePlotter

class Canvas:
    def __init__(self):
        # TODO optional xrange and yrange args, crop to these ranges (i.e. split crossing lines intelligently) in emit
        self.lines = []
        self.x = 0
        self.y = 0
        self.current_line = [[0, 0]]

    def emit(self):
        if len(self.current_line) > 1:
            self.lines.append(self.current_line)
            self.current_line = [[self.x, self.y]]
        return self.lines

    def __m(self, x, y):
        if len(self.current_line) > 1:
            self.lines.append(self.current_line)
        self.x = x
        self.y = y
        self.current_line = [[self.x, self.y]]

    def __l(self, x, y):
        self.current_line.append([x, y])
        self.x = x
        self.y = y

    def move(self, x, y):
        self.__m(x, y)

    def line(self, x, y):
        self.__l(x, y)

    def rect(self, x0, y0, x1, y1):
        self.__m(x0, y0)
        self.__l(x1, y0)
        self.__l(x1, y1)
        self.__l(x0, y1)
        self.__l(x0, y0)

    def __xy(self, cx, cy, r, a):
        # TODO comment: polar to xy

        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        return [x, y]

    def arc(self, cx, cy, r, s, e, detail=0.1):
        # TODO arc: maybe detail = r/10pi multiplied with detail setting? hmm, might ruin old things
        # TODO comment: s, e in radians
        # via https://stackoverflow.com/a/839931

        cmp = lambda a: a < e

        # if r negative, draw the other way around
        if r < 0:
            detail = -detail
            r = -r
            tmp = s
            s = e
            e = tmp
            cmp = lambda a: a > e

        def xy(a):
            return self.__xy(cx, cy, r, a)

        increment = TAU / (360 * detail)

        # start point
        [x, y] = xy(s)
        self.__m(x, y)

        # intermediate points
        a = s + increment
        while cmp(a):
            [x, y] = xy(a)
            self.__l(x, y)
            a += increment

        # end point
        [x, y] = xy(e)
        self.__l(x, y)

    def circle(self, cx, cy, r, detail=0.1):
        # TODO arc: maybe detail = r/10pi multiplied with detail setting? hmm, might ruin old things
        self.arc(cx, cy, r, 0, TAU, detail)

    def spiral(self, cx, cy, w, j=1, detail=0.1):
        # TODO arc: maybe detail = r/10pi multiplied with detail setting? hmm, might ruin old things
        # TODO comment: w = windings, j = jump between windings
        # TODO could use different increment in the middle, mult with square root of distance from outermost?

        def xy(r, a):
            return self.__xy(cx, cy, r, a)

        increment = 1 / (360 * detail)

        # start point
        self.__m(cx, cy)

        # intermediate points
        n = 0
        while n < w:
            r = (n / w) * (j * w)
            a = (n % 1) * TAU
            [x, y] = xy(r, a)
            self.__l(x, y)
            #n += increment
            n += increment / max(n / w, 0.2)  # relax increment in the middle

        # end point
        [x, y] = xy(j * w, (w % 1) * TAU)
        self.__l(x, y)

def main():
    c = Canvas()

    # concentric circles
    for i in range(0, 10):
        c.circle(0, 0, i + 2)

    plotter = AutoPlotter().from_canvas(c)
    #plotter = AutoPlotter().from_file("test-patterns/accuracy.json")
    plotter.emit()

if __name__ == "__main__":
    main()
