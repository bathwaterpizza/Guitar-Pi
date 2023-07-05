import cfg

if cfg.GAME_USEKEYBOARDINPUT:
    import pygame

    def getBoardInput(): # type: ignore
        boardInput = []

        keys = pygame.key.get_pressed()

        if keys[pygame.K_z]:
            boardInput.append('r')
        if keys[pygame.K_x]:
            boardInput.append('g')
        if keys[pygame.K_c]:
            boardInput.append('b')
        if keys[pygame.K_v]:
            boardInput.append('y')
        
        return boardInput
else:
    import RPi.GPIO as GPIO # type: ignore

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN) # Red touch input
    GPIO.setup(24, GPIO.IN) # Green touch input
    GPIO.setup(17, GPIO.IN) # Blue touch input
    GPIO.setup(27, GPIO.IN) # Yellow touch input
    GPIO.setup(22, GPIO.IN) # Joystick digital from Nano

    def getBoardInput(): # type: ignore
        boardInput = []
        
        if GPIO.input(22): # Only check input if joystick has moved
            if GPIO.input(23):
                boardInput.append('r')
            if GPIO.input(24):
                boardInput.append('g')
            if GPIO.input(17):
                boardInput.append('b')
            if GPIO.input(27):
                boardInput.append('y')
        
        return boardInput