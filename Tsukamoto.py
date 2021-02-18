import math

# Linguistic variable class
class Variable:
    # New variable initialization
    def __init__(self, name, terms, universum):
        self.name = name
        self.terms = terms
        self.universum = universum
        # check if terms are in universum
        for term in self.terms:
            curr = self.terms[term]
            try:
                if not 2 <= len(curr) <= 4:
                    print("Term error: term points quantity is not 2, 3 or 4")
                    raise SystemExit
            except:
                print("Term error: term points quantity is not 2, 3 or 4")
                raise SystemExit
            if min(curr) < self.universum[0] or max(curr) > self.universum[1]:
                print("Term error: term points are not in variable's universum")
                raise SystemExit
            if 3 <= len(curr) <= 4 and not list(curr) == sorted(list(curr)):
                print("Term error: term points are not in ascending order")
                raise SystemExit

    # Member function calculation description
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


# Rule base forming class
class Rule:
    # Empty rule base initialization
    def __init__(self):
        self.rules = {}

    # New rule addition method
    def add_rule(self, conditions, conclusions):
        self.rules[conditions] = conclusions


# Fuzzy logics methods
class FuzzyMethods:
    # Initialization of empty sets needed for methods to work together
    def __init__(self):
        self.fuzz = {}
        self.aggr = {}
        self.activ = []

    # Input variables fuzzyfication
    def fuzzification(self, variables):  # variables = {var_1: val_1, var_2: val_2...}
        self.fuzz = {}
        for var in variables:
            mem_func = var.mf(variables[var])
            for i in range(len(mem_func)):
                self.fuzz[list(var.terms.keys())[i]] = mem_func[i]
        return self.fuzz

    # Aggregating subconditions
    def aggregation(self, rules):  # rules = {...}
        self.aggr = {}
        for rule in rules:
            self.aggr[rules[rule]] = (min(self.fuzz[rule[0]], self.fuzz[rule[2]]))
        return self.aggr

    # Activation by solving equations of membership functions
    def activation(self, var):
        self.activ = []
        for conclusion in self.aggr:
            curr = var.terms[conclusion]
            if len(curr) == 4:
                self.activ.append((self.aggr[conclusion], curr[1] - (1 - self.aggr[conclusion]) * (curr[1] - curr[0])))
                self.activ.append((self.aggr[conclusion], curr[2] + (1 - self.aggr[conclusion]) * (curr[3] - curr[2])))
            elif len(curr) == 3:
                self.activ.append((self.aggr[conclusion], curr[1] - (1 - self.aggr[conclusion]) * (curr[1] - curr[0])))
                self.activ.append((self.aggr[conclusion], curr[1] + (1 - self.aggr[conclusion]) * (curr[2] - curr[1])))
            elif len(curr) == 2:
                self.activ.append((self.aggr[conclusion], curr[0] + curr[1] * math.sqrt(-math.log(self.aggr[conclusion]))))
                self.activ.append((self.aggr[conclusion], curr[0] - curr[1] * math.sqrt(-math.log(self.aggr[conclusion]))))
        return self.activ

    # Defuzzifaication
    def defuzzification(self):
        sum_c_w = sum([c[0] * c[1] for c in self.activ])
        sum_c = sum([c[0] for c in self.activ])
        return sum_c_w / sum_c
