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
            FROM Radical r, (SELECT COUNT(*) givenrads FROM rads)
            LEFT JOIN Krad kr
            ON kr.radical = r.radical
            LEFT JOIN Kanji k ON kr.kanji = k.kanji
            WHERE r.radical in rads
            GROUP BY k.kanji
            HAVING COUNT(r.radical) >= givenrads
        """
        self.radicals = find_radicals_query

        # TODO replace japanese IME symbols with standard symbols




class Rlux:
    def __init__(self, exp):
        self.querystr = self.__create_query_str(exp)
        self.blockexp = None # root
        self.blocks = []
        self.params = [self.querystr] # passed into the query later. I would do the :var version, but sqlite doens't allow that...
        blocks = re.finditer(r'\(\w*\)', exp)
        for block in blocks:
            self.blocks.append(Block(block.group(0), block.start(0) + 1, self.params))


    # from the expression, creates the string we will use directly in our query
    def __create_query_str(self, exp):
        querystr = re.sub(r'\(\w*\)', '_', exp)
        querystr = re.sub(r'\?', '_', querystr)
        querystr = re.sub(r'\*', '%', querystr)
        return querystr
        

    # returns the query we need, and the the variable info
    def generate_query(self):
        query = """
            SELECT wordid, lang, lemma, pron, pos
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
    exp = Rlux("高(木父)")
    query, vrs = exp.generate_query()
    printjp(query)
    for var, kanji in vrs.items():
        printjp(kanji)

    exp = Rlux("(込)")
    exp = Rlux("(込)(道)")
    exp = Rlux("(込道)")

