class DeathDetector:
    def __init__(self):
        self.baseline = None
        self.dead = False
        self.t_death = None
        self.history = []
        self.reported = False   

    def update(self, t, S):
        self.history.append((t, S))

        if self.baseline is None:
            self.baseline = S
            return

        if (not self.dead) and S < 0.8 * self.baseline:
            self.dead = True
            self.t_death = t



class HumanPrediction:
    def __init__(self):
        self.t_predict = None

    def predict(self, t):
        if self.t_predict is None:
            self.t_predict = t
