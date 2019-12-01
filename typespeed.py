from random import choice, randrange
import sys

import pyglet
from pyglet import gl
from pyglet.window import key

# Game controls
pressed_keys = set()

def on_key_press(symbol, modifiers):
    if symbol == key.BACKSPACE:
        pressed_keys.add(('back',0))
    if symbol == key.SPACE:
        pressed_keys.add(('space',0))
    if symbol == key.ENTER:
        pressed_keys.add(('enter',0))


# List of words selection
def select_List_of_words(arg):
    '''
    Selects a file based on input from the terminal.
    Default = eng

    Basic options are:
      eng = English words from words_eng.txt
      cz = Czech words from words_cz.txt
      py = Python words from words_py.txt
    '''
    set_words = 'eng'
    if len(arg) > 1:
        set_words = arg[1]
    return open_List_of_words(set_words)


def open_List_of_words(set_words):
    '''
    Opens file with words and returns this words as list.
    '''
    WORDS = []
    with open('words_{}.txt'.format(set_words), mode='r', encoding='utf-8') as file:
        for row in file:
            WORDS.append(row.strip())
    return WORDS


class Game():
    def __init__(self):
        '''
        Set game settings.
        '''
        self.window_x = 1000
        self.window_y = 400
        self.words_ingame = {}
        self.last_word_ingame_coor_y = 0
        self.guess = ''
        self.score = 0
        self.lost = 0
        self.state = 1
        self.speed = 1
        self.add_word_speed = -1

    def add_word(self, t):
        '''
        Add new word as object into game.
        '''
        if self.add_word_speed < 0:
            self.add_word_speed = 6
            while self.state:
                new_word = WordInGame()
                if new_word.name not in self.words_ingame and new_word.y != self.last_word_ingame_coor_y:
                    self.words_ingame[new_word.name] = new_word
                    self.last_word_ingame_coor_y = new_word.y
                    break
        else:
            self.add_word_speed -= self.speed


class WordInGame():
    def __init__(self):
        self.name = choice(WORDS)
        self.x = 0
        self.y = randrange(60, game.window_y-20) // 10 * 10
        self.color = choice(list(colors.values()))
        self.size = 20


def move(t):
    words_for_deleting = []
    if game.state == 1:
        if game.words_ingame:
            for word, value in game.words_ingame.items():
                if value.x > game.window_x:
                    words_for_deleting.append(word)
                    game.lost += 1
                value.x += 1*game.speed
        if ('back', 0) in pressed_keys:
            game.guess = game.guess[:-1]
            pressed_keys.discard(('back',0))
        if words_for_deleting:
            for item in words_for_deleting:
                del game.words_ingame[item]
        if game.guess and game.guess in game.words_ingame:
            del game.words_ingame[game.guess]
            game.guess = ''
            game.score += 1
        if ('space', 0) in pressed_keys:
            game.guess = ''
            pressed_keys.discard(('space', 0))
        game.speed = min(max(game.score / 10,1),8)
        if ('enter', 0) in pressed_keys:
            game.state = 0
            pressed_keys.discard(('enter', 0))
    if game.state == 0:
        if ('enter', 0) in pressed_keys:
            game.state = 1
            pressed_keys.discard(('enter', 0))


def on_draw():
    window.clear()
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glColor3f(1, 1, 1)
    gl.glLineWidth(4)
    x1, x2 = 0, game.window_x
    y1, y2 = 50, game.window_y
    draw_polygon((x1,y1), (x1,y2), (x2,y2), (x2,y1))
    x1, x2 = 0, game.window_x
    y1, y2 = 0, 50
    draw_polygon((x1,y1), (x1,y2), (x2,y2), (x2,y1))
    draw_guess_word()
    draw_score()
    draw_lost()
    if game.state:
        for item in game.words_ingame.values():
            draw_word(item)
    else:
        x1, x2 = game.window_x//2-100, game.window_x//2+100
        y1, y2 = game.window_y//2-20, game.window_y//2+100
        draw_polygon((x1,y1), (x1,y2), (x2,y2), (x2,y1))
        draw_pause()


def draw_pause():
    draw_text('PAUSE ',
                  x = game.window_x//2-95,
                  y = game.window_y//2+20,
                  size = 40,
                  anchor_x = 'left',
                  color = colors['white']
                  )


def draw_score():
    draw_text('SCORE: ' + str(game.score),
                  x = game.window_x - 150,
                  y = 15,
                  size = 20,
                  anchor_x = 'left',
                  color = colors['white']
                  )


def draw_lost():
    draw_text('LOST: ' + str(game.lost),
                  x = game.window_x - 300,
                  y = 15,
                  size = 20,
                  anchor_x = 'left',
                  color = colors['white']
                  )


def draw_guess_word():
    draw_text('>>>  ' + game.guess,
                  x = 10,
                  y = 15,
                  size = 20,
                  anchor_x = 'left',
                  color = colors['white']
                  )


def draw_word(item):
    draw_text(item.name,
                  x = item.x,
                  y = item.y,
                  size = item.size,
                  anchor_x = 'right',
                  color = item.color
                  )


def draw_text(text, x, y, size, anchor_x, color):
    '''
    Draw text in playfield.
    '''
    text = pyglet.text.Label(
        text,
        font_name='Arial',
        font_size=size,
        x=x, y=y, anchor_x=anchor_x,
        color=color
        )
    text.draw()


def on_text(text):
    game.guess += text


def draw_polygon(xy1, xy2, xy3, xy4):
    '''
    Draw polygon.

    '''
    gl.glBegin(gl.GL_LINE_LOOP);
    gl.glVertex2f(int(xy1[0]), int(xy1[1]));
    gl.glVertex2f(int(xy2[0]), int(xy2[1]));
    gl.glVertex2f(int(xy3[0]), int(xy3[1]));
    gl.glVertex2f(int(xy4[0]), int(xy4[1]));
    gl.glEnd();


colors = {'white': (255,255,255,255),
          'red': (255,0,0,255),
          'green': (0,255,0,255),
          'blue': (0,0,255,255),
          'yellow': (255,255,0,255),
          'magenta': (255,0,255,255),
          'cyan': (0,255,255,255)
          }


WORDS = select_List_of_words(sys.argv)
game = Game()


window = pyglet.window.Window(game.window_x, game.window_y)


window.push_handlers(
    on_draw=on_draw,
    on_text=on_text,
    on_key_press=on_key_press,
    # on_mouse_press=on_mouse_press,
)

pyglet.clock.schedule_interval(move, 1/40)
pyglet.clock.schedule_interval(game.add_word, 1/3)

pyglet.app.run()
