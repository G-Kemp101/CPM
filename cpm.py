class wip:

    def __init__(self, name, duration, dependencies):
        self.name = name
        self.duration = duration
        self.dependencies = dependencies
        self.forward = False
        self.backward = False

    def early_sf(self):
        if not self.dependencies:
            self.ES = 0
        else:
            prev_ef = max(self.dependencies, key=lambda ef: ef.EF)
            self.ES = prev_ef.EF

        self.EF = self.ES + self.duration
        self.forward = True
        
    def late_sf(self):
        if not self.dependents:
            self.LF = self.EF
        else:
            prev_ls = min(self.dependents, key=lambda ls: ls.LS)
            self.LF = prev_ls.LS

        self.LS = self.LF - self.duration
        self.TF = self.LS - self.ES
        self.backward = True
    
    def __str__(self):
        activity = "{:<4}{:<5}{:<5}{:<5}\n{:<4}{:<5}{:<5}{:<5}\n{}".format(self.name,
                        self.ES,
                        self.duration,
                        self.EF,
                        " ",
                        self.LS,
                        self.TF,
                        self.LF,
                        "="*20)
        return activity


def main():

    S = wip("S", 0, [])
    A = wip("A", 30, [S])
    B = wip("B", 45, [S])
    C = wip("C", 60, [A])
    D = wip("D", 30, [A])
    E = wip("E", 90, [C,D])
    F = wip("F", 20, [E])
    G = wip("G", 30, [E])
    H = wip("H", 20, [F])
    I = wip("I", 20, [G,H])
    J = wip("J", 5, [I])
    K = wip("K", 15, [J])
    Fin = wip("Fin", 0, [K,B])

    S.dependents = [A,B]
    A.dependents = [C,D]
    B.dependents = [Fin]
    C.dependents = [E]
    D.dependents = [E]
    E.dependents = [G,F]
    F.dependents = [H]
    G.dependents = [I]
    H.dependents = [I]
    I.dependents = [J]
    J.dependents = [K]
    K.dependents = [Fin]
    Fin.dependents = []

    forward_pass(S)
    backward_pass(Fin)
    for c in [A,B,C,D,E,F,G,H,I,J,K]:
        print(c)
    
    CPM = critical_path(S, [])
    print([activity.name for activity in CPM])


def forward_pass(S):
    queue = [S]
    S.early_sf()

    while queue:
        v = queue.pop(0)
        for c in v.dependents:
            if not c.forward and all(b.forward for b in c.dependencies):
                c.early_sf()
                queue.append(c)

def backward_pass(S):
    queue = [S]
    S.late_sf()
    
    while queue:
        v = queue.pop(0)
        for c in v.dependencies:
            if not c.backward and all(b.backward for b in c.dependents):
                c.late_sf()
                queue.append(c)
            

def critical_path(S, CPM):

    for c in S.dependents:
        if c.TF == 0:
            CPM.append(c)
            critical_path(c, CPM)
    
    return CPM



if __name__ == "__main__":
    main()  
