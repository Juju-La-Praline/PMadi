# script pion.py hjyf
from tkinter import *

import numpy as np

class Display:
    def __init__(self, zoom, alea, nb_lines, nb_columns, global_cost) -> None:
        self.window = Tk()
        self.window.title("MDP")
        self.zoom = zoom
        self.alea = alea  # transitions aleatoires si alea =1 sinon mettre alea=0

        # taille de la grille
        self.nb_lines = nb_lines
        self.nb_columns = nb_columns

        self.cost = np.zeros(5, dtype=int)
        self.weight = np.zeros(5, dtype=int)
        self.global_cost = global_cost

        self.pos_x = 20 + 10 * self.zoom
        self.pos_y = 20 + 10 * self.zoom

        # Creation d'un widget Canvas (pour la grille)
        self.width = self.zoom * 20 * self.nb_columns + 40
        self.height = self.zoom * 20 * self.nb_lines + 40
        self.g = np.zeros((self.nb_lines, self.nb_columns), dtype=int)

        self.cj = int((self.pos_x - 30) / (20 * self.zoom))
        self.li = int((self.pos_y - 30) / (20 * self.zoom))

        # def des couleurs
        self.my_red = "#D20B18"
        self.my_green = "#25A531"
        self.my_blue = "#0B79F7"
        self.my_grey = "#E8E8EB"
        self.my_yellow = "#F9FB70"
        self.my_black = "#101010"
        self.my_walls = "#5E5E64"
        self.my_white = "#FFFFFF"
        self.color = [self.my_white, self.my_green, self.my_blue, self.my_red, self.my_black]

        self.Canvas = Canvas(self.window, width=self.width, height=self.height, bg=self.my_white)
        
        self.w = Label(
            self.window,
            text='Cost = ' +
            str(self.global_cost),
            fg=self.my_black,
            font="Verdana 14 bold"
        )

        self.Pawn = self.Canvas.create_oval(
            self.pos_x - 10,
            self.pos_y - 10,
            self.pos_x + 10,
            self.pos_y + 10,
            width=2,
            outline='black',
            fill=self.my_yellow
        )

    def initialize(self):
        self.pos_x = 20 + 10 * self.zoom
        self.pos_y = 20 + 10 * self.zoom
        for k in range(5):
            self.cost[k] = 0

        # cout et affichage
        self.Canvas.coords(
            self.Pawn, 
            self.pos_x - 9 * self.zoom,
            self.pos_y - 9 * self.zoom,
            self.pos_x + 9 * self.zoom,
            self.pos_y + 9 * self.zoom
        )
        self.w.pack()
        self.w.config(text='Cost = ' + str(self.global_cost))

        self.weight[0] = 1
        self.weight[1] = 10
        self.weight[2] = 20
        self.weight[3] = 30
        self.weight[4] = 40

    # specification des proportion de murs, case _whitehes et pts de couleur
    def color_draw(self, g):
        p_wall = 0.15
        p_white = 0.45
        p_green = 0.0
        p_blue = 0.2
        p_red = 0.2
        # pnoire=0.1 mais pas besoin de le specifier c'est la couleur restante
        for i in range(self.nb_lines):
            for j in range(self.nb_columns):
                z = np.random.uniform(0, 1)
                if z < p_wall:
                    c = -1
                elif z < p_wall + p_white:
                    c = 0
                elif z < p_wall + p_white + p_green:
                    c = 1
                elif z < p_wall + p_white + p_green + p_blue:
                    c = 2
                elif z < p_wall + p_white + p_green + p_blue + p_red:
                    c = 3
                else:
                    c = 4

                g[i, j] = c
        g[0, 0] = 0
        g[0, 1] = 0
        g[2, 0] = 0
        g[self.nb_lines - 1, self.nb_columns - 1] = 0
        g[self.nb_lines - 2, self.nb_columns - 1] = 0
        g[self.nb_lines - 1, self.nb_columns - 2] = 0
        for i in range(self.nb_lines):
            for j in range(self.nb_columns):
                y = self.zoom * 20 * i + 20
                x = self.zoom * 20 * j + 20
                if g[i, j] > 0:
                    self.Canvas.create_oval(
                        x + self.zoom * (10 - 3),
                        y + self.zoom * (10 - 3),
                        x + self.zoom * (10 + 3),
                        y + self.zoom * (10 + 3),
                        width=1,
                        outline=self.color[g[i, j]],
                        fill=self.color[g[i, j]]
                    )
                else:
                    if g[i, j] < 0:
                        self.Canvas.create_rectangle(x, y, x + self.zoom * 20, y + self.zoom * 20, fill=self.my_black)
                        self.Canvas.create_rectangle(x, y, x + self.zoom * 20, y + self.zoom * 20, fill=self.my_black)

    def move(self, direction):
        changed = 0

        if direction == 'space':
            t = np.random.randint(6)
            lettre = ['f', 'g', 'h', 'j', 'y', 'u']
            direction = lettre[t]

        # deplacement (-2,1)
        if direction == 'y' and self.li > 1 and self.cj < self.nb_columns - 1 and self.g[self.li - 2, self.cj + 1] > -1:
            self.pos_y -= self.zoom * 20 * 2
            self.pos_x += self.zoom * 20
            self.cost[self.g[self.li - 2, self.cj + 1]] += 1
            changed = 1

        # deplacement (-2,-1)
        if direction == 't' and self.li > 1 and self.cj > 0 and self.g[self.li - 2, self.cj - 1] > -1:
            self.pos_y -= self.zoom * 20 * 2
            self.pos_x -= self.zoom * 20
            self.cost[self.g[self.li - 2, self.cj - 1]] += 1
            changed = 1

        # deplacement (-1,2)
        if direction == 'u' and self.li > 0 and self.cj < self.nb_columns - 2 and self.g[self.li - 1, self.cj + 2] > -1:
            self.pos_y -= self.zoom * 20
            self.pos_x += self.zoom * 20 * 2
            self.cost[self.g[self.li - 1, self.cj + 2]] += 1
            changed = 1

        # deplacement (-1,-2)
        if direction == 'r' and self.li > 0 and self.cj > 1 and self.g[self.li - 1, self.cj - 2] > -1:
            self.pos_y -= self.zoom * 20
            self.pos_x -= self.zoom * 20 * 2
            self.cost[self.g[self.li - 1, self.cj - 2]] += 1
            changed = 1

        # deplacement (2,1)
        if direction == 'h' and self.li < self.nb_lines - 2 and self.cj < self.nb_columns - 1 and self.g[self.li + 2, self.cj + 1] > -1:
            self.pos_y += self.zoom * 20 * 2
            self.pos_x += self.zoom * 20
            self.cost[self.g[self.li + 2, self.cj + 1]] += 1
            changed = 1

        # deplacement (2,-1)
        if direction == 'g' and self.li < self.nb_lines - 2 and self.cj > 0 and self.g[self.li + 2, self.cj - 1] > -1:
            self.pos_y += self.zoom * 20 * 2
            self.pos_x -= self.zoom * 20
            self.cost[self.g[self.li + 2, self.cj - 1]] += 1
            changed = 1

        # deplacement (1,2)
        if direction == 'j' and self.li < self.nb_lines - 1 and self.cj < self.nb_columns - 2 and self.g[self.li + 1, self.cj + 2] > -1:
            self.pos_y += self.zoom * 20
            self.pos_x += self.zoom * 20 * 2
            self.cost[self.g[self.li + 1, self.cj + 2]] += 1
            changed = 1

        # deplacement (1,-2)
        if direction == 'f' and self.li < self.nb_lines - 1 and self.cj > 1 and self.g[self.li + 1, self.cj - 2] > -1:
            self.pos_y += self.zoom * 20
            self.pos_x -= self.zoom * 20 * 2
            self.cost[self.g[self.li + 1, self.cj - 2]] += 1
            changed = 1
        
        self.window.update()

        # return changed


    def keyboard(self, event):
        key = event.keysym
        changed = 0

        changed = self.move(key)
    

    # La variable alea =1 si on veut des effets aleatoires sinon les transitions sont deterministes
        # On ajoute un effet aleatoire dans les transitions
        if self.alea == 1 and changed == 1:
            t = np.random.uniform(0, 1)
            if t > 0.5:
                d = np.random.randint(8)
                dli = 0
                if d == 0 or d == 1 or d == 2:
                    dli = -1
                if d == 4 or d == 5 or d == 6:
                    dli == 1
                dcj = 0
                if d == 0 or d == 7 or d == 6:
                    dcj = -1
                if d == 2 or d == 3 or d == 4:
                    dcj = 1
            # l'effet aleatoire est applique s'il cree un deplacement sur une
            # case admissible
                NewPosY = self.pos_y + self.zoom * 20 * dli
                NewPosX = self.pos_x + self.zoom * 20 * dcj
                newcj = int((NewPosX - 30) / (20 * self.zoom))
                newli = int((NewPosY - 30) / (20 * self.zoom))
                print('d', dli, dcj)
                if newli >= 0 and newcj >= 0 and newli <= self.nb_lines - \
                        1 and newcj <= self.nb_columns - 1 and self.g[newli, newcj] > -1:
                    self.pos_y = NewPosY
                    self.pos_x = NewPosX

    # on dessine le pion a sa nouvelle position
        self.Canvas.coords(
            self.Pawn,
            self.pos_x - 9 * self.zoom,
            self.pos_y - 9 * self.zoom,
            self.pos_x + 9 * self.zoom,
            self.pos_y + 9 * self.zoom
        )
        global_cost = 0
        for k in range(5):
            global_cost += self.cost[k] * self.weight[k]
        self.w.config(text='Cost = ' + str(global_cost))

    def draw_grid(self):
        for i in range(self.nb_lines + 1):
            ni = self.zoom * 20 * i + 20
            self.Canvas.create_line(20, ni, self.width - 20, ni)
        for j in range(self.nb_columns + 1):
            nj = self.zoom * 20 * j + 20
            self.Canvas.create_line(nj, 20, nj, self.height - 20)
        self.color_draw(self.g)
    
    def run(self):
        self.draw_grid()
        self.Canvas.focus_set()
        self.Canvas.bind('<Key>', self.keyboard)
        self.Canvas.pack(padx=5, pady=5)

        pos_x = 20 + 10 * self.zoom
        pos_y = 20 + 10 * self.zoom

        # Creation d'un widget Button (bouton Quitter)
        Button(
            self.window,
            text='Restart',
            command=self.initialize).pack(
                side=LEFT,
                padx=5,
            pady=5)
        Button(
            self.window,
            text='Quit',
            command=self.window.destroy).pack(
                side=LEFT,
                padx=5,
            pady=5)

        self.window.mainloop()

if __name__ == '__main__':
    display = Display(2, 0, 10, 20, 0)
    display.initialize()
    display.run()
