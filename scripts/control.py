import pygame
pygame.init()
from scripts.utils import write_save

class Control:
    def __init__(self, save, game):
        self.game = game
        self.save_file = save
        self.curr_block = save['curr_profile']
        self.controls = self.save_file['controls'][str(self.curr_block)]
        self.confirm_key = 0
        self.setup()
    
    def update(self, actions):
        if self.select: self.set_new()
        else: self.navigate(actions)

    def render(self, surf):
        self.render_controls(surf, self.save_file['controls'][str(self.curr_block)])
        
        pygame.draw.polygon(surf, 'black', [(285, 160), (320, 277)], 220)
        pygame.draw.polygon(surf, 'black', [(285, 130), (320, 247)], 220)
        txt = self.game.fonts['font_start'].render('설정', False, 'white')
        surf.blit(txt, (190, 135))
        if self.curr_block == self.save_file['curr_profile']:
            self.draw_txt(surf, "USING", 20, pygame.Color('red'), 215, 200)
        self.draw_txt(surf,'위로: '+pygame.key.name(self.controls['UP/JUMP']).capitalize()+'|아래로: '+pygame.key.name(self.controls['DOWN']).capitalize()
                      , 20, pygame.Color('white'), 260, 165)
        self.draw_txt(surf,'확인: '+pygame.key.name(self.controls['ACTION1']).capitalize(),
                       20, pygame.Color('white'), 281, 185)
        
        self.draw_txt(surf, 'CONTROL', 12, pygame.Color('white'), self.game.canvas.get_width() - 85,
                       self.game.canvas.get_height() - 25)
        self.draw_txt(surf, 'OPTION' + str(self.curr_block + 1), 12, pygame.Color('white')
                      , self.game.canvas.get_width() - 80, self.game.canvas.get_height() - 10)

    def navigate(self, actions):
        if actions['DOWN']:self.curr_index=(self.curr_index + 1) % (len(self.save_file['controls'][str(self.curr_block)]) + 1)
        if actions['UP/JUMP']:self.curr_index=(self.curr_index - 1) % (len(self.save_file['controls'][str(self.curr_block)]) + 1)
        if actions['LEFT']:self.curr_block=(self.curr_block - 1) % (len(self.save_file['controls']))
        if actions['RIGHT']:self.curr_block=(self.curr_block + 1) % (len(self.save_file['controls']))

        if actions['ACTION1']:
            if self.curs_dict[self.curr_index] == "Set":
                self.controls = self.save_file['controls'][str(self.curr_block)]
                self.save_file['curr_profile'] = self.curr_block
                write_save(self.save_file)
            else:
                self.select = True
    
    def set_new(self):
        selected_control = self.curs_dict[self.curr_index]
        run = True
        while run:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    exit()
                elif ev.type == pygame.KEYDOWN:
                    if ev.key not in self.save_file['controls'][str(self.curr_block)].values():
                        self.save_file['controls'][str(self.curr_block)][selected_control] = ev.key
                        self.game.sfx['confirm_option'].play()
                        #self.confirm_key = self.save_file['controls'][str(self.curr_block)][selected_control] if self.save_file['controls'][str(self.curr_block)][selected_control] == "MELEE" else ""
                        write_save(self.save_file)
                        self.select = False
                        run = False
    
    def render_controls(self, surf, controls):
        color = (125, 13, 5)
        pygame.draw.rect(surf, color, (0, (self.curr_index*20), 320, 20))
        i = 0
        for ctrl in controls:
            self.draw_txt(surf, ctrl + ' = ' + pygame.key.name(controls[ctrl]), 1, pygame.Color('white'),
                           self.game.canvas.get_width()/3 - 25, 10 + i)
            i += 20
        self.draw_txt(surf, "Change Curr Profile", 1, pygame.Color('dark green'), self.game.canvas.get_width()/3 - 25, 10 + i)

    def setup(self):
        self.select = False
        self.font = self.game.fonts['dialouge_font_smol']
        self.curs_dict = {}
        self.curr_index = 0
        i = 0
        for control in self.controls:
            self.curs_dict[i] = control
            i += 1
        self.curs_dict[i] = 'Set'

    def draw_txt(self, surf, txt, size, color, x, y):
        text = self.font.render(txt, False, color, size)
        text.set_colorkey('black')
        text_rect = text.get_rect()
        text_rect.center = (x, y)
        surf.blit(text , text_rect)