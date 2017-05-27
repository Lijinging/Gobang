import pygame
import pygame.locals

pygame.init()
screen = pygame.display.set_mode((800, 600))

# Variable to keep our main loop running
running = True

print(pygame.locals.KEYDOWN)
# Our main loop!
while running:
   # for loop through the event queue
   for event in pygame.event.get():
       # Check for KEYDOWN event; KEYDOWN is a constant defined in pygame.locals, which we imported earlier
       if event.type == pygame.locals.KEYDOWN:
           print(event.key)
           # If the Esc key has been pressed set running to false to exit the main loop
           if event.key == 27:  #sec键
               print("exit")
               running = False
       # Check for QUIT event; if QUIT, set running to false
       elif event.type == pygame.locals.QUIT:
           running = False