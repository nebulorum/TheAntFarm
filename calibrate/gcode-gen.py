from typing import NamedTuple, List, Tuple
from functools import partial

Vertex = NamedTuple("Vertex", [('x', float), ('y', float),('dx', int),('dy', int),])
Pattern = NamedTuple("Pattern", [('width', float), ('height',float), ('vertexi', List[Vertex])])
Point = NamedTuple('Point', [('x', float),('y', float)])

def dual_pad(track_width: float)-> Pattern:
    return Pattern(
        4, 2, [
            Vertex(-2, 0, -1, 0),
            Vertex(-2, 0.5, -1, +1),
            Vertex(-1, 0.5, +1, +1),
            Vertex(-1, track_width/2, +1, +1),

            Vertex(1, track_width/2, -1, +1),
            Vertex(1, track_width * 1.5, -1, +1),
            Vertex(1 + track_width * 3, track_width * 1.5, +1, +1),
            Vertex(1 + track_width * 3, -track_width * 1.5, +1, -1),
            Vertex(1, -track_width * 1.5, -1, -1),
            Vertex(1, -track_width/2, -1, -1),

            Vertex(1, -track_width/2, -1, -1),
            Vertex(-1, -track_width/2, +1, -1),
            Vertex(-1, -0.5, +1, -1),
            Vertex(-2, -0.5, -1, -1),
        ] )

def vertex_offset(offset:float, v:Vertex) -> Vertex:
    return Vertex(v.x + v.dx * offset, v.y + v.dy * offset, v.dx, v.dy)


def vertex_translate(dx:float, dy:float, v:Vertex) -> Vertex: 
    return Vertex(v.x + dx, v.y + dy, v.dx, v.dy)


def pattern_transform(t, p:Pattern)-> Pattern: 
    return Pattern(p.width, p.height, list(map(t, p.vertexi)))


def pattern_to_gcode(p:Pattern, depth, travel): 
    start = p.vertexi[0]
    gcode_jog(start.x, start.y, travel)
    for v in p.vertexi:
        gcode_mill(v.x,v.y,depth)
    gcode_mill(start.x, start.y, depth)
    gcode_jog(start.x, start.y, travel)

def gcode_jog(x,y,z):
    print("G0X%.4fY%.4fZ%.4f"% (x,y, z))

def gcode_mill(x,y,z):
    print('G01 X%.4f Y%.4f Z%.4f' % (x,y,z))

def pattern_dimension(p:Pattern): 
    xs = list(map(lambda v: v.x, p.vertexi))
    ys = list(map(lambda v: v.y, p.vertexi))
    return Point(min(xs), min(ys)), Point(max(xs), max(ys))

def pattern_rebase(p: Pattern, margin:float)-> Pattern :
    dim=pattern_dimension(p)
    print(dim)
    pwm = pattern_transform(partial(vertex_translate, -dim[0].x + margin, -dim[0].y + margin), p)
    height = dim[1].y - dim[0].y + 2 * margin
    width = dim[1].x - dim[0].x + 2 * margin
    return Pattern(width,height, pwm.vertexi)


def main():
    p2 = dual_pad(0.25)
    pattern_to_gcode(
        pattern_transform(partial(vertex_offset, 0.5), p2),
        -0.035,
        0.7)

    p2_t = pattern_transform(partial(vertex_translate, 0, p2.height), p2)
    pattern_to_gcode(
        pattern_transform(partial(vertex_offset, 0.15), p2_t),
        -0.07,
        0.7)

    pattern_to_gcode(
        pattern_transform(partial(vertex_offset, 0.20), p2_t),
        -0.07,
        0.7)
    pwm = pattern_rebase(p2, 0.5)
    for i in range(4):
        for j in range(3):
            pattern_to_gcode(
                pattern_transform(
                    partial(vertex_translate, i * pwm.width, j * pwm.height), pwm),
                -0.07, 0.7)

if __name__ == '__main__':
    main()