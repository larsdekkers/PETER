import serial

arduino = serial.Serial(port='COM3',  baudrate=9600, timeout=0.1)

def Write(rawinput) -> None:
    data = rawinput + "\n"
    arduino.write(bytes(data, 'utf-8'))

def Read() -> str:
    waiting = True
    while waiting :
        rawoutput = arduino.readline()
        output = rawoutput.decode("utf-8").strip()
        if output != (''):
            return output

