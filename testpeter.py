import pygame

import ArduinoTalk
canvas = pygame.display.set_mode((500,500))
running = True
motorspeed = 110 #between 0 and 255
forwardtime = 5000 #in ms
rotatetime = 260 # in ms
starttime = 100 # in ms
motorAdjustment = 97 # in %
sensStopDistance = 100 #in cm
ArduinoTalk.Write(f"s{motorspeed}")
ArduinoTalk.Write(f"t{forwardtime}")
ArduinoTalk.Write(f"r{rotatetime}")
ArduinoTalk.Write(f"a{starttime}")
ArduinoTalk.Write(f"m{motorAdjustment}")
ArduinoTalk.Write(f"d{sensStopDistance}")

while running :
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.KEYDOWN :
            canvas.fill((0,255,0))
            if event.key == pygame.K_w :
                ArduinoTalk.Write("start")
            elif event.key == pygame.K_a :
                ArduinoTalk.Write("left")            
            elif event.key == pygame.K_s :
                ArduinoTalk.Write("bothB")
            elif event.key == pygame.K_d :
                ArduinoTalk.Write("right")
            elif event.key == pygame.K_o :
                sensStopDistance += -1
                print(sensStopDistance)
                ArduinoTalk.Write(f"d{sensStopDistance}")
            elif event.key == pygame.K_p :
                sensStopDistance += 1
                print(sensStopDistance)
                ArduinoTalk.Write(f"d{sensStopDistance}")
        elif event.type == pygame.KEYUP :
            canvas.fill((255,0,0))
            ArduinoTalk.Write("0")
    pygame.time.Clock().tick(60)

        