# script pion.py hjyf
from tkinter import *

import numpy as np

class Display:
    def __init__(self, zoom, env, v) -> None:
        self.window = Tk()
        self.window.title("MDP")
        self.zoom = zoom
        self.env = env
        self.v = v
        self.next_move = None

        # Creation d'un widget Canvas (pour la grille)
        self.width = self.zoom * 20 * self.env.nb_columns + 40
        self.height = self.zoom * 20 * self.env.nb_lines + 40

        # def des couleurs
        self.my_red = "#D20B18"
        self.my_green = "#25A531"
        self.my_blue = "#0B79F7"
        self.my_grey = "#E8E8EB"
        self.my_yellow = "#F9FB70"
        self.my_black = "#101010"
        self.my_walls = "#5E5E64"
        self.my_white = "#FFFFFF"
        self.color = [self.my_white, self.my_green, self.my_blue, self.my_red, self.my_black, self.my_grey]

        self.Canvas = Canvas(self.window, width=self.width, height=self.height, bg=self.my_white)
        
        self.w = Label(
            self.window,
            text='Cost = ' +
            str(self.env.global_cost),
            fg=self.my_black,
            font="Verdana 14 bold"
        )

        self.best_path = Label(
            self.window,
            text='Next best move: ' + str(self.next_move),
            fg=self.my_black,
            font="Verdana 14 bold"
        )


        self.Pawn = self.Canvas.create_oval(
            self.env.pos_x - 10,
            self.env.pos_y - 10,
            self.env.pos_x + 10,
            self.env.pos_y + 10,
            width=2,
            outline='black',
            fill=self.my_yellow
        )

    def draw_grid(self):
        for i in range(self.env.nb_lines + 1):
            ni = self.zoom * 20 * i + 20
            self.Canvas.create_line(20, ni, self.width - 20, ni)
        for j in range(self.env.nb_columns + 1):
            nj = self.zoom * 20 * j + 20
            self.Canvas.create_line(nj, 20, nj, self.height - 20)
        self.color_draw()

    def initialize(self):
        self.env.pos_x = 20 + 10 * self.zoom
        self.env.pos_y = 20 + 10 * self.zoom

        # cout et affichage
        self.Canvas.coords(
            self.Pawn, 
            self.env.pos_x - 9 * self.zoom,
            self.env.pos_y - 9 * self.zoom,
            self.env.pos_x + 9 * self.zoom,
            self.env.pos_y + 9 * self.zoom
        )
        cj = int((self.env.pos_x - 30) / (20 * self.zoom))
        li = int((self.env.pos_y - 30) / (20 * self.zoom))
        for move in self.v:
            if f"{li}, {cj}" in move.varName and move.x > 0:
                self.next_move = move.varName
        self.best_path.pack()
        self.best_path.config(text='Next best move: ' + str(self.next_move))
        self.w.pack()
        self.w.config(text='Cost = ' + str(self.env.global_cost))

        self.draw_grid()

    # specification des proportion de murs, case _whitehes et pts de couleur
    def color_draw(self):
        for i in range(self.env.nb_lines):
            for j in range(self.env.nb_columns):
                y = self.zoom * 20 * i + 20
                x = self.zoom * 20 * j + 20
                if self.env.g[i, j] > 0:
                    self.Canvas.create_oval(
                        x + self.zoom * (10 - 3),
                        y + self.zoom * (10 - 3),
                        x + self.zoom * (10 + 3),
                        y + self.zoom * (10 + 3),
                        width=1,
                        outline=self.color[self.env.g[i, j]],
                        fill=self.color[self.env.g[i, j]]
                    )
                else:
                    if self.env.g[i, j] < 0:
                        self.Canvas.create_rectangle(x, y, x + self.zoom * 20, y + self.zoom * 20, fill=self.my_black)
                        self.Canvas.create_rectangle(x, y, x + self.zoom * 20, y + self.zoom * 20, fill=self.my_black)

    def move(self, direction):
        changed = 0
        cost = np.zeros(6,dtype=np.int)

        cj = int((self.env.pos_x - 30) / (20 * self.zoom))
        li = int((self.env.pos_y - 30) / (20 * self.zoom))

        if direction == 'space':
            t = np.random.randint(6)
            lettre = ['f', 'g', 'h', 'j', 'y', 'u']
            direction = lettre[t]

        # deplacement (-2,1)
        if direction == 'y' and li > 1 and cj < self.env.nb_columns - 1 and self.env.g[li - 2, cj + 1] > -1:
            self.env.pos_y -= self.zoom * 20 * 2
            self.env.pos_x += self.zoom * 20
            cost[self.env.g[li - 2, cj + 1]] += 1
            changed = 1

        # deplacement (-2,-1)
        if direction == 't' and li > 1 and cj > 0 and self.env.g[li - 2, cj - 1] > -1:
            self.env.pos_y -= self.zoom * 20 * 2
            self.env.pos_x -= self.zoom * 20
            cost[self.env.g[li - 2, cj - 1]] += 1
            changed = 1

        # deplacement (-1,2)
        if direction == 'u' and li > 0 and cj < self.env.nb_columns - 2 and self.env.g[li - 1, cj + 2] > -1:
            self.env.pos_y -= self.zoom * 20
            self.env.pos_x += self.zoom * 20 * 2
            cost[self.env.g[li - 1, cj + 2]] += 1
            changed = 1

        # deplacement (-1,-2)
        if direction == 'r' and li > 0 and cj > 1 and self.env.g[li - 1, cj - 2] > -1:
            self.env.pos_y -= self.zoom * 20
            self.env.pos_x -= self.zoom * 20 * 2
            cost[self.env.g[li - 1, cj - 2]] += 1
            changed = 1

        # deplacement (2,1)
        if direction == 'h' and li < self.env.nb_lines - 2 and cj < self.env.nb_columns - 1 and self.env.g[li + 2, cj + 1] > -1:
            self.env.pos_y += self.zoom * 20 * 2
            self.env.pos_x += self.zoom * 20
            cost[self.env.g[li + 2, cj + 1]] += 1
            changed = 1

        # deplacement (2,-1)
        if direction == 'g' and li < self.env.nb_lines - 2 and cj > 0 and self.env.g[li + 2, cj - 1] > -1:
            self.env.pos_y += self.zoom * 20 * 2
            self.env.pos_x -= self.zoom * 20
            cost[self.env.g[li + 2, cj - 1]] += 1
            changed = 1

        # deplacement (1,2)
        if direction == 'j' and li < self.env.nb_lines - 1 and cj < self.env.nb_columns - 2 and self.env.g[li + 1, cj + 2] > -1:
            self.env.pos_y += self.zoom * 20
            self.env.pos_x += self.zoom * 20 * 2
            cost[self.env.g[li + 1, cj + 2]] += 1
            changed = 1

        # deplacement (1,-2)
        if direction == 'f' and li < self.env.nb_lines - 1 and cj > 1 and self.env.g[li + 1, cj - 2] > -1:
            self.env.pos_y += self.zoom * 20
            self.env.pos_x -= self.zoom * 20 * 2
            cost[self.env.g[li + 1, cj - 2]] += 1
            changed = 1
        
        self.window.update()

        if changed > 0:
            cj = int((self.env.pos_x - 30) / (20 * self.zoom))
            li = int((self.env.pos_y - 30) / (20 * self.zoom))
            for move in self.v:
                if f"({li}, {cj})" in move.varName and move.x > 0:
                    self.next_move = move.varName
            self.best_path.config(text='Next best move: ' + str(self.next_move))

        return changed, cost


    def keyboard(self, event):
        key = event.keysym

        changed, cost = self.move(key)
    

    # La variable alea =1 si on veut des effets aleatoires sinon les transitions sont deterministes
        # On ajoute un effet aleatoire dans les transitions
        if self.env.alea == 1 and changed == 1:
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
                NewPosY = self.env.pos_y + self.zoom * 20 * dli
                NewPosX = self.env.pos_x + self.zoom * 20 * dcj
                newcj = int((NewPosX - 30) / (20 * self.zoom))
                newli = int((NewPosY - 30) / (20 * self.zoom))
                print('d', dli, dcj)
                if newli >= 0 and newcj >= 0 and newli <= self.env.nb_lines - \
                        1 and newcj <= self.env.nb_columns - 1 and self.env.g[newli, newcj] > -1:
                    self.env.pos_y = NewPosY
                    self.env.pos_x = NewPosX

    # on dessine le pion a sa nouvelle position
        self.Canvas.coords(
            self.Pawn,
            self.env.pos_x - 9 * self.zoom,
            self.env.pos_y - 9 * self.zoom,
            self.env.pos_x + 9 * self.zoom,
            self.env.pos_y + 9 * self.zoom
        )
        for k in range(5):
            self.env.global_cost += cost[k] * self.env.weight[k]
        self.w.config(text='Cost = ' + str(self.env.global_cost))
    
    def run(self):
        self.draw_grid()
        self.Canvas.focus_set()
        self.Canvas.bind('<Key>', self.keyboard)
        self.Canvas.pack(padx=5, pady=5)

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
