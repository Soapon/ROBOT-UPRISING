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
JUMP_ANIMATION_SPEED = 0.03
POWERUP_DURATION = 2.0  # How long the powerup lasts in seconds
JUMPING_SPEED = 10
HOLD_AT_POSITION_DURATION = 3.5  # How long to stay at top/bottom in seconds
POWERUP_ENEMY_DESTRUCTION_TIME = 2.5  # When to destroy all enemies during powerup

# Health constant
PLAYER_MAX_HEALTH = 3

#Imported for GameState
from enum import Enum
# Game state enumeration for managing different screens
class GameState(Enum):
    START_SCREEN = 1
    PLAYING = 2
    GAME_OVER = 3

# Jump states
class JumpState(Enum):
    NOT_JUMPING = 0
    MOVING_TO_POSITION = 1
    HOLDING_AT_POSITION = 2
    RETURNING_TO_ORIGINAL = 3

#Player setup class
class Player:
    """Player class that manages the player sprite with animation"""
    
    def __init__(self, sprite_sheet_path, x, y, num_frames, jump_frames=4):
        """
        Initialize player with sprite sheet animation
        """
        # Load the full sprite sheet image (I couldn't find a way in the documentation to automatically split sprite sheets, so if you go to enemies class you can see the for loop i used to cut them up)
        from PIL import Image
        
        #Extract individual frames from the sprite sheet manually
        self.textures = []
        self.jumping_textures = []
        sprite_image = Image.open(sprite_sheet_path)
        
        #adds the frames to the textures list
        for i in range(num_frames):
            temp_path = f"CA_{i}.png"
            texture = arcade.load_texture(temp_path)
            self.textures.append(texture)
        
        sprite_image.close()

        #rotating through the textures
        for i in range(jump_frames):
            temp_path = f"CJ_{i}.png"  # Adjust filename to match your jump sprite files
            texture = arcade.load_texture(temp_path)
            self.jumping_textures.append(texture)
        
        # create the sprite with the first
        self.player_sprite = arcade.Sprite()
        self.player_sprite.texture = self.textures[0]
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y
        self.player_sprite.scale = 1.6
        
        #animation state
        self.is_jumping = False
        self.is_powering = False
        self.is_attacking = False
        self.current_frame = 0
        self.animation_timer = 0
        self.jump_animation_complete = False
        self.powerup_timer = 0
        self.powerup_elapsed = 0  # Track elapsed time during powerup
        self.enemies_destroyed = False  # Track if enemies have been destroyed this powerup
        
        # Jump movement state
        self.jump_state = JumpState.NOT_JUMPING
        self.hold_timer = 0
        self.original_y = y
        
        # Movement
        self.change_y = 0
        self.change_x = 0

    #Start the firing animation
    def start_attack(self):
        """Start the attack animation, only start if not already attacking"""
        if not self.is_attacking:
            self.is_attacking = True
            self.current_frame = 0
            self.animation_timer = 0
        
    #Jumping motion, to be called in powerup    
    def start_jump(self):
        """Start the jump animation, only start if not already jumping"""
        if not self.is_jumping:
            self.is_jumping = True
            self.current_frame = 0
            self.animation_timer = 0
            self.jump_animation_complete = False
            self.jump_state = JumpState.MOVING_TO_POSITION
            self.original_y = self.player_sprite.center_y
    
    #Start the power
    def start_power(self):
        """Start the powerup animation"""
        if not self.is_powering:
            self.is_powering = True
            self.start_jump()  # Start jump animation when powering up
            self.powerup_timer = POWERUP_DURATION
            self.powerup_elapsed = 0  # Reset elapsed time
            self.enemies_destroyed = False  # Reset destruction flag
    
    #update player
    def update(self, delta_time=0):
        """Update player position and animation"""
        # Update powerup elapsed time
        if self.is_powering:
            self.powerup_elapsed += delta_time
        
        # Handle jump movement states
        if self.jump_state == JumpState.MOVING_TO_POSITION:
            # Move upward
            self.player_sprite.center_y += JUMPING_SPEED
            
            # Check if reached top of screen
            if self.player_sprite.center_y >= SCREEN_HEIGHT - self.player_sprite.height // 2:
                self.player_sprite.center_y = SCREEN_HEIGHT - self.player_sprite.height // 2
                self.jump_state = JumpState.HOLDING_AT_POSITION
                self.hold_timer = HOLD_AT_POSITION_DURATION
        
        elif self.jump_state == JumpState.HOLDING_AT_POSITION:
            #stay at position for duration
            self.hold_timer -= delta_time
            if self.hold_timer <= 0:
                self.jump_state = JumpState.RETURNING_TO_ORIGINAL
        
        elif self.jump_state == JumpState.RETURNING_TO_ORIGINAL:
            #Move back to original position
            if self.player_sprite.center_y > self.original_y:
                self.player_sprite.center_y -= JUMPING_SPEED
                
                # Check if reached original position
                if self.player_sprite.center_y <= self.original_y:
                    self.player_sprite.center_y = self.original_y
                    self.jump_state = JumpState.NOT_JUMPING
                    self.is_powering = False
                    self.is_jumping = False
                    self.jump_animation_complete = False
        
        # Normal horizontal movement
        if self.jump_state == JumpState.NOT_JUMPING:
            self.player_sprite.center_y += self.change_y
            self.player_sprite.center_x += self.change_x
        else:
            #Only allow horizontal movement during jump
            self.player_sprite.center_x += self.change_x
        
        # Keep player within screen bounds
        if self.jump_state == JumpState.NOT_JUMPING:
            if self.player_sprite.center_y < self.player_sprite.height // 2 + 50:
                self.player_sprite.center_y = self.player_sprite.height // 2 + 50
            elif self.player_sprite.center_y > SCREEN_HEIGHT - self.player_sprite.height // 2:
                self.player_sprite.center_y = SCREEN_HEIGHT - self.player_sprite.height // 2
        
        if self.player_sprite.center_x < self.player_sprite.width // 2:
            self.player_sprite.center_x = self.player_sprite.width // 2
        elif self.player_sprite.center_x > SCREEN_WIDTH - self.player_sprite.width // 2:
            self.player_sprite.center_x = SCREEN_WIDTH - self.player_sprite.width // 2
        
        #Update animation
        if self.is_attacking and not self.is_powering:
            self.animation_timer += delta_time
            
            #check if it's time to advance to the next frame
            if self.animation_timer >= ATTACK_ANIMATION_SPEED:
                self.animation_timer = 0
                self.current_frame += 1
                
                #finish animation for attack
                if self.current_frame >= len(self.textures):
                    self.is_attacking = False
                    self.current_frame = 0
                else:
                    # Update the sprite's texture
                    self.player_sprite.texture = self.textures[self.current_frame]
            
        elif self.is_jumping:
            self.animation_timer += delta_time
            
            # Check if it's time to advance to the next frame
            if self.animation_timer >= JUMP_ANIMATION_SPEED:
                self.animation_timer = 0
                
                # Only advance frame if we haven't completed the animation yet
                if not self.jump_animation_complete:
                    self.current_frame += 1
                    
                    # Check if animation reached the last frame
                    if self.current_frame >= len(self.jumping_textures):
                        # Freeze on the last frame
                        self.current_frame = len(self.jumping_textures) - 1
                        self.jump_animation_complete = True
                    
                    # Update the sprite's texture
                    self.player_sprite.texture = self.jumping_textures[self.current_frame]
        else:
            # Return to idle (first frame)
            self.player_sprite.texture = self.textures[0]

#Enemy drone class
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

        #This is the loop i used to cut up the sprites, I deleted it from the other classes after all of them are properly generated, but I left it here
        
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
            
            #save to temporary location and load as texture
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

#Bullet class ~
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

#This is background
class Background(arcade.Sprite):
    """Scrolling background sprite"""
    
    def __init__(self, image_path, x, y):
        super().__init__(image_path)
        self.center_x = x
        self.center_y = y
    
    def update(self, delta_time=0):
        """Scroll the background to the left"""
        self.center_x -= BACKGROUND_SCROLL_SPEED

#Explosion, i realize now that I could have just replaced the destroyed enemies with the image but this works too
class Explosion:
    """Explosion effect that displays briefly and then disappears"""
    
    def __init__(self, x, y):
        self.explosion_sprite = arcade.Sprite("EXPLOSION.png", scale=0.4)
        self.explosion_sprite.center_x = x
        self.explosion_sprite.center_y = y
        self.timer = 0.1  # Duration in seconds
        self.finished = False
    
    def update(self, delta_time=0):
        """Update explosion timer"""
        self.timer -= delta_time
        if self.timer <= 0:
            self.finished = True

#The main gamewindow
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
        self.explosion_list = None
        
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
        # Power cooldown
        self.power_cooldown = 0
        self.power_cooldown_time = 45.0
        
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
        self.explosion_list = arcade.SpriteList()
        self.explosion_objects = []
        # Reset score
        self.score = 0
        
        # Reset health
        self.health = PLAYER_MAX_HEALTH
        
        # Reset bullet cooldown
        self.bullet_cooldown = 0
        
        # Reset power cooldown
        self.power_cooldown = 0
        
        # Create player with sprite sheet animation
        self.player = Player(
            "Cyborg_attack3.png",
            PLAYER_X,
            PLAYER_INITIAL_Y,
            num_frames=6,
            jump_frames=6
        )

        self.player_list.append(self.player.player_sprite)
        
        #Create friend drone that carries the player around
        self.friend = Player.__new__(Player)  # Create instance without __init__
        self.friend.player_texture = arcade.load_texture("Friendly_Drone.png")
        self.friend.player_sprite = arcade.Sprite(self.friend.player_texture, scale=1.6)
        self.friend.player_sprite.center_x = PLAYER_X
        self.friend.player_sprite.center_y = PLAYER_INITIAL_Y - 50
        self.friend.change_y = 0
        self.friend.change_x = 0
        self.friend.jump_state = JumpState.NOT_JUMPING
        self.friend.hold_timer = 0
        self.friend.original_y = PLAYER_INITIAL_Y - 50

        # Add simple update method for friend
        self.friend.update = lambda dt: self._friend_update(dt)
        self.player_list.append(self.friend.player_sprite)
        
        # Schedule enemy spawning every 1 seconds
        spawn_cooldown = random.uniform(0.5, 1.5)  # Randomize spawn cooldown between 0.5 and 1.5 seconds
        arcade.schedule(self.spawn_enemy, spawn_cooldown)
    
    def _friend_update(self, delta_time=0):
        # Handle jump movement states (opposite direction of player)
        if self.friend.jump_state == JumpState.MOVING_TO_POSITION:
            # Move downward (opposite of player)
            self.friend.player_sprite.center_y -= JUMPING_SPEED
            
            # check if reached bottom of screen
            if self.friend.player_sprite.center_y <= self.friend.player_sprite.height // 2:
                self.friend.player_sprite.center_y = self.friend.player_sprite.height // 2
                self.friend.jump_state = JumpState.HOLDING_AT_POSITION
                self.friend.hold_timer = HOLD_AT_POSITION_DURATION
        
        #At the very tippy top :>
        elif self.friend.jump_state == JumpState.HOLDING_AT_POSITION:
            # Stay at position for duration
            self.friend.hold_timer -= delta_time
            if self.friend.hold_timer <= 0:
                self.friend.jump_state = JumpState.RETURNING_TO_ORIGINAL
        
        elif self.friend.jump_state == JumpState.RETURNING_TO_ORIGINAL:
            #Move back to original position
            if self.friend.player_sprite.center_y < self.friend.original_y:
                self.friend.player_sprite.center_y += JUMPING_SPEED
                
                # Check if reached original position
                if self.friend.player_sprite.center_y >= self.friend.original_y:
                    self.friend.player_sprite.center_y = self.friend.original_y
                    self.friend.jump_state = JumpState.NOT_JUMPING
        
        #Normal movement when not jumping
        if self.friend.jump_state == JumpState.NOT_JUMPING:
            self.friend.player_sprite.center_y += self.friend.change_y
        
        # Always follow player's x position
        self.friend.player_sprite.center_x = self.player.player_sprite.center_x
        
        #keep within bounds
        if self.friend.jump_state == JumpState.NOT_JUMPING:
            if self.friend.player_sprite.center_y < self.friend.player_sprite.height // 2:
                self.friend.player_sprite.center_y = self.friend.player_sprite.height // 2
            elif self.friend.player_sprite.center_y > SCREEN_HEIGHT - self.friend.player_sprite.height // 2 - 50:
                self.friend.player_sprite.center_y = SCREEN_HEIGHT - self.friend.player_sprite.height // 2 - 50
    
    def spawn_enemy(self, delta_time):
        """Spawn a new enemy at a random height"""
        if self.current_state == GameState.PLAYING:
            #random y position in increments of 30 from 100 to 670
            possible_heights = list(range(100, 671, 30))
            y_position = random.choice(possible_heights)
        
            # Create enemy at x = -30, moving right so that it looks smooth
            enemy = Enemy(-30, y_position, speed=1)
            self.enemy_list.append(enemy.enemy_sprite)  # Add sprite to sprite list
            self.enemy_objects.append(enemy)  # Add Enemy object to tracking list
    
    #adding bullet
    def shoot_bullet(self):
        """Create and fire a bullet from the player's position"""
        bullet = Bullet(
            "Bullet.png",
            self.player.player_sprite.center_x,
            self.player.player_sprite.center_y,
            Bullet_speed
        )
        self.bullet_list.append(bullet)
    

    def create_explosion(self, x, y):
        """Create an explosion effect at the given position (the position of the dead robot)"""
        explosion = Explosion(x, y)
        self.explosion_list.append(explosion.explosion_sprite)
        self.explosion_objects.append(explosion)
    
    def draw_start_screen(self):
        """Draw the start screen with background"""
        # Draw background
        self.background_list.draw()
        
        #Draws the big start logo in the middle of the screen (only on the start screen)
        self.start_logo_texture = arcade.load_texture("START_LOGO.png")
        self.start_logo_sprite = arcade.Sprite(self.start_logo_texture)
        self.start_logo_sprite.center_x = SCREEN_WIDTH / 2
        self.start_logo_sprite.center_y = SCREEN_HEIGHT / 2 + 10
        arcade.draw_sprite(self.start_logo_sprite)
    
    #last screen
    def draw_game_over(self):
        """Draw the game over screen with frozen game state"""
        # Draw the frozen game state, stops moving/updating
        self.background_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        
        #Draw transparent overlay
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
    #the vertical yellowish line
    def draw_powerup_line(self):
        """Draw a yellow line between player and friend drone during powerup"""
        if self.player.is_powering:
            # Calculate the line coordinates
            player_x = self.player.player_sprite.center_x
            player_y = self.player.player_sprite.center_y
            friend_y = self.friend.player_sprite.center_y
            
            #draw a thin yellow line
            arcade.draw_line(
                player_x+8, player_y,
                player_x+8, friend_y,
                arcade.color.WHITE,
                5  # Line thickness
            )
            arcade.draw_line(
                player_x+8, player_y,
                player_x+8, friend_y,
                arcade.color.EARTH_YELLOW,
                3  # Line thickness
            )
    
    def on_draw(self):
        """Draw everything"""
        self.clear()
        
        if self.current_state == GameState.START_SCREEN:
            self.draw_start_screen()
        
        elif self.current_state == GameState.PLAYING:
            # Draw backgrounds first so they're behind the player, :(
            self.background_list.draw()

            # Draw enemies
            self.enemy_list.draw()
            
            # Draw bullets
            self.bullet_list.draw()
            
            # Draw explosions
            self.explosion_list.draw()
            
            # Draw powerup line BEFORE drawing player
            self.draw_powerup_line()
            
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

            # Draw powerup cooldown indicator
            arcade.draw_text(
                "E:",
                6,
                SCREEN_HEIGHT - 98,
                arcade.color.WHITE,
                font_size=20,
                bold=True
            )
            arcade.draw_lbwh_rectangle_filled(
            28, SCREEN_HEIGHT - 100,
            200, 20,
            arcade.color.BLACK
            )
                        
            arcade.draw_lbwh_rectangle_filled(
            32, SCREEN_HEIGHT - 96,
            192, 12,
            arcade.color.GREEN
            )
            #shrink black transparent cooldown
            cooldown_proportion = (self.power_cooldown)/self.power_cooldown_time
            arcade.draw_lbwh_rectangle_filled(
            32, SCREEN_HEIGHT - 96,
            192*cooldown_proportion, 12,
            (0,0,0,150)
            )
        
        #game over
        elif self.current_state == GameState.GAME_OVER:
            self.draw_game_over()
    
    def draw_health_bar(self):
        """Draw the health bar below the score"""
        # Load the appropriate health bar texture based on current health, only draw if there is heart remaining
        if self.health > 0:
            heart_bar_texture = arcade.load_texture(f"HEART_BAR_{self.health}.png")
            heart_bar_sprite = arcade.Sprite(heart_bar_texture, scale = 0.6)
            
            # Position it below the score (adjust these values as needed)
            heart_bar_sprite.left = 8
            heart_bar_sprite.bottom = SCREEN_HEIGHT - 70  # Right Below the score
            
            arcade.draw_sprite(heart_bar_sprite)
    
    def on_update(self, delta_time):
        """Update game"""
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
            
            # Update power cooldown
            if self.power_cooldown > 0:
                self.power_cooldown -= delta_time
            
            # Check if it's time to destroy all enemies during powerup
            if (self.player.is_powering and 
                self.player.powerup_elapsed >= POWERUP_ENEMY_DESTRUCTION_TIME and 
                not self.player.enemies_destroyed):
                # Destroy all enemies and award points
                for enemy in self.enemy_objects[:]:
                    # Create explosion at enemy position
                    self.create_explosion(
                        enemy.enemy_sprite.center_x,
                        enemy.enemy_sprite.center_y
                    )
                    #remove the enemy
                    enemy.enemy_sprite.remove_from_sprite_lists()
                    self.enemy_objects.remove(enemy)
                    self.score += 10  # Award points for each destroyed enemy
                self.player.enemies_destroyed = True  # Mark as destroyed
            
            # Update bullets
            self.bullet_list.update()
            # Update enemies
            for enemy in self.enemy_list:
                enemy.update(delta_time)
            
            # Update explosions
            for explosion in self.explosion_objects[:]:
                explosion.update(delta_time)
                if explosion.finished:
                    explosion.explosion_sprite.remove_from_sprite_lists()
                    self.explosion_objects.remove(explosion)
            
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
                    # Create explosion at enemy position
                    self.create_explosion(
                        enemy.enemy_sprite.center_x,
                        enemy.enemy_sprite.center_y
                    )
                    enemy.enemy_sprite.remove_from_sprite_lists()
                    self.health -= 1
                    self.enemy_objects.remove(enemy)
                    if self.health <= 0:
                        self.current_state = GameState.GAME_OVER
                        arcade.unschedule(self.spawn_enemy)
            # Check for bullet-enemy collisions
            for bullet in self.bullet_list:
                enemies_hit = arcade.check_for_collision_with_list(bullet, self.enemy_list)
    
                for enemy_sprite in enemies_hit:
                    # Remove the bullet
                    bullet.remove_from_sprite_lists()
        
                    # Remove the enemy
                    for enemy in self.enemy_objects[:]:  # Changed
                        if enemy.enemy_sprite == enemy_sprite:
                            # Create explosion at enemy position
                            self.create_explosion(
                                enemy.enemy_sprite.center_x,
                                enemy.enemy_sprite.center_y
                            )
                            enemy.enemy_sprite.remove_from_sprite_lists()
                            self.enemy_objects.remove(enemy)  # Changed
                            self.score += 10
                            break
                    break
            # Check for player-enemy collisions (only if not powering up)
            if not self.player.is_powering:
                for enemy in self.enemy_objects:  # Changed
                    if arcade.check_for_collision(self.player.player_sprite, enemy.enemy_sprite):
                        # Reduce health instead of immediately ending game
                        self.health -= 1
                        
                        # Create explosion at collision position
                        self.create_explosion(
                            enemy.enemy_sprite.center_x,
                            enemy.enemy_sprite.center_y
                        )
                        
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
        #playing :>
        elif self.current_state == GameState.PLAYING:
            #moves in direction
            if key == arcade.key.UP or key == arcade.key.W:
                if self.player.jump_state == JumpState.NOT_JUMPING:
                    self.player.change_y = PLAYER_MOVEMENT_SPEED
                    self.friend.change_y = PLAYER_MOVEMENT_SPEED
            elif key == arcade.key.DOWN or key == arcade.key.S:
                if self.player.jump_state == JumpState.NOT_JUMPING:
                    self.player.change_y = -PLAYER_MOVEMENT_SPEED
                    self.friend.change_y = -PLAYER_MOVEMENT_SPEED
            elif key == arcade.key.LEFT or key == arcade.key.A:
                self.player.change_x = -PLAYER_HORIZONTAL_SPEED
                self.friend.change_x = -PLAYER_HORIZONTAL_SPEED
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.player.change_x = PLAYER_HORIZONTAL_SPEED
                self.friend.change_x = PLAYER_HORIZONTAL_SPEED
            #shoot
            elif key == arcade.key.SPACE:
                # Only shoot if cooldown has expired and not powering up
                if self.bullet_cooldown <= 0 and not self.player.is_powering:
                    # Trigger attack animation and shoot bullet
                    self.player.start_attack()
                    self.shoot_bullet()
                    self.bullet_cooldown = self.bullet_cooldown_time
            #powerup
            elif key == arcade.key.E:
                if self.power_cooldown <= 0:
                    # Trigger power animation and sync friend's jump state
                    self.player.start_power()
                    self.friend.jump_state = JumpState.MOVING_TO_POSITION
                    self.friend.original_y = self.friend.player_sprite.center_y
                    self.power_cooldown = self.power_cooldown_time
        #start game when its not started
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
#Main function
def main():
    """Main function"""
    window = GameWindow()
    window.setup()
    arcade.run()
#run main
if __name__ == "__main__":
    main()