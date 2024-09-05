import pygame
from scripts.dialouge_data import level_name

class UI:
    def __init__(self, game):
        self.game = game
        self.boss_fight = False
        self.heal = self.game.assets['heal']

        self.game.assets['magic_icon_fire'].set_alpha(255)
        self.game.assets['magic_icon_light'].set_alpha(255)
        self.game.assets['magic_icon_ice'].set_alpha(255)
        
        self.inventory = game.player.inventory

        self.magic_icon = self.game.assets['magic_icon_none']

        self.dash = self.game.assets['dash_icon']
        self.melee = self.game.assets['melee_icon']
        self.box = self.game.assets['icons_box']


        self.ui_key = self.game.assets['ui_key_bg']
        self.heart = self.game.assets['ui_heart']
        self.health_bar = self.game.assets['health_bar']
        self.health_bar_rect = self.health_bar.get_rect(topleft = (3, 176))

        self.health_bar_pos = (20,190)
        self.bar_max_width = 70
        self.bar_height = 5

        self.boss_health_bar_pos = (19, 30)
        self.boss_bar_max_width = 141
        self.boss_bar_height = 10

        self.boss_shield_health_bar_pos = (19, 43)
        self.boss_shield_bar_max_width = 141
        self.boss_shield_bar_height = 3

        self.dash.set_alpha(255)
        self.melee.set_alpha(255)
        self.magic_icon.set_alpha(255)
        self.heart.set_alpha(255)
        self.heal.set_alpha(255)

        self.dash_rect = self.dash.get_rect()
        self.melee_rect = self.melee.get_rect()
        self.magic_rect = self.magic_icon.get_rect()

        self.show_timer = 220
        self.level = -1
        self.render_txt = self.game.fonts['font_stop'].render('', False, 'white')
        self.alpha = 255

    def level_intro(self, surf, level):
        #레벨이 달라졌을 경우 리로드
        if level != self.level:
            self.show_timer = 220
            self.level = level
            self.alpha = 255
        text = level_name[level]
        if self.show_timer:
            self.show_timer -= 1
            self.render_txt = self.game.fonts['font_stop'].render('[' + text + ']', False, 'white')
            self.render_txt.set_alpha(self.alpha * 0.99)
            #100부터 사라지기
            if self.show_timer <= 100:
                self.alpha *= 0.99
            
            #텍스트 위치 및 그리기
            render_rect = self.render_txt.get_rect()
            render_rect.center = surf.get_rect().center
            surf.blit(self.render_txt, (render_rect))
        else:
            return

    def update(self):
        #보스전인지 아닌지 확인
        if self.boss_fight:
            self.boss = self.game.enemies[-1]


        #마법 아이콘 이미지
        if self.game.player.using_plugin == 'empty':
            self.magic_icon = self.game.assets['magic_icon_none']
        elif self.game.player.using_plugin == 'fire':
            self.magic_icon = self.game.assets['magic_icon_fire']   
        elif self.game.player.using_plugin == 'ice':
            self.magic_icon = self.game.assets['magic_icon_ice']  
        elif self.game.player.using_plugin == 'light':
            self.magic_icon = self.game.assets['magic_icon_light']
            
        #이렇게 하면 부드럽게 alpha value가 늘어나거나/줄어듦
        #근접공격
        if self.game.player.attk_cooldown:
            self.melee.set_alpha(max(50, self.melee.get_alpha() - 40))
        else:
            self.melee.set_alpha(min(255, self.melee.get_alpha() + 40))

        #대쉬
        if abs(self.game.player.dashing) >= 50:
            
            self.dash.set_alpha(max(50, self.dash.get_alpha() - 40))
        elif self.game.player.dashing == 0:
            self.dash.set_alpha(min(255, self.dash.get_alpha() + 40))

        #마법 아이콘
        if self.game.player.magic_attk_cooldown:
            
            self.magic_icon.set_alpha(max(50, self.magic_icon.get_alpha() - 40))
        else:
            self.magic_icon.set_alpha(min(255, self.magic_icon.get_alpha() + 40))

        #플레이어 체력이 낮아질수록 하트가 불투명 해짐
        self.heart.set_alpha((self.game.player.player_health * 255) / self.game.player.player_max_health)

        if self.boss_fight:
            #플레이어 체력바
            boss_curr_health_ratio = self.boss.health / self.boss.max_health
            boss_curr_bar_width = self.boss_bar_max_width * boss_curr_health_ratio
            self.boss_healthbar_rect = pygame.Rect(self.boss_health_bar_pos, (boss_curr_bar_width, self.boss_bar_height))

            #플레이어 체력바
            boss_shield_curr_health_ratio = self.boss.shield_health / self.boss.max_shield_health
            boss_shield_curr_bar_width = self.boss_shield_bar_max_width * boss_shield_curr_health_ratio
            self.boss_shield_healthbar_rect = pygame.Rect(self.boss_shield_health_bar_pos,
                                                           (boss_shield_curr_bar_width, self.boss_shield_bar_height))

        #플레이어 체력바
        curr_health_ratio = self.game.player.player_health / self.game.player.player_max_health
        curr_bar_width = self.bar_max_width * curr_health_ratio
        self.healthbar_rect = pygame.Rect(self.health_bar_pos, (curr_bar_width, self.bar_height))

        if self.game.player.can_heal == 0:self.heal.set_alpha(100)
        else:self.heal.set_alpha(255)
        

    def key_guide(self, txt):
        return self.game.fonts['key_guide'].render(txt, False, (0,0,0))

    def render(self, surface):
        
        surface.blit(self.box, (0, surface.get_height() - self.box.get_height()))
        
        surface.blit(self.health_bar, self.health_bar_rect)
        
        surface.blit(self.magic_icon, (6, (surface.get_height() - self.magic_icon.get_height()) - 6))
        surface.blit(self.dash, (self.magic_icon.get_width() + 14,
                                  (surface.get_height() - self.magic_icon.get_height()) - 6))
        surface.blit(self.melee, (self.magic_icon.get_width() + self.dash.get_width() + 22,
                                   (surface.get_height() - self.magic_icon.get_height()) - 6))

        pygame.draw.circle(surface, (100,100,100), (6, surface.get_height() - 7), 5)
        surface.blit(self.key_guide(pygame.key.name(self.game.control_handler.controls['MAGIC']).capitalize()),
                      (3, surface.get_height() - 10))

        pygame.draw.circle(surface, (100,100,100), (40, surface.get_height() - 7), 5)
        surface.blit(self.key_guide(pygame.key.name(self.game.control_handler.controls['DASH']).capitalize()),
                      (37, surface.get_height() - 10))

        pygame.draw.circle(surface, (100,100,100), (72, surface.get_height() - 7), 5)
        surface.blit(self.key_guide(pygame.key.name(self.game.control_handler.controls['MELEE']).capitalize()),
                      (69, surface.get_height() - 10))

        surface.blit(self.heart, (6, 179))
        
        surface.blit(self.game.assets['heal_bg'], (self.magic_icon.get_width() + self.dash.get_width() + 55,
                                                    (surface.get_height() - self.magic_icon.get_height()) - 7))
        surface.blit(self.heal, (self.magic_icon.get_width() + self.dash.get_width() + 55,
                                  (surface.get_height() - self.magic_icon.get_height()) - 7))
        pygame.draw.circle(surface, (100,100,100), (132, surface.get_height() - 8), 5)
        surface.blit(self.key_guide(pygame.key.name(self.game.control_handler.controls['HEAL']).capitalize()),
                      (130, surface.get_height() - 11))
        pygame.draw.circle(surface, (125,125,125), (110, surface.get_height() - 28), 5)
        surface.blit(self.key_guide(str(self.game.player.can_heal)), (107, surface.get_height() - 31))


        pygame.draw.rect(surface, 'red', self.healthbar_rect)

        #보스전 일때 보스의 체력 표시
        if self.boss_fight:
            surface.blit(self.game.assets['boss_bar'], (15, 25))
            pygame.draw.rect(surface, 'red', self.boss_healthbar_rect)
            pygame.draw.rect(surface, 'purple', self.boss_shield_healthbar_rect)

