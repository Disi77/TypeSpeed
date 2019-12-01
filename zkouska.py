import pyglet

def draw_text(text, x, y, size, anchor_x):
    '''
    Draw text in playfield.
    '''
    print(colors['yellow'])
    a = colors['cyan']
    text = pyglet.text.Label(
        text,
        font_name='Arial',
        font_size=size,
        x=x, y=y, anchor_x=anchor_x,
        color=colors['yellow']
        )
    text.draw()

def draw_lost():
    draw_text('LOST: ' + '10',
                  x = 100,
                  y = 100,
                  size = 20,
                  anchor_x = 'left',
                  #color = colors['white']
                  )

def on_draw():
    window.clear()
    draw_lost()

colors = {'black': (0,0,0,255),
          'white': (255,255,255,255),
          'red': (255,0,0,255),
          'green': (0,255,0,255),
          'blue': (0,0,255,255),
          'yellow': (255,255,0,255),
          'magenta': (255,0,255,255),
          'cyan': (0,255,255,255)
          }


window = pyglet.window.Window()
#pyglet.gl.glClearColor(0.5,0,0,1)

window.push_handlers(
    on_draw=on_draw,
)

pyglet.app.run()
