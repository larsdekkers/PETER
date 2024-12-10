import serial

arduino = serial.Serial(port='COM5',  baudrate=9600, timeout=0.1)

def Write(rawinput):
    data = rawinput + "\n"
    arduino.write(bytes(data, 'utf-8'))

def Read() :
    rawoutput = arduino.readline()
    output = rawoutput.decode("utf-8")
    if output != (''):
        print(output)

while True:
    data = input("write : ")
    Write(data)
    Read()
