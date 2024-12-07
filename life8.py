# -*- mode:python;coding:utf-8 -*-
u'''
点字フォントを使って表示するライフゲーム。
'''
import collections
import curses
import time
from bitmap8 import BitMapDisplay

class Life(object):
    u'''ライフゲーム
    '''
    def __init__(self, bmd :BitMapDisplay) -> None:
        u'''初期状態では「生」状態セルはなし。
        '''
        self._bmd = bmd
        self._cells :set[tuple[int, int]] = set()
    def set(self, y :int, x :int) -> None:
        u'''「生」状態セルを置く。
        '''
        self._cells.add((y, x))
    def next_step(self) -> None:
        u'''次ステップでのセル状態を決定する。
        '''
        self._cells = {
            point
            for point, n in collections.Counter(
                    [self._clipping((y + dy, x + dx))
                     for (y, x) in self._cells
                     for dy in range(-1, 2)
                     for dx in range(-1, 2)
                     if dy != 0 or dx != 0]).items()
            if n == 3 or (n == 2 and point in self._cells)}
        self._bmd.clear()
        for (y, x) in self._cells:
            self._bmd.set(y, x, True)
    def _clipping(self, point : tuple[int, int]) -> tuple[int, int]:
        u'''境界条件処理（周期的境界条件を用いる）。'''
        (y, x) = point
        return (y % self._bmd.height, x % self._bmd.width)
def main() -> None:
    stdscr = curses.initscr()
    try:
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        stdscr.nodelay(True)
        bmd = BitMapDisplay(stdscr)
        life = Life(bmd)
        center_y, center_x = bmd.height // 2, bmd.width // 2
        life.set(center_y, center_x)
        life.set(center_y, center_x + 1)
        life.set(center_y - 2, center_x + 1)
        life.set(center_y - 1, center_x + 3)
        life.set(center_y, center_x + 4)
        life.set(center_y, center_x + 5)
        life.set(center_y, center_x + 6)
        running = True
        generation = 1
        while True:
            bmd.draw()
            stdscr.addstr(stdscr.getmaxyx()[0] - 1, 1,
                          'generation: {}'.format(generation))
            stdscr.refresh()
            if running:
                generation += 1
                life.next_step()
                time.sleep(0.1)
            else:
                time.sleep(1)
            if stdscr.getch() == ord(' '):
                running = not running
    finally:
        curses.endwin()
if __name__ == '__main__':
    main()
