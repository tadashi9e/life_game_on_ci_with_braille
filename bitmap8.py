# -*- mode:python;coding:utf-8 -*-
# bitmap8.py

import curses

class BitMapDisplay(object):
    u'''漢点字フォント（8ドット）を使ったビットマップ表示。
    '''
    P = ('⠀⠁⠈⠉⠂⠃⠊⠋⠐⠑⠘⠙⠒⠓⠚⠛' +
         '⠄⠅⠌⠍⠆⠇⠎⠏⠔⠕⠜⠝⠖⠗⠞⠟' +
         '⠠⠡⠨⠩⠢⠣⠪⠫⠰⠱⠸⠹⠲⠳⠺⠻' +
         '⠤⠥⠬⠭⠦⠧⠮⠯⠴⠵⠼⠽⠶⠷⠾⠿' +
         '⡀⡁⡈⡉⡂⡃⡊⡋⡐⡑⡘⡙⡒⡓⡚⡛' +
         '⡄⡅⡌⡍⡆⡇⡎⡏⡔⡕⡜⡝⡖⡗⡞⡟' +
         '⡠⡡⡨⡩⡢⡣⡪⡫⡰⡱⡸⡹⡲⡳⡺⡻' +
         '⡤⡥⡬⡭⡦⡧⡮⡯⡴⡵⡼⡽⡶⡷⡾⡿' +
         '⢀⢁⢈⢉⢂⢃⢊⢋⢐⢑⢘⢙⢒⢓⢚⢛' +
         '⢄⢅⢌⢍⢆⢇⢎⢏⢔⢕⢜⢝⢖⢗⢞⢟' +
         '⢠⢡⢨⢩⢢⢣⢪⢫⢰⢱⢸⢹⢲⢳⢺⢻' +
         '⢤⢥⢬⢭⢦⢧⢮⢯⢴⢵⢼⢽⢶⢷⢾⢿' +
         '⣀⣁⣈⣉⣂⣃⣊⣋⣐⣑⣘⣙⣒⣓⣚⣛' +
         '⣄⣅⣌⣍⣆⣇⣎⣏⣔⣕⣜⣝⣖⣗⣞⣟' +
         '⣠⣡⣨⣩⣢⣣⣪⣫⣰⣱⣸⣹⣲⣳⣺⣻' +
         '⣤⣥⣬⣭⣦⣧⣮⣯⣴⣵⣼⣽⣶⣷⣾⣿')
    def __init__(self, scr :'curses._CursesWindow') -> None:
        h, w = scr.getmaxyx()
        self.height, self.width = 4 * (h - 1), 2 * (w - 1)
        self._scr = scr
        self._bmap = [[False for x in range(self.width)]
                      for y in range(self.height)]
        self._lines = ['' for y in range(self.height)]
        scr.clear()
    def clear(self) -> None:
        u'''ビットマップをクリアする。
        '''
        self._bmap = [[False for x in range(self.width)]
                      for y in range(self.height)]
    def set(self, y :int, x :int, b :bool) -> None:
        u'''ビットマップ上に値を設定する。
        y, x -- 画面上の位置（ドット単位）
        '''
        self._bmap[y % self.height][x % self.width] = b
    def get(self, y :int, x :int) -> bool:
        u'''ビットマップ上から値を取得する。
        y, x -- 画面上の位置（ドット単位）
        '''
        return self._bmap[y % self.height][x % self.width]
    def get_character(self, cy :int, cx :int) -> str:
        u'''画面上に表示するキャラクタを取得する。
        cy, cx -- 画面上の位置（キャラクタ単位）。
        '''
        i = sum([(1 << (2 * dy + dx) if self._bmap[4 * cy + dy][2 * cx + dx] else 0)
                 for dy in range(4) for dx in range(2)])
        return BitMapDisplay.P[i]
    def draw(self) -> None:
        u'''画面に描画する。
        '''
        for cy in range(0, self.height // 4):
            # 行の表示内容を取得（末尾の空白部分は削除）
            line = ''.join([self.get_character(cy, cx)
                            for cx in range(self.width // 2)]).rstrip('⠀')
            if self._lines[cy] == line:
                continue  # 書き換え不要
            self._scr.addstr(cy, 0, line)
            self._scr.clrtoeol()  # 行末まで削除
            self._lines[cy] = line
