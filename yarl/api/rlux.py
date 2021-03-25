from enum import Enum
import sys
import sqlite3
import re

def printjp(string):
    out = string + '\n'
    sys.stdout.buffer.write(out.encode('utf8'))


class Rlux:
    def __init__(self, exp):
        self.querystr = self.__create_query_str(exp)
        self.blockexp = None # root
        self.blocks = []
        cur = None

        collection = set()
        for c in exp:
            if c == '(':
                # TODO split the char up into it's parts per krad file
                collection.add(c)
            elif c == ')':
                block = AllBlock(collection)
                collection = set() # reset this
            else:
                collection.add(c)

    # from the expression, creates the string we will use directly in our query
    def __create_query_str(self, exp):
        querystr = re.sub('\([^()]*\))', '_' exp)
        querystr = re.sub('\?', '_' querystr)
        querystr = re.sub('\*', '%' querystr)
        return querystr
        

    def __generate_query():
        query = """
        SELECT w.lemma
        FROM word w
        WHERE w.lemma LIKE %s
        """ % self.querystr

        

        query += ';'
        return query
    
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
