# ROBOT UPRISING GAME
# PEW PEW PEW
# -Sophia Ren
import arcade

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "ROBOT UPRISING"

# Player constants
PLAYER_MOVEMENT_SPEED = 5
PLAYER_HORIZONTAL_SPEED = 5
# Background scroll speed
BACKGROUND_SCROLL_SPEED = 2

PLAYER_X = 1100
PLAYER_INITIAL_Y = SCREEN_HEIGHT // 2

# Animation constants
ATTACK_ANIMATION_SPEED = 0.05  # Time per frame in seconds


class Player:
    """Player class that manages the player sprite with animation"""
    
    def __init__(self, sprite_sheet_path, x, y, frame_width, frame_height, num_frames):
        """
        Initialize player with sprite sheet animation
        
        Args:
            sprite_sheet_path: Path to the sprite sheet image
            x, y: Initial position
            frame_width: Width of each frame in the sprite sheet
            frame_height: Height of each frame in the sprite sheet
            num_frames: Number of frames in the sprite sheet
        """
        # Load the full sprite sheet image
        from PIL import Image
        
        # Extract individual frames from the sprite sheet manually
        self.textures = []
        sprite_image = Image.open(sprite_sheet_path)
        
        for i in range(num_frames):
            # Calculate the position of each frame
            left = i * frame_width
            upper = 0
            right = left + frame_width
            lower = frame_height
            
            # Crop the frame from the sprite sheet
            frame = sprite_image.crop((left, upper, right, lower))
            
            # Save to a temporary location and load as texture
            #This is my current solution, not sure if there's a better way
            temp_path = f"temp_frame_{i}.png"
            frame.save(temp_path)
            texture = arcade.load_texture(temp_path)
            self.textures.append(texture)
        
        sprite_image.close()
        
        # Create the sprite with the first (idle) texture
        self.player_sprite = arcade.Sprite()
        self.player_sprite.texture = self.textures[0]
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y
        self.player_sprite.scale = 1.6
        
        # Animation state
        self.is_attacking = False
        self.current_frame = 0
        self.animation_timer = 0
        
        # Movement
        self.change_y = 0
        self.change_x = 0
    
    def start_attack(self):
        """Start the attack animation"""
        if not self.is_attacking:
            self.is_attacking = True
            self.current_frame = 0
            self.animation_timer = 0
    
    def update(self, delta_time=0):
        """Update player position and animation"""
        # Update position
        self.player_sprite.center_y += self.change_y
        self.player_sprite.center_x += self.change_x
        
        # Keep player within screen bounds
        if self.player_sprite.center_y < self.player_sprite.height // 2:
            self.player_sprite.center_y = self.player_sprite.height // 2
        elif self.player_sprite.center_y > SCREEN_HEIGHT - self.player_sprite.height // 2:
            self.player_sprite.center_y = SCREEN_HEIGHT - self.player_sprite.height // 2
        if self.player_sprite.center_x < self.player_sprite.width // 2:
            self.player_sprite.center_x = self.player_sprite.width // 2
        elif self.player_sprite.center_x > SCREEN_WIDTH - self.player_sprite.width // 2:
            self.player_sprite.center_x = SCREEN_WIDTH - self.player_sprite.width // 2
        
        # Update animation
        if self.is_attacking:
            self.animation_timer += delta_time
            
            # Check if it's time to advance to the next frame
            if self.animation_timer >= ATTACK_ANIMATION_SPEED:
                self.animation_timer = 0
                self.current_frame += 1
                
                # Check if animation is complete
                if self.current_frame >= len(self.textures):
                    self.is_attacking = False
                    self.current_frame = 0
                else:
                    # Update the sprite's texture
                    self.player_sprite.texture = self.textures[self.current_frame]
            
        else:
            # Return to idle (first frame)
            self.player_sprite.texture = self.textures[0]


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
        self.friend = None
        
        # Background sprites
        self.background1 = None
        self.background2 = None
        
        arcade.set_background_color(arcade.color.SKY_BLUE)
        
        # Create sprite lists
        self.player_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        
        # Create player with sprite sheet animation
        # Adjust frame_width and frame_height based on your sprite sheet
        # If your sprite sheet is 6 frames wide, divide total width by 6
        self.player = Player(
            "Cyborg_attack3.png",
            PLAYER_X,
            PLAYER_INITIAL_Y,
            frame_width=48,  # Adjust this to match your sprite sheet frame width
            frame_height=48,  # Adjust this to match your sprite sheet frame height
            num_frames=6
        )
        self.player_list.append(self.player.player_sprite)
        
        # Create friend drone (using original single image)
        self.friend = Player.__new__(Player)  # Create instance without __init__
        self.friend.player_texture = arcade.load_texture("Friendly_Drone.png")
        self.friend.player_sprite = arcade.Sprite(self.friend.player_texture, scale=1.6)
        self.friend.player_sprite.center_x = PLAYER_X
        self.friend.player_sprite.center_y = PLAYER_INITIAL_Y - 50
        self.friend.change_y = 0
        self.friend.change_x = 0

        # Add simple update method for friend
        self.friend.update = self._friend_update
        self.player_list.append(self.friend.player_sprite)

        # Create two background sprites for seamless scrolling
        self.background1 = Background("Background.png", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.background_list.append(self.background1)
        
        self.background2 = Background("Background.png", SCREEN_WIDTH // 2 + SCREEN_WIDTH, SCREEN_HEIGHT // 2)
        self.background_list.append(self.background2)
    
    def _friend_update(self, delta_time=0):
        """Simple update for friend drone"""
        self.friend.player_sprite.center_y += self.friend.change_y
        self.friend.player_sprite.center_x += self.friend.change_x
        
        if self.friend.player_sprite.center_y < self.friend.player_sprite.height // 2:
            self.friend.player_sprite.center_y = self.friend.player_sprite.height // 2
        elif self.friend.player_sprite.center_y > SCREEN_HEIGHT - self.friend.player_sprite.height // 2:
            self.friend.player_sprite.center_y = SCREEN_HEIGHT - self.friend.player_sprite.height // 2
    
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
                # Position it immediately after the other background
                if background == self.background1:
                    background.left = self.background2.right
                else:
                    background.left = self.background1.right
        
        # Update player with delta_time for animation
        self.player.update(delta_time)
        self.friend.update(delta_time)
    
    def on_key_press(self, key, modifiers):
        """Handle key presses"""
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = PLAYER_MOVEMENT_SPEED
            self.friend.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -PLAYER_MOVEMENT_SPEED
            self.friend.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -PLAYER_HORIZONTAL_SPEED
            self.friend.change_x = -PLAYER_HORIZONTAL_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = PLAYER_HORIZONTAL_SPEED
            self.friend.change_x = PLAYER_HORIZONTAL_SPEED
        elif key == arcade.key.SPACE:
            # Trigger attack animation
            self.player.start_attack()
    
    def on_key_release(self, key, modifiers):
        """Handle key releases"""
        if key in (arcade.key.UP, arcade.key.W, arcade.key.DOWN, arcade.key.S):
            self.player.change_y = 0
            self.friend.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
            self.player.change_x = 0
            self.friend.change_x = 0

def main():
    """Main function"""
    window = GameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()