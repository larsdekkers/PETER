import pygame

import ArduinoTalk
canvas = pygame.display.set_mode((500,500))
running = True
while running :
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.KEYDOWN :
            canvas.fill((0,255,0))
            if event.key == pygame.K_w :
                print("w")
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

        