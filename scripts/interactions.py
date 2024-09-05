import pygame

class Interaction:
    def __init__(self, rect, action, game, key):
        self.game = game
        self.rect = rect
        self.key = key
        self.font = game.fonts['key_guide']
        self.return_action = action

    def update(self):
        if self.rect.colliderect(self.game.player.rect()):
            return self.return_action
        elif not self.rect.colliderect(self.game.player.rect()):
            return False
    
    