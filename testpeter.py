import pygame

import ArduinoTalk
canvas = pygame.display.set_mode((500,500))
running = True
motorspeed = 190 #between 0 and 255
forwardtime = 400 #in ms
rotatetime = 400 # in ms
ArduinoTalk.Write(f"s{motorspeed}")
ArduinoTalk.Write(f"t{forwardtime}")
ArduinoTalk.Write(f"r{rotatetime}")


while running :
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.KEYDOWN :
            canvas.fill((0,255,0))
            if event.key == pygame.K_w :
                ArduinoTalk.Write("bothF")
            elif event.key == pygame.K_a :
                ArduinoTalk.Write("lMotor")            
            elif event.key == pygame.K_s :
                ArduinoTalk.Write("bothB")
            elif event.key == pygame.K_d :
                ArduinoTalk.Write("rMotor")
        elif event.type == pygame.KEYUP :
            canvas.fill((255,0,0))
            ArduinoTalk.Write("0")
    pygame.time.Clock().tick(60)

        