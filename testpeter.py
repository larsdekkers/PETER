import pygame

import ArduinoTalk
canvas = pygame.display.set_mode((500,500))
running = True
motorSpeed = 110 #between 0 and 255

forwardTime = 260 #in ms
forwardStartTime = 400 #in ms
forwardStopTime = 170 #in ms

rotateTimeL = 710 #in ms
rotateTimeR = 810 #in ms

startTime = 100 #in ms
motorAdjustment = 92 #in %
sensStopDistance = 100 #in cm
ArduinoTalk.Write(f"s{motorSpeed}")

ArduinoTalk.Write(f"ft{forwardStartTime}")
ArduinoTalk.Write(f"fp{forwardStopTime}")
ArduinoTalk.Write(f"ff{forwardTime}")

ArduinoTalk.Write(f"rl{rotateTimeL}")
ArduinoTalk.Write(f"rr{rotateTimeR}")

ArduinoTalk.Write(f"a{startTime}")
ArduinoTalk.Write(f"m{motorAdjustment}")
ArduinoTalk.Write(f"d{sensStopDistance}")

tingy = forwardTime
tingyshort = "ff"
tingyamount = 10

    
while running :
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.KEYDOWN :
            canvas.fill((0,255,0))
            if event.key == pygame.K_w :
                ArduinoTalk.Write("forwardStart")
                ArduinoTalk.Write("forward")
                ArduinoTalk.Write("forward")
                ArduinoTalk.Write("forwardStop")
            elif event.key == pygame.K_a :
                ArduinoTalk.Write("left")            
            elif event.key == pygame.K_s :
                #ArduinoTalk.Write("bothB")
                pass
            elif event.key == pygame.K_d :
                ArduinoTalk.Write("right")
            elif event.key == pygame.K_o :
                tingy += -tingyamount
                print(tingy)
                ArduinoTalk.Write(f"{tingyshort}{tingy}")
            elif event.key == pygame.K_p :
                tingy += tingyamount
                print(tingy)
                ArduinoTalk.Write(f"{tingyshort}{tingy}")
        elif event.type == pygame.KEYUP :
            canvas.fill((255,0,0))
           # ArduinoTalk.Write("0")
    pygame.time.Clock().tick(60)

        