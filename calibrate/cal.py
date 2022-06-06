import math

cell_margin = 0.5
cell_size = 1.0
travel_z = 0.7
bit_angle = 30

PREFIX="""
(2001)
G90 ; Absolute G94 ; Rate per minut
G91.1 ; Incremental radius 
G40 ; Clear tool compensator
G49 ; Clear tool height
G17 G21 ; XY plane metric
(PROFILE)
M05 ; Stop Spindle
M09 ; Collant off
"""

SPINDLE = """
M03 S10  ; Minimum speed of 1%
G04 P2   ; Pause for 2 seconds to allow ESC to get into operation
; T3 M06 Tool change (not used)

M03 S1000 ; Spindle max
"""

T="""

G54 ; Set working datum, bottom left
; G41  D3 ; Compensation from table
; G43 Z15 H3 ; Tool height compensation

; M08 Coolent on

G00 X0 Y-20
Z5 ; Tool up 5 rapid

G01 Z-5 F120

Y160 F300
G02 X20 Y180 I20 J0; Center 20 right from point, endpoint (20,180)

G01 X160

G02 X180 Y160 I0 J-20

Y40

G02 X140 Y0 I-40 J0

X-20

G00 Z15
G00 X50 Y50

Z-1
G03 I-5 
Z1 
G0 X60

Z-1
G3 I-4
Z0
G0 X70 Y80
"""
END="""
;G00 X0 Y0
;G01 X10 
;G01 Y10
;G01 X0 Y10
;G01 X0 Y0
(End)
M05
M30 ; End of program
"""

def offset(n):
    return (2 * cell_margin + cell_size) * n + cell_margin + cell_size

def produce_cell(cx, cy, depth, tip):
    tool_offset = vbit_dia(depth, tip)
    half_move= cell_size /2 + tool_offset
    print("G00 Z%.4f;" % travel_z)
    print("(X=%.4f Y=%.4f Depth=%.4f Tip=%.4f Offset=%.4f)" % (cx,cy, depth, tip, tool_offset))
    print("G00 X%.4f Y%.4f ; jump to start\n" %(cx + half_move, cy))
    print("G01 Z%.4f F60" % -depth)
    # print("G03 I-%.4f" % (cell_margin + tool_offset))
    print("G01 X%.4f Y%.4f F120" % (cx + half_move, cy+half_move))
    print("G01 X%.4f Y%.4f" % (cx - half_move, cy+half_move))
    print("G01 X%.4f Y%.4f" % (cx - half_move, cy-half_move))
    print("G01 X%.4f Y%.4f" % (cx + half_move, cy-half_move))
    print("G01 X%.4f Y%.4f" % (cx + half_move, cy))

def vbit_dia(depth: float, tip:float) -> float:
    return depth * math.tan(math.radians(bit_angle/2)) * 2.0 + tip


def main(depths, vtips):
    print("(Hello)")
    for i in range(len(depths)):
        for j in range(len(vtips)):
            produce_cell(offset(j),offset(i), depths[i], vtips[j])

if __name__ == "__main__":
    depths = [0, 0.035, 0.07, 0.09]
    vtips = [0.1, 0.15, 0.2]
    print(PREFIX)
    print(SPINDLE)
    main(depths, vtips)
    print("G00 Z%.4f;\nX0.0 Y0.0;\n" % travel_z)
    print(END)