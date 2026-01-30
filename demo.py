"""
Platformer Game

python -m arcade.examples.platform_tutorial.01_open_window
"""
import arcade

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"


class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class to set up the window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.background_color = arcade.csscolor.GOLD
        self.player_texture = arcade.load_texture("Frendly_Drone.png")
        #self.player_sprite_sheet = arcade.load_spritesheet(":resources:images/---", 64, 64, 4)
        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = WINDOW_WIDTH / 2
        self.player_sprite.center_y = WINDOW_HEIGHT / 2
    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Render the screen."""

        # The clear method should always be called at the start of on_draw.
        # It clears the whole screen to whatever the background color is
        # set to. This ensures that you have a clean slate for drawing each
        # frame of the game.
        self.clear()
        arcade.draw_sprite(self.player_sprite)
        # Code to draw other things will go here


def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()