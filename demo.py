import arcade as a
import Welcome as w

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Beep Boop Video Games"


"""a.open_window(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,True) #True makes it so that the game window is resizable

#Leave space here to add things to the window
a.set_background_color(a.color.ALICE_BLUE)


a.start_render()

#using screen dimensions to define objects keeps window responsive
a.draw_circle_outline(SCREEN_WIDTH/2,SCREEN_HEIGHT/2,100,a.color.ALLOY_ORANGE)

a.finish_render()"""
app = w.Welcome(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)

app.on_draw()

a.start_render()



a.finish_render()

a.run()