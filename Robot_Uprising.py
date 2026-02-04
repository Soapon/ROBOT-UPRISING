# ROBOT UPRISING GAME
# PEW PEW PEW
# -Sophia Ren
import arcade
import random

# Constants - This is the adjusted screen size from tutorial
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
Bullet_speed = 26
# Animation constants
ATTACK_ANIMATION_SPEED = 0.05  # Time per frame in seconds

# Health constants
PLAYER_MAX_HEALTH = 3

# Imported for GameState
from enum import Enum

# Game state enumeration for managing different screens
class GameState(Enum):
    START_SCREEN = 1
    PLAYING = 2
    GAME_OVER = 3

#Player setup class
class Player:
    """Player class that manages the player sprite with animation"""
    
    def __init__(self, sprite_sheet_path, x, y, num_frames):
        """
        Initialize player with sprite sheet animation
        """
        # Load the full sprite sheet image (I couldn't find a way in the documentation to automatically split sprite sheets)
        from PIL import Image
        
        #Extract individual frames from the sprite sheet manually
        self.textures = []
        sprite_image = Image.open(sprite_sheet_path)
        
        for i in range(num_frames):
            temp_path = f"CA_{i}.png"
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
        """Start the attack animation, only start if not already attacking"""
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
        if self.player_sprite.center_y < self.player_sprite.height // 2 + 50:
            self.player_sprite.center_y = self.player_sprite.height // 2 + 50
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

class Enemy:
    """Enemy drone class that randomly selects from available drone types with animation"""
    
    def __init__(self, x, y, speed=1):
        """
        Initialize enemy drone with animation
        """
        from PIL import Image
        
        # Randomly choose a drone type from 1 to 5
        drone_number = random.randint(1, 5)
        
        # Load animation frames for this enemy type
        self.textures = []
        num_frames = 4
        
        
        for i in range(num_frames):
            sprite_image = Image.open(f"Enemy_Drone_{drone_number}.png")
            frame_width = sprite_image.height
            frame_height = sprite_image.height
            left = i * frame_width
            upper = 0
            right = left + frame_width
            lower = frame_height
            
            # Crop the frame from the sprite sheet
            frame = sprite_image.crop((left, upper, right, lower))
            
            # Save to a temporary location and load as texture
            #This is my current solution, not sure if there's a better way
            temp_path = f"Enemy_Drone_{drone_number}_frame_{i}.png"
            frame.save(temp_path)
            frame_path = f"Enemy_Drone_{drone_number}_frame_{i}.png"
            texture = arcade.load_texture(frame_path)
            self.textures.append(texture)
        
        # Create the sprite with the first frame
        self.enemy_sprite = arcade.Sprite()
        self.enemy_sprite.texture = self.textures[0]
        self.enemy_sprite.center_x = x
        self.enemy_sprite.center_y = y
        self.enemy_sprite.scale = 1.2
        
        # Movement
        self.speed = speed
        self.change_x = speed
        self.change_y = 0
        
        # Animation state
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1  # Time per frame in seconds (adjust for faster/slower animation)
    
    def update(self, delta_time=0):
        """Update enemy position and animation"""
        # Update position
        self.enemy_sprite.center_x += self.change_x
        self.enemy_sprite.center_y += self.change_y
        
        # Update animation
        self.animation_timer += delta_time
        
        # Check if it's time to advance to the next frame
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.textures)
            self.enemy_sprite.texture = self.textures[self.current_frame]

class Bullet(arcade.Sprite):
    """Bullet sprite fired by the player"""
    
    def __init__(self, image_path, x, y, speed):
        super().__init__(image_path)
        self.center_x = x
        self.center_y = y
        self.speed = speed
    
    def update(self, delta_time=0):
        """Move the bullet to the left (negative x direction)"""
        self.center_x -= self.speed


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
        
        # Game state
        self.current_state = GameState.START_SCREEN
        
        # Sprite lists
        self.player_list = None
        self.background_list = None
        self.bullet_list = None
        self.enemy_list = None
        
        # Player object
        self.player = None
        self.friend = None
        
        # Background sprites
        self.background1 = None
        self.background2 = None
        
        # Score
        self.score = 0
        
        # Health
        self.health = PLAYER_MAX_HEALTH
        
        # Health bar texture
        self.health_bar_texture = None
        
        # Bullet cooldown
        self.bullet_cooldown = 0
        self.bullet_cooldown_time = 0.4
        
        arcade.set_background_color(arcade.color.SKY_BLUE)
        
        # Initialize backgrounds immediately so they show on start screen
        self.background_list = arcade.SpriteList()
        self.background1 = Background("Background.png", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.background_list.append(self.background1)
        self.background2 = Background("Background.png", SCREEN_WIDTH // 2 + SCREEN_WIDTH, SCREEN_HEIGHT // 2)
        self.background_list.append(self.background2)
    
    def setup(self):
        """Set up the game"""
        # Unschedule any previous enemy spawning
        arcade.unschedule(self.spawn_enemy)
        
        # Create sprite lists
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.enemy_objects = []
        # Reset score
        self.score = 0
        
        # Reset health
        self.health = PLAYER_MAX_HEALTH
        
        # Reset bullet cooldown
        self.bullet_cooldown = 0
        
        # Create player with sprite sheet animation
        self.player = Player(
            "Cyborg_attack3.png",
            PLAYER_X,
            PLAYER_INITIAL_Y,
            num_frames=6
        )
        self.player_list.append(self.player.player_sprite)
        
        # Create friend drone that follows the player (at y - 50)
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
        
        # Schedule enemy spawning every 1 seconds
        spawn_cooldown = random.uniform(0.5, 1.5)  # Randomize spawn cooldown between 0.5 and 1.5 seconds
        arcade.schedule(self.spawn_enemy, spawn_cooldown)
    
    def _friend_update(self, delta_time=0):
        """Simple update for friend drone"""
        self.friend.player_sprite.center_y += self.friend.change_y
        self.friend.player_sprite.center_x = self.player.player_sprite.center_x
        
        if self.friend.player_sprite.center_y < self.friend.player_sprite.height // 2:
            self.friend.player_sprite.center_y = self.friend.player_sprite.height // 2
        elif self.friend.player_sprite.center_y > SCREEN_HEIGHT - self.friend.player_sprite.height // 2 - 50:
            self.friend.player_sprite.center_y = SCREEN_HEIGHT - self.friend.player_sprite.height // 2 - 50
    
    def spawn_enemy(self, delta_time):
        """Spawn a new enemy at a random height"""
        if self.current_state == GameState.PLAYING:
            # Generate random y position in increments of 30 from 100 to 670
            possible_heights = list(range(100, 671, 30))
            y_position = random.choice(possible_heights)
        
            # Create enemy at x = -30, moving right
            enemy = Enemy(-30, y_position, speed=1)
            self.enemy_list.append(enemy.enemy_sprite)  # Add sprite to sprite list
            self.enemy_objects.append(enemy)  # Add Enemy object to tracking list
    
    def shoot_bullet(self):
        """Create and fire a bullet from the player's position"""
        bullet = Bullet(
            "Bullet.png",
            self.player.player_sprite.center_x,
            self.player.player_sprite.center_y,
            Bullet_speed
        )
        self.bullet_list.append(bullet)
    
    def draw_start_screen(self):
        """Draw the start screen with background"""
        # Draw background
        self.background_list.draw()
        
        #Draws the big start logo in the middle of the screen (only on the start screen)
        self.start_logo_texture = arcade.load_texture("START_LOGO.png")
        self.start_logo_sprite = arcade.Sprite(self.start_logo_texture)
        self.start_logo_sprite.center_x = SCREEN_WIDTH / 2
        self.start_logo_sprite.center_y = SCREEN_HEIGHT / 2 - 10
        arcade.draw_sprite(self.start_logo_sprite)

    def draw_game_over(self):
        """Draw the game over screen with frozen game state"""
        # Draw the frozen game state
        self.background_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        
        # Draw semi-transparent overlay
        arcade.draw_lbwh_rectangle_filled(
            0, 0,
            SCREEN_WIDTH, SCREEN_HEIGHT,
            (0, 0, 0, 150)  # Semi-transparent black
        )
        #Draws the big end in the middle of the screen
        self.end_screen_texture = arcade.load_texture("END_SCREEN.png")
        self.end_screen_sprite = arcade.Sprite(self.end_screen_texture)
        self.end_screen_sprite.center_x = SCREEN_WIDTH / 2
        self.end_screen_sprite.center_y = SCREEN_HEIGHT / 2 - 10
        arcade.draw_sprite(self.end_screen_sprite)

        arcade.draw_text(
            score_text := f"{self.score}",
            SCREEN_WIDTH / 2 + 20,
            SCREEN_HEIGHT / 2 - 55,
            arcade.color.EARTH_YELLOW,
            font_size=30,
            anchor_x="center"
        )


    def on_draw(self):
        """Draw everything"""
        self.clear()
        
        if self.current_state == GameState.START_SCREEN:
            self.draw_start_screen()
        
        elif self.current_state == GameState.PLAYING:
            # Draw backgrounds first (so they're behind the player)
            self.background_list.draw()
            
            # Draw enemies
            self.enemy_list.draw()
            
            # Draw bullets
            self.bullet_list.draw()
            
            # Draw player
            self.player_list.draw()
            

            # Draw score
            arcade.draw_text(
                f"Score: {self.score}",
                10,
                SCREEN_HEIGHT - 30,
                arcade.color.WHITE,
                font_size=20,
                bold=True
            )
            
            # Draw health bar
            self.draw_health_bar()
        
        elif self.current_state == GameState.GAME_OVER:
            self.draw_game_over()
    
    def draw_health_bar(self):
        """Draw the health bar below the score"""
        try:
            # Load the appropriate health bar texture based on current health
            heart_bar_texture = arcade.load_texture(f"HEART_BAR_{self.health}.png")
            heart_bar_sprite = arcade.Sprite(heart_bar_texture, scale = 0.6)
            
            # Position it below the score (adjust these values as needed)
            heart_bar_sprite.left = 8  # I didn't want to show the text "Health: " so I just moved the health bar left to cover it up, this is a bit hacky but it works for now
            heart_bar_sprite.bottom = SCREEN_HEIGHT - 70  # Below the score
            
            arcade.draw_sprite(heart_bar_sprite)
        except FileNotFoundError:
            # Fallback to text if image not found
            arcade.draw_text(
                f"Health: {self.health}",
                10,
                SCREEN_HEIGHT - 60,
                arcade.color.WHITE,
                font_size=20,
                bold=True
            )
    
    def on_update(self, delta_time):
        """Update game logic"""
        # Update background scrolling on start screen and during gameplay
        if self.current_state in [GameState.START_SCREEN, GameState.PLAYING]:
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
        

        if self.current_state == GameState.PLAYING:
            # Update bullet cooldown
            if self.bullet_cooldown > 0:
                self.bullet_cooldown -= delta_time
            
            # Update bullets
            self.bullet_list.update()
            # Update enemies
            for enemy in self.enemy_list:
                enemy.update(delta_time)
            
            # Remove bullets that are off-screen
            for bullet in self.bullet_list:
                if bullet.center_x < -bullet.width:
                    bullet.remove_from_sprite_lists()
            
            # Update enemies
            for enemy in self.enemy_objects:  # Changed from self.enemy_list
                enemy.update(delta_time)

            # Remove enemies that are off-screen
            for enemy in self.enemy_objects[:]:  # Create a copy to iterate over
                if enemy.enemy_sprite.right > SCREEN_WIDTH:  # Fixed the condition
                    enemy.enemy_sprite.remove_from_sprite_lists()
                    self.health -= 1
                    self.enemy_objects.remove(enemy)
            # Check for bullet-enemy collisions
            for bullet in self.bullet_list:
                enemies_hit = arcade.check_for_collision_with_list(bullet, self.enemy_list)
    
                for enemy_sprite in enemies_hit:
                    # Remove the bullet
                    bullet.remove_from_sprite_lists()
        
                    # Remove the enemy
                    for enemy in self.enemy_objects[:]:  # Changed
                        if enemy.enemy_sprite == enemy_sprite:
                            enemy.enemy_sprite.remove_from_sprite_lists()
                            self.enemy_objects.remove(enemy)  # Changed
                            self.score += 10
                            break
                    break

            # Check for player-enemy collisions
            for enemy in self.enemy_objects:  # Changed
                if arcade.check_for_collision(self.player.player_sprite, enemy.enemy_sprite):
                    # Reduce health instead of immediately ending game
                    self.health -= 1
                    
                    # Remove the enemy that hit the player
                    enemy.enemy_sprite.remove_from_sprite_lists()
                    self.enemy_objects.remove(enemy)
                    
                    # Check if health reached zero
                    if self.health <= 0:
                        self.current_state = GameState.GAME_OVER
                        arcade.unschedule(self.spawn_enemy)
                    break  # Exit loop after collision detected


            # Update player with delta_time for animation
            self.player.update(delta_time)
            self.friend.update(delta_time)
    
    def on_key_press(self, key, modifiers):
        """Handle key presses"""
        if self.current_state == GameState.START_SCREEN:
            if key == arcade.key.SPACE:
                self.current_state = GameState.PLAYING
                self.setup()
        
        elif self.current_state == GameState.PLAYING:
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
                # Only shoot if cooldown has expired
                if self.bullet_cooldown <= 0:
                    # Trigger attack animation and shoot bullet
                    self.player.start_attack()
                    self.shoot_bullet()
                    # Reset cooldown
                    self.bullet_cooldown = self.bullet_cooldown_time
        
        elif self.current_state == GameState.GAME_OVER:
            if key == arcade.key.SPACE:
                self.current_state = GameState.PLAYING
                self.setup()
    
    def on_key_release(self, key, modifiers):
        """Handle key releases"""
        if self.current_state == GameState.PLAYING:
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