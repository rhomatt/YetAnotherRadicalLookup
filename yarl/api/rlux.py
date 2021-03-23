# coding:utf-8
# creates an expression tree from a radical lookup expression (rlux)
# information for how to build parse tree referenced here: https://runestone.academy/runestone/books/published/pythonds/Trees/ParseTree.html
from enum import Enum

class Rlux:
    def __init__(self, exp):
        self.postexp = self.__postfix(exp)

    # tokenizes an expression. return a list, where each val is a tuple (type, val)
    def __postfix(self, exp):
        stack = []
        out = ''
        ops = { # key is op, val is precedence
                '|': 0,
                '.': 1,
                '?': 2,
                '*': 2,
                '&': 3,
                }
        bkt = { # corresponding brackets
                ')': '(',
                ']': '[', 
                '}': '{',
                '」': '「', # this is what bracket gets replaced with for a jp ime
                }

        for c in exp:
            if c in bkt.values(): # opening bracket
                stack.push(c)
            elif c in bkt: # closing bracket
                top = stack.pop()
                while top != bkt[c]:
                    out += stack.pop()
            elif c in ops: # operator
                while stack and ops[stack[-1]] > ops[c]:
                    out += stack.pop()
                stack.push(c)
            else: # a character
                out += c

        while stack:
            out += stack.pop()

        return out

if __name__ == "__main__":
    exp = Rlux("学「三」")
    print(exp.postexp)
