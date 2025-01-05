import pygame
import random


pygame.init()

clock = pygame.time.Clock()

fps = 60

# Game window dimensions
bottom_panel = 150
screen_width = 1000
screen_height = 450 + bottom_panel

# Create game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

#def fonts
font = pygame.font.SysFont('Arial', 26)



#def game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90








#def colors
red = (255, 0 ,0)
green = (0, 255 ,0)



# Load and scale background image to match screen size 
background_img = pygame.image.load('game/Background.jpg').convert_alpha()
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
panel_img = pygame.image.load('game/icons/panel.png').convert_alpha()


#create function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    



# Function to draw the background
def draw_bg():
    screen.blit(background_img, (0, 0))
    
    
    


def draw_panel():
	#draw panel rectangle
	screen.blit(panel_img, (135, 500))
	#show knight stats
	draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel + 30)
	for count, i in enumerate(enemy_list):
		#show name and health
		draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel + 10) + count * 30)


# Fighter class
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: idle, 1: attack, 2: hurt, 3: dead
        self.update_time = pygame.time.get_ticks()
        # Load idle images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'game/{self.name}/idle/{i}.png')
            img = self.image = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'game/{self.name}/attack/{i}.png')
            img = self.image = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5))
            temp_list.append(img)

        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        # Handle animation
        # Update image
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # If the animation has run out then reset back to start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def attack(self, target):
        #deal damage
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
    
    
    def draw(self):
        screen.blit(self.image, self.rect)


class healthbar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
        
    def draw(self, hp):
        pygame.draw.rect(screen, red, (self.x, self.y, 50, 10))


knight = Fighter(200, 300, 'knight', 30, 10, 3)
enemy1 = Fighter(650, 420, 'enemy', 20, 6, 1)
enemy2 = Fighter(800, 420, 'enemy', 20, 6, 1)

enemy_list = [enemy1, enemy2]


knight_health_bar = healthbar(100, screen_height - bottom_panel + 60, knight.hp, knight.max_hp)
enemy2_health_bar = healthbar(100, screen_height - bottom_panel + 100, enemy2.hp, enemy2.max_hp)
enemy1_health_bar = healthbar(100, screen_height - bottom_panel + 40, enemy1.hp, enemy1.max_hp)

# Add movement and physics variables
gravity = 1
floor_y = 500  # Y position of the "floor"
knight_speed = 5
knight_dx, knight_dy = 0, 0
knight_jump = False
knight_jump_force = -15

# Game state variables
paused = False
menu_option = 0  # 0: Continue, 1: Exit

# Font setup for rendering text
font = pygame.font.SysFont('Arial', 72)
small_font = pygame.font.SysFont('Arial', 36)

def draw_pause_menu():
    screen.fill((0, 0, 0, 150))  # Semi-transparent black overlay
    text = font.render("PAUSED", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(text, text_rect)

    # Draw menu options
    continue_text = small_font.render("Continue", True, (255, 255, 255))
    continue_rect = continue_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(continue_text, continue_rect)

    exit_text = small_font.render("Exit", True, (255, 255, 255))
    exit_rect = exit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(exit_text, exit_rect)

    # Highlight the selected option
    if menu_option == 0:
        pygame.draw.rect(screen, (255, 0, 0), continue_rect.inflate(10, 10), 3)
    else:
        pygame.draw.rect(screen, (255, 0, 0), exit_rect.inflate(10, 10), 3)

    return continue_rect, exit_rect

def handle_pause_menu_input(event):
    global menu_option, paused, run

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            menu_option = 0  # Select "Continue"
        elif event.key == pygame.K_DOWN:
            menu_option = 1  # Select "Exit"
        elif event.key == pygame.K_RETURN:  # Press Enter
            if menu_option == 0:
                paused = False  # Continue the game
            elif menu_option == 1:
                run = False  # Exit the game

def handle_mouse_click():
    global paused, run

    mouse_x, mouse_y = pygame.mouse.get_pos()
    continue_rect, exit_rect = draw_pause_menu()  # Get the position of buttons

    # Check if the mouse click is within the "Continue" button
    if continue_rect.collidepoint(mouse_x, mouse_y):
        paused = False  # Continue the game

    # Check if the mouse click is within the "Exit" button
    elif exit_rect.collidepoint(mouse_x, mouse_y):
        run = False  # Exit the game

# Main game loop
run = True
while run:
    clock.tick(fps)
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Handle input during the pause menu
        if paused:
            handle_pause_menu_input(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESC to pause/unpause
                paused = not paused  # Toggle the pause state

        # Handle mouse click during the pause menu
        if event.type == pygame.MOUSEBUTTONDOWN:
            if paused:
                handle_mouse_click()

    if paused:
        # Draw the pause menu
        draw_pause_menu()
    else:
        # Draw background
        draw_bg()
        draw_panel()
        #knight_health_bar.draw(knight.hp)
        #enemy1_health_bar.draw(enemy1.hp)
        #enemy2_health_bar.draw(enemy2.hp)
        # Gravity for knight
        if knight.rect.y + knight.rect.height < floor_y:  # Check if the knight is above the floor
            knight_dy += gravity  # Apply gravity
        else:
            knight_dy = 0  # Stop vertical movement
            knight.rect.y = floor_y - knight.rect.height  # Correct position to stay on the floor
            knight_jump = False  # Reset jump when on the floor

        # Apply movement
        knight.rect.x += knight_dx
        knight.rect.y += knight_dy
        knight.update()
        knight.draw()

        # Gravity for enemies (no movement)
        for enemy in enemy_list:
            # Apply gravity
            if enemy.rect.y + enemy.rect.height < floor_y:
                enemy.rect.y += gravity
            else:
                enemy.rect.y = floor_y - enemy.rect.height

            enemy.update()
            enemy.draw()
        if knight.alive == True:
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    #look for player action
                    #attack
                    knight.attack(enemy1)
                    current_fighter += 1
                    action_cooldown
    # Update display
    pygame.display.update()

# Quit pygame
pygame.quit()
