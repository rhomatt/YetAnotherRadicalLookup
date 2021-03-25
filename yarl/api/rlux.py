from enum import Enum
import sys
import sqlite3
import re

def printjp(string):
    out = string + '\n'
    sys.stdout.buffer.write(out.encode('utf8'))

class Block:
    def __init__(self, val):
        self.val = val
        self.index = 1
        self.next = None

    def connect(self, block):
        self.next = block
        block.index += self.index+1

    def transition(self, string, index):
        if index >= len(string):
            return []
        if string[index] == self.val:
            return [(self.next, index+1)]


class WildBlock(Block):
    def __init__(self, val):
        super().__init__(val)

    def transition(self, string, index):
        return [(self.next, index+1)]


class QuestionBlock(Block):
    def __init__(self, val):
        super().__init__(val)

    def transition(self, string, index):
        return [(self.next, index+1),
                (self.next, index)]



class StarBlock(Block):
    def __init__(self, val):
        super().__init__(val)

    def transition(self, string, index):
        return [(self, index+1),
                (self.next, index),
                (self.next, index+1)]



class AllBlock(Block):
    def __init__(self, val):
        # val in this case should be a set of all chars we need to see
        super().__init__(val) 

    def transition(self, string, index):
        char = string[index]
        charparts = parts[char] # TODO parts is a dict, key: a kanji, val: set of parts of that kanji
        if index >= len(string):
            return []
        if all([v in charparts for v in val]):
            return [(self.next, index+1)]
        

class Rlux:
    def __init__(self, exp):
        self.querystr = self.__create_query_str(exp)
        self.blockexp = None # root
        cur = None

        collection = set()
        for c in exp:
            if c == '.':
                block = WildBlock(c)
            elif c == '?':
                block = QuestionBlock(c)
            elif c == '*':
                block = StarBlock(c)
            elif c == '(':
                # TODO split the char up into it's parts per krad file
                collection.add(c)
                continue
            elif c == ')':
                block = AllBlock(collection)
                collection = set() # reset this
            else:
                block = Block(c)

            if not self.blockexp:
                self.blockexp = block
                cur = block
            else:
                cur.connect(block)
                cur = block

    # from the expression, creates the string we will use directly in our query
    def __create_query_str(self, exp):
        querystr = re.sub('\(.*\))', '_' exp)
        querystr = re.sub('\?', '_' querystr)
        querystr = re.sub('\*', '%' querystr)
        return querystr
        

    def __generate_query():
        query = """
        SELECT w.lemma
        FROM word w
        WHERE w.lemma LIKE %s
        """ % self.querystr

    
    # given a set of kanji to look at, return only the kanji that match the exp
    def search(self, adict):
        matches = [] 
        for word in adict:
            fm = (self.blockexp, 0) # first move
            stack = [fm]
            visited = set(fm) # we don't want to visit the same thing
            while stack:
                state, index = stack.pop()
                # goal check
                if not state and index == len(word):
                    matches.append(word)
                    break
                if not state:
                    continue

                for res in state.transition(word, index):
                    if res in visited:
                        continue
                    visited.add(res)
                    stack.append(res)
        return matches


if __name__ == "__main__":
    exp = Rlux("高?校?")
    adict = ["高校", "高校生"]
    matches = exp.search(adict)
    for match in matches:
        printjp(match)
