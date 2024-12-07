import curses
import datetime
import math
import time
from bitmap8 import BitMapDisplay

def main() -> None:
    stdscr = curses.initscr()
    try:
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        stdscr.nodelay(True)
        bmd = BitMapDisplay(stdscr)
        scale = min([bmd.height // 2, bmd.width // 2])
        step = 10
        offset = 0.0
        running = True
        start_time = datetime.datetime.now()
        count = 1
        while True:
            if running:
                offset += 0.1
                bmd.clear()
                for t in range(scale * step):
                    t1 = t / step
                    r = t1
                    a = 2 * math.pi * (t1 / scale) * 3
                    (y, x) = (r * math.sin(a + offset),
                              r * math.cos(a + offset))
                    bmd.set(round(bmd.height / 2 + y),
                            round(bmd.width / 2 + x),
                            True)
                bmd.draw()
                current_time = datetime.datetime.now()
                draw_per_sec = count / (current_time - start_time).total_seconds()
                count += 1
                stdscr.addstr(
                    stdscr.getmaxyx()[0] - 1, 1,
                    'width = {}, height = {}, draw/sec = {}'.format(
                        stdscr.getmaxyx()[1],
                        stdscr.getmaxyx()[0],
                        draw_per_sec))
                stdscr.refresh()
                #time.sleep(0.1)  # 回転速度
            else:
                time.sleep(1)
                # reset
                start_time = datetime.datetime.now()
                count = 1
            if stdscr.getch() == ord(' '):
                running = not running
    finally:
        curses.endwin()
if __name__ == '__main__':
    main()
