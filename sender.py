import serial

D="""
W <class 'str'> : G90
<R< 'ok'
<R< ''
W <class 'bytes'> : b'?'
W <class 'str'> : G90
W <class 'str'> : G91.1
W <class 'str'> : G40
W <class 'str'> : G49
W <class 'str'> : G17G21
W <class 'str'> : M05
W <class 'str'> : M09
W <class 'str'> : G00Z0.7
<R< '<Idle|MPos:0.000,0.000,0.000|FS:0,0|Pn:P>'
W <class 'str'> : G00X2.1Y1.5
<R< 'ok'
W <class 'str'> : G01Z0F60
<R< 'ok'
W <class 'str'> : G01X2.1Y2.1F120
<R< 'ok'
W <class 'str'> : G01X0.9Y2.1
<R< 'ok'
W <class 'str'> : G01X0.9Y0.9
<R< 'ok'
W <class 'str'> : G01X2.1Y0.9
<R< 'ok'
W <class 'str'> : G01X2.1Y1.5
<R< 'ok'
<R< 'ok'
W <class 'str'> : G00Z0.7
<R< 'ok'
W <class 'str'> : G00X4.15Y1.5
<R< 'ok'
W <class 'str'> : G01Z0F60
<R< 'ok'
W <class 'str'> : G01X4.15Y2.15F120
"""
ser = None

def send_wait(msg):
    global ser
    print("Sending: " ,type(msg), msg)
    ser.write(msg)
    ser.write(b'?')
    line = ser.readline()
    print(line)

def main():
    global ser
    ser = serial.Serial('/dev/cu.usbmodem14203', 115200)
    print(ser.name)         # check which port was really used
    send_wait(b'$X\n')
    send_wait(b'?')
    send_wait(b'F100\n')
    for i in range(10):
        send_wait(b"G01X10Y10")
        send_wait(b"G01X0Y0")

if __name__ == '__main__':
    main()