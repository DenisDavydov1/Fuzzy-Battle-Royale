import math

# Класс лингвистической переменной
class Variable:
    # Инициализация новой переменной
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

    # Описание вычисления функиций принадлежности
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


# Класс формирования базы правил системы нечеткого вывода
class Rule:
    # Инициализация пустой базы правил
    def __init__(self):
        self.rules = {}

    # Метод добавления нового правила
    def add_rule(self, conditions, conclusions):
        self.rules[conditions] = conclusions


# Методы нечеткой логики
class FuzzyMethods:
    # Иннициализация пустых множеств, необходимых для совместной работы методов
    def __init__(self):
        self.fuzz = {}
        self.aggr = {}
        self.activ = []

    # Фаззификация входных переменных
    def fuzzification(self, variables):  # variables = {var_1: val_1, var_2: val_2...}
        self.fuzz = {}
        for var in variables:
            mem_func = var.mf(variables[var])
            for i in range(len(mem_func)):
                self.fuzz[list(var.terms.keys())[i]] = mem_func[i]
        return self.fuzz

    # Агрегирование подусловий
    def aggregation(self, rules):  # rules = {...}
        self.aggr = {}
        for rule in rules:
            self.aggr[rules[rule]] = (min(self.fuzz[rule[0]], self.fuzz[rule[2]]))
        return self.aggr

    # Активизация через нахождение значения выходной переменной в явном виде
    def activation(self, val_x, val_y, var_out):
        self.activ = []
        e1 = 0.5
        e2 = 0.05
        for conclusion in self.aggr:
            c = self.aggr[conclusion]
            w = e1 * val_x + e2 * val_y
            if w <= var_out.universum[0]:
                w = -30
            elif w >= var_out.universum[1]:
                w = 30
            self.activ.append((c, w))
        return self.activ

    # Дефаззифаикация
    def defuzzification(self):
        sum_c_w = sum([c[0] * c[1] for c in self.activ])
        sum_c = sum([c[0] for c in self.activ])
        return sum_c_w / sum_c
