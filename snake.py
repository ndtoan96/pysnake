"""
A small snake game forked from https://gist.github.com/sanchitgangwar/2158089 with some more spices

Contributor: Nguyen Duc Toan
Email: ntoan96@gmail.com

Shortkey:
    - Press Esc to quit
    - Press c for constant speed (50ms)
    - Press a for auto play
"""

import curses
from curses import wrapper
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint


def main(win):
    height = 20
    width = 60
    win = curses.newwin(height, width, 0, 0)
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    win.border(0)
    win.nodelay(1)

    key = KEY_RIGHT
    score = 0

    snake = [[4, 10], [4, 9], [4, 8]]
    food = [10, 20]
    constant_speed = False

    death_flag = None

    for node in snake:
        win.addch(node[0], node[1], '#')
    win.addch(food[0], food[1], '*')
    auto = False 

    def autoPlay():
        nonlocal death_flag
        bestkey = prevKey

        # avoid death flag
        if death_flag=='horizontal':
            bestkey = KEY_RIGHT if (snake[0][0], snake[0][1]+1) not in snake[1:]+[[snake[0][0],1], [snake[0][0],width-2]] else KEY_LEFT
            death_flag = None
        if death_flag=='vertical':
            bestkey = KEY_UP if (snake[0][0]-1, snake[0][1]) not in snake[1:]+[[1,snake[0][1]], [height-2, snake[0][1]]] else KEY_DOWN
            death_flag = None

        # move away from food
        if key==KEY_LEFT and snake[0][0]==food[0] and snake[0][1]<food[1]:
            bestkey = KEY_DOWN if snake[0][0] < height/2 else KEY_UP
        if key==KEY_RIGHT and snake[0][0]==food[0] and snake[0][1]>food[1]:
            bestkey = KEY_DOWN if snake[0][0] < height/2 else KEY_UP
        if key==KEY_UP and snake[0][0]<food[0] and snake[0][1]==food[1]:
            bestkey = KEY_LEFT if snake[0][1] < width/2 else KEY_RIGHT
        if key==KEY_DOWN and snake[0][0]>food[0] and snake[0][1]==food[1]:
            bestkey = KEY_LEFT if snake[0][1] < width/2 else KEY_RIGHT

        # encounter borders
        if key==KEY_LEFT and snake[0][1]==1:
            bestkey = KEY_DOWN if snake[0][0] < food[0] else KEY_UP
            for i, node in enumerate(snake[1:]):
                if node[1]==1 and abs(node[0]-snake[0][0])<=len(snake)-i-1:
                    bestkey = KEY_UP if node[0] > snake[0][0] else KEY_DOWN
                    if bestkey==KEY_UP and snake[0][0]==1:
                        bestkey = KEY_DOWN
                        death_flag = 'horizontal'
                    if bestkey==KEY_DOWN and snake[0][0]==height-2:
                        bestkey = KEY_UP
                        death_flag = 'horizontal'
                    break
        if key==KEY_RIGHT and snake[0][1]==width-2:
            bestkey = KEY_DOWN if snake[0][0] < food[0] else KEY_UP
            for i, node in enumerate(snake[1:]):
                if node[1]==width-2 and abs(node[0]-snake[0][0])<=len(snake)-i-1:
                    bestkey = KEY_UP if node[0] > snake[0][0] else KEY_DOWN
                    if bestkey==KEY_UP and snake[0][0]==1:
                        bestkey = KEY_DOWN
                        death_flag = 'horizontal'
                    if bestkey==KEY_DOWN and snake[0][0]==height-2:
                        bestkey = KEY_UP
                        death_flag = 'horizontal'
                    break
        if key==KEY_UP and snake[0][0]==1:
            bestkey = KEY_LEFT if snake[0][1] > food[1] else KEY_RIGHT
            for i, node in enumerate(snake[1:]):
                if node[0]==1 and abs(node[1]-snake[0][1])<=len(snake)-i-1:
                    bestkey = KEY_RIGHT if node[1] < snake[0][1] else KEY_LEFT
                    if bestkey==KEY_RIGHT and snake[0][1]==width-2:
                        bestkey = KEY_LEFT
                        death_flag = 'vertical'
                    if bestkey==KEY_LEFT and snake[0][1]==1:
                        bestkey = KEY_RIGHT
                        death_flag = 'vertical'
                    break
        if key==KEY_DOWN and snake[0][0]==height-2:
            bestkey = KEY_LEFT if snake[0][1] > food[1] else KEY_RIGHT
            for i, node in enumerate(snake[1:]):
                if node[0]==height-2 and abs(node[1]-snake[0][1])<=len(snake)-i-1:
                    bestkey = KEY_RIGHT if node[1] < snake[0][1] else KEY_LEFT
                    if bestkey==KEY_RIGHT and snake[0][1]==width-2:
                        bestkey = KEY_LEFT
                        death_flag = 'vertical'
                    if bestkey==KEY_LEFT and snake[0][1]==1:
                        bestkey = KEY_RIGHT
                        death_flag = 'vertical'
                    break

        # find food
        if key in (KEY_UP, KEY_DOWN) and snake[0][0]==food[0]:
            bestkey = KEY_RIGHT if snake[0][1] < food[1] else KEY_LEFT
            for i, node in enumerate(snake[1:]):
                if node[0]==snake[0][0] and abs(node[1]-snake[0][1]) <= len(snake)-i-1:
                    bestkey = key
                    break

        if key in (KEY_LEFT, KEY_RIGHT) and snake[0][1]==food[1]:
            bestkey = KEY_DOWN if snake[0][0] < food[0] else KEY_UP
            for i, node in enumerate(snake[1:]):
                if node[1]==snake[0][1] and abs(node[0]-snake[0][0]) <= len(snake)-i-1:
                    bestkey = key
                    break

        # avoid self-colliding
        if key==KEY_DOWN and [snake[0][0]+1, snake[0][1]] in snake[1:]:
            for node in snake[1:]:
                if node[0]==snake[0][0]:
                    break
            bestkey = KEY_LEFT if node[1] > snake[0][1] else KEY_RIGHT
        if key==KEY_UP and [snake[0][0]-1, snake[0][1]] in snake[1:]:
            for node in snake[1:]:
                if node[0]==snake[0][0]:
                    break
            bestkey = KEY_LEFT if node[1] > snake[0][1] else KEY_RIGHT
        if key==KEY_LEFT and [snake[0][0], snake[0][1]-1] in snake[1:]:
            for node in snake[1:]:
                if node[1]==snake[0][1]:
                    break
            bestkey = KEY_UP if node[0] > snake[0][0] else KEY_DOWN
        if key==KEY_RIGHT and [snake[0][0], snake[0][1]+1] in snake[1:]:
            for node in snake[1:]:
                if node[1]==snake[0][1]:
                    break
            bestkey = KEY_UP if node[0] > snake[0][0] else KEY_DOWN

        return bestkey

    while True:
        win.addstr(0, 2, f'Length: {len(snake)} ')
        win.addstr(0, width//2-3, ' SNAKE ')
        win.addstr(height-1, width//3-4, f'Auto: {"on " if auto else "off"}')
        if constant_speed:
            timeout = 50
        else:
            timeout = 300 - len(snake) * 5
            if timeout < 50: timeout = 50
        win.addstr(height-1, width//3*2-7, f'Speed: {timeout:3} ms')
        win.timeout(timeout)

        prevKey = key
        event = win.getch()
        if event == 27:
            break
        if prevKey == KEY_DOWN: oposite_key = KEY_UP
        if prevKey == KEY_UP: oposite_key = KEY_DOWN
        if prevKey == KEY_LEFT: oposite_key = KEY_RIGHT
        if prevKey == KEY_RIGHT: oposite_key = KEY_LEFT
        key = key if (event == -1 or event == oposite_key) else event

        # pause
        if key == ord(' '):
            key = -1
            while key != ord(' '):
                key = win.getch()
            key = prevKey
            continue

        # auto play
        if key == ord('a'):
            auto = not auto
            key = prevKey
            continue

        # constant_speed
        if key == ord('c'):
            constant_speed = not constant_speed
            key = prevKey
            continue

        # invalid key
        if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27, ord('a')]:
            key = prevKey

        if auto:
            key = autoPlay()

        snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_RIGHT and 1) + (key == KEY_LEFT and -1)])

        # encouter border
        if snake[0][0] in [0, height-1] or snake[0][1] in [0, width-1]: break

        # encouter food
        if snake[0] == food:
            win.addch(food[0], food[1], '#')
            food = []
            #score += 1
            while food == []:
                food = [randint(1, height-2), randint(1, width-2)]
                if food in snake: food = []
            win.addch(food[0], food[1], '*')
        else:
            last = snake.pop()
            win.addch(last[0], last[1], ' ')
            win.addch(snake[0][0], snake[0][1], '#')

        # self-colliding
        if snake[0] in snake[1:]:
            break

    curses.endwin()
    print(f"\nLength - {len(snake)}")

wrapper(main)
