import numpy as np


class State:
    def __init__(self, coords, value, reward, dictNStates, dictAroundStates, isReward):
        self.coords = coords
        self.value = value
        self.reward = reward
        self.bestAction = ' '
        self.IsaReward = isReward
        self.dictNextStates = dictNStates
        self.nbNextStates = len(self.dictNextStates)
        self.dictAroundStates = dictAroundStates
        self.nbStatesAround = len(dictAroundStates)
        self.Probability = 1 - self.nbStatesAround / 16

    def __repr__(self) -> str:
        return f"coord: {self.coords}\nvalue: {self.value}\nreward: {self.reward}\ndictNStates: {self.dictNextStates}\ndictAroundStates: {self.dictAroundStates}\nnbStatesAround: {self.nbStatesAround}"

    def __str__(self) -> str:
        return f"({self.coords[0]}, {self.coords[1]})"

class Env:
    def __init__(self, nb_columns, nb_lines, weight, alea, p_tile_type, seed):
        self.nb_columns = nb_columns
        self.nb_lines = nb_lines
        self.g = np.zeros((nb_lines, nb_columns), dtype=int)
        self.weight = weight

        # self.zoom = zoom
        self.alea = alea
        self.global_cost = 0
        self.p_tile_type = p_tile_type
        self.seed = seed

        self.pos_x = 20
        self.pos_y = 20
        self.create_rnd_map()
        self.listAllStates = self.create_all_states()

    def create_rnd_map(self):
        np.random.seed(self.seed)

        for i in range(self.nb_lines):
            for j in range(self.nb_columns):
                z = np.random.uniform(0, 1)
                if z < self.p_tile_type['pwall']:
                    c = -1
                elif z < self.p_tile_type['pwall'] + self.p_tile_type['pwhite']:
                    c = 0
                elif z < self.p_tile_type['pwall'] + self.p_tile_type['pwhite'] + self.p_tile_type['pgreen']:
                    c = 1
                elif z < self.p_tile_type['pwall'] + self.p_tile_type['pwhite'] + self.p_tile_type['pgreen'] + self.p_tile_type['pblue']:
                    c = 2
                elif z < self.p_tile_type['pwall'] + self.p_tile_type['pwhite'] + self.p_tile_type['pgreen'] + self.p_tile_type['pblue'] + self.p_tile_type['pred']:
                    c = 3
                else:
                    c = 4
                self.g[i, j] = c
        self.g[0, 0] = 0
        self.g[0, 1] = 0
        self.g[2, 0] = 0
        self.g[self.nb_lines - 1, self.nb_columns - 1] = 0
        self.g[self.nb_lines - 2, self.nb_columns - 1] = 0
        self.g[self.nb_lines - 1, self.nb_columns - 2] = 0
        self.goal_x = np.random.randint(2, self.nb_lines - 1)
        self.goal_y = np.random.randint(2, self.nb_columns - 1)
        self.g[self.goal_x, self.goal_y] = 5

    def create_all_states(self):
        l = list()
        for i in range(self.nb_lines):
            for j in range(self.nb_columns):
                coord = (i, j)
                isaReward = False
                if self.g[i, j] < 0:
                    reward = " mur "
                else:
                    # reward = np.format_float_scientific(self.weight[env.g[i,j]],exp_digits=1)
                    reward = -self.weight[self.g[i, j]]
                    if type(reward) is int and reward > 0:
                        isaReward = True
                value = 0
                dictNStates = self.get_dictNextStates(i, j)
                dictAroundStates = self.get_around_States_Proba(i, j)

                s = State(
                    coord,
                    value,
                    reward,
                    dictNStates,
                    dictAroundStates,
                    isaReward
                )
                l.append(s)
        return l

    def get_dictNextStates(self, i, j):
        # check OutOfBound
        di = dict()
        if i - 2 >= 0 and j + 1 < self.nb_columns and self.g[i - 2, j + 1] != -1:
            di['y'] = (i - 2, j + 1)
        if i - 1 >= 0 and j + 2 < self.nb_columns and self.g[i - 1, j + 2] != -1:
            di['u'] = (i - 1, j + 2)
        if i + 1 < self.nb_lines and j + 2 < self.nb_columns and self.g[i + 1, j + 2] != -1:
            di['j'] = (i + 1, j + 2)
        if i + 2 < self.nb_lines and j + 1 < self.nb_columns and self.g[i + 2, j + 1] != -1:
            di['h'] = (i + 2, j + 1)
        if i + 2 < self.nb_lines and j - 1 >= 0 and self.g[i + 2, j - 1] != -1:
            di['g'] = (i + 2, j - 1)
        if i + 1 < self.nb_lines and j - 2 >= 0 and self.g[i + 1, j - 2] != -1:
            di['f'] = (i + 1, j - 2)
        if i - 1 >= 0 and j - 2 >= 0 and self.g[i - 1, j - 2] != -1:
            di['r'] = (i - 1, j - 2)
        if i - 2 >= 0 and j - 1 >= 0 and self.g[i - 2, j - 1] != -1:
            di['t'] = (i - 2, j - 1)
        return di

    def get_around_States_Proba(self, i, j):
        # check OutOfBound
        diStateAround = dict()
        if i + 1 < self.nb_lines and j < self.nb_columns and self.g[i + 1, j] != -1:
            diStateAround['md'] = (i + 1, j, 1 / 16)

        if i - 1 >= 0 and j < self.nb_columns and self.g[i - 1, j] != -1:
            diStateAround['mg'] = (i - 1, j, 1 / 16)

        if i + 1 < self.nb_lines and j + 1 < self.nb_columns and self.g[i + 1, j + 1] != -1:
            diStateAround['hd'] = (i + 1, j + 1, 1 / 16)

        if i - 1 >= 0 and j - 1 >= 0 and self.g[i - 1, j - 1] != -1:
            diStateAround['bg'] = (i - 1, j - 1, 1 / 16)

        if i + 1 < self.nb_lines and j - 1 >= 0 and self.g[i + 1, j - 1] != -1:
            diStateAround['bd'] = (i + 1, j - 1, 1 / 16)

        if i - 1 >= 0 and j + 1 < self.nb_columns and self.g[i - 1, j + 1] != -1:
            diStateAround['hg'] = (i - 1, j + 1, 1 / 16)

        if i < self.nb_lines and j + 1 < self.nb_columns and self.g[i, j + 1] != -1:
            diStateAround['hm'] = (i, j + 1, 1 / 16)

        if i < self.nb_lines and j - 1 >= 0 and self.g[i, j - 1] != -1:
            diStateAround['bm'] = (i, j - 1, 1 / 16)

        return diStateAround

    def get_state(self, i, j):
        i = int(i)
        j = int(j)
        if i >= 0 and i < self.nb_lines and j >= 0 and j < self.nb_columns:
            return self.listAllStates[i * self.nb_columns + j]
        return None

    def get_previous_states(self, s):
        l = list()
        for sp in self.listAllStates:
            if s.coords in sp.dictNextStates.values():
                l.append(sp)
        if self.alea == 1:
            neighbors = self.get_around_States_Proba(s.coords[0], s.coords[1])
            for neighbor in neighbors.values():
                for sp in self.listAllStates:
                    if (neighbor[0], neighbor[1]) in sp.dictNextStates.values():
                        l.append(sp)
        return l
    
    def T(self, s, a, sp):
        if s.dictNextStates[a] == sp.coords:
            if self.alea == 0:
                return 1
            else:
                return sp.Probability
        else:
            return 0

    def afficheV(self):
        print("Valeur de l'etat selon l'algo")
        for i in range(self.nb_lines):
            l = list()
            for j in range(self.nb_columns):
                value = "{:.2e}".format(self.get_state(i, j).value)
                l.append(value)
            print(l)

    def afficheBestAction(self):
        print("meilleure Action")
        for i in range(self.nb_lines):
            l = list()
            for j in range(self.nb_columns):
                l.append(self.get_state(i, j).bestAction)
            print(l)

    def afficheP(self):
        print("Proba d'arriver ce State")
        for i in range(self.nb_lines):
            l = list()
            for j in range(self.nb_columns):
                l.append(self.get_state(i, j).Probability)
            print(l)

    def afficheNBSA(self):
        print("NB State Around")
        for i in range(self.nb_lines):
            l = list()
            for j in range(self.nb_columns):
                l.append(self.get_state(i, j).nbStatesAround)
            print(l)

    def afficheR(self):
        print("Rewards")
        for i in range(self.nb_lines):
            l = list()
            for j in range(self.nb_columns):
                l.append(self.get_state(i, j).reward)
            print(l)

    def afficheNBNS(self):
        print("NB Next State ")
        for i in range(self.nb_lines):
            l = list()
            for j in range(self.nb_columns):
                l.append(
                    (self.get_state(i, j).nbNextStates, self.get_state(i, j).dictNextStates))
            print(l)
