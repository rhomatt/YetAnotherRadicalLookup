import sqlite3
import sys
import atexit
from bs4 import BeautifulSoup

def printjp(string):
    out = string + '\n'
    sys.stdout.buffer.write(out.encode('utf8'))

con = sqlite3.connect('wnjpn.db')
def exit_handler():
    commit = input("commit changes? y/n")
    if commit and commit.lower() == 'y':
        con.commit()
    con.close()
    print("closing the connection...")
atexit.register(exit_handler)


print("Type commands() for help")
def commands():
    print("commands()")
    print("initialize_tables()")
    print("parse_krad(<filename>)")

def initialize_tables():
    init_tables = [
    """
        DROP TABLE IF EXISTS Kanji;
    """,
    """
        DROP TABLE IF EXISTS Radicals;
    """,
    """
        DROP TABLE IF EXISTS Krad;
    """,
    """
        CREATE TABLE Kanji (
            kanji CHAR(1) PRIMARY KEY,
            strokes INTEGER,
            frequency INTEGER
        );
    """,
    """
        CREATE TABLE Radicals (
            radical CHAR(1) PRIMARY KEY,
            strokes INTEGER
        );   
    """,
    """
        CREATE TABLE Krad (
            kanji CHAR(1),
            radical CHAR(1),
            FOREIGN KEY(kanji) REFERENCES Kanji(kanji),
            FOREIGN KEY(radical) REFERENCES Radicals(radical),
            UNIQUE(kanji, radical)
        );
    """,
            ]

    for statement in init_tables:
        con.execute(statement)
    print("Tables should have initialized successfully", flush=True)

def parse_krad(krad):
    with open(krad, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            # empty or comment line
            if line == '' or line[0] == '#':
                continue 
            kanji, radicals = line.split(':')
            kanji = kanji.strip()
            radicals = radicals.split()
            try:
                con.execute("INSERT INTO Kanji VALUES ('%s')" % kanji)
            except:
                printjp("Failed to insert kanji %s" % kanji)

            for rad in radicals:
                try:
                    con.execute("INSERT INTO Radicals VALUES ('%s')" % rad)
                except:
                    printjp("Failed to insert radical %s" % rad)
            # it's possible that radical insertion may fail, as we may be inserting dupes. re-loop through
            # to make the relations to kanji

            for rad in radicals:
                try:
                    con.execute("INSERT INTO Krad VALUES ('%s', '%s')" % (kanji, rad))
                except:
                    printjp("Failed to create relation on %s and %s" % (kanji, rad))

def parse_radk(radk):
    with open(radk, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        cur = None
        for line in lines:
            line = line.strip()
            # empty or comment line
            if line == '' or line[0] == '#':
                continue
            data = line.split()
            if data[0] == '$':
                cur = data[1] # New radical found. Update current
                try:
                    # insert radical
                    con.execute("INSERT INTO Radicals VALUES(?, ?)", (cur, int(data[2])))
                except Exception as e:
                    printjp("Failed to insert radical %s" % cur)
            else:
                # we have kanji that belong to a radical
                for char in line:
                    try:
                        con.execute("INSERT INTO Krad VALUEs(?, ?)", (char, cur))
                    except Exception as e:
                        printjp("Failed to create relation on %s and %s" % (char, cur))

                    

def parse_kanjidic(kanjidic):
    with open(kanjidic, mode='r', encoding='utf8') as f:
        soup = BeautifulSoup(f, 'xml')
        print("soup parsed")
        for character in soup.find_all('character'):
            KANJI = character.literal.string
            STROKES = character.misc.find('stroke_count')
            if STROKES:
                STROKES = int(STROKES.string)
            FREQ = character.misc.find('freq')
            if FREQ:
                FREQ = int(FREQ.string)

            try:
                con.execute("INSERT INTO Kanji VALUES (?, ?, ?)", (KANJI, STROKES, FREQ))
            except Exception as e:
                print(e, flush=True)
                printjp("Failed to insert kanji %s" % KANJI)




if __name__ == "__main__":
    initialize_tables()
    parse_kanjidic("kanjidic2.xml")
    parse_radk("radkfile")
