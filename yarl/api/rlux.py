from enum import Enum
import sys
import re
from django.db import connection

def printjp(string):
    out = string + '\n'
    sys.stdout.buffer.write(out.encode('utf8'))

class Block:
    def __init__(self, block):
        printjp(block)
        self.minstrokes = None
        self.maxstrokes = None
        self.leniency = 0
        # http://www.localizingjapan.com/blog/2012/01/20/regular-expressions-for-japanese-text/
        # found information on japanese unicode here 
        self.kanji = set(re.findall(u"[\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A]", block))
        self.radicals = set()
        
        find_radicals_query = "SELECT r.radical FROM Radicals r LEFT JOIN Krad kr ON r.radical = kr.radical WHERE\n"
        rad_from_kanji = "kr.kanji = %s AND %s NOT IN (SELECT radical FROM Radicals)\n"

        for k in self.kanji:
            find_radicals_query += rad_from_kanji
            if rad_from_kanji[:2] != "OR":
                rad_from_kanji = "OR " + rad_from_kanji # each subsequent time, there will be an OR added

        for k in self.kanji:
            find_radicals_query += "UNION SELECT %s\n"
        find_radicals_query += "EXCEPT SELECT k.kanji FROM Kanji k LEFT JOIN Radicals r2 ON k.kanji = r2.radical WHERE r2.radical IS NULL;"
        printjp(find_radicals_query)

        # QUERY DB HERE

        # TODO replace japanese IME symbols with standard symbols

        # find max and minstrokes (if applicable)
        maxstrokes = re.match(r"-\d+", block)
        if maxstrokes:
            self.maxstrokes = int(maxstrokes.group(0)[1:])
        minstrokes = re.match(r"\d+-", block)
        if minstrokes:
            self.minstrokes = int(minstrokes.group(0)[:-1])

        leniency = re.match(r"[Ll]\d+", block)
        if leniency:
            self.leniency = int(leniency.group(0)[1:])




class Rlux:
    def __init__(self, exp):
        self.querystr = self.__create_query_str(exp)
        self.blockexp = None # root
        self.blocks = []
        cur = None
        blocks = re.findall(r'\(\w*\)', exp)
        for block in blocks:
            self.blocks.append(Block(block))
            



    # from the expression, creates the string we will use directly in our query
    def __create_query_str(self, exp):
        querystr = re.sub(r'\(\w*\)', '_', exp)
        querystr = re.sub(r'\?', '_', querystr)
        querystr = re.sub(r'\*', '%', querystr)
        return querystr
        

    def generate_query():
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
    exp = Rlux("高(木父校)")
    exp = Rlux("(込)")
    exp = Rlux("(込道)")

