#임포트
import pygame
import json

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2, 
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone','shrine', 'dirt', 'boss_tile', 'brick', 'util', 'grav', 'ice_grass', 'snowy_grass', 'snow'}
AUTOTILE_TYPES = {'grass', 'stone', 'shrine', 'dirt', 'boss_tile', 'brick', 'ice_grass', 'snowy_grass', 'snow'}
DO_NOT_DRAW_TILES = ('spawners', 'interaction')

#타일 맵
class Tilemap:
    def __init__(self, game, tile_size = 16):
        #셋팅
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        #            #그냥 위치 key  #타입          #종류                #실질적인 위치 그릴때는 self.tile_size를 곱해서 틈을 벌린다(그리드에 맞춤).
        #self.tilemap['1;1'] = {'type' : '잔디, 'variant' : 3(종류), 'pos' : (1, 1)}
    
    def extract(self, id_pairs, keep=False):
        #맵중에 있는 id_pairs -> [('타입',variant)] 를 찾아 
        # 찾은 타일의 값들을 리스트로 반환
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)
                    
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())#값만 있음 (리스트)
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]
        
        return matches
        
    def tiles_around(self, pos):
        #주어진 pos주변에 있는 타일을 반환
        #pos // self.tile_size - NEIGHBOR_OFFSETS에서 막 다 더하거나 뺌 그값을 돌려줌
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_location = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            # self.tilemap 안에 pos // self.tile_size - NEIGHBOR_OFFSETS중 아무거나 있다면
            if check_location in self.tilemap:
                tiles.append(self.tilemap[check_location])
        return tiles
    
    def save(self, path):
        #맵 세이브
        file = open(path, 'w')
        json.dump({'tilemap' : self.tilemap, 
                   'tile_size' : self.tile_size,
                    'offgrid' : self.offgrid_tiles}, file)
        file.close()

    def load(self, path):
        #맵 로드
        file = open(path, 'r')
        map_data = json.load(file)
        file.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def solid_tile_check(self, pos):
        tile_loc = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_loc]

    def physics_rects_around(self, pos):
        #주어진 pos주변에  물리력이 있는 타일을 반환
        rects = []
        for tile in self.tiles_around([int(pos[0]), int(pos[1])]):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size,
                                          tile['pos'][1] * self.tile_size,
                                            self.tile_size,
                                              self.tile_size))
        return rects
    
    
    def autotile(self):
        #자동 타일 두르기
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0]+shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neighbors]


    
    def render(self, surf, offset=(0, 0), running = True):
        if running:
            #그리드에 그려지지 않은 타일:
            for tile in self.offgrid_tiles:
                if str(tile['type']) in self.game.assets:
                    #그리려는 타일이 self.game.assets에 있는지 확인
                        surf.blit(self.game.assets[tile['type']][tile['variant']],
                                   (tile['pos'][0] - offset[0],
                                     tile['pos'][1] - offset[1]))
                elif not str(tile['type']) in DO_NOT_DRAW_TILES:
                    #타일이 그려지지 않았을 경우 경고
                        print('경고!: ' + str(tile['type']) + '가 그려지지 않음!')

            #그리드에 맞춰진 타일 
            for x in range(offset[0] // self.tile_size,
                            (offset[0] + surf.get_width()) // self.tile_size + 1):
                for y in range(offset[1] // self.tile_size,
                                (offset[1] + surf.get_height()) // self.tile_size + 1):
                    loc = str(x) + ';' + str(y)
                    if loc in self.tilemap:
                        tile = self.tilemap[loc]
                        if str(tile['type']) in self.game.assets:
                            #그리려는 타일이 self.game.assets에 있는지 확인
                                surf.blit(self.game.assets[tile['type']][tile['variant']], 
                                          (tile['pos'][0] * self.tile_size - offset[0],
                                            tile['pos'][1] * self.tile_size - offset[1]))
                        elif not str(tile['type']) in DO_NOT_DRAW_TILES:
                            #타일이 그려지지 않았을 경우 경고
                                print('경고!: ' + str(tile['type']) + '가 그려지지 않음!')