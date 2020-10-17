import time
import curses
from curses import wrapper
from snake import Snake

# Используем системную кодировку
# Вместо кодировки использовать code
import locale
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

DELAY = .1

# Инициализируем экран
# screen = curses.initscr()

# Не выводить вводимые сиволы
# curses.noecho()

# Войти в cbreak режим
# выключает буффер строк и читает символы по одному
# curses.cbreak()

# Позволить curses обрабатывать спец. символы
# screen.keypad(True)
# Если запускать через wrapper, то он сам всё это сделает


def main(screen):
    # Позволить менять цвета
    curses.start_color()

    # Использовать цвета терминала
    curses.use_default_colors()

    # Отключить мигание курсора
    curses.curs_set(0)

    # Очистить экран
    screen.clear()

    # Ожидание клавиш не блокирует ввод
    screen.nodelay(True)

    screen.border(0)

    game_resolution = (curses.LINES - 2, curses.COLS - 2)
    game_window = curses.newwin(*game_resolution, 1, 1)
    game = Snake(game_resolution[0], (game_resolution[1] - 1) // 2)

    while not game.finish():
        game_window.clear()
        rows = game.get_board()
        for y, row in enumerate(rows):
            for x, el in enumerate(row):
                try:
                    if el == 0:
                        game_window.addstr(y, x*2, '  ')
                    elif el == 1:
                        game_window.addstr(y, x*2, '  ', curses.A_REVERSE)
                    elif el == 2:
                        game_window.addstr(y, x*2, '★ ')
                except Exception as e:
                    game_window.addstr(2, 2, str(e))
        screen.addstr(0, 2, f' Счёт: {str(game.score())} ')
        screen.addstr(curses.LINES - 1, 2, ' Пробел - Пауза ')

        direction = None
        quit = False
        start = time.time()

        while time.time() - start < DELAY:
            try:
                key = screen.getkey()
                if key == 'KEY_UP':
                    direction = 'up'
                elif key == 'KEY_DOWN':
                    direction = 'down'
                elif key == 'KEY_LEFT':
                    direction = 'left'
                elif key == 'KEY_RIGHT':
                    direction = 'right'
                elif key == ' ':
                    screen.nodelay(False)
                    screen.addstr(curses.LINES // 2 - 2, curses.COLS //
                                  2 - 5, 'Пауза', curses.A_REVERSE)
                    screen.addstr(curses.LINES // 2, curses.COLS //
                                  2 - 13, 'Нажмите любую клавишу', curses.A_REVERSE)
                    screen.refresh()
                    screen.getkey()
                    screen.nodelay(True)
                elif key == 'q':
                    raise KeyboardInterrupt
            except KeyboardInterrupt:
                quit = True
                break
            except:
                pass
        if quit: 
            break
        game_window.refresh()
        game.tick(direction)
    screen.addstr(curses.LINES // 2 - 2, curses.COLS //
                  2 - 5, 'GAME OVER!', curses.A_REVERSE)
    screen.addstr(curses.LINES // 2 , curses.COLS //
                  2 - 4, f'СЧЁТ: {game.score()}', curses.A_REVERSE)
    screen.addstr(curses.LINES // 2 + 2, curses.COLS //
                  2 - 8, f'Нажмите Enter...', curses.A_REVERSE)
    screen.refresh()
    screen.nodelay(False)
    screen.getkey()

wrapper(main)
