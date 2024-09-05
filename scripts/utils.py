import pygame
import os, json

BASE_IMAGE_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMAGE_PATH + path).convert()
    img.set_colorkey((0,0,0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMAGE_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

class Animation:
    def __init__(self, images, img_dur = 5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)].convert_alpha()
    

def create_save():
    save = {
        'controls' : {
            "0" : {"LEFT" : pygame.K_LEFT,
                "RIGHT" : pygame.K_RIGHT,
                "UP/JUMP" : pygame.K_UP,
                "DOWN" : pygame.K_DOWN,
                "MAGIC" : pygame.K_z,
                "DASH" : pygame.K_x,
                "MELEE" : pygame.K_c,
                "HEAL" : pygame.K_f,
                "ACTION1" : pygame.K_RETURN,
                "ACTION2" : pygame.K_TAB},
            
            "1" : {"LEFT" : pygame.K_LEFT,
                "RIGHT" : pygame.K_RIGHT,
                "UP/JUMP" : pygame.K_UP,
                "DOWN" : pygame.K_DOWN,
                "MAGIC" : pygame.K_z,
                "DASH" : pygame.K_x,
                "MELEE" : pygame.K_c,
                "HEAL" : pygame.K_f,
                "ACTION1" : pygame.K_RETURN,
                "ACTION2" : pygame.K_TAB},
        },
        
        'game_data' : [],
        'curr_profile' : 0
    }
    return save

def load_controls(save_file):
    with open(os.path.join(save_file), 'r+') as file:
        controls = json.load(file)
    return controls

def write_save(data):
    with open(os.path.join(os.getcwd(), 'save.json'), 'w') as file:
        json.dump(data, file)

def load_save():
    try:
        save = load_controls('save.json')
    except:
        save = create_save()
        write_save(save)
    return save

def reset_key(action):
    for act in action:
        action[act] = False
    return action