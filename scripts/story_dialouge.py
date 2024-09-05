import pygame
import random
class Dialouge:
    def __init__(self, game, txts, imgs):
        self.game = game
        self.imgscript = imgs
        self.active_message = 0
        self.txtscript = txts
        self.stack = 0
        self.active_message = 0
        self.isDone = False

        self.font = self.game.fonts['dialouge_font']
        self.key_guide_font = self.game.fonts['dialouge_font_smol']

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] and self.isDone and len(self.txtscript) > self.active_message + 1 :
            # 텍스트 넘기기
            self.active_message += 1
            self.isDone = False
            self.stack = 0
            self.text = self.txtscript[self.active_message]
            self.game.sfx['confirm'].play()

        if self.isDone and len(self.txtscript) == self.active_message + 1 and keys[pygame.K_SPACE]:
            self.game.sfx['confirm'].play()
            return True
        
        if keys[pygame.K_ESCAPE]:
            self.game.sfx['confirm'].play()
            return True
    
    def key_guide(self, txt):
        return self.key_guide_font.render(txt, False, 'white')
    
    def render(self, surface):
        pygame.draw.rect(surface, 'white', (45, 20, 230, 160))
        #----변수
        self.text = self.txtscript[self.active_message]
        self.speed = 5
        
        #self.sound = sound
        self.snip = self.font
        #대화----
        self.snip = self.font.render("", True, 'white')
        if self.stack <= self.speed * len(self.text):
            self.stack += 1
        if self.stack >= self.speed * len(self.text) or self.stack // self.speed >= len(self.text) or self.stack // self.speed == len(self.text):
            self.isDone = True
        #렌더
        if self.stack%self.speed == 0 :
            self.game.sfx['key'].play()
        self.snip = self.font.render(str(self.text[0:self.stack//self.speed]), True, 'white')
        snip_rect = self.snip.get_rect()
        #
        snip_rect.y = 200
        snip_rect.x = 60
        #----
        surface.blit(self.snip, snip_rect)
        surface.blit(self.imgscript[self.active_message], (45, 20))
        #키 가이드
        surface.blit(self.key_guide('SPACE to NEXT' if self.isDone and len(self.txtscript) == self.active_message + 1 else 'Z to NEXT'), (0, 0))

class Credits:
    def __init__(self, game, txts, txt_all):
        self.game = game
        self.active_message = 0
        self.txtscript = txts
        self.stack = 0
        self.active_message = 0
        self.isDone = False
        self.txt_finall = txt_all

        self.font = self.game.fonts['dialouge_font']
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] and self.isDone and len(self.txtscript) > self.active_message + 1 :
            # 텍스트 넘기기
            self.active_message += 1
            self.isDone = False
            self.stack = 0
            self.text = self.txtscript[self.active_message]
            self.game.sfx['confirm'].play()
    
    def key_guide(self, txt):
        return self.font.render(txt, False, 'white')
    
    def render(self, surface):
        #----변수
        self.text = self.txtscript[self.active_message]
        self.speed = 5
    
        self.snip = self.font
        #대화----
        self.snip = self.font.render("", True, 'white')
        if self.stack <= self.speed * len(self.text):
            self.stack += 1
        if self.stack >= self.speed * len(self.text) or self.stack // self.speed >= len(self.text) or self.stack // self.speed == len(self.text):
            self.isDone = True
        #렌더
        if self.stack%self.speed == 0:
            self.game.sfx['key'].play()
        self.snip = self.font.render(str(self.text[0:self.stack//self.speed]), True, 'white')
        snip_rect = self.snip.get_rect()
        #
        snip_rect.y = 50
        snip_rect.x = 60
        #----
        surface.blit(self.snip, snip_rect)

        # 문장에 c이 있다면 여러 줄로 나누어서 개별적으로 렌더링
        lines = self.txt_finall.split('c')
        y_offset = 0
        for line in lines:
            line = line.strip()  # 개행 문자 제거
            line_snip = self.font.render(line, True, 'white')
            snip_line_rect = line_snip.get_rect()
            snip_line_rect.y = 150 + y_offset
            snip_line_rect.x = 70
            surface.blit(line_snip, snip_line_rect)
            y_offset += line_snip.get_height()

        surface.blit(self.key_guide('Z to next'), (0,0))

        