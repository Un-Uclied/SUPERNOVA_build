import pygame, random
from scripts.dialouge_data import shop_dialouge_hello, shop_talk,item_explanation, enforce_talk, plugin_enforce_info
from scripts.dialouge_data import enforce_dialouge_hello, talk
from scripts.item_data import sapphire, topaz, ruby

class Shop_UI:
    def __init__(self, game):
        self.game = game
        #구매
        self.ui_bg = game.assets['shop_ui']
        self.select_bg = game.assets['select_ui']
        self.item_bg  = game.assets['show_item_bg']
        self.status = 'talk'#talk, buy
        self.select = 0
        self.font = self.game.fonts['dialouge_font']
        self.font_big = self.game.fonts['key_guide_big']
        self.font_smol = self.game.fonts['dialouge_font_smol']
        self.items = game.assets['shop_items']
        self.item_info = item_explanation
        self.price = '0'

        #대화
        self.hand = game.assets['select_hand']
        self.rect = self.hand.get_rect()
        self.stack = 0
        self.txtscript = shop_dialouge_hello
        self.selection = shop_talk


    def update(self):
        if self.status == 'talk':
            self.txtscript = shop_dialouge_hello
        if self.select == 0:
            self.rect[1] = 150
        if self.select == 1:
            self.rect[1] = 170
        if self.select == 2:
            self.rect[1] = 190
        if self.select == 3:
            self.rect[1] = 210
        if self.select == 4:
            self.rect[1] = 230

        if self.status == 'say':
            self.text = talk[0]

        if self.status == 'buy':
            if self.select == 0:
                self.txtscript = item_explanation[0]['info']
                self.price = item_explanation[0]['price']
            if self.select == 1:
                self.txtscript = item_explanation[1]['info']
                self.price = item_explanation[1]['price']
            if self.select == 2:
                self.txtscript = item_explanation[2]['info']
                self.price = item_explanation[2]['price']
            if self.select == 3:
                self.txtscript = item_explanation[3]['info']
                self.price = item_explanation[3]['price']
            if self.select == 4:
                self.txtscript = item_explanation[4]['info']
                self.price = item_explanation[4]['price']

    #그냥 텍스트 반환함
    def key_guide(self,txt , color = (0,0,0)):
        return self.font.render(txt, False, color)
    def key_guide_smol(self,txt , color = (0,0,0)):
        return self.font_smol.render(txt, False, color)
    def key_guide_big(self, txt , color = (0,0,0)):
        return self.font_big.render(txt, False, color)

    def render(self, surface):
        if self.game.player_status == 'shop':
            surface.blit(self.game.assets['shop_bg'], (0, 0))
            
            surface.blit(self.ui_bg, (0, surface.get_height() - self.ui_bg.get_height()))

            surface.blit(self.select_bg, (surface.get_width() - self.select_bg.get_width(),
                                           surface.get_height() - self.select_bg.get_height()))

            if self.status == 'buy':
                surface.blit(self.item_bg, (0,0))
                surface.blit(self.items[self.select], (0,0))

            if self.status == 'talk':
                #선택지
                surface.blit(self.key_guide(self.selection[0]), (surface.get_width()- 65,150))
                surface.blit(self.key_guide(self.selection[1]), (surface.get_width()- 65,170))
                surface.blit(self.key_guide(self.selection[2]), (surface.get_width()- 65,190))

            if self.status == 'buy':
                #선택지
                surface.blit(self.key_guide(self.item_info[0]['name']), (surface.get_width()- 65,150))
                surface.blit(self.key_guide(self.item_info[1]['name']), (surface.get_width()- 65,170))
                surface.blit(self.key_guide(self.item_info[2]['name']), (surface.get_width()- 65,190))

                self.text = self.txtscript[0]

            # 문장에 c이 있다면 여러 줄로 나누어서 개별적으로 렌더링
            lines = self.text.split('c')
            y_offset = 0
            for line in lines:
                line = line.strip()  # 개행 문자 제거
                line_snip = self.font.render(line, False, (0, 0, 0))
                snip_line_rect = line_snip.get_rect()
                snip_line_rect.y = 165 + y_offset
                snip_line_rect.x = 10
                surface.blit(line_snip, snip_line_rect)
                y_offset += line_snip.get_height()

            #----
            surface.blit(self.hand, (surface.get_width()- 60 - self.rect[2], self.rect[1]))
            if self.status == 'buy':
                surface.blit(self.key_guide(str(self.price) + 'coin', (250 , 220, 110)), (10, surface.get_height() - 17))
                surface.blit(self.game.assets['money_bar'], (10, surface.get_height() - 104))
                pygame.draw.circle(surface, (100,100,100), (10, surface.get_height() - 95), 10)

                surface.blit(self.key_guide_big('Z'), (5, surface.get_height() - 101))
                surface.blit(self.key_guide_smol('로 구매/' + str(self.game.player.inventory['countable']['코인'] )+ ' 코인소유'),
                              (20, surface.get_height() - 101))
                surface.blit(self.key_guide_smol('X로 뒤로가기'), (surface.get_width() - 65, surface.get_height()-12))

class Smithy_UI():
    def __init__(self, game):
        self.game = game
        self.player_inventory = self.game.player.inventory
        self.can_buy = False
        self.plugin_change_info = plugin_enforce_info
        #구매
        self.ui_bg = game.assets['shop_ui']
        self.select_bg = game.assets['select_ui']
        self.item_bg  = game.assets['show_item_bg']
        self.status = 'talk'#talk, enforce, plugin
        self.select = 0
        self.price = 0
        self.font = self.game.fonts['dialouge_font']
        self.font_big = self.game.fonts['key_guide_big']
        self.font_smol = self.game.fonts['dialouge_font_smol']
        self.item_info = plugin_enforce_info
        self.show_level = '0'
        
        #대화
        self.hand = game.assets['select_hand']
        self.rect = self.hand.get_rect()
        self.txtscript = enforce_dialouge_hello
        self.selection = enforce_talk
    
    #그냥 텍스트 반환함
    def key_guide(self,txt , color = (0,0,0)):
        return self.font.render(txt, False, color)
    def key_guide_smol(self,txt , color = (0,0,0)):
        return self.font_smol.render(txt, False, color)
    def key_guide_big(self, txt , color = (0,0,0)):
        return self.font_big.render(txt, False, color)

    def update(self):
        
        if self.status == 'talk':
            self.txtscript = enforce_dialouge_hello
        if self.select == 0:
            self.rect[1] = 150
        if self.select == 1:
            self.rect[1] = 170
        if self.select == 2:
            self.rect[1] = 190
        if self.select == 3:
            self.rect[1] = 210

        if self.status == 'say':
            self.text = talk[1]

        if self.status == 'enforce' and self.player_inventory['plugin'] != []:
            if self.select == 0 and plugin_enforce_info[0]['name'] in self.player_inventory['plugin']:
                self.text = plugin_enforce_info[0]['info']
                self.price = plugin_enforce_info[0]['price']
                self.can_buy = True
                self.show_level = sapphire['level']
            elif self.select == 0:
                self.text = '해당 플러그인이 없다.'
                self.price = 0
                self.can_buy = False

            if self.select == 1 and plugin_enforce_info[1]['name'] in self.player_inventory['plugin']:
                self.text = plugin_enforce_info[1]['info']
                self.price = plugin_enforce_info[1]['price']
                self.can_buy = True
                self.show_level = topaz['level']
            elif self.select == 1 and not plugin_enforce_info[1]['name'] in self.player_inventory['plugin']:
                 self.text = '해당 플러그인이 없다.'
                 self.price = 0
                 self.can_buy = False

            if self.select == 2 and plugin_enforce_info[2]['name'] in self.player_inventory['plugin']:
                self.text = plugin_enforce_info[2]['info']
                self.price = plugin_enforce_info[2]['price']
                self.can_buy = True
                self.show_level = ruby['level']
            elif self.select == 2 and not plugin_enforce_info[2]['name'] in self.player_inventory['plugin']:
                self.text = '해당 플러그인이 없다.'
                self.price = 0
                self.can_buy = False

        if self.status == 'plugin' and self.player_inventory['plugin'] != []:
            if self.select == 0 and plugin_enforce_info[0]['name'] in self.player_inventory['plugin']:
                self.text = plugin_enforce_info[0]['info_change']
                self.price = plugin_enforce_info[0]['change']
                self.can_buy = True
            elif self.select == 0:
                self.text = '해당 플러그인이 없다.'
                self.price = 0
                self.can_buy = False

            if self.select == 1 and plugin_enforce_info[1]['name'] in self.player_inventory['plugin']:
                self.text = plugin_enforce_info[1]['info_change']
                self.price = plugin_enforce_info[1]['change']
                self.can_buy = True
            elif self.select == 1 and not plugin_enforce_info[1]['name'] in self.player_inventory['plugin']:
                 self.text = '해당 플러그인이 없다.'
                 self.price = 0
                 self.can_buy = False

            if self.select == 2 and plugin_enforce_info[2]['name'] in self.player_inventory['plugin']:
                self.text = plugin_enforce_info[2]['info_change']
                self.price = plugin_enforce_info[2]['change']
                self.can_buy = True
            elif self.select == 2 and not plugin_enforce_info[2]['name'] in self.player_inventory['plugin']:
                self.text = '해당 플러그인이 없다.'
                self.price = 0
                self.can_buy = False


    
    def render(self, surface):
        if self.game.player_status == 'smithy':
            surface.blit(self.game.assets['smithy_bg'], (0, 0))
            surface.blit(self.ui_bg, (0, surface.get_height() - self.ui_bg.get_height()))

            surface.blit(self.select_bg, (surface.get_width() - self.select_bg.get_width(), surface.get_height() - self.select_bg.get_height()))

            if self.status == 'talk':
                #선택지
                surface.blit(self.key_guide(self.selection[0]), (surface.get_width()- 65,150))
                surface.blit(self.key_guide(self.selection[1]), (surface.get_width()- 65,170))
                surface.blit(self.key_guide(self.selection[2]), (surface.get_width()- 65,190))
                surface.blit(self.key_guide(self.selection[3]), (surface.get_width()- 65,210))
            
            #플러그인 장착
            if self.status == 'plugin':
                #선택지
                if plugin_enforce_info[0]['name'] in self.player_inventory['plugin']:
                    surface.blit(self.key_guide(self.item_info[0]['name']), (surface.get_width()- 65,150))  
                else:
                    surface.blit(self.key_guide('없음'), (surface.get_width()- 65,150))
                    

                if plugin_enforce_info[1]['name'] in self.player_inventory['plugin']:
                    surface.blit(self.key_guide(self.item_info[1]['name']), (surface.get_width()- 65,170))
                else:
                    surface.blit(self.key_guide('없음'), (surface.get_width()- 65,170))
                    

                if plugin_enforce_info[2]['name'] in self.player_inventory['plugin']:
                    surface.blit(self.key_guide(self.item_info[2]['name']), (surface.get_width()- 65,190))  
                else:
                    surface.blit(self.key_guide('없음'), (surface.get_width()- 65,190))
        
                if self.player_inventory['plugin'] == []:
                    self.text = '장착할 플러그인이 없다.'

            #강화
            if self.status == 'enforce':
            #선택지
                if plugin_enforce_info[0]['name'] in self.player_inventory['plugin']:
                    surface.blit(self.key_guide(self.item_info[0]['name']), (surface.get_width()- 65,150))   
                else:
                    surface.blit(self.key_guide('없음'), (surface.get_width()- 65,150))  

                if plugin_enforce_info[1]['name'] in self.player_inventory['plugin']:
                    surface.blit(self.key_guide(self.item_info[1]['name']), (surface.get_width()- 65,170))
                else:
                    surface.blit(self.key_guide('없음'), (surface.get_width()- 65,170))

                if plugin_enforce_info[2]['name'] in self.player_inventory['plugin']:
                    surface.blit(self.key_guide(self.item_info[2]['name']), (surface.get_width()- 65,190))  
                else:
                    surface.blit(self.key_guide('없음'), (surface.get_width()- 65,190))
                        
                if self.player_inventory['plugin'] == []:
                        self.text = '강화할 플러그인이 없다.'


            if self.status == 'enforce' or self.status == 'plugin':
                surface.blit(self.game.assets['money_bar'], (10, surface.get_height() - 104))
                pygame.draw.circle(surface, (100,100,100), (10, surface.get_height() - 95), 10)
                surface.blit(self.key_guide_big('Z'), (5, surface.get_height() - 101))
                surface.blit(self.key_guide_smol('로 의뢰/' + str(self.game.player.inventory['countable']['코인'] )+ ' 코인소유'), (20, surface.get_height() - 101))
                surface.blit(self.key_guide_smol('X로 뒤로가기'), (surface.get_width() - 65, surface.get_height()-12))

                

            # 문장에 c이 있다면 여러 줄로 나누어서 개별적으로 렌더링
            lines = self.text.split('c')
            y_offset = 0
            for line in lines:
                line = line.strip()  # 개행 문자 제거
                line_snip = self.font.render(line, False, (0, 0, 0))
                snip_line_rect = line_snip.get_rect()
                snip_line_rect.y = 165 + y_offset
                snip_line_rect.x = 10
                surface.blit(line_snip, snip_line_rect)
                y_offset += line_snip.get_height()

            surface.blit(self.hand, (surface.get_width()- 60 - self.rect[2], self.rect[1]))
            if self.status == 'enforce' or self.status == 'plugin':
                surface.blit(self.key_guide(str(self.price) + 'coin', (250 , 220, 110)), (10, surface.get_height() - 17))
            if self.status == 'enforce':
                surface.blit(self.key_guide('현재' + str(self.show_level) + '레벨'), (100, surface.get_height() - 19))