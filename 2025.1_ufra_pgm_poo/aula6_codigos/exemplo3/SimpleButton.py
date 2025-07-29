import pygame
from pygame.locals import *

class SimpleButton():    
        
    def __init__(self, window, loc, up, down):
        # Used to track the state of the button
        self.STATE_IDLE = 'idle' # button is up, mouse not over button
        self.STATE_ARMED = 'armed' # button is down, mouse over button
        self.STATE_DISARMED = 'disarmed' # clicked down on button, rolled off
        self.window = window
        self.loc = loc
        self.surfaceUp = pygame.image.load(up)
        self.surfaceDown = pygame.image.load(down)

        # Get the rect of the button (used to see if the mouse is over the button)
        self.rect = self.surfaceUp.get_rect()
        self.rect[0] = loc[0]
        self.rect[1] = loc[1]

        self.state = self.STATE_IDLE

    def handleEvent(self, eventObj):
        # This method will return True if user clicks the button.
        # Normally returns False.

        if eventObj.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN):
            # The button only cares about mouse-related events
            return False

        eventPointInButtonRect = self.rect.collidepoint(eventObj.pos)

        if self.state == self.STATE_IDLE:
            if (eventObj.type == MOUSEBUTTONDOWN) and eventPointInButtonRect:
                self.state = self.STATE_ARMED

        elif self.state == self.STATE_ARMED:
            if (eventObj.type == MOUSEBUTTONUP) and eventPointInButtonRect:
                self.state = self.STATE_IDLE
                return True  # clicked!

            if (eventObj.type == MOUSEMOTION) and (not eventPointInButtonRect):
                self.state = self.STATE_DISARMED

        elif self.state == self.STATE_DISARMED:
            if eventPointInButtonRect:
                self.state = self.STATE_ARMED
            elif eventObj.type == MOUSEBUTTONUP:
                self.state = self.STATE_IDLE

        return False

    def draw(self):
        # Draw the button's current appearance to the window
        if self.state == self.STATE_ARMED:
            self.window.blit(self.surfaceDown, self.loc)

        else:  # IDLE or DISARMED
            self.window.blit(self.surfaceUp, self.loc)
