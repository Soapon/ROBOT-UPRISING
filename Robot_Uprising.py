#ROBOT UPRISING GAME
#PEW PEW PEW
#-Sophia Ren
import arcade

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "ROBOT UPRISING"

# Player constants

PLAYER_MOVEMENT_SPEED = 5

# Background scroll speed
BACKGROUND_SCROLL_SPEED = 2

PLAYER_X = 2200
PLAYER_INITIAL_Y = SCREEN_HEIGHT // 2

class Player:
    """Player class that manages the player sprite"""
    
    def __init__(self, image_path, x, y):
        self.player_texture = arcade.load_texture(image_path)
        self.player_sprite = arcade.Sprite(self.player_texture, scale=1.0)
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y
        self.change_y = 0
    
    def update(self, delta_time=0):
        """Update player position"""
        self.player_sprite.center_y += self.change_y
        
        # Keep player within screen bounds
        if self.player_sprite.center_y < self.player_sprite.height // 2:
            self.player_sprite.center_y = self.player_sprite.height // 2
        elif self.player_sprite.center_y > SCREEN_HEIGHT - self.player_sprite.height // 2:
            self.player_sprite.center_y = SCREEN_HEIGHT - self.player_sprite.height // 2


class Background(arcade.Sprite):
    """Scrolling background sprite"""
    
    def __init__(self, image_path, x, y):
        super().__init__(image_path)
        self.center_x = x
        self.center_y = y
    
    def update(self, delta_time=0):
        """Scroll the background to the left"""
        self.center_x -= BACKGROUND_SCROLL_SPEED


class GameWindow(arcade.Window):
    """Main game window"""
    
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        # Sprite lists
        self.player_list = None
        self.background_list = None
        
        # Player object
        self.player = None
        
        # Background sprites
        self.background1 = None
        self.background2 = None
        
        arcade.set_background_color(arcade.color.SKY_BLUE)
    
        PLAYER_X = 2200
        PLAYER_INITIAL_Y = SCREEN_HEIGHT // 2

        """Set up the game"""
        # Create sprite lists
        self.player_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        
        # Create player
        self.player = Player("Friendly_Drone.png", 500, 550)
        self.player_list.append(self.player.player_sprite)
        #self.player_texture = arcade.load_texture("Friendly_Drone.png")
        #self.player_sprite_sheet = arcade.load_spritesheet(":resources:images/---", 64, 64, 4)
        #self.player_sprite = arcade.Sprite(self.player_texture)
        #self.player_sprite.center_x = WINDOW_WIDTH / 2
        #self.player_sprite.center_y = WINDOW_HEIGHT / 2
        
        # Create two background sprites for seamless scrolling
        # First background starts at center of screen

        self.background1 = Background("Background.png", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.background_list.append(self.background1)
        
        # Second background starts to the right of the first one
        # This assumes the background image width - adjust if needed
        self.background2 = Background("Background.png", SCREEN_WIDTH // 2 + SCREEN_WIDTH, SCREEN_HEIGHT // 2)
        self.background_list.append(self.background2)
    def setup(self):
        pass

    def on_draw(self):
        """Render the screen"""
        self.clear()
        
        # Draw backgrounds first (so they're behind the player)
        self.background_list.draw()
        
        # Draw player
        self.player_list.draw()
    
    def on_update(self, delta_time):
        """Update game logic"""
        # Update background
        self.background_list.update()
        
        # Reset background positions for infinite scrolling
        for background in self.background_list:
            # When a background scrolls off the left side, move it to the right
            if background.right < 0:
                background.left = SCREEN_WIDTH
        
        # Update player
        self.player.update()
    
    def on_key_press(self, key, modifiers):
        """Handle key presses"""
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -PLAYER_MOVEMENT_SPEED
    
    def on_key_release(self, key, modifiers):
        """Handle key releases"""
        if key in (arcade.key.UP, arcade.key.W, arcade.key.DOWN, arcade.key.S):
            self.player.change_y = 0


def main():
    """Main function"""
    window = GameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()