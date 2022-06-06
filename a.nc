(Block-name: Header)
(Block-expand: 0)
(Block-enable: 1)

(2001)
G90 ; Absolute G94 ; Rate per minut
G91.1 ; Incremental radius 
G40 ; Clear tool compensator
G49 ; Clear tool height
G17 G21 ; XY plane metric
(PROFILE)
M05 ; Stop Spindle
M09 ; Collant off

(Hello)
G00 Z0.7000;
(Block-name: block)
(Block-expand: 0)
(Block-enable: 1)
(X=1.5000 Y=1.5000 Depth=0.0000 Tip=0.1000 Offset=0.1000)
G00 X2.1000 Y1.5000 ; jump to start

G01 Z0.0000 F60
G01 X2.1000 Y2.1000 F120
G01 X0.9000 Y2.1000
G01 X0.9000 Y0.9000
G01 X2.1000 Y0.9000
G01 X2.1000 Y1.5000
G00 Z0.7000;
(Block-name: block)
(Block-expand: 0)
(Block-enable: 1)
(X=3.5000 Y=1.5000 Depth=0.0000 Tip=0.1500 Offset=0.1500)
G00 X4.1500 Y1.5000 ; jump to start

G01 Z0.0000 F60
G01 X4.1500 Y2.1500 F120
G01 X2.8500 Y2.1500
G01 X2.8500 Y0.8500
G01 X4.1500 Y0.8500
G01 X4.1500 Y1.5000
G00 Z0.7000;
(Block-name: block)
(Block-expand: 0)
(Block-enable: 1)
(X=5.5000 Y=1.5000 Depth=0.0000 Tip=0.2000 Offset=0.2000)
G00 X6.2000 Y1.5000 ; jump to start

G01 Z0.0000 F60
G01 X6.2000 Y2.2000 F120
G01 X4.8000 Y2.2000
G01 X4.8000 Y0.8000
G01 X6.2000 Y0.8000
G01 X6.2000 Y1.5000
G00 Z0.7000;
(Block-name: block)
(Block-expand: 0)
(Block-enable: 1)
(X=1.5000 Y=3.5000 Depth=0.0350 Tip=0.1000 Offset=0.1188)
G00 X2.1188 Y3.5000 ; jump to start

G01 Z-0.0350 F60
G01 X2.1188 Y4.1188 F120
G01 X0.8812 Y4.1188
G01 X0.8812 Y2.8812
G01 X2.1188 Y2.8812
G01 X2.1188 Y3.5000
G00 Z0.7000;
(Block-name: block)
(Block-expand: 0)
(Block-enable: 1)
(X=3.5000 Y=3.5000 Depth=0.0350 Tip=0.1500 Offset=0.1688)
G00 X4.1688 Y3.5000 ; jump to start

G01 Z-0.0350 F60
G01 X4.1688 Y4.1688 F120
G01 X2.8312 Y4.1688
G01 X2.8312 Y2.8312
G01 X4.1688 Y2.8312
G01 X4.1688 Y3.5000
G00 Z0.7000;
(Block-name: block)
(Block-expand: 0)
(Block-enable: 1)
(X=5.5000 Y=3.5000 Depth=0.0350 Tip=0.2000 Offset=0.2188)
G00 X6.2188 Y3.5000 ; jump to start

G01 Z-0.0350 F60
G01 X6.2188 Y4.2188 F120
G01 X4.7812 Y4.2188
G01 X4.7812 Y2.7812
G01 X6.2188 Y2.7812
G01 X6.2188 Y3.5000
G00 Z0.7000;
(Block-name: block)
(Block-expand: 0)
(Block-enable: 1)
(X=1.5000 Y=5.5000 Depth=0.0700 Tip=0.1000 Offset=0.1375)
G00 X2.1375 Y5.5000 ; jump to start

G01 Z-0.0700 F60
G01 X2.1375 Y6.1375 F120
G01 X0.8625 Y6.1375
G01 X0.8625 Y4.8625
G01 X2.1375 Y4.8625
G01 X2.1375 Y5.5000
G00 Z0.7000;
(Block-name: block)
(Block-expand: 0)
(Block-enable: 1)
(X=3.5000 Y=5.5000 Depth=0.0700 Tip=0.1500 Offset=0.1875)
G00 X4.1875 Y5.5000 ; jump to start

G01 Z-0.0700 F60
G01 X4.1875 Y6.1875 F120
G01 X2.8125 Y6.1875
G01 X2.8125 Y4.8125
G01 X4.1875 Y4.8125
G01 X4.1875 Y5.5000
G00 Z0.7000;
(Block-name: block)
(Block-expand: 0)
(Block-enable: 1)
(X=5.5000 Y=5.5000 Depth=0.0700 Tip=0.2000 Offset=0.2375)
G00 X6.2375 Y5.5000 ; jump to start

G01 Z-0.0700 F60
G01 X6.2375 Y6.2375 F120
G01 X4.7625 Y6.2375
G01 X4.7625 Y4.7625
G01 X6.2375 Y4.7625
G01 X6.2375 Y5.5000
G00 Z0.7000;
(Block-name: block)
(Block-expand: 0)
(Block-enable: 1)
(X=1.5000 Y=7.5000 Depth=0.0900 Tip=0.1000 Offset=0.1482)
G00 X2.1482 Y7.5000 ; jump to start

G01 Z-0.0900 F60
G01 X2.1482 Y8.1482 F120
G01 X0.8518 Y8.1482
G01 X0.8518 Y6.8518
G01 X2.1482 Y6.8518
G01 X2.1482 Y7.5000
G00 Z0.7000;
(Block-name: block)
(Block-expand: 0)
(Block-enable: 1)
(X=3.5000 Y=7.5000 Depth=0.0900 Tip=0.1500 Offset=0.1982)
G00 X4.1982 Y7.5000 ; jump to start

G01 Z-0.0900 F60
G01 X4.1982 Y8.1982 F120
G01 X2.8018 Y8.1982
G01 X2.8018 Y6.8018
G01 X4.1982 Y6.8018
G01 X4.1982 Y7.5000
G00 Z0.7000;
(Block-name: block)
(Block-expand: 0)
(Block-enable: 1)
(X=5.5000 Y=7.5000 Depth=0.0900 Tip=0.2000 Offset=0.2482)
G00 X6.2482 Y7.5000 ; jump to start

G01 Z-0.0900 F60
G01 X6.2482 Y8.2482 F120
G01 X4.7518 Y8.2482
G01 X4.7518 Y6.7518
G01 X6.2482 Y6.7518
G01 X6.2482 Y7.5000
G00 Z0.7000;
(Block-name: block)
(Block-expand: 0)
(Block-enable: 1)
X0.0 Y0.0;


;G00 X0 Y0
;G01 X10 
;G01 Y10
;G01 X0 Y10
;G01 X0 Y0
(End)
M05
M30 ; End of program

