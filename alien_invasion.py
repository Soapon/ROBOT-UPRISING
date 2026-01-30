import arcade
import random
from enum import Enum

# Constants
SCREEN_WIDTH = 2400
SCREEN_HEIGHT = 1300
SCREEN_TITLE = "Alien Invasion"
FPS = 60

# Player constants
PLAYER_X = 2200
PLAYER_SPEED = 7
FIRE_COOLDOWN = 0.25  # seconds

# Projectile constants
PROJECTILE_SPEED = 15

# Alien constants
ALIEN_SPAWN_X = -100

# Game States
class GameState(Enum):
    START_SCREEN = 1
    PLAYING = 2
    GAME_OVER = 3

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        
        # Load sprite
        try:
            self.texture = arcade.load_texture("Cyborg.png")
        except:
            # Create a simple colored sprite if image not found
            self.texture = arcade.make_soft_square_texture(64, arcade.color.BLUE, 255, 255)
        
        self.center_x = PLAYER_X
        self.center_y = SCREEN_HEIGHT // 2
        self.speed = PLAYER_SPEED
        self.last_shot_time = 0
        
    def update(self):
        # Movement is handled by keyboard state in main game
        
        # Keep player on screen
        if self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT
        if self.bottom < 0:
            self.bottom = 0
            
    def can_shoot(self, current_time):
        return current_time - self.last_shot_time >= FIRE_COOLDOWN
        
    def shoot(self, current_time):
        if self.can_shoot(current_time):
            self.last_shot_time = current_time
            return Projectile(self.center_x - 30, self.center_y)
        return None

class Projectile(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Create a yellow projectile
        self.texture = arcade.make_soft_square_texture(20, arcade.color.YELLOW, 255, 255)
        
        self.center_x = x
        self.center_y = y
        self.change_x = -PROJECTILE_SPEED
        
    def update(self):
        self.center_x += self.change_x
        
        # Remove if off screen
        if self.right < 0:
            self.remove_from_sprite_lists()

class Alien(arcade.Sprite):
    def __init__(self, alien_type, y_pos):
        super().__init__()
        
        self.alien_type = alien_type
        
        # Load drone sprites based on type
        drone_images = {
            1: "Enemy_Drones_1.png",
            2: "Enemy_Drones_2.png",
            3: "Enemy_Drones_3.png",
            4: "Enemy_Drones_4.png",
            5: "Enemy_Drones_5.png"
        }
        
        # Select image based on type (with wrapping for more than 5 types)
        image_key = ((alien_type - 1) % 5) + 1
        
        try:
            self.texture = arcade.load_texture(drone_images[image_key])
        except:
            # Fallback colored sprites
            if alien_type == 1:
                self.texture = arcade.make_soft_circle_texture(48, arcade.color.GREEN, 255, 255)
            elif alien_type == 2:
                self.texture = arcade.make_soft_circle_texture(64, arcade.color.RED, 255, 255)
            else:
                self.texture = arcade.make_soft_circle_texture(96, arcade.color.PURPLE, 255, 255)
        
        # Type 1: Scout
        if alien_type == 1:
            self.speed = 3
            self.hp = 1
            self.max_hp = 1
            self.points = 10
            
        # Type 2: Fighter
        elif alien_type == 2:
            self.speed = 4
            self.hp = 2
            self.max_hp = 2
            self.points = 25
            self.wobble_offset = random.randint(0, 100)
            self.frame_count = 0
            
        # Type 3: Bomber
        else:
            self.speed = 2
            self.hp = 4
            self.max_hp = 4
            self.points = 50
            
        self.center_x = ALIEN_SPAWN_X
        self.center_y = y_pos
        
    def update(self):
        # Move right
        self.center_x += self.speed
        
        # Type 2 wobbles
        if self.alien_type == 2:
            self.frame_count += 1
            wobble = 3 * arcade.math.cos(arcade.math.radians(self.frame_count * 4 + self.wobble_offset))
            self.center_y += wobble
            
        # Keep on screen vertically
        if self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT
        if self.bottom < 0:
            self.bottom = 0
            
    def take_damage(self):
        self.hp -= 1
        return self.hp <= 0

class Explosion(arcade.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        
        self.center_x = x
        self.center_y = y
        self.size = size
        self.frame = 0
        self.max_frames = 12
        
        # Start with yellow explosion
        self.texture = arcade.make_soft_circle_texture(size, arcade.color.YELLOW, 255, 255)
        
    def update(self):
        self.frame += 1
        
        if self.frame >= self.max_frames:
            self.remove_from_sprite_lists()
            return
            
        # Animate explosion
        progress = self.frame / self.max_frames
        radius = int(self.size * progress * 0.5)
        
        if progress < 0.5:
            color = arcade.color.YELLOW
        else:
            color = arcade.color.RED
            
        self.texture = arcade.make_soft_circle_texture(radius * 2, color, 255, 255)

class AlienInvasionGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        # Set background color
        arcade.set_background_color(arcade.color.BLACK)
        
        # Load background
        try:
            self.background = arcade.load_texture("Background.png")
            self.use_background = True
            self.bg_x = 0
        except:
            self.use_background = False
            print("Background.png not found, using black background")
        
        # Sprite lists
        self.player_list = None
        self.projectile_list = None
        self.alien_list = None
        self.explosion_list = None
        
        # Game state
        self.state = GameState.START_SCREEN
        self.player = None
        self.score = 0
        self.wave = 1
        self.aliens_spawned = 0
        self.aliens_per_wave = 10
        self.last_spawn_time = 0
        self.spawn_delay = 2.0  # seconds
        self.wave_complete = False
        self.wave_transition_time = 0
        self.total_shots = 0
        self.total_hits = 0
        
    def setup(self):
        """Set up the game"""
        # Create sprite lists
        self.player_list = arcade.SpriteList()
        self.projectile_list = arcade.SpriteList()
        self.alien_list = arcade.SpriteList()
        self.explosion_list = arcade.SpriteList()
        
        # Create player
        self.player = Player()
        self.player_list.append(self.player)
        
        # Reset game variables
        self.score = 0
        self.wave = 1
        self.aliens_spawned = 0
        self.aliens_per_wave = 10
        self.last_spawn_time = 0
        self.spawn_delay = 2.0
        self.wave_complete = False
        self.wave_transition_time = 0
        self.total_shots = 0
        self.total_hits = 0
        self.bg_x = 0
        
    def spawn_alien(self, current_time):
        """Spawn a new alien"""
        if current_time - self.last_spawn_time > self.spawn_delay and self.aliens_spawned < self.aliens_per_wave:
            self.last_spawn_time = current_time
            
            # Determine alien type based on wave
            if self.wave == 1:
                alien_type = 1
            elif self.wave == 2:
                alien_type = 1 if random.random() < 0.75 else 2
            else:
                rand = random.random()
                if rand < 0.5:
                    alien_type = 1
                elif rand < 0.85:
                    alien_type = 2
                else:
                    alien_type = 3
                    
            y_pos = random.randint(100, SCREEN_HEIGHT - 100)
            alien = Alien(alien_type, y_pos)
            self.alien_list.append(alien)
            self.aliens_spawned += 1
            
    def check_wave_complete(self):
        """Check if current wave is complete"""
        if self.aliens_spawned >= self.aliens_per_wave and len(self.alien_list) == 0:
            if not self.wave_complete:
                self.wave_complete = True
                self.wave_transition_time = self.total_time
                # Wave completion bonus
                self.score += self.wave * 100
                
    def next_wave(self):
        """Start the next wave"""
        if self.total_time - self.wave_transition_time > 3.0:  # 3 second transition
            self.wave += 1
            self.aliens_spawned = 0
            self.aliens_per_wave = int(10 * (1.2 ** (self.wave - 1)))
            self.spawn_delay = max(0.5, 2.0 - (self.wave * 0.1))
            self.wave_complete = False
            
    def on_draw(self):
        """Render the screen"""
        self.clear()
        
        # Draw background
        if self.use_background:
            # Draw scrolling background
            arcade.draw_lbwh_rectangle_filled(
                self.bg_x, 0,
                self.background.width, SCREEN_HEIGHT,
                self.background
            )
            # Draw second copy for seamless scrolling
            arcade.draw_lbwh_rectangle_filled(
                self.bg_x + self.background.width, 0,
                self.background.width, SCREEN_HEIGHT,
                self.background
            )
        
        if self.state == GameState.START_SCREEN:
            # Draw title
            arcade.draw_text(
                "ALIEN INVASION",
                SCREEN_WIDTH / 2, 300,
                arcade.color.CYAN, 120,
                anchor_x="center", font_name="Arial", bold=True
            )
            
            # Draw instructions
            arcade.draw_text(
                "Press SPACE to Start",
                SCREEN_WIDTH / 2, 600,
                arcade.color.MAGENTA, 72,
                anchor_x="center", font_name="Arial"
            )
            
            arcade.draw_text(
                "W/UP - Move Up | S/DOWN - Move Down",
                SCREEN_WIDTH / 2, 800,
                arcade.color.WHITE, 48,
                anchor_x="center", font_name="Arial"
            )
            
            arcade.draw_text(
                "SPACE - Fire",
                SCREEN_WIDTH / 2, 870,
                arcade.color.WHITE, 48,
                anchor_x="center", font_name="Arial"
            )
            
        elif self.state == GameState.PLAYING:
            # Draw all sprites
            self.alien_list.draw()
            self.projectile_list.draw()
            self.player_list.draw()
            self.explosion_list.draw()
            
            # Draw HUD
            arcade.draw_text(
                f"Score: {self.score}",
                50, SCREEN_HEIGHT - 50,
                arcade.color.CYAN, 48,
                anchor_y="top", font_name="Arial"
            )
            
            arcade.draw_text(
                f"Wave: {self.wave}",
                SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50,
                arcade.color.MAGENTA, 48,
                anchor_x="right", anchor_y="top", font_name="Arial"
            )
            
            # Wave transition message
            if self.wave_complete:
                arcade.draw_text(
                    f"WAVE {self.wave} COMPLETE!",
                    SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                    arcade.color.YELLOW, 120,
                    anchor_x="center", anchor_y="center", font_name="Arial", bold=True
                )
                
                arcade.draw_text(
                    f"Wave {self.wave + 1} Incoming...",
                    SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 120,
                    arcade.color.WHITE, 72,
                    anchor_x="center", anchor_y="center", font_name="Arial"
                )
                
        elif self.state == GameState.GAME_OVER:
            arcade.draw_text(
                "GAME OVER",
                SCREEN_WIDTH / 2, 400,
                arcade.color.RED, 120,
                anchor_x="center", font_name="Arial", bold=True
            )
            
            arcade.draw_text(
                f"Final Score: {self.score}",
                SCREEN_WIDTH / 2, 600,
                arcade.color.CYAN, 72,
                anchor_x="center", font_name="Arial"
            )
            
            arcade.draw_text(
                f"Waves Completed: {self.wave - 1}",
                SCREEN_WIDTH / 2, 700,
                arcade.color.MAGENTA, 72,
                anchor_x="center", font_name="Arial"
            )
            
            accuracy = (self.total_hits / self.total_shots * 100) if self.total_shots > 0 else 0
            arcade.draw_text(
                f"Accuracy: {accuracy:.1f}%",
                SCREEN_WIDTH / 2, 800,
                arcade.color.YELLOW, 48,
                anchor_x="center", font_name="Arial"
            )
            
            arcade.draw_text(
                "Press SPACE to Continue",
                SCREEN_WIDTH / 2, 950,
                arcade.color.WHITE, 72,
                anchor_x="center", font_name="Arial"
            )
            
    def on_update(self, delta_time):
        """Update game logic"""
        
        # Track total time
        if not hasattr(self, 'total_time'):
            self.total_time = 0
        self.total_time += delta_time
        
        if self.state == GameState.START_SCREEN:
            # Scroll background slowly
            if self.use_background:
                self.bg_x -= 0.5
                if self.bg_x <= -self.background.width:
                    self.bg_x = 0
                    
        elif self.state == GameState.PLAYING:
            # Scroll background
            if self.use_background:
                self.bg_x -= 1
                if self.bg_x <= -self.background.width:
                    self.bg_x = 0
            
            # Update player
            self.player_list.update()
            
            # Spawn aliens
            if not self.wave_complete:
                self.spawn_alien(self.total_time)
            
            # Update all sprites
            self.projectile_list.update()
            self.alien_list.update()
            self.explosion_list.update()
            
            # Check projectile-alien collisions
            for projectile in self.projectile_list:
                hit_aliens = arcade.check_for_collision_with_list(projectile, self.alien_list)
                if hit_aliens:
                    projectile.remove_from_sprite_lists()
                    self.total_hits += 1
                    for alien in hit_aliens:
                        if alien.take_damage():
                            self.score += alien.points
                            explosion = Explosion(alien.center_x, alien.center_y, alien.width)
                            self.explosion_list.append(explosion)
                            alien.remove_from_sprite_lists()
                            
            # Check alien-player collisions
            hit_player = arcade.check_for_collision_with_list(self.player, self.alien_list)
            if hit_player:
                self.state = GameState.GAME_OVER
                
            # Check if aliens reached player's x position
            for alien in self.alien_list:
                if alien.center_x >= PLAYER_X:
                    self.state = GameState.GAME_OVER
                    
            # Check wave completion
            self.check_wave_complete()
            if self.wave_complete:
                self.next_wave()
                
    def on_key_press(self, key, modifiers):
        """Handle key presses"""
        if self.state == GameState.START_SCREEN:
            if key == arcade.key.SPACE:
                self.state = GameState.PLAYING
                self.setup()
                
        elif self.state == GameState.GAME_OVER:
            if key == arcade.key.SPACE:
                self.state = GameState.START_SCREEN
                
        elif self.state == GameState.PLAYING:
            # Movement keys
            if key == arcade.key.W or key == arcade.key.UP:
                self.player.change_y = PLAYER_SPEED
            elif key == arcade.key.S or key == arcade.key.DOWN:
                self.player.change_y = -PLAYER_SPEED
                
            # Shooting
            if key == arcade.key.SPACE:
                projectile = self.player.shoot(self.total_time)
                if projectile:
                    self.projectile_list.append(projectile)
                    self.total_shots += 1
                    
    def on_key_release(self, key, modifiers):
        """Handle key releases"""
        if self.state == GameState.PLAYING:
            if key == arcade.key.W or key == arcade.key.UP:
                if self.player.change_y > 0:
                    self.player.change_y = 0
            elif key == arcade.key.S or key == arcade.key.DOWN:
                if self.player.change_y < 0:
                    self.player.change_y = 0

def main():
    """Main function"""
    game = AlienInvasionGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()