import pygame

pygame.init()


clock = pygame.time.Clock()

fps = 60


# Game window dimensions
screen_width = 1000
screen_height = 600

# Create game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

# Load and scale background image to match screen size 
background_img = pygame.image.load('game/Background.jpg').convert_alpha()
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Function to draw the background
def draw_bg():
    screen.blit(background_img, (0, 0))






#fighter class

class Fighter():
    def __init__ (self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 #0: idle 1;attack 2;hurt 3;dead
        self.update_time = pygame.time.get_ticks()
        #load idle images
        
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'game/{self.name}/idle/{i}.png')
            img = self.image = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5 ))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        
        
        
        
                #load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'game/{self.name}/attack/{i}.png')
            img = self.image = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5 ))
            temp_list.append(img)



        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)




    def update(self):
        animation_cooldown = 100
        #handle animation
        #update image 
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enought time passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out then reset back to start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        
        
        
    def draw(self):
        screen.blit(self.image, self.rect)
        
        
knight = Fighter(200, 300, 'knight', 30, 10, 3)
enemy1 = Fighter(550, 320, 'enemy', 20, 6, 1)
enemy2 = Fighter(700, 320, 'enemy', 20, 6, 1)
enemy3 = Fighter(850, 320, 'enemy', 20, 6, 1)


enemy_list = []
enemy_list.append(enemy1)
enemy_list.append(enemy2)
enemy_list.append(enemy3)




# Main game loop
run = True
while run:
    
    clock.tick(fps)
    
    # Draw background
    draw_bg()
    
    
    #draw fighter
    knight.update()
    knight.draw()
    
    for enemy in enemy_list:
        enemy.draw()
        enemy.update()
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            # If the Q key is pressed, quit the game
            if event.key == pygame.K_q:
                run = False
    
    # Update display
    pygame.display.update()

    # Update display
    pygame.display.update()

# Quit pygame
pygame.quit()


