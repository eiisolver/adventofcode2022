from functools import reduce
import operator as op

data = open("21_input.txt", "r").read().splitlines()
monkeys = {a[:4]: a[6:].split() for a in data}
ops = {"+": op.add, "-": op.sub, "*": op.mul, "/": op.truediv}
opposite_ops = {"+": "-", "-": "+", "*": "/", "/": "*"}

# Part 1
def yells(monkey):
    """Part 1 calculation"""
    expr = monkeys[monkey]
    if len(expr) == 1:
        return int(expr[0])
    return reduce(ops[expr[1]], (yells(expr[0]), yells(expr[2])))


print("Part 1:", yells("root"))

# Part 2
class Human:
    def __init__(self):
        pass

    def __repr__(self) -> str:
        return "H"


class Const:
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

    def __repr__(self) -> str:
        return str(self.value)


class Op:
    def __init__(self, op, p1, p2):
        self.op = op
        self.p1 = p1
        self.p2 = p2

    def eval(self):
        return reduce(ops[self.op], (self.p1.eval(), self.p2.eval()))

    def __repr__(self) -> str:
        p1 = self.p1.eval() if isinstance(self.p1, Const) else "X"
        p2 = self.p2.eval() if isinstance(self.p2, Const) else "Y"
        return f"{p1} {self.op} {p2}"


human = Human()


def yells2(monkey):
    """Part 2 calculation"""
    if monkey == "humn":
        return human
    expr = monkeys[monkey]
    if len(expr) == 1:
        return Const(int(expr[0]))
    p1 = yells2(expr[0])
    p2 = yells2(expr[2])
    op = expr[1]
    if monkey == "root":
        return (p1, p2)
    if isinstance(p1, Const) and isinstance(p2, Const):
        return Const(reduce(ops[op], (p1.eval(), p2.eval())))
    return Op(op, p1, p2)


def simplify(expr: Op, val: Const):
    if isinstance(expr, Human):
        return val.eval()
    if isinstance(expr.p1, Const):
        if expr.op in ("+", "*"):
            val2 = Const(Op(opposite_ops[expr.op], val, expr.p1).eval())
        else:
            val2 = Const(Op(expr.op, expr.p1, val).eval())
        return simplify(expr.p2, val2)
    elif isinstance(expr.p2, Const):
        val2 = Const(Op(opposite_ops[expr.op], val, expr.p2).eval())
        return simplify(expr.p1, val2)


expr = yells2("root")
print("Part 2:", simplify(expr[0], expr[1]))
