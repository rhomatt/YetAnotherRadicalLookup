from enum import Enum
import sys
import re
from django.db import connection

def printjp(string):
    out = string + '\n'
    sys.stdout.buffer.write(out.encode('utf8'))

class Block:
    def __init__(self, block, pos, params):
        self.minstrokes = None
        self.maxstrokes = None
        self.leniency = 0
        self.pos = pos
        # http://www.localizingjapan.com/blog/2012/01/20/regular-expressions-for-japanese-text/
        # found information on japanese unicode here 
        self.kanji = set(re.findall(u"[\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A]", block))
            # we will need these for queries later to avoid SQL injection
        
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

        find_radicals_query = "WITH rads AS (SELECT r.radical FROM Radical r LEFT JOIN Krad kr ON r.radical = kr.radical WHERE\n"
        rad_from_kanji = "kr.kanji = %s AND %s NOT IN (SELECT radical FROM Radical)\n"

        for k in self.kanji:
            find_radicals_query += rad_from_kanji
            params.append(k)
            params.append(k)
            if rad_from_kanji[:2] != "OR":
                rad_from_kanji = "OR " + rad_from_kanji # each subsequent time, there will be an OR added

        for k in self.kanji:
            find_radicals_query += "UNION SELECT %s\n"
            params.append(k)

        find_radicals_query += "EXCEPT SELECT kanji FROM Kanji LEFT JOIN Radical ON kanji = radical WHERE radical IS NULL)"
        find_radicals_query += """
            SELECT k.kanji
            FROM (SELECT COUNT(*) count FROM rads) AS givenrads, radical r
            LEFT JOIN Krad kr ON kr.radical = r.radical
            LEFT JOIN Kanji k ON kr.kanji = k.kanji
            WHERE r.radical IN (SELECT * FROM rads)
            GROUP BY k.kanji, givenrads.count
            HAVING COUNT(r.radical) >= givenrads.count
        """
        self.radicals = find_radicals_query





class Rlux:
    def __init__(self, exp):
        exp = self.__filter_exp(exp)
        self.querystr = self.__create_query_str(exp)
        self.blockexp = None # root
        self.blocks = []
        self.params = [self.querystr] # passed into the query later. I would do the :var version, but sqlite doens't allow that...
        blocks = re.finditer(r'\(\w*\)', exp) # find the contents of the original blocks
        positions = [pos.start(0)+1 for pos in re.finditer(r'#', self.querystr)]
        count = 0
        for block in blocks:
            self.blocks.append(Block(block.group(0), positions[count], self.params))
            count+=1
        self.querystr = re.sub(r'#', '_', self.querystr)
        self.params[0] = self.querystr # since '#' represents a block, the first string parameter must be updated to work as a sql like statement

    def __filter_exp(self, exp):
        exp = re.sub(r'（', '(', exp) # replace japanese parens
        exp = re.sub(r'）', ')', exp)
        exp = re.sub(r'？', '?', exp)
        exp = re.sub(r'＊', '*', exp)
        exp = re.sub(r'#', '', exp) # we use this as a special symbol later denoting block positions. don't allow user to input this
        return exp


    # from the expression, creates the string we will use directly in our query
    def __create_query_str(self, exp):
        exp = re.sub(r'\(\w*\)', '#', exp)
        exp = re.sub(r'\?', '_', exp)
        exp = re.sub(r'\*', '%', exp)
        return exp
        

    # returns the query we need, and the the variable info
    def generate_query(self):
        query = """
            SELECT id, lemma
            FROM word 
            WHERE lemma LIKE %s 
        """

        if self.blocks:
            sub_query = """
                AND SUBSTR(lemma, %d, 1)  IN (
                %s
                )\n
            """
            
            for block in self.blocks:
                query += sub_query % (block.pos, block.radicals)

        query += ';'

        return query, self.params
    
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
    exp = Rlux("高(木)")
    exp = Rlux("自？（正）")
    query, vrs = exp.generate_query()
    printjp(query)
    for kanji in vrs:
        printjp(kanji)

    exp = Rlux("(込)")
    exp = Rlux("(込)(道)")
    exp = Rlux("(込道)")

