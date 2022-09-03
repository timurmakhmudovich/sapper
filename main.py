import random


class Cell:
    def __init__(self, mine, around_mines=0, fl_open=False):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = fl_open
        self.done = False


class Field:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.pole = [[Cell(False) for _ in range(n)] for _ in range(n)]
        self.init()

    def init(self):
        c = self.m
        while c > 0:
            i = random.randint(0, self.n - 1)
            j = random.randint(0, self.n - 1)
            if self.pole[i][j].mine:
                continue
            else:
                self.pole[i][j].mine = True
                c -= 1

        for i in range(self.n):
            for j in range(self.n):
                around_mines = 0
                left = max(j - 1, 0)
                right = min(j + 1, self.n)
                top = max(i - 1, 0)
                bottom = min(i + 1, self.n)
                lst = [x[left:right + 1] for x in self.pole[top:bottom + 1]]

                for el in lst:
                    for x in el:
                        if x.mine:
                            around_mines += 1

                if self.pole[i][j].mine:
                    around_mines -= 1

                self.pole[i][j].around_mines = around_mines

    def show(self):
        res = ""
        for x in self.pole:
            for y in x:
                if y.fl_open:
                    res += f"{y.around_mines} "
                else:
                    res += "# "
            res += "\n"
        return res


class Play:
    def __init__(self, pole_game):
        self.pole_game = pole_game

    def coord_input(self, coord_name):
        while True:
            print(f"Put {coord_name} coord from 0 to {self.pole_game.n - 1}:", end=" ")
            try:
                coord = int(input())
                if 0 <= coord < self.pole_game.n:
                    break
                else:
                    print(f"Incorrect {coord_name} value")
            except ValueError:
                print(f"Incorrect {coord_name} value")
        return coord

    def clear(self, x, y):
        if self.pole_game.n > x >= 0 and self.pole_game.n > y >= 0 and self.pole_game.pole[x][y].around_mines != 0:
            self.pole_game.pole[x][y].fl_open = True
            self.pole_game.pole[x][y].done = True
            return

        if self.pole_game.n > x >= 0 and self.pole_game.n > y >= 0 and self.pole_game.pole[x][y].around_mines == 0 and \
                not self.pole_game.pole[x][y].mine and not self.pole_game.pole[x][y].done:
            for i in range(max(x - 1, 0), min(x + 2, self.pole_game.n)):
                for j in range(max(y - 1, 0), min(y + 2, self.pole_game.n)):
                    self.pole_game.pole[i][j].fl_open = True
                    self.pole_game.pole[x][y].done = True

            self.clear(x, y + 1)
            self.clear(x, y - 1)
            self.clear(x + 1, y)
            self.clear(x - 1, y)

    def start(self):
        while True:
            x = self.coord_input("X")
            y = self.coord_input("Y")

            if self.pole_game.pole[x][y].mine:
                print("\nSorry, you lost...\n")
                break

            self.clear(x, y)
            closed = [x.fl_open for line in self.pole_game.pole for x in line].count(False)

            if closed == self.pole_game.m:
                print("\nYOU WIN!!!\n")
                print(self.pole_game.show())
                break

            print(self.pole_game.show())


if __name__ == "__main__":
    N = 6
    M = 2
    pole_game = Field(N, M)
    p = Play(pole_game)
    p.start()
