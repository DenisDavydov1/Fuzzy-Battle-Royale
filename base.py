import math

class Variable:
    def __init__(self, name, terms, universum):
        self.name = name
        self.terms = terms
        self.universum = universum
        # check if terms are in universum
        for term in self.terms:
            curr = self.terms[term]
            try:
                if not 2 <= len(curr) <= 4:
                    print("Term error: term points quantity is not 2, 3 or 4")  # HERE: change to print error in tkinter window
                    raise SystemExit
            except:
                print("Term error: term points quantity is not 2, 3 or 4")  # HERE: change to print error in tkinter window
                raise SystemExit
            if min(curr) < self.universum[0] or max(curr) > self.universum[1]:
                print("Term error: term points are not in variable's universum")  # HERE: change to print error in tkinter window
                raise SystemExit
            if 3 <= len(curr) <= 4 and not list(curr) == sorted(list(curr)):
                print("Term error: term points are not in ascending order")  # HERE: change to print error in tkinter window
                raise SystemExit

    def mf(self, value):
        out = []
        for term in self.terms:
            curr = self.terms[term]
            if len(curr) == 4:
                if curr[0] <= value <= curr[1]:
                    out.append(1 - (curr[1] - value) / (curr[1] - curr[0]))
                elif curr[1] <= value <= curr[2]:
                    out.append(1)
                elif curr[2] <= value <= curr[3]:
                    out.append(1 - (value - curr[2]) / (curr[3] - curr[2]))
                else:
                    out.append(0)
            elif len(curr) == 3:
                if curr[0] <= value <= curr[1]:
                    out.append(1 - (curr[1] - value) / (curr[1] - curr[0]))
                elif curr[1] <= value <= curr[2]:
                    out.append(1 - (value - curr[1]) / (curr[2] - curr[1]))
                else:
                    out.append(0)
            elif len(curr) == 2:
                out.append(math.exp(-((value - curr[0]) / curr[1]) ** 2))
        return out


def get_conditions(variables, mode):  # variables = {var_1: val_1, var_2: val_2...} # mode = "min" or "max"
    cond_arr = []
    for var in variables:
        arr = var.mf(variables[var])
        cond_arr.append(eval("list(var.terms.keys())[arr.index(" + mode + "(arr))]"))
    return tuple(cond_arr)


class Rule:
    rules = {}

    def add_rule(self, conditions, conclusions):
        self.rules[conditions] = conclusions

    def defuzzification(self, conditions):
        return self.rules[conditions]

