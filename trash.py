################################################### GAME FIELD TRASH ###################################################
"""
class Block:
    def __init__(self, master):
        self.e = Entry(master, width=20)
        self.b = Button(master, text="Convert")
        self.l = Label(master, bg='black', fg='white', width=20)
        self.e.pack()
        self.b.pack()
        self.l.pack()

    def setFunc(self, func):
        self.b['command'] = eval('self.' + func)

    def strToSortList(self):
        s = self.e.get()
        s = s.split()
        s.sort()
        self.l['text'] = ' '.join(s)

    def strReverse(self):
        s = self.e.get()
        s = s.split()
        s.reverse()
        self.l['text'] = ' '.join(s)

root = Tk()
first_block = Block(root)
first_block.setFunc('strToSortList')
second_block = Block(root)
second_block.setFunc('strReverse')
root.mainloop()
"""

"""
# keyboard press handle
def movement_handler(event):
    global RIGHT_PAD_SPEED
    if event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":
        RIGHT_PAD_SPEED = PAD_SPEED

def movement_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == "w":
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "s":
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":
        RIGHT_PAD_SPEED = PAD_SPEED
"""

"""
# reaction on button release
def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in ("w", "s"):
        LEFT_PAD_SPEED = 0
    elif event.keysym in ("Up", "Down"):
        RIGHT_PAD_SPEED = 0


# bind keyboard control
c.bind("<KeyPress>", movement_handler)
c.bind("<KeyRelease>", stop_pad)
"""



#################################################### MAMDANI TRASH #####################################################
"""
mamdani_x = Variable("X",
                     {"LeftFar": (-600,-599,-250,-200), "Left": (-300,-200,-50,0), "Center": (-50,0,50), "Right": (0,50,200,300), "RightFar":(200,250,599,600)},
                     (-600, 600))
mamdani_y = Variable("Y",
                     {"Close": (0,1,100,150), "Far": (100,160,599,600)},
                     (0, 600))
mamdani_out = Variable("Out",
                       {"LeftSprint": (-30,-29,-20), "LeftFast": (-30,-20,-15), "LeftNormal": (-20,-15,-10), "LeftSlow": (-15,-10,0),
                        "StopFar": (-10,-5,5,10), "StopClose": (-10,-5,5,10),
                        "RightSlow": (0,10,15), "RightNormal": (10,15,20), "RightFast": (15,20,30), "RightSprint": (20,29,30)},
                       (-30, 30))

mamdani_rules = Rule()
mamdani_rules.add_rule(("LeftFar", "and", "Close"), "LeftSprint")
mamdani_rules.add_rule(("LeftFar", "and", "Far"), "LeftFast")
mamdani_rules.add_rule(("Left", "and", "Close"), "LeftNormal")
mamdani_rules.add_rule(("Left", "and", "Far"), "LeftSlow")
mamdani_rules.add_rule(("Center", "and", "Far"), "StopFar")
mamdani_rules.add_rule(("Center", "and", "Close"), "StopClose")
mamdani_rules.add_rule(("Right", "and", "Far"), "RightSlow")
mamdani_rules.add_rule(("Right", "and", "Close"), "RightNormal")
mamdani_rules.add_rule(("RightFar", "and", "Far"), "RightFast")
mamdani_rules.add_rule(("RightFar", "and", "Close"), "RightSprint")


x = 225
y = 225
f = fuzzification({mamdani_x: x, mamdani_y: y})
print(f)
a = aggregation(f, mamdani_rules.rules)
print(a)
#act = activation(a, mamdani_out, "min")
#print(act)
#accum = accumulation(act, "max")
#print(accum)
#aa = accum_activation(14, a, mamdani_out, "min")
#print(aa)
d = defuzzification(a, mamdani_out)
print(d)
"""

"""
def fuzzyfication(variables, mode):  # variables = {var_1: val_1, var_2: val_2...} # mode = "min" or "max"
    cond_arr = []
    for var in variables:
        arr = var.mf(variables[var])
        cond_arr.append(eval("list(var.terms.keys())[arr.index(" + mode + "(arr))]"))
    return tuple(cond_arr)
"""

"""
def fuzzification(variables):  # variables = {var_1: val_1, var_2: val_2...} # mode = "min" or "max"
    fuzz = {}
    for var in variables:
        mem_func = var.mf(variables[var])
        for i in range(len(mem_func)):
            fuzz[list(var.terms.keys())[i]] = mem_func[i]
    return fuzz


def aggregation(fuzz, rules):
    aggr = {}
    for rule in rules:
        aggr[rules[rule]] = (min(fuzz[rule[0]], fuzz[rule[2]]))
    return aggr
"""

"""
def activation(aggr, var, mode):
    out = []
    if mode == "min":
        for conclusion in aggr:
            if aggr[conclusion]:
                func = lambda x: min(aggr[conclusion], var.mf(x)[list(aggr.keys()).index(conclusion)])
                out.append(func)
            else:
                out.append(0)
    return out


def accumulation(activ, mode):
    activ = [func for func in activ if func != 0]
    print(activ[0](5))
    #x = 10
    #arr = [mf(x) for mf in activ]
    #print(arr)
    #if mode == "max":
        #arr = [lambda x: min(x, 5), lambda x: x+2]
        #func = lambda x: max([mf(x) for mf in activ])
        #print(func(10))
"""

"""

def accum_activation(x_value, aggr, var, activ_mode):  # HERE: make more activation modes
    out = []
    for conclusion in aggr:
        if activ_mode == "min":
            out.append(min(aggr[conclusion], var.mf(x_value)[list(aggr.keys()).index(conclusion)]))
    print(out)
    return max(out)  # Accumulation mode here

"""

"""
def get_integr_range(aggr, var):
    frm = next(i for i in aggr if aggr[i] != 0)
    to = list(aggr.keys())[len(aggr) - 1 - next(i for i, j in enumerate(list(aggr.values())[::-1]) if j != 0)]
    frm = var.terms[frm][0]
    to = var.terms[to][-1]
    return frm, to
"""

"""

# Метод центра площади
def defuzzification(aggr, var):
    func1 = lambda x: x * accum_activation(x, aggr, var, "min")
    func2 = lambda x: accum_activation(x, aggr, var, "min")
    #int_range = get_integr_range(aggr, var)
    i1 = integrate.quad(func1, var.universum[0], var.universum[1], limit=1) # HERE: define integration range less wide
    i2 = integrate.quad(func2, var.universum[0], var.universum[1], limit=1)
    return i1[0] / i2[0]


class Rule:
    rules = {}

    def add_rule(self, conditions, conclusions):
        self.rules[conditions] = conclusions

    def defuzzification(self, conditions):
        return self.rules[conditions]

"""



#################################################### TSUKAMOTO TRASH ###################################################
"""

tsukamoto_x = Variable("X",
                     {"LeftFar": (-600,-599,-250,-200), "Left": (-300,-200,-50,0), "Center": (-50,0,50), "Right": (0,50,200,300), "RightFar":(200,250,599,600)},
                     (-600, 600))
tsukamoto_y = Variable("Y",
                     {"Close": (0,1,100,150), "Far": (100,160,599,600)},
                     (0, 600))
tsukamoto_out = Variable("Out",
                       {"LeftSprint": (-30,-29,-20), "LeftFast": (-30,-20,-15), "LeftNormal": (-20,-15,-10), "LeftSlow": (-15,-10,0),
                        "StopFar": (-10,-5,5,10), "StopClose": (-10,-5,5,10),
                        "RightSlow": (0,10,15), "RightNormal": (10,15,20), "RightFast": (15,20,30), "RightSprint": (20,29,30)},
                       (-30, 30))

tsukamoto_rules = Rule()
tsukamoto_rules.add_rule(("LeftFar", "and", "Close"), "LeftSprint")
tsukamoto_rules.add_rule(("LeftFar", "and", "Far"), "LeftFast")
tsukamoto_rules.add_rule(("Left", "and", "Close"), "LeftNormal")
tsukamoto_rules.add_rule(("Left", "and", "Far"), "LeftSlow")
tsukamoto_rules.add_rule(("Center", "and", "Far"), "StopFar")
tsukamoto_rules.add_rule(("Center", "and", "Close"), "StopClose")
tsukamoto_rules.add_rule(("Right", "and", "Far"), "RightSlow")
tsukamoto_rules.add_rule(("Right", "and", "Close"), "RightNormal")
tsukamoto_rules.add_rule(("RightFar", "and", "Far"), "RightFast")
tsukamoto_rules.add_rule(("RightFar", "and", "Close"), "RightSprint")


x = 225
y = 225

curr = FuzzyMethods()

curr.fuzzification({tsukamoto_x: x, tsukamoto_y: y})
print(curr.fuzz)

curr.aggregation(tsukamoto_rules.rules)
print(curr.aggr)

curr.activation(tsukamoto_out)
print(curr.activ)

d = curr.defuzzification()
print(d)
"""



##################################################### SUGENO TRASH #####################################################

"""

sug_x = Variable("X",
                     {"LeftFar": (-600,-599,-250,-200), "Left": (-300,-200,-50,0), "Center": (-50,0,50), "Right": (0,50,200,300), "RightFar":(200,250,599,600)},
                     (-600, 600))
sug_y = Variable("Y",
                     {"Close": (0,1,100,150), "Far": (100,160,599,600)},
                     (0, 600))
sug_out = Variable("Out",
                       {"LeftSprint": (-30,-29,-20), "LeftFast": (-30,-20,-15), "LeftNormal": (-20,-15,-10), "LeftSlow": (-15,-10,0),
                        "StopFar": (-10,-5,5,10), "StopClose": (-10,-5,5,10),
                        "RightSlow": (0,10,15), "RightNormal": (10,15,20), "RightFast": (15,20,30), "RightSprint": (20,29,30)},
                       (-30, 30))

sug_rules = Rule()
sug_rules.add_rule(("LeftFar", "and", "Close"), "LeftSprint")
sug_rules.add_rule(("LeftFar", "and", "Far"), "LeftFast")
sug_rules.add_rule(("Left", "and", "Close"), "LeftNormal")
sug_rules.add_rule(("Left", "and", "Far"), "LeftSlow")
sug_rules.add_rule(("Center", "and", "Far"), "StopFar")
sug_rules.add_rule(("Center", "and", "Close"), "StopClose")
sug_rules.add_rule(("Right", "and", "Far"), "RightSlow")
sug_rules.add_rule(("Right", "and", "Close"), "RightNormal")
sug_rules.add_rule(("RightFar", "and", "Far"), "RightFast")
sug_rules.add_rule(("RightFar", "and", "Close"), "RightSprint")


x = -250
y = 50

curr = FuzzyMethods()

curr.fuzzification({sug_x: x, sug_y: y})
print(curr.fuzz)

curr.aggregation(sug_rules.rules)
print(curr.aggr)

curr.activation(x, y, sug_rules.rules)
print(curr.activ)

d = curr.defuzzification()
print(d)
"""

##################################################### LARSEN TRASH #####################################################
