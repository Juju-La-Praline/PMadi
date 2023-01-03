class State:
    def __init__(self, coords, Value, reward, dictNStates, dictAroundStates, isReward):
        self.coords = coords
        self.value = Value
        self.reward = reward
        self.bestAction = ' '
        self.IsaReward = isReward
        self.dictNextStates = dictNStates
        self.nbNextStates = len(self.dictNextStates)
        self.dictAroundStates = dictAroundStates
        self.nbStatesAround = len(dictAroundStates)
        self.Probability = 1 - self.nbStatesAround/16 


    def __repr__(self) -> str:
        return f"coord: {self.coords}\nvalue: {self.value}\nreward: {self.reward}\ndictNStates: {self.dictNextStates}\ndictAroundStates: {self.dictAroundStates}\nnbStatesAround: {self.nbStatesAround}"


class Env:
    def __init__(self, nbcolonnes, nblignes, g, weight):
        self.nbcolonnes = nbcolonnes
        self.nblignes = nblignes
        self.g = g
        self.weight = weight
        self.listAllStates = self.create_all_states()

    def create_all_states(self):
        l = list()
        for i in range(self.nblignes):
            for j in range(self.nbcolonnes):
                coord = (i, j)
                isaReward = False
                if self.g[i, j] < 0:
                    reward = ' mur '
                else:
                    # reward = np.format_float_scientific(self.weight[g[i,j]],exp_digits=1)
                    reward = -self.weight[self.g[i, j]]
                    if reward > 0:
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
                    isaReward,
                )
                l.append(s)
        return l

    def get_dictNextStates(self, i, j):
        # check OutOfBound
        di = dict()
        if i - 2 >= 0 and j + 1 < self.nbcolonnes and self.g[i - 2, j + 1] != -1:
            di['y'] = (i - 2, j + 1)
        if i - 1 >= 0 and j + 2 < self.nbcolonnes and self.g[i - 1, j + 2] != -1:
            di['u'] = (i - 1, j + 2)
        if i + 1 < self.nblignes and j + 2 < self.nbcolonnes and self.g[i + 1, j + 2] != -1:
            di['j'] = (i + 1, j + 2)
        if i + 2 < self.nblignes and j + 1 < self.nbcolonnes and self.g[i + 2, j + 1] != -1:
            di['h'] = (i + 2, j + 1)
        if i + 2 < self.nblignes and j - 1 >= 0 and self.g[i + 2, j - 1] != -1:
            di['g'] = (i + 2, j - 1)
        if i + 1 < self.nblignes and j - 2 >= 0 and self.g[i + 1, j - 2] != -1:
            di['f'] = (i + 1, j - 2)
        if i - 1 >= 0 and j - 2 >= 0 and self.g[i - 1, j - 2] != -1:
            di['r'] = (i - 1, j - 2)
        if i - 2 >= 0 and j - 1 >= 0 and self.g[i - 2, j - 1] != -1:
            di['t'] = (i - 2, j - 1)

        return di

    def get_around_States_Proba(self, i, j):
        # check OutOfBound
        diStateAround = dict()
        if i + 1 < self.nblignes and j < self.nbcolonnes and self.g[i
                + 1, j] != -1:
            diStateAround['md'] = (i + 1, j, 1 / 16)

        if i - 1 >= 0 and j < self.nbcolonnes and self.g[i - 1, j] != -1:
            diStateAround['mg'] = (i - 1, j, 1 / 16)

        if i + 1 < self.nblignes and j + 1 < self.nbcolonnes and self.g[i + 1, j + 1] != -1:
            diStateAround['hd'] = (i + 1, j + 1, 1 / 16)

        if i - 1 >= 0 and j - 1 >= 0 and self.g[i - 1, j - 1] != -1:
            diStateAround['bg'] = (i - 1, j - 1, 1 / 16)

        if i + 1 < self.nblignes and j - 1 >= 0 and self.g[i + 1, j
                - 1] != -1:
            diStateAround['bd'] = (i + 1, j - 1, 1 / 16)

        if i - 1 >= 0 and j + 1 < self.nbcolonnes and self.g[i - 1, j
                + 1] != -1:
            diStateAround['hg'] = (i - 1, j + 1, 1 / 16)

        if i < self.nblignes and j + 1 < self.nbcolonnes and self.g[i,
                j + 1] != -1:
            diStateAround['hm'] = (i, j + 1, 1 / 16)

        if i < self.nblignes and j - 1 >= 0 and self.g[i, j - 1] != -1:
            diStateAround['bm'] = (i, j - 1, 1 / 16)

        return diStateAround

    def get_state(self, i, j):
        i = int(i)
        j = int(j)
        if i >= 0 and i < self.nblignes and j >= 0 and j < self.nbcolonnes:
            return self.listAllStates[i * self.nbcolonnes + j]
        return None

    def afficheV(self):
        print("Valeur de l'etat selon l'algo")
        for i in range(self.nblignes):
            l = list()
            for j in range(self.nbcolonnes):
                value = '{:.2e}'.format(self.get_state(i, j).value)
                l.append(value)
            print(l)

    def afficheBestAction(self):
        print('meilleure Action')
        for i in range(self.nblignes):
            l = list()
            for j in range(self.nbcolonnes):
                l.append(self.get_state(i, j).bestAction)
            print(l)

    def afficheP(self):
        print("Proba d'arriver ce State")
        for i in range(self.nblignes):
            l = list()
            for j in range(self.nbcolonnes):
                l.append(self.get_state(i, j).Probability)
            print(l)

    def afficheNBSA(self):
        print('NB State Around')
        for i in range(self.nblignes):
            l = list()
            for j in range(self.nbcolonnes):
                l.append(self.get_state(i, j).nbStatesAround)
            print(l)

    def afficheR(self):
        print('Rewards')
        for i in range(self.nblignes):
            l = list()
            for j in range(self.nbcolonnes):
                l.append(self.get_state(i, j).reward)
            print(l)

    def afficheNBNS(self):
        print('NB Next State ')
        for i in range(self.nblignes):
            l = list()
            for j in range(self.nbcolonnes):
                l.append((self.get_state(i, j).nbNextStates,
                         self.get_state(i, j).dictNextStates))
            print(l)
    
    def get_rewards(self):
        rewards = []
        for i in range(self.nblignes):
            temp = []
            for j in range(self.nbcolonnes):
                temp.append(self.get_state(i, j).reward)
            rewards.append(temp)
        return rewards