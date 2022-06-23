from typing import NamedTuple, List
from functools import partial
import math

Vertex = NamedTuple("Vertex", [('x', float), ('y', float), ('dx', int), ('dy', int), ])
Pattern = NamedTuple("Pattern", [('width', float), ('height', float), ('vertexi', List[Vertex])])
Point = NamedTuple('Point', [('x', float), ('y', float)])

SAFE_TRAVEL_Z = 0.7


def dual_pad(track_width: float) -> Pattern:
    return Pattern(
        4, 2, [
            Vertex(-2, 0, -1, 0),
            Vertex(-2, 0.5, -1, +1),
            Vertex(-1, 0.5, +1, +1),
            Vertex(-1, track_width / 2, +1, +1),

            Vertex(1, track_width / 2, -1, +1),
            Vertex(1, track_width * 1.5, -1, +1),
            Vertex(1 + track_width * 3, track_width * 1.5, +1, +1),
            Vertex(1 + track_width * 3, -track_width * 1.5, +1, -1),
            Vertex(1, -track_width * 1.5, -1, -1),
            Vertex(1, -track_width / 2, -1, -1),

            Vertex(1, -track_width / 2, -1, -1),
            Vertex(-1, -track_width / 2, +1, -1),
            Vertex(-1, -0.5, +1, -1),
            Vertex(-2, -0.5, -1, -1),
        ])


def vertex_offset(offset: float, v: Vertex) -> Vertex:
    return Vertex(v.x + v.dx * offset, v.y + v.dy * offset, v.dx, v.dy)


def vertex_translate(dx: float, dy: float, v: Vertex) -> Vertex:
    return Vertex(v.x + dx, v.y + dy, v.dx, v.dy)


def pattern_transform(t, p: Pattern) -> Pattern:
    return Pattern(p.width, p.height, list(map(t, p.vertexi)))


def pattern_to_gcode(p: Pattern, depth, travel):
    start = p.vertexi[0]
    gcode_jog(start.x, start.y, travel)
    for v in p.vertexi:
        gcode_mill(v.x, v.y, depth)
    gcode_mill(start.x, start.y, depth)
    gcode_jog(start.x, start.y, travel)


def gcode_jog(x, y, z):
    print("G0X%.4fY%.4fZ%.4f" % (x, y, z))


def gcode_mill(x, y, z):
    print('G01 X%.4f Y%.4f Z%.4f' % (x, y, z))


def pattern_dimension(p: Pattern):
    xs = list(map(lambda v: v.x, p.vertexi))
    ys = list(map(lambda v: v.y, p.vertexi))
    return Point(min(xs), min(ys)), Point(max(xs), max(ys))


def pattern_rebase(p: Pattern, margin: float) -> Pattern:
    dim = pattern_dimension(p)
    pwm = pattern_transform(partial(vertex_translate, -dim[0].x + margin, -dim[0].y + margin), p)
    height = dim[1].y - dim[0].y + 2 * margin
    width = dim[1].x - dim[0].x + 2 * margin
    return Pattern(width, height, pwm.vertexi)


def multi_pass(mill_width: float, passes: int, overlap: float, inout: bool, pattern: Pattern):
    depth = 0.07
    offsets = multi_pass_offsets(mill_width, passes, overlap)
    if inout:
        offsets = list(reversed(offsets))
    print("(MP %f %d %f %s)" % (mill_width, passes, overlap, inout))
    for offset in offsets:
        modified = pattern_transform(partial(vertex_offset, offset), pattern)
        pattern_to_gcode(modified, -depth, SAFE_TRAVEL_Z)


def multi_pass_offsets(mill_width: float, passes: int, overlap: float) -> List[float]:
    offsets = list([mill_width * i * (1 - overlap) + mill_width / 2 for i in range(passes)])
    return offsets


def multi_depth(mill_width: float, depths: List[float], pattern: Pattern):
    for depth in depths:
        modified = pattern_transform(partial(vertex_offset, mill_width / 2), pattern)
        pattern_to_gcode(modified, -depth, SAFE_TRAVEL_Z)


def vbit_toolwidth(depth: float, tip: float, bit_angle: float) -> float:
    return depth * math.tan(math.radians(bit_angle / 2)) * 2.0 + tip


def main():
    p2 = dual_pad(0.25)
    pwm = pattern_rebase(p2, 0.5)
    vbit_dia = vbit_toolwidth(0.07, 0.1, 30)
    methods = [
        partial(multi_pass, vbit_dia, 1, 0, True),
        partial(multi_pass, vbit_dia, 3, .4, True),
        partial(multi_pass, vbit_dia, 3, .4, False),
        partial(multi_depth, vbit_dia, [0.035, 0.07])
    ]
    for i in range(len(methods)):
        for j in range(3):
            tp = pattern_transform(partial(vertex_translate, i * pwm.width, j * pwm.height), pwm)
            methods[i](tp)
        print(i)


if __name__ == '__main__':
    main()
